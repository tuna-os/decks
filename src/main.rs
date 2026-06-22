// main.rs — Decks presentation app, pure Rust + gtk4-rs.
// SPDX-License-Identifier: GPL-3.0-or-later

mod window;

fn main() {
    let app = libadwaita::Application::builder()
        .application_id("org.tunaos.decks")
        .build();
    app.connect_activate(|app| {
        let win = window::DecksWindow::new(app);
        win.present();
    });
    app.run();
}
