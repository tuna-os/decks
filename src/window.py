# window.py — Decks main window: slide sidebar + Fabric canvas.
# SPDX-License-Identifier: GPL-3.0-or-later

import json
import os

import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw, GLib  # noqa: E402
from suite_common.window import SuiteWindow  # noqa: E402
from suite_common.webview import SuiteWebView, build_document  # noqa: E402

VENDOR_ASSETS = [
    ('css', 'reveal.css'),
    ('css', 'reveal-theme.css'),
    ('js', 'fabric.min.js'),
    ('js', 'reveal.js'),
]


class DecksWindow(SuiteWindow):
    def __init__(self, **kwargs):
        super().__init__(app_name='Decks', use_tabs=False, **kwargs)
        self._moduledir = os.path.dirname(__file__)
        self._selftest = os.environ.get('DECKS_SELFTEST')
        print('[decks] selftest =', self._selftest, flush=True)

        self.slides = [None]      # list of fabric JSON (None = blank)
        self.current = 0
        self._pending = None      # index to switch to after saving current

        self.webview = SuiteWebView(on_message=self._on_message)

        self._build_layout()
        self._refresh_sidebar()
        self.webview.load_app(self._build_html())

    # ----- layout -----------------------------------------------------------

    def _build_layout(self):
        self.slide_list = Gtk.ListBox()
        self.slide_list.add_css_class('navigation-sidebar')
        self.slide_list.set_selection_mode(Gtk.SelectionMode.SINGLE)
        self.slide_list.connect('row-selected', self._on_row_selected)

        scroller = Gtk.ScrolledWindow()
        scroller.set_child(self.slide_list)
        scroller.set_vexpand(True)

        add_btn = Gtk.Button(label='Add Slide', margin_top=6, margin_bottom=6,
                             margin_start=6, margin_end=6)
        add_btn.connect('clicked', lambda *_: self.add_slide())

        sidebar = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        sidebar.append(scroller)
        sidebar.append(add_btn)
        sidebar.set_size_request(200, -1)

        split = Adw.OverlaySplitView()
        split.set_sidebar(sidebar)
        split.set_content(self.webview)
        split.set_max_sidebar_width(260)
        self.set_main_content(split)

        present_btn = Gtk.Button(icon_name='view-fullscreen-symbolic')
        present_btn.set_tooltip_text('Present')
        present_btn.connect('clicked', lambda *_: self.webview.send('present', None))
        self.header_bar.pack_start(present_btn)

        add_text_btn = Gtk.Button(icon_name='insert-text-symbolic')
        add_text_btn.set_tooltip_text('Add text box')
        add_text_btn.connect('clicked', lambda *_: self.webview.send('addText', None))
        self.header_bar.pack_start(add_text_btn)

    def _build_html(self):
        vendor_dir = os.path.join(self._moduledir, 'vendor')
        with open(os.path.join(self._moduledir, 'engine.js'), encoding='utf-8') as fh:
            engine = fh.read()
        body = ('<div style="display:flex;justify-content:center;align-items:center;'
                'height:100vh;background:#dcdcdc">'
                '<canvas id="canvas" width="960" height="540" '
                'style="box-shadow:0 0 12px rgba(0,0,0,0.3)"></canvas></div>')
        head_extra = f'<script>{engine}</script>'
        return build_document(vendor_dir, VENDOR_ASSETS, body, head_extra)

    # ----- slide management -------------------------------------------------

    def _refresh_sidebar(self):
        self.slide_list.remove_all()
        for i in range(len(self.slides)):
            row = Adw.ActionRow(title=f'Slide {i + 1}')
            self.slide_list.append(row)
        row = self.slide_list.get_row_at_index(self.current)
        if row:
            self.slide_list.select_row(row)

    def add_slide(self):
        # Save current, then append + switch.
        self.slides.append(None)
        self._pending = len(self.slides) - 1
        self.webview.send('getSlide', None)
        self._refresh_sidebar()

    def _on_row_selected(self, listbox, row):
        if row is None:
            return
        idx = row.get_index()
        if idx == self.current:
            return
        self._pending = idx
        self.webview.send('getSlide', None)   # save current, then load pending

    def _switch_to_pending(self):
        if self._pending is None:
            return
        self.current = self._pending
        self._pending = None
        self.webview.send('loadSlide', self.slides[self.current])

    # ----- bridge -----------------------------------------------------------

    def _on_message(self, payload):
        kind = payload.get('type')
        if kind == 'ready':
            print('[decks] engine ready:', payload.get('engine'),
                  'reveal=', payload.get('reveal'), flush=True)
            if self._selftest:
                self._run_selftest()
        elif kind == 'slide':
            # Store the just-saved current slide, then complete a pending switch.
            self.slides[self.current] = payload.get('data')
            if self._selftest_target:
                self._write_selftest(payload.get('data'))
            self._switch_to_pending()
        elif kind == 'changed':
            pass

    # ----- self-test --------------------------------------------------------

    _selftest_target = None

    def _run_selftest(self):
        try:
            _, _, out_path = self._selftest.partition(':')
            self._selftest_target = out_path
            print('[decks] selftest requesting slide', flush=True)
            GLib.timeout_add(600, lambda: (self.webview.send('getSlide', None), False)[1])
        except Exception as exc:  # noqa: BLE001
            print('[decks] selftest error:', exc, flush=True)

    def _write_selftest(self, data):
        target = self._selftest_target
        self._selftest_target = None
        try:
            with open(target, 'w', encoding='utf-8') as fh:
                json.dump(data, fh)
            print('[decks] selftest wrote slide JSON', flush=True)
        except OSError as exc:
            print('[decks] selftest write error:', exc, flush=True)
