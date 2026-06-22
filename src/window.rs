// window.rs — Decks main window: slide sidebar + native canvas.
// SPDX-License-Identifier: GPL-3.0-or-later

use gtk4 as gtk;
use gtk::prelude::*;
use libadwaita::prelude::AdwApplicationWindowExt;

struct Slide {
    id: usize,
    title: String,
}

pub struct DecksWindow {
    window: libadwaita::ApplicationWindow,
    slides: std::cell::RefCell<Vec<Slide>>,
    current: std::cell::Cell<usize>,
    canvas: gtk::DrawingArea,
}

impl DecksWindow {
    pub fn new(app: &libadwaita::Application) -> Self {
        let win = libadwaita::ApplicationWindow::new(app);
        win.set_title(Some("Decks"));
        win.set_default_size(960, 600);

        let slides = std::cell::RefCell::new(vec![
            Slide { id: 0, title: "Slide 1".into() },
        ]);
        let current = std::cell::Cell::new(0);

        // Header bar
        let header = libadwaita::HeaderBar::new();
        let add_btn = gtk::Button::with_label("+ Slide");
        header.pack_start(&add_btn);
        let del_btn = gtk::Button::with_label("- Slide");
        header.pack_start(&del_btn);
        let present_btn = gtk::Button::with_label("Present");
        header.pack_end(&present_btn);

        // Toolbar
        let toolbar = gtk::Box::new(gtk::Orientation::Horizontal, 4);
        toolbar.set_halign(gtk::Align::Center);
        toolbar.add_css_class("toolbar");
        toolbar.append(&gtk::Button::with_label("Text"));
        toolbar.append(&gtk::Button::with_label("Rect"));
        toolbar.append(&gtk::Button::with_label("Image"));

        // Slide sidebar
        let sidebar_list = gtk::ListBox::new();
        sidebar_list.set_width_request(180);
        for s in slides.borrow().iter() {
            let row = gtk::Label::new(Some(&s.title));
            sidebar_list.append(&row);
        }

        // Canvas
        let canvas = gtk::DrawingArea::new();
        canvas.set_draw_func(|area, cr, w, h| {
            cr.set_source_rgb(1.0, 1.0, 1.0);  // white
            cr.paint().unwrap();
            cr.set_source_rgb(0.2, 0.2, 0.2);
            cr.select_font_face("Sans", cairo::FontSlant::Normal, cairo::FontWeight::Bold);
            cr.set_font_size(32.0);
            cr.move_to(80.0, 200.0);
            cr.show_text("Slide canvas").unwrap();
        });
        canvas.set_hexpand(true);
        canvas.set_vexpand(true);
        let canvas_clone = canvas.clone();
        add_btn.connect_clicked(move |_| {
            let _ = &canvas_clone;  // placeholder
        });

        let content = gtk::Box::new(gtk::Orientation::Horizontal, 0);
        content.append(&sidebar_list);
        content.append(&canvas);

        let main_box = gtk::Box::new(gtk::Orientation::Vertical, 0);
        main_box.append(&toolbar);
        main_box.append(&content);

        let container = gtk::Box::new(gtk::Orientation::Vertical, 0);
        container.append(&header);
        container.append(&main_box);
        win.set_content(Some(&container));

        Self { window: win, slides, current, canvas }
    }

    pub fn present(&self) {
        self.window.present();
    }
}
