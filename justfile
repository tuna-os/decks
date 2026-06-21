# Decks — build & run as a Flatpak using the org.flatpak.Builder flatpak (himachal).

app_id := "io.github.hanthor.decks"
manifest := app_id + ".json"

default:
    @just --list

# Fetch vendored JS engines into src/vendor/ (commit the result; flatpak builds offline).
vendor:
    #!/usr/bin/env bash
    set -euo pipefail
    mkdir -p src/vendor
    base="https://cdn.jsdelivr.net/npm"
    curl -fsSL "$base/fabric@5/dist/fabric.min.js"          -o src/vendor/fabric.min.js
    curl -fsSL "$base/reveal.js@4/dist/reveal.js"           -o src/vendor/reveal.js
    curl -fsSL "$base/reveal.js@4/dist/reveal.css"          -o src/vendor/reveal.css
    curl -fsSL "$base/reveal.js@4/dist/theme/white.css"     -o src/vendor/reveal-theme.css
    echo "vendored:"; ls -la src/vendor

setup:
    #!/usr/bin/env bash
    set -euo pipefail
    mkdir -p subprojects
    if [ -d subprojects/suite-common/.git ]; then
        git -C subprojects/suite-common fetch --depth 1 origin main
        git -C subprojects/suite-common reset --hard origin/main
    else
        rm -rf subprojects/suite-common
        git clone --depth 1 https://github.com/hanthor/suite-common.git subprojects/suite-common
    fi

build: setup
    #!/usr/bin/env bash
    set -euo pipefail
    state="$HOME/.cache/decks-flatpak"
    mkdir -p "$state"
    flatpak run --cwd="$PWD" --filesystem=host org.flatpak.Builder \
        --force-clean --user --install --install-deps-from=flathub \
        --state-dir="$state/state" \
        --repo="$state/repo" \
        "$state/build" "{{manifest}}"

run:
    flatpak run {{app_id}}

# Build, launch on the session, assert Fabric + bridge are live.
verify: build
    #!/usr/bin/env bash
    set -uo pipefail
    flatpak kill {{app_id}} 2>/dev/null || true; sleep 1
    export XDG_RUNTIME_DIR="/run/user/$(id -u)"
    export WAYLAND_DISPLAY="$(ls "$XDG_RUNTIME_DIR" 2>/dev/null | grep -m1 -E '^wayland-[0-9]+$' || echo wayland-0)"
    log=$(mktemp)
    timeout 8 flatpak run --env=PYTHONUNBUFFERED=1 {{app_id}} >"$log" 2>&1 &
    pid=$!; sleep 6; flatpak kill {{app_id}} 2>/dev/null; kill "$pid" 2>/dev/null || true
    echo "--- console ---"; cat "$log"
    if grep -q "\[decks\] engine ready" "$log" && grep -q "Fabric ready" "$log"; then
        echo "VERIFY: PASS (Fabric canvas + JS<->Python bridge live)"
    else echo "VERIFY: FAIL"; exit 1; fi

# Headless slide round-trip (decks #2): assert the canvas serialises its text box.
slidetest: build
    #!/usr/bin/env bash
    set -uo pipefail
    flatpak kill {{app_id}} 2>/dev/null || true; sleep 1
    export XDG_RUNTIME_DIR="/run/user/$(id -u)"
    export WAYLAND_DISPLAY="$(ls "$XDG_RUNTIME_DIR" 2>/dev/null | grep -m1 -E '^wayland-[0-9]+$' || echo wayland-0)"
    d="$HOME/.cache/decks-slidetest"; rm -rf "$d"; mkdir -p "$d"
    timeout 8 flatpak run --env=PYTHONUNBUFFERED=1 --filesystem="$d" \
        --env=DECKS_SELFTEST=":$d/slide.json" {{app_id}} >"$d/log" 2>&1 &
    pid=$!; sleep 6; flatpak kill {{app_id}} 2>/dev/null; kill "$pid" 2>/dev/null || true
    echo "--- log ---"; cat "$d/log"
    echo "--- slide.json ---"; cat "$d/slide.json" 2>/dev/null || echo "(none)"
    if [ -f "$d/slide.json" ] && grep -q "Double-click to edit" "$d/slide.json"; then
        echo "SLIDETEST: PASS (Fabric serialised text box round-tripped)"; rm -rf "$d"
    else echo "SLIDETEST: FAIL"; exit 1; fi

clean:
    rm -rf subprojects/suite-common "$HOME/.cache/decks-flatpak"
