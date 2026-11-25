/* ==================================================================
   netzfest – Verhalten (Vanilla JS, ohne Bibliotheken)
   1 Speicher  2 Rollen  3 Menüs  4 Akut-Dialog & Navigator
   5 Merkliste  6 Bibliothek  7 Hero & Netz  8 Fake Detektiv
   Alles funktioniert auch ohne JS lesbar; dieses Skript verstärkt nur.
   ================================================================== */
(function () {
  'use strict';

  var D = window.NETZFEST || { hilfe: {}, rollen: {} };
  var $ = function (sel, ctx) { return (ctx || document).querySelector(sel); };
  var $$ = function (sel, ctx) { return Array.prototype.slice.call((ctx || document).querySelectorAll(sel)); };
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* 1 · Speicher (robust, falls localStorage gesperrt ist) ---------- */
  var notfall = {};   // Ersatz im Arbeitsspeicher, wenn der Browser localStorage sperrt
  var store = {
    get: function (k, fb) {
      try { var v = localStorage.getItem(k); return v == null ? fb : JSON.parse(v); }
      catch (e) { return Object.prototype.hasOwnProperty.call(notfall, k) ? notfall[k] : fb; }
    },
    set: function (k, v) { notfall[k] = v; try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) { /* Notfallspeicher reicht */ } }
  };

  // Als Datei geöffnet (file://, z. B. per Doppelklick): Firefox und Safari geben dann jeder Seite einen eigenen
  // oder gar keinen Speicher. Damit Merkliste und Ansicht trotzdem von Seite zu Seite mitkommen, reichen interne
  // Links den Stand in der Adresse weiter (?nf=…). Auf einem Webserver passiert nichts davon.
  var alsDatei = location.protocol === 'file:';
  if (alsDatei) {
    var startParams = new URLSearchParams(location.search);
    if (startParams.has('nf')) {
      try {
        var stand = JSON.parse(startParams.get('nf'));
        if (Array.isArray(stand.m)) store.set('netzfest:merkliste', stand.m);
        store.set('netzfest:rolle', typeof stand.r === 'string' ? stand.r : null);
      } catch (e) { /* kaputter Parameter: ignorieren */ }
      startParams.delete('nf');
      var restParams = startParams.toString();
      try { history.replaceState(null, '', location.pathname + (restParams ? '?' + restParams : '') + location.hash); } catch (e) { /* egal */ }
    }
    // an window: läuft nach allen anderen Klick-Handlern, die Links selbst abfangen (Dialoge, Menüs)
    window.addEventListener('click', function (e) {
      if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
      var a = e.target.closest('a[href]');
      if (!a || a.target === '_blank' || a.hasAttribute('download')) return;
      var href = a.getAttribute('href');
      if (/^(?:[a-z]+:|#|\/\/)/i.test(href) || !/\.html(?:[?#]|$)/.test(href)) return;
      var ziel = new URL(href, location.href);
      ziel.searchParams.set('nf', JSON.stringify({ m: store.get('netzfest:merkliste', []), r: store.get('netzfest:rolle', null) }));
      e.preventDefault();
      location.href = ziel.href;
    });
  }

  /* 2 · Rollen ------------------------------------------------------ */
  var role = store.get('netzfest:rolle', null) || null;
  // Ansicht per Link wählbar, z. B. index.html?rolle=schueler (die alte Adresse kinder.html leitet so weiter)
  var urlRole = new URLSearchParams(location.search).get('rolle');
  if (urlRole && D.rollen[urlRole]) { role = urlRole; store.set('netzfest:rolle', role); }
  if (/[?&]raster\b/.test(location.search)) document.documentElement.classList.add('raster-an');

  function applyRole() {
    var root = document.documentElement;
    if (role) root.dataset.role = role; else delete root.dataset.role;

    $$('[data-fuer]').forEach(function (el) {
      var list = el.getAttribute('data-fuer').split(/\s+/);
      el.hidden = role ? list.indexOf(role) === -1 : list.indexOf('alle') === -1;
    });
    $$('[data-role-pick]').forEach(function (b) {
      b.setAttribute('aria-pressed', String(b.getAttribute('data-role-pick') === role));
    });
    $$('[data-role-set]').forEach(function (b) {
      if (b.getAttribute('role') === 'menuitemradio') b.setAttribute('aria-checked', String(b.getAttribute('data-role-set') === role));
    });
    $$('[data-role-label]').forEach(function (s) { s.textContent = role ? D.rollen[role] : 'Alle'; });
  }

  function setRole(r) {
    role = r || null;
    store.set('netzfest:rolle', role);
    applyRole();
    document.dispatchEvent(new CustomEvent('netzfest:role', { detail: role }));
  }

  document.addEventListener('click', function (e) {
    var pick = e.target.closest('[data-role-pick]');
    if (pick) {
      var r = pick.getAttribute('data-role-pick');
      setRole(role === r ? null : r);
      var target = $('[data-role-target]');
      var live = $('[data-role-live]');
      if (live && target) {
        // Rückmeldung mit dem nächsten Schritt – kein automatisches Springen
        if (!role) live.textContent = 'Du siehst wieder alle Inhalte.';
        else if (role === 'schueler') live.innerHTML = 'Fertig. Deine Tipps stehen direkt darunter: <a href="#fuer-schueler-start">Zu deinen Tipps ↓</a>';
        else live.innerHTML = 'Fertig. Die Seite zeigt jetzt Inhalte für ' + D.rollen[role] + ': <a href="#fuer-dich">Zum passenden Material ↓</a>';
      }
    }
    var set = e.target.closest('[data-role-set]');
    if (set) {
      setRole(set.getAttribute('data-role-set'));
      closeRoleMenus();
    }
  });

  /* 3 · Menüs ------------------------------------------------------- */
  function closeRoleMenus(except) {
    $$('[data-role-menu]').forEach(function (m) {
      if (m === except) return;
      var btn = $('[data-role-toggle]', m), list = $('[role="menu"]', m);
      btn.setAttribute('aria-expanded', 'false');
      list.hidden = true;
    });
  }

  $$('[data-role-menu]').forEach(function (menu) {
    var btn = $('[data-role-toggle]', menu), list = $('[role="menu"]', menu);
    btn.addEventListener('click', function () {
      var open = btn.getAttribute('aria-expanded') === 'true';
      closeRoleMenus(menu);
      btn.setAttribute('aria-expanded', String(!open));
      list.hidden = open;
      if (!open) { var first = $('[aria-checked="true"]', list) || $('button', list); if (first) first.focus(); }
    });
    list.addEventListener('keydown', function (e) {
      var items = $$('button', list), i = items.indexOf(document.activeElement);
      if (e.key === 'ArrowDown') { e.preventDefault(); items[(i + 1) % items.length].focus(); }
      if (e.key === 'ArrowUp') { e.preventDefault(); items[(i - 1 + items.length) % items.length].focus(); }
      if (e.key === 'Escape') { closeRoleMenus(); btn.focus(); }
    });
  });
  document.addEventListener('click', function (e) { if (!e.target.closest('[data-role-menu]')) closeRoleMenus(); });

  var menuBtn = $('[data-menu-toggle]'), mobileNav = $('#mobile-nav');
  if (menuBtn && mobileNav) {
    menuBtn.addEventListener('click', function () {
      var open = menuBtn.getAttribute('aria-expanded') === 'true';
      menuBtn.setAttribute('aria-expanded', String(!open));
      mobileNav.hidden = open;
    });
  }
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && menuBtn && menuBtn.getAttribute('aria-expanded') === 'true') {
      menuBtn.click(); menuBtn.focus();
    }
  });

  /* 4 · Akut-Dialog & Erste-Hilfe-Navigator ------------------------- */
  var dialog = $('#akut-dialog');
  $$('[data-akut]').forEach(function (a) {
    a.addEventListener('click', function (e) {
      if (!dialog || typeof dialog.showModal !== 'function') return; // Fallback: Link zur Hilfe-Seite
      e.preventDefault();
      dialog.showModal();
      var first = $('.chip', dialog); if (first) first.focus();
    });
  });
  if (dialog) {
    $$('[data-dialog-close]', dialog).forEach(function (b) { b.addEventListener('click', function () { dialog.close(); }); });
    dialog.addEventListener('click', function (e) { if (e.target === dialog) dialog.close(); });
  }

  var NAV_INTRO = {
    ich: 'Du bist nicht schuld. Niemand verdient so etwas – und du musst da nicht allein durch.',
    andere: 'Gut, dass du hinschaust. Frag die Person zuerst privat, was sie sich wünscht, und hilf ihr bei diesen Schritten.',
    kind: 'Bleib ruhig und hör zu. Dein Kind braucht jetzt Rückhalt, kein Handyverbot. Diese Schritte geht ihr gemeinsam.',
    gruppe: 'Schützen Sie zuerst die betroffene Person, dann klären Sie den Vorfall. Diese Schritte gelten für die betroffene Person:'
  };
  var NAV_TITLE = {
    mobbing: 'Bei Beleidigung und Ausgrenzung',
    bild: 'Wenn ein Foto oder Video verbreitet wird',
    drohung: 'Bei Drohung oder Erpressung',
    hass: 'Bei Hass gegen dich oder eine Gruppe',
    fake: 'Bei Gerüchten und Fake-Profilen'
  };
  var NAV_STEPS = {
    mobbing: [
      'Nicht antworten, auch wenn es schwerfällt. Antworten stacheln oft weiter an.',
      'Screenshots machen: Nachricht, Datum, Uhrzeit und Absender müssen zu sehen sein.',
      'Absender blockieren und den Inhalt über die Meldefunktion der Plattform melden.',
      'Einer Vertrauensperson davon erzählen – Eltern, Freund:in, Lehrkraft oder Beratung.'
    ],
    bild: [
      'Das Bild oder Video nicht weiterleiten, auch nicht, um es jemandem zu zeigen. Stattdessen Screenshot und Link des Beitrags sichern.',
      'Bei der Plattform melden und Löschung verlangen. Fotos ohne Erlaubnis zu verbreiten, verletzt das Recht am eigenen Bild.',
      'Bei intimen Bildern gilt: Das kann strafbar sein, und du bist nicht schuld. Hol dir sofort Unterstützung.',
      'Mit einer Vertrauensperson entscheiden, ob ihr Anzeige erstattet.'
    ],
    drohung: [
      'Wenn du dich in Gefahr fühlst: sofort die Polizei unter 110 anrufen.',
      'Nicht auf Forderungen eingehen – kein Geld zahlen, keine Bilder schicken.',
      'Alles sichern: Screenshots, Links und Profilnamen.',
      'Profile auf privat stellen, keinen Aufenthaltsort posten, Passwörter ändern und nicht allein bleiben.',
      'Anzeige erstatten – das geht auch über die Online-Wache der Polizei deines Bundeslandes.'
    ],
    hass: [
      'Nicht zurückhassen und dich nicht auf Diskussionen einlassen.',
      'Beweistaugliche Screenshots: Kommentar, Datum, Uhrzeit, Absender, Bezugs-Post und Plattform.',
      'Den Kommentar bei der Plattform melden und bei Beleidigung, Drohung oder Volksverhetzung „rechtswidrig“ wählen.',
      'Kostenlose Beratung nutzen, zum Beispiel bei HateAid – der erste Kontakt geht auch anonym.',
      'Pausen machen und Kommentare ausblenden. Du musst das nicht aushalten.'
    ],
    fake: [
      'Ruhig bleiben und nicht öffentlich dagegen anschreiben.',
      'Fake-Profil oder Beitrag sichern: Screenshot und Link.',
      'Bei der Plattform melden – Fake-Profile und Identitätsdiebstahl sind eigene Meldegründe.',
      'Freund:innen bitten, ebenfalls zu melden und nichts zu teilen.',
      'Mit einer Vertrauensperson besprechen, ob weitere Schritte nötig sind.'
    ]
  };
  var NAV_EXTRA_GRUPPE = [
    'Schulleitung informieren und das Vorgehen nach dem Krisenplan Ihrer Einrichtung abstimmen.',
    'Die Eltern einbeziehen – in Absprache mit der betroffenen Person.'
  ];

  function contactsFor(wer, was) {
    var list = [];
    if (was === 'drohung') list.push('notruf');
    if (wer === 'kind') list.push('eltern', 'kjt');
    else if (wer === 'gruppe') list.push(was === 'hass' ? 'hateaid' : 'kjt', 'eltern');
    else list.push('kjt', 'juuuport');
    if (was === 'hass' && list.indexOf('hateaid') === -1) list.push('hateaid');
    return list.slice(0, 3);
  }

  function helpCard(id) {
    var h = D.hilfe[id]; if (!h) return '';
    var urgent = id === 'notruf' ? ' help-card--urgent' : '';
    var tel = h.tel ? '<a class="help-card__tel" href="tel:' + h.tel.replace(/[^\d+]/g, '') + '">' + h.tel + '</a>' : '';
    var link = h.url ? '<a class="link-arrow" href="' + h.url + '" rel="noopener">Zur Website →</a>' : '';
    return '<article class="help-card' + urgent + '"><p class="help-card__for">' + h.fuer + '</p><h4>' + h.name + '</h4>' + tel + '<p>' + h.wann + '</p>' + link + '</article>';
  }

  $$('[data-navigator]').forEach(function (nav) {
    nav.hidden = false;
    var stat = nav.parentNode.querySelector('[data-nav-static]');
    if (stat) stat.hidden = true;
    var answers = {}, result = $('[data-result]', nav);

    nav.addEventListener('click', function (e) {
      var chip = e.target.closest('[data-q]');
      if (!chip) return;
      var q = chip.getAttribute('data-q');
      answers[q] = chip.getAttribute('data-a');
      $$('[data-q="' + q + '"]', nav).forEach(function (c) { c.setAttribute('aria-pressed', String(c === chip)); });
      if (answers.wer && answers.was) render();
    });

    function render() {
      var steps = NAV_STEPS[answers.was].slice();
      if (answers.wer === 'gruppe') steps = steps.concat(NAV_EXTRA_GRUPPE);
      var html = '<h3>' + NAV_TITLE[answers.was] + '</h3>' +
        '<p class="muted" style="margin-top:.5rem">' + NAV_INTRO[answers.wer] + '</p>' +
        '<ol>' + steps.map(function (s) { return '<li>' + s + '</li>'; }).join('') + '</ol>' +
        '<h4 style="margin-top:1.5rem">Hier bekommst du Hilfe</h4>' +
        '<div class="help-grid" style="margin-top:.75rem">' + contactsFor(answers.wer, answers.was).map(helpCard).join('') + '</div>' +
        '<p style="margin-top:1.25rem"><a class="link-arrow" href="hilfe.html#beweise">So sicherst du Beweise richtig →</a></p>';
      result.innerHTML = html;
      result.hidden = false;
      var h = $('h3', result); h.setAttribute('tabindex', '-1'); h.focus({ preventScroll: true });
      result.scrollIntoView({ behavior: reduceMotion ? 'auto' : 'smooth', block: 'nearest' });
    }
  });

  /* 5 · Merkliste ---------------------------------------------------- */
  // Gespeichert wird nur eine Liste von IDs im Browser. Unbekannte IDs (z. B. nach Umbenennungen) fallen raus.
  var TITEL = D.materialien || null;
  function ladeMerkliste() {
    var s = store.get('netzfest:merkliste', []);
    if (!Array.isArray(s)) s = [];
    var sauber = s.filter(function (id, i) {
      return typeof id === 'string' && s.indexOf(id) === i && (!TITEL || Object.prototype.hasOwnProperty.call(TITEL, id));
    });
    if (sauber.length !== s.length) store.set('netzfest:merkliste', sauber);
    return sauber;
  }
  var saved = ladeMerkliste();

  // Ansage für Screenreader (sichtbar ist die Rückmeldung am Knopf und an der Zahl im Kopf)
  var saveLive = document.createElement('p');
  saveLive.className = 'sr-only'; saveLive.setAttribute('aria-live', 'polite');
  document.body.appendChild(saveLive);
  function ansage(text) { saveLive.textContent = ''; setTimeout(function () { saveLive.textContent = text; }, 50); }
  function anzahlText(n) { return n === 1 ? '1 Material gemerkt' : n + ' Materialien gemerkt'; }

  function syncSaved() {
    $$('[data-save]').forEach(function (b) {
      var on = saved.indexOf(b.getAttribute('data-save')) !== -1;
      b.setAttribute('aria-pressed', String(on));
      b.title = on ? 'Aus der Merkliste entfernen' : 'Zur Merkliste hinzufügen';
      var lbl = $('.lbl', b); if (lbl) lbl.textContent = on ? 'Gemerkt' : 'Merken';
    });
    $$('[data-save-count]').forEach(function (c) { c.textContent = saved.length; c.hidden = saved.length === 0; });
    var coll = $('[data-collection]');
    if (coll) {
      // zuletzt Gemerktes zuerst
      saved.slice().reverse().forEach(function (id) {
        var card = $('.mcard[data-id="' + id + '"]', coll);
        if (card) coll.appendChild(card);
      });
      $$('.mcard', coll).forEach(function (card) { card.hidden = saved.indexOf(card.getAttribute('data-id')) === -1; });
      $('[data-collection-empty]').hidden = saved.length > 0;
      var bar = $('[data-collection-bar]');
      if (bar) { bar.hidden = saved.length === 0; $('[data-collection-count]', bar).textContent = anzahlText(saved.length); }
    }
  }

  document.addEventListener('click', function (e) {
    var b = e.target.closest('[data-save]');
    if (b) {
      e.preventDefault();
      var id = b.getAttribute('data-save');
      saved = ladeMerkliste();                      // aktuellen Stand holen (anderer Tab)
      var i = saved.indexOf(id), titel = (TITEL && TITEL[id]) || 'Material';
      var coll = $('[data-collection]');
      var karte = coll && b.closest('.mcard');
      var naechste = null;
      if (karte && i !== -1) {                      // auf der Merkliste: Fokus nach dem Entfernen sinnvoll setzen
        var sichtbar = $$('.mcard', coll).filter(function (c) { return !c.hidden; });
        var pos = sichtbar.indexOf(karte);
        naechste = sichtbar[pos + 1] || sichtbar[pos - 1] || null;
      }
      if (i === -1) saved.push(id); else saved.splice(i, 1);
      store.set('netzfest:merkliste', saved);
      syncSaved();
      ansage('„' + titel + '“ ' + (i === -1 ? 'gemerkt' : 'aus der Merkliste entfernt') + '. ' + anzahlText(saved.length) + '.');
      if (karte && i !== -1) {
        if (naechste) $('[data-save]', naechste).focus();
        else { var t = $('[data-collection-empty-title]'); if (t) t.focus(); }
      }
      return;
    }
    if (e.target.closest('[data-collection-clear]')) {
      if (!saved.length || !window.confirm('Alle ' + saved.length + ' gemerkten Materialien entfernen?')) return;
      saved = [];
      store.set('netzfest:merkliste', saved);
      syncSaved();
      ansage('Merkliste geleert.');
      var leer = $('[data-collection-empty-title]'); if (leer) leer.focus();
    }
  });

  // Stand angleichen: anderer Tab hat geändert, oder Seite kommt per „Zurück“ aus dem Zwischenspeicher
  window.addEventListener('storage', function (e) {
    if (e.key === null || e.key === 'netzfest:merkliste') { saved = ladeMerkliste(); syncSaved(); }
  });
  window.addEventListener('pageshow', function (e) {
    if (e.persisted) { saved = ladeMerkliste(); syncSaved(); }
  });

  /* 6 · Bibliothek --------------------------------------------------- */
  var lib = $('[data-library]');
  if (lib) {
    var GROUPS = ['thema', 'fuer', 'niveau', 'schule', 'alter', 'zeit'];
    var state = {}; GROUPS.forEach(function (g) { state[g] = []; });
    var params = new URLSearchParams(location.search);
    GROUPS.forEach(function (g) { if (params.get(g)) state[g] = params.get(g).split(','); });
    var search = $('[data-search]', lib);
    search.value = params.get('q') || '';
    if (!params.get('fuer') && role) state.fuer = [role];

    var cards = $$('.mcard', lib), countEl = $('[data-count]', lib), empty = $('[data-empty]', lib);
    var activeEl = $('[data-active-count]', lib), panel = $('#filter-panel'), toggle = $('[data-filter-toggle]', lib);
    var banner = $('[data-role-banner]');

    function matches(c) {
      var d = c.dataset, f = state;
      if (f.thema.length && f.thema.indexOf(d.thema) === -1) return false;
      if (f.fuer.length && !f.fuer.some(function (x) { return d.zielgruppe.split(' ').indexOf(x) !== -1; })) return false;
      if (f.niveau.length && f.niveau.indexOf(d.niveau) === -1) return false;
      if (f.schule.length && !f.schule.some(function (x) { return d.schule.split(' ').indexOf(x) !== -1; })) return false;
      if (f.alter.length && d.alter) {
        var mm = d.alter.split('-').map(Number);
        var fits = f.alter.some(function (k) { var g = k.split('-').map(Number); return mm[0] <= g[1] && mm[1] >= g[0]; });
        if (!fits) return false;
      }
      if (f.zeit.length) {
        var max = Math.max.apply(null, f.zeit.map(Number));
        if (Number(d.dauer) > max) return false;
      }
      var q = search.value.trim().toLowerCase();
      if (q && d.text.indexOf(q) === -1) return false;
      return true;
    }

    function update() {
      var n = 0;
      cards.forEach(function (c) { var ok = matches(c); c.hidden = !ok; if (ok) n++; });
      countEl.textContent = n === 1 ? '1 Material passt' : n + ' Materialien passen';
      $('[data-filter-done]', lib).textContent = n === 1 ? '1 Ergebnis anzeigen' : n + ' Ergebnisse anzeigen';
      empty.hidden = n !== 0;
      $$('[data-filter]', lib).forEach(function (chip) {
        chip.setAttribute('aria-pressed', String(state[chip.dataset.filter].indexOf(chip.dataset.value) !== -1));
      });
      var active = GROUPS.reduce(function (s, g) { return s + state[g].length; }, 0);
      var more = $('[data-more-filters]', lib);
      if (more && (state.alter.length || state.schule.length || state.niveau.length)) more.open = true;
      activeEl.textContent = active ? '(' + active + ')' : '';
      var p = new URLSearchParams();
      GROUPS.forEach(function (g) { if (state[g].length) p.set(g, state[g].join(',')); });
      if (search.value.trim()) p.set('q', search.value.trim());
      history.replaceState(null, '', location.pathname + (p.toString() ? '?' + p : ''));
      if (banner) {
        banner.hidden = !role;
        if (role) {
          $('[data-role-name]', banner).textContent = D.rollen[role];
        }
      }
    }

    lib.addEventListener('click', function (e) {
      var chip = e.target.closest('[data-filter]');
      if (chip) {
        var g = chip.dataset.filter, v = chip.dataset.value, i = state[g].indexOf(v);
        if (i === -1) state[g].push(v); else state[g].splice(i, 1);
        update();
      }
      if (e.target.closest('[data-reset]')) {
        GROUPS.forEach(function (g) { state[g] = []; }); search.value = ''; update();
      }
    });
    search.addEventListener('input', update);
    function setPanel(open) {
      toggle.setAttribute('aria-expanded', String(open));
      panel.classList.toggle('is-open', open);
      if (open) { panel.scrollIntoView({ block: 'start', behavior: reduceMotion ? 'auto' : 'smooth' }); var c = $('.chip', panel); if (c) c.focus({ preventScroll: true }); }
    }
    toggle.addEventListener('click', function () { setPanel(toggle.getAttribute('aria-expanded') !== 'true'); });
    $('[data-filter-done]', lib).addEventListener('click', function () {
      setPanel(false);
      toggle.scrollIntoView({ block: 'start', behavior: reduceMotion ? 'auto' : 'smooth' });
      toggle.focus({ preventScroll: true });
    });
    if (banner) {
      $('[data-role-clear]', banner).addEventListener('click', function () { setRole(null); });
      $('[data-role-clear]', banner).textContent = 'Alle Inhalte zeigen';
    }
    document.addEventListener('netzfest:role', function (e) { state.fuer = e.detail ? [e.detail] : []; update(); });
    update();
  }

  /* 7 · Hero: Einblenden & „Das Netz hält“ -------------------------- */
  $$('[data-reveal-root]').forEach(function (el) {
    var done = false;
    var go = function () { if (!done) { done = true; el.classList.add('is-in'); } };
    requestAnimationFrame(function () { requestAnimationFrame(go); });
    setTimeout(go, 400); // Absicherung, falls rAF im Hintergrund-Tab ruht
  });

  var canvas = $('[data-net]');
  if (canvas && !reduceMotion && canvas.getContext) {
    var hero = canvas.parentNode;
    hero.classList.add('js-net');
    var ctx = canvas.getContext('2d'), pts = [], W = 0, H = 0, dpr = 1;
    var pointer = null, running = false, visible = true, raf = 0;
    var LINK = 110, REACH = 170;

    function resize() {
      var r = hero.getBoundingClientRect();
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      W = r.width; H = r.height;
      canvas.width = W * dpr; canvas.height = H * dpr;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      var n = Math.max(36, Math.min(90, Math.round(W * H / 15000)));
      pts = [];
      for (var i = 0; i < n; i++) {
        pts.push({ x: Math.random() * W, y: Math.random() * H, vx: (Math.random() - 0.5) * 0.25, vy: (Math.random() - 0.5) * 0.25 });
      }
    }

    function frame() {
      ctx.clearRect(0, 0, W, H);
      var reach = REACH * (role ? 1.3 : 1); // gewählte Rolle → das Netz wird enger
      var i, j, a, b, dx, dy, d, alpha;
      for (i = 0; i < pts.length; i++) {
        a = pts[i];
        a.x += a.vx; a.y += a.vy;
        if (a.x < -20) a.x = W + 20; if (a.x > W + 20) a.x = -20;
        if (a.y < -20) a.y = H + 20; if (a.y > H + 20) a.y = -20;
        a.near = pointer ? Math.hypot(a.x - pointer.x, a.y - pointer.y) < reach : false;
      }
      ctx.lineWidth = 1;
      for (i = 0; i < pts.length; i++) {
        a = pts[i];
        for (j = i + 1; j < pts.length; j++) {
          b = pts[j]; dx = a.x - b.x; dy = a.y - b.y; d = dx * dx + dy * dy;
          var lim = (a.near && b.near) ? reach * 0.9 : LINK;
          if (d < lim * lim) {
            d = Math.sqrt(d);
            alpha = (a.near && b.near ? 0.6 : 0.2) * (1 - d / lim);
            ctx.strokeStyle = 'rgba(124,152,133,' + alpha.toFixed(3) + ')';
            ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y); ctx.stroke();
          }
        }
        if (a.near) {
          d = Math.hypot(a.x - pointer.x, a.y - pointer.y);
          ctx.strokeStyle = 'rgba(3,63,99,' + (0.35 * (1 - d / reach)).toFixed(3) + ')';
          ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(pointer.x, pointer.y); ctx.stroke();
        }
      }
      for (i = 0; i < pts.length; i++) {
        a = pts[i];
        ctx.fillStyle = a.near ? 'rgba(3,63,99,.9)' : 'rgba(40,102,110,.45)';
        ctx.beginPath(); ctx.arc(a.x, a.y, a.near ? 2.6 : 1.8, 0, Math.PI * 2); ctx.fill();
      }
      raf = requestAnimationFrame(frame);
    }
    function start() { if (!running && visible && !document.hidden) { running = true; frame(); } }
    function stop() { running = false; cancelAnimationFrame(raf); }

    hero.addEventListener('pointermove', function (e) {
      var r = hero.getBoundingClientRect(); pointer = { x: e.clientX - r.left, y: e.clientY - r.top };
    });
    hero.addEventListener('pointerleave', function () { pointer = null; });
    window.addEventListener('resize', function () { resize(); });
    document.addEventListener('visibilitychange', function () { if (document.hidden) stop(); else start(); });
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (en) { visible = en[0].isIntersecting; if (visible) start(); else stop(); }).observe(hero);
    }
    resize(); start();
  }

  /* 8 · Fake Detektiv ------------------------------------------------ */
  var QUIZ = [
    { h: ['Die Nummer gegen Kummer ist für Kinder und Jugendliche kostenlos und anonym erreichbar.',
      'Neue Studie: Wer morgens Schokolade isst, schreibt zwei Noten besser!',
      'Screenshots mit Datum und Uhrzeit können bei Cybermobbing als Beweis helfen.',
      'Viele Plattformen haben eine Funktion, um Beiträge zu melden.'], fake: 1,
      why: 'Keine Quelle, kein Name der Studie – und das Ergebnis klingt zu schön, um wahr zu sein.' },
    { h: ['Mit einer Rückwärts-Bildersuche kann man herausfinden, wo ein Foto schon einmal aufgetaucht ist.',
      'Bilder lassen sich mit KI so verändern, dass sie täuschend echt aussehen.',
      'EILMELDUNG!!! Ab Montag kostet WhatsApp Geld – leite das an 10 Kontakte weiter, sonst wird dein Konto gelöscht!',
      'Beleidigungen können auch im Internet strafbar sein.'], fake: 2,
      why: 'Typischer Kettenbrief: Großbuchstaben, Zeitdruck, eine Drohung und die Aufforderung zum Weiterleiten.' },
    { h: ['In Deutschland gibt es Meldestellen, an die man Hass im Netz melden kann.',
      'Seriöse Nachrichtenseiten nennen Autor:in und Datum ihrer Artikel.',
      'In den meisten Messengern kann man Kontakte blockieren.',
      'Foto beweist: Hai schwimmt nach Unwetter durch die Fußgängerzone!'], fake: 3,
      why: 'Solche „Beweisfotos“ sind oft Montagen oder stammen aus einem ganz anderen Zusammenhang. Eine Rückwärts-Bildersuche hilft.' },
    { h: ['Insider verrät: Lehrkräfte dürfen ab sofort alle Handys jederzeit durchsuchen!',
      'Wer peinliche Fotos von anderen ohne Erlaubnis verbreitet, kann gegen deren Rechte verstoßen.',
      'Faktencheck-Redaktionen prüfen virale Behauptungen und veröffentlichen die Ergebnisse.',
      'Viele Falschmeldungen setzen auf starke Gefühle wie Wut oder Angst.'], fake: 0,
      why: 'Ein anonymer „Insider“ ist keine Quelle. Neue Regeln würden offiziell von Schule oder Ministerium bekannt gegeben.' },
    { h: ['KI-Bilder können Fehler bei Händen, Schrift oder Schatten zeigen – müssen es aber nicht.',
      'Sensation: Neues Update lädt deinen Handy-Akku in 3 Sekunden – einfach diesen Link öffnen!',
      'Satire-Seiten veröffentlichen absichtlich erfundene Meldungen, um zu unterhalten oder zu kritisieren.',
      'Wer Hasskommentare meldet, sollte vorher Screenshots machen.'], fake: 1,
      why: 'Clickbait mit Link: Unglaubliches Versprechen plus Aufforderung zum Klicken ist eine klassische Masche – oft steckt Betrug dahinter.' },
    { h: ['Auch Liken und Weiterleiten kann bei Cybermobbing verletzen.',
      'Zwei-Quellen-Prinzip: Eine Information erst übernehmen, wenn zwei unabhängige Quellen sie bestätigen.',
      'Fake-Profile können bei den Plattformen gemeldet werden.',
      'Arzt packt aus: Diese Wahrheit über Handystrahlung wollen alle Behörden verschweigen!'], fake: 3,
      why: 'Typisches Muster: ein angeblicher Experte, ein großes Geheimnis („wollen verschweigen“) und keine überprüfbaren Belege.' }
  ];

  var quiz = $('[data-quiz]');
  if (quiz) {
    var round = 0, score = 0, picked = null;
    var LETTERS = 'ABCD';

    function drawRound() {
      var r = QUIZ[round];
      quiz.innerHTML =
        '<div class="quiz__top"><span>Runde ' + (round + 1) + ' von ' + QUIZ.length + '</span><span>Punkte: ' + score + '</span></div>' +
        '<div class="progress" aria-hidden="true"><span style="width:' + (round / QUIZ.length * 100) + '%"></span></div>' +
        '<h2 tabindex="-1">Welche Meldung ist erfunden?</h2>' +
        '<ul class="quiz__options">' + r.h.map(function (t, i) {
          return '<li><button type="button" class="quiz__opt" data-opt="' + i + '"><span class="quiz__letter">' + LETTERS[i] + '</span><span>' + t + '</span><span class="quiz__mark"></span></button></li>';
        }).join('') + '</ul><div data-feedback aria-live="polite"></div>';
      picked = null;
    }

    function answer(i) {
      if (picked !== null) return;
      picked = i;
      var r = QUIZ[round], right = i === r.fake;
      if (right) score++;
      $$('.quiz__opt', quiz).forEach(function (b, k) {
        b.disabled = true;
        b.classList.add(k === r.fake ? 'is-fake' : 'is-true');
        if (k === i) b.classList.add('is-picked');
        $('.quiz__mark', b).textContent = k === r.fake ? 'erfunden' : 'stimmt';
      });
      var last = round + 1 >= QUIZ.length;
      var fb = $('[data-feedback]', quiz);
      fb.innerHTML = '<div class="quiz__feedback ' + (right ? 'is-right' : 'is-wrong') + '"><p><strong>' +
        (right ? 'Richtig erkannt!' : 'Knapp daneben – Meldung ' + LETTERS[r.fake] + ' war erfunden.') + '</strong></p><p>' + r.why + '</p>' +
        '<p style="margin-top:1rem"><button type="button" class="btn btn--ink" data-next>' + (last ? 'Ergebnis ansehen' : 'Nächste Runde') + ' →</button></p></div>';
      $('[data-next]', fb).focus();
    }

    function result() {
      var all = score === QUIZ.length;
      quiz.innerHTML = '<div class="quiz__result"><p class="eyebrow">Ergebnis</p><p class="score">' + score + ' von ' + QUIZ.length + '</p>' +
        '<h2 tabindex="-1" style="margin-top:.5rem">' + (all ? 'Stark! Dich legt so schnell niemand rein.' : score >= QUIZ.length / 2 ? 'Gut gemacht!' : 'Guter Anfang!') + '</h2>' +
        '<p class="muted" style="margin:.75rem auto 0;max-width:30rem">Merke dir: Erst prüfen, dann teilen. Quelle, Datum, Gegencheck – und dem Bauchgefühl misstrauen, wenn eine Meldung sehr wütend oder sehr glücklich macht.</p>' +
        '<p style="margin-top:1.5rem;display:flex;gap:.75rem;justify-content:center;flex-wrap:wrap"><button type="button" class="btn btn--ink" data-restart>Nochmal spielen</button>' +
        '<a class="btn btn--ghost" href="wissen-fakenews.html#pruefen">So prüfst du Fakes</a></p></div>';
      $('h2', quiz).focus();
    }

    quiz.addEventListener('click', function (e) {
      var opt = e.target.closest('[data-opt]');
      if (opt) answer(Number(opt.getAttribute('data-opt')));
      if (e.target.closest('[data-next]')) {
        round++;
        if (round >= QUIZ.length) result(); else { drawRound(); $('h2', quiz).focus(); }
      }
      if (e.target.closest('[data-restart]')) { round = 0; score = 0; drawRound(); $('h2', quiz).focus(); }
    });
    drawRound();
  }

  /* Start ------------------------------------------------------------ */
  applyRole();
  syncSaved();
})();
