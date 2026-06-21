# main.py — Decks application entry point.
# SPDX-License-Identifier: GPL-3.0-or-later

import sys
import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Adw  # noqa: E402
from suite_common.application import SuiteApplication  # noqa: E402
from .window import DecksWindow  # noqa: E402


class DecksApplication(SuiteApplication):
    def __init__(self, version):
        super().__init__(application_id='io.github.hanthor.decks',
                         window_class=DecksWindow,
                         app_name='Decks',
                         version=version)


def main(version):
    Adw.init()
    app = DecksApplication(version)
    return app.run(sys.argv)
