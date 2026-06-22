# Decks — GNOME GUI Spec Audit

**Spec:** [hanthor/gnome-gui-spec](https://github.com/hanthor/gnome-gui-spec) v0.2.0
**App:** `org.tunaos.decks` — Python + PyGObject + GTK4 + libadwaita + WebKitGTK 6.0
**Audit date:** 2026-06-22

Decks inherits its chrome from [suite-common](https://github.com/hanthor/suite-common)
(Letters' idioms: raised toolbar, responsive action toolbar, sizing, accessibility) and
adds an `AdwOverlaySplitView` slide sidebar over a `WebKit.WebView` Fabric.js canvas.

## 1. Widget Inventory

### Adw
| Widget | Where |
|---|---|
| `AdwApplicationWindow` | suite_common/window.py |
| `AdwToolbarView` (`top-bar-style: raised`) | suite_common/window.py |
| `AdwHeaderBar` | suite_common/window.py |
| `AdwOverlaySplitView` (slide sidebar) | decks window.py |
| `AdwBreakpoint` ×2 (sidebar 600sp; action bar 500sp) | decks + suite_common |
| `AdwToastOverlay` | suite_common/window.py |
| `AdwPreferencesDialog` + `SwitchRow` | suite_common/dialogs.py |
| `AdwAboutDialog`, `AdwStyleManager` | suite_common |

### Gtk
| Widget | Where |
|---|---|
| `GtkButton` (open/save/export/present + tools) | decks window.py |
| `GtkMenuButton` (primary, `more`) | suite_common/window.py |
| `GtkListBox` (slide list, `.navigation-sidebar`) | decks window.py |
| `GtkScrolledWindow`, `GtkBox` (`.toolbar`) | decks / suite_common |
| `GtkEventControllerKey` (Escape exits present) | decks window.py |
| `GtkShortcutsWindow`, `GtkFileDialog` | suite_common / decks |

## 2. Checklist Compliance (§14)

**Architecture** — ✅ `AdwApplication`+`AdwApplicationWindow`; ✅ single window;
✅ adaptive (min 296×360; two breakpoints).

**Header Bar** — ✅ centred title; ✅ primary [start] / menu [end]; ✅ tooltips on all buttons;
✅ flat; ✅ `<control>comma` → Preferences.

**Navigation** — ✅ one pattern (slide sidebar via `AdwOverlaySplitView`, collapses ≤600sp).

**Preferences** — ✅ `AdwPreferencesDialog`; ✅ `search-enabled`; ✅ `AdwSwitchRow` (Dark Style);
🟡 not GSettings-backed.

**Feedback** — ✅ toasts; 🟡 no undo-toast; 🟡 no empty-state `AdwStatusPage`.

**Styling** — ✅ system light/dark + toggle; ✅ symbolic icons; ✅ `.toolbar`/`.navigation-sidebar`
CSS; 🟡 typography classes not explicitly applied (canvas-rendered slides).

**Accessibility** — ✅ `AccessibleProperty.LABEL` + tooltips on all buttons, menu, window;
🟡 the Fabric canvas internals aren't bridged to AT-SPI.

## 3. Anti-pattern check (§13)
None present: `AdwApplicationWindow`/`AdwHeaderBar`, `AdwPreferencesDialog`, toasts,
in-window navigation (`AdwOverlaySplitView`), symbolic icons, header tooltips, menu access keys.

## 4. Score

| Area | Score |
|---|---|
| Architecture | 10/10 |
| Header Bar | 10/10 |
| Navigation (sidebar) | 9/9 |
| Toolbar (responsive action bar) | 7/7 |
| Preferences | 6/7 (no GSettings) |
| Dialogs | 7/7 |
| Shortcuts | 7/7 |
| Menus | 7/7 |
| Typography | 6/7 |
| Spacing | 5/5 |
| Accessibility | 5/6 (canvas) |
| Adaptive | 5/5 (two breakpoints) |
| Feedback | 4/5 (no undo/empty-state) |
| **Total** | **88/92 (96%)** |

## 5. Findings / follow-ups
1. GSettings-back preferences (Preferences 6→7).
2. Empty-state `AdwStatusPage` for a fresh deck (Feedback 4→5).
3. AT-SPI bridging for the Fabric canvas (Accessibility 5→6).
