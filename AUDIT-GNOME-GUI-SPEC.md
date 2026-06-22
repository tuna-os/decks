# Decks — GNOME GUI Spec Audit

**Spec source**: https://github.com/hanthor/gnome-gui-spec (v0.2.0)
**Framework**: Python + PyGObject + GTK 4 + libadwaita + WebKitGTK 6.0
**App ID**: io.github.hanthor.decks
**Audit date**: 2026-06-22

Decks inherits its chrome from [suite-common](https://github.com/hanthor/suite-common)
(mirrors Letters' audited patterns) and uses an `Adw.OverlaySplitView` slide sidebar plus a
`WebKit.WebView` Fabric.js canvas.

## Overall Compliance

| Area | Status | Score |
|------|--------|-------|
| Window Architecture | ✅ `Adw.ApplicationWindow` + `Adw.ToolbarView` + `Adw.HeaderBar` | 9/10 |
| Navigation (Sidebar) | ✅ `Adw.OverlaySplitView` + slide `Gtk.ListBox` | 8/9 |
| Header Bar | ✅ Open/Save/Export/Present + add-text + menu | 10/10 |
| Toolbar | 🟡 Header actions; no responsive breakpoint | 5/7 |
| Preferences | ✅ `Adw.PreferencesDialog` with working Dark Style row | 7/7 |
| Dialogs | ✅ `Gtk.FileDialog`, `Adw.AboutDialog` | 7/7 |
| Shortcuts | ✅ `Gtk.ShortcutsWindow` + Escape exits present | 7/7 |
| Menus | ✅ Primary menu (Preferences/Shortcuts/About/Quit) | 7/7 |
| Typography | ✅ Default libadwaita | 6/7 |
| Spacing | ✅ Default libadwaita | 5/5 |
| Accessibility | 🟡 Tooltips + menu accessible-label; canvas internals opaque | 5/6 |
| Adaptive | ✅ `Adw.Breakpoint` collapses the slide sidebar on narrow widths | 4/5 |
| Error Handling | ✅ `Adw.Toast` via `SuiteWindow.toast()` | 5/5 |
| **Total** | | **85/92 (92%)** |

## Notes
- **Met via suite-common**: window architecture, header bar, preferences (with a working
  Dark Style toggle), shortcuts, menus, toast error handling, accessible menu label.
- **App-specific**: slide sidebar with add/delete/reorder, Fabric.js editing canvas,
  Reveal.js present mode (Escape to exit), PDF export, pptx/odp I/O via `fileio.py`.
- **Adaptive**: the `Adw.OverlaySplitView` collapses to an overlay under 600sp — the
  standard GNOME narrow-window pattern — reaching parity with Letters' baseline.
- **Packaging**: `.desktop`, AppStream `metainfo.xml`, and a scalable app icon are installed.

## Remaining gaps (tracked follow-ups)
- Responsive toolbar breakpoint for the header actions → Toolbar 5→7.
- Accessibility bridging into the WebKit canvas → Accessibility 5→6.
