/* engine.js — Decks presentation engine: Fabric.js slide canvas + Reveal.js.
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 * One Fabric canvas edits the current slide; slide list/order is managed in
 * Python (the libadwaita sidebar). Talks over the suite-common `bridge` channel.
 */
(function () {
  'use strict';

  var SLIDE_W = 960, SLIDE_H = 540;

  function post(msg) {
    try { window.webkit.messageHandlers.bridge.postMessage(msg); }
    catch (e) { console.log('bridge post failed: ' + e); }
  }

  var canvas = null;

  function sampleText() {
    return new fabric.IText('Double-click to edit', {
      left: 80, top: 220, fontSize: 44, fontFamily: 'sans-serif', fill: '#202020'
    });
  }

  function init() {
    canvas = new fabric.Canvas('canvas', { backgroundColor: '#ffffff' });
    canvas.setWidth(SLIDE_W);
    canvas.setHeight(SLIDE_H);
    canvas.add(sampleText());
    canvas.on('object:modified', function () { post({ type: 'changed' }); });
    canvas.on('text:changed', function () { post({ type: 'changed' }); });
    window.__canvas = canvas;

    console.log('Fabric ready: ' + (fabric.version || '?'));
    console.log('Reveal available: ' + (typeof Reveal !== 'undefined'));
    post({ type: 'ready', engine: 'fabric', reveal: (typeof Reveal !== 'undefined') });
  }

  // Python -> JS
  window.bridgeReceive = function (name, data) {
    if (name === 'loadSlide') {
      if (!data || !data.objects) { canvas.clear(); canvas.backgroundColor = '#ffffff'; canvas.renderAll(); }
      else { canvas.loadFromJSON(data, function () { canvas.renderAll(); }); }
    } else if (name === 'getSlide') {
      post({ type: 'slide', data: canvas.toJSON() });
    } else if (name === 'addText') {
      canvas.add(sampleText()); canvas.renderAll(); post({ type: 'changed' });
    } else if (name === 'newSlide') {
      canvas.clear(); canvas.backgroundColor = '#ffffff'; canvas.add(sampleText()); canvas.renderAll();
    }
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
