# main.py — Decks application entry point.
# SPDX-License-Identifier: GPL-3.0-or-later

import sys
import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gio, Adw  # noqa: E402
from suite_common.application import SuiteApplication  # noqa: E402
from .window import DecksWindow  # noqa: E402


class DecksApplication(SuiteApplication):
    def __init__(self, version):
        super().__init__(application_id='io.github.hanthor.decks',
                         window_class=DecksWindow,
                         app_name='Decks',
                         version=version)

        # ── Slide shortcuts ────────────────────────────────────────
        self._add_action('add-slide', self._on_add_slide, ['<primary>m'])
        self._add_action('delete-slide', self._on_delete_slide, ['<primary>d'])
        self._add_action('present', self._on_present, ['F5'])

        # Add to shortcuts overlay
        self.shortcuts[_('Slide')] = [
            ('<primary>m', _('Add Slide')),
            ('<primary>d', _('Delete Slide')),
            ('F5', _('Present')),
        ]

    def _on_add_slide(self, *a):
        win = self.props.active_window
        if win and hasattr(win, 'add_slide'):
            win.add_slide()

    def _on_delete_slide(self, *a):
        win = self.props.active_window
        if win and hasattr(win, 'delete_slide'):
            win.delete_slide()

    def _on_present(self, *a):
        win = self.props.active_window
        if win and hasattr(win, 'present'):
            win.present()


def main(version):
    Adw.init()
    app = DecksApplication(version)
    return app.run(sys.argv)
