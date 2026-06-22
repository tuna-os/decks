#!/usr/bin/env python3
# Dogtail GUI test for Decks — drives the running Flatpak via AT-SPI.
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Uses AT-SPI actions (no X mouse synthesis) so it runs headlessly on Wayland.
#   python3 tests/gui/test_decks.py     (`just guitest` handles launch/teardown)

import sys
import time

from dogtail import tree  # noqa: E402


def click(node):
    for action in ('click', 'activate', 'press'):
        try:
            node.doActionNamed(action)
            return
        except Exception:
            continue
    raise AssertionError(f'no clickable action on {node}')


def main():
    app = tree.root.application('decks')
    print('found application: decks')

    # The tools toolbar (Letters idiom): Add Text Box is the primary tool.
    add_text = app.child(name='Add Text Box', roleName='push button', showingOnly=False)
    click(add_text)
    time.sleep(0.5)
    print('Add Text Box driven via AT-SPI: OK')

    # The slide sidebar controls are accessible.
    app.child(name='Add slide', roleName='push button', showingOnly=False)
    print('slide sidebar control "Add slide" found: OK')

    # The primary menu button.
    menu = app.child(name='Main Menu', roleName='toggle button', showingOnly=False)
    click(menu)
    time.sleep(0.4)
    print('primary menu found + activated: OK')

    # A slide row is listed in the sidebar.
    app.child(roleName='list box', showingOnly=False)
    print('slide list (list box) found: OK')

    def count(node):
        total = 1
        try:
            for child in node.children:
                total += count(child)
        except Exception:
            pass
        return total

    nodes = count(app)
    assert nodes > 15, f'expected a populated a11y tree, got {nodes} nodes'
    print(f'a11y tree populated: {nodes} accessible nodes')

    print('GUITEST: PASS')
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as exc:  # noqa: BLE001
        print(f'GUITEST: FAIL — {exc}')
        sys.exit(1)
