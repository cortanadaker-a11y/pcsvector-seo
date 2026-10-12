/* PCS Vector UI wiring (browser only). Depends on PCS (pcs.js). */
(function () {
  'use strict';
  if (typeof document === 'undefined') return;
  var P = window.PCS, D = null;
  var $ = function (id) { return document.getElementById(id); };
  var S = { g: 'E-5', d: 0, y: 4, cur: 'Fort Campbell, KY', tgt: 'Fort Bragg, NC', bar: false };
  var snap = null, gateOpen = false;
  var fine = window.matchMedia && window.matchMedia('(pointer:fine)').matches;

  function readQuery() {
    try {
      var q = new URLSearchParams(location.search);
      if (q.get('g')) S.g = q.get('g');
      if (q.get('d') !== null && q.get('d') !== '' && !isNaN(+q.get('d'))) S.d = Math.max(0, Math.min(5, parseInt(q.get('d'), 10)));
      if (q.get('y') !== null && q.get('y') !== '' && !isNaN(+q.get('y'))) S.y = Math.max(0, Math.min(40, parseInt(q.get('y'), 10)));
      if (q.has('cur')) S.cur = q.get('cur') || P.NONE_CURRENT;
      if (q.get('tgt')) S.tgt = q.get('tgt');
      if (q.get('bar') === '1') S.bar = true;
    } catch (e) {}
  }

  /* ---------- select widgets (native select; custom list on fine pointers to match Streamlit) ---------- */
  function setupSelect(id, opts, value, onChange) {
    var sel = $(id), wrap = sel.parentNode, val = wrap.querySelector('.val');
    sel.innerHTML = opts.map(function (o) { return '<option value="' + P.escAttr(o[0]) + '">' + P.escAttr(o[1]) + '</option>'; }).join('');
    function label(v) { for (var i = 0; i < opts.length; i++) if (opts[i][0] === v) return opts[i][1]; return v; }
    function set(v, fire) { sel.value = v; val.textContent = label(sel.value); if (fire) onChange(sel.value); }
    set(String(value), false);
    sel.addEventListener('change', function () { set(sel.value, true); });
    if (!fine) return set;
    var list = null, act = -1;
    function close() { if (list) { list.remove(); list = null; wrap.setAttribute('aria-expanded', 'false'); document.removeEventListener('mousedown', outside, true); } }
    function outside(e) { if (list && !wrap.contains(e.target)) close(); }
    function mark(i) {
      if (!list) return; var items = list.children;
      if (act >= 0 && items[act]) items[act].classList.remove('act');
      act = Math.max(0, Math.min(items.length - 1, i)); items[act].classList.add('act');
      var it = items[act]; if (it.offsetTop < list.scrollTop) list.scrollTop = it.offsetTop; else if (it.offsetTop + it.offsetHeight > list.scrollTop + list.clientHeight) list.scrollTop = it.offsetTop + it.offsetHeight - list.clientHeight;
    }
    function open() {
      if (list) return; list = document.createElement('ul'); list.className = 'pcs-list'; list.setAttribute('role', 'listbox');
      var cur = opts.findIndex(function (o) { return o[0] === sel.value; });
      list.innerHTML = opts.map(function (o, i) { return '<li role="option" data-i="' + i + '" aria-selected="' + (i === cur) + '">' + P.escAttr(o[1]) + '</li>'; }).join('');
      wrap.appendChild(list); wrap.setAttribute('aria-expanded', 'true'); act = -1; mark(cur < 0 ? 0 : cur);
      list.scrollTop = Math.max(0, list.children[act].offsetTop - 120);
      list.addEventListener('mousedown', function (e) { e.preventDefault(); var li = e.target.closest('li'); if (li) { set(opts[+li.dataset.i][0], true); close(); sel.focus(); } });
      list.addEventListener('mousemove', function (e) { var li = e.target.closest('li'); if (li) mark(+li.dataset.i); });
      document.addEventListener('mousedown', outside, true);
    }
    var typed = '', typedAt = 0;
    sel.addEventListener('mousedown', function (e) { e.preventDefault(); sel.focus(); list ? close() : open(); });
    sel.addEventListener('blur', function () { setTimeout(close, 120); });
    sel.addEventListener('keydown', function (e) {
      var k = e.key;
      if (!list && (k === 'ArrowDown' || k === 'ArrowUp' || k === 'Enter' || k === ' ')) { e.preventDefault(); open(); return; }
      if (!list) return;
      if (k === 'Escape' || k === 'Tab') { close(); return; }
      if (k === 'ArrowDown') { e.preventDefault(); mark(act + 1); } else if (k === 'ArrowUp') { e.preventDefault(); mark(act - 1); }
      else if (k === 'Home') { e.preventDefault(); mark(0); } else if (k === 'End') { e.preventDefault(); mark(opts.length - 1); }
      else if (k === 'Enter' || k === ' ') { e.preventDefault(); set(opts[act][0], true); close(); }
      else if (k.length === 1) {
        e.preventDefault(); var now = Date.now(); typed = (now - typedAt < 700 ? typed : '') + k.toLowerCase(); typedAt = now;
        for (var i = 0; i < opts.length; i++) if (opts[i][1].toLowerCase().indexOf(typed) === 0) { mark(i); break; }
      }
    });
    return set;
  }

  /* ---------- results + Wayfinder ---------- */
  function render() {
    var r = P.renderResults(D, S);
    $('pcs-results').innerHTML = r.warn ? '<div class="pcs-alert pcs-alert-' + (r.kind || 'warn') + '" role="status">' + P.safeHtml(r.warn) + '</div>' : r.html;
    snap = r.snap;
    renderReferral();
  }
  function renderReferral() {
    var c = P.calcFields(snap || {}), dest = c.destination, ready = !!dest;
    var bit = dest ? P.shortDest(dest, 22) : '';
    $('pcs-way-kicker').innerHTML = P.safeHtml(bit ? 'Military-approved agents \u00b7 ' + bit : 'Military-approved local agents \u00b7 worldwide');
    $('referral_submit_btn').disabled = !ready;
    $('pcs-ref-caption').textContent = ready ? 'Free \u00b7 no obligation' : 'Pick a New post above first';
    var bar = $('pcs-sticky-ref-bar');
    if (!dest) { bar.hidden = true; document.documentElement.classList.remove('pcs-has-sticky-ref'); return; }
    bar.hidden = false; document.documentElement.classList.add('pcs-has-sticky-ref');
    var line = $('pcs-sticky-ref-line');
    line.title = dest; line.textContent = P.shortDest(dest) + ' \u00b7 ' + (c.rank || '\u2014') + ' \u00b7 ' + (c.dependents_short || '\u2014');
  }
  function openGate(focus) {
    gateOpen = true; $('pcs-match-panel').classList.add('pcs-ref-open');
    if (focus) setTimeout(function () { try { $('referral_first_name').focus({ preventScroll: true }); } catch (e) {} }, 50);
  }
  function scrollToReferral() { var t = $('pcs-referral'); if (t && t.scrollIntoView) t.scrollIntoView({ block: 'start', behavior: 'smooth' }); }
  function submitReferral(e) {
    e.preventDefault();
    var msg = $('pcs-ref-msg'); msg.innerHTML = '';
    var res = P.validate(snap, $('referral_first_name').value, $('referral_email_address').value);
    if (res.error) { msg.innerHTML = '<div class="pcs-alert pcs-alert-err" role="alert">' + P.safeHtml(res.error) + '</div>'; return; }
    try { sessionStorage.setItem('pcs_referral_lead', JSON.stringify(res.row)); } catch (e2) {}
    msg.innerHTML = '<div class="pcs-alert pcs-alert-ok" role="status">Opening your pre-filled form \u2014 tap <strong>Submit</strong> on the next page. ' +
      '<a href="' + P.escAttr(res.url) + '" rel="noopener">Open the form \u2794</a></div>';
    setTimeout(function () { window.location.assign(res.url); }, 350);
  }

  function setupHelp() {
    Array.prototype.forEach.call(document.querySelectorAll('.pcs-help'), function (b) {
      var tip = b.querySelector('.pcs-tip');
      function place() {
        if (!tip) return; tip.style.transform = '';
        var r = tip.getBoundingClientRect(); if (!r.width) return;
        var vw = document.documentElement.clientWidth, dx = r.left < 8 ? 8 - r.left : (r.right > vw - 8 ? vw - 8 - r.right : 0);
        if (dx) tip.style.transform = 'translateX(' + Math.round(dx) + 'px)';
      }
      b.addEventListener('mouseenter', place); b.addEventListener('focus', place);
      b.addEventListener('click', function (e) { e.preventDefault(); e.stopPropagation(); b.classList.toggle('show'); place(); });
      b.addEventListener('blur', function () { b.classList.remove('show'); });
    });
  }
  function setupSidebar() {
    var sb = $('pcs-sidebar'), scrim = $('pcs-scrim');
    function set(o) { sb.classList.toggle('open', o); scrim.classList.toggle('open', o); sb.setAttribute('aria-hidden', String(!o)); if (o) sb.removeAttribute('inert'); else sb.setAttribute('inert', ''); $('pcs-sidebar-open').setAttribute('aria-expanded', String(o)); if (o) $('pcs-sidebar-close').focus(); }
    $('pcs-sidebar-open').addEventListener('click', function () { set(true); });
    $('pcs-sidebar-close').addEventListener('click', function () { set(false); $('pcs-sidebar-open').focus(); });
    scrim.addEventListener('click', function () { set(false); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && sb.classList.contains('open')) set(false); });
  }
  function setupSticky() {
    var bar = $('pcs-sticky-ref-bar'), target = $('pcs-match-panel');
    $('pcs-sticky-ref-go').addEventListener('click', function (e) { e.preventDefault(); if (!gateOpen) openGate(false); scrollToReferral(); });
    if (!('IntersectionObserver' in window)) return;
    new IntersectionObserver(function (es) {
      var en = es[0]; bar.classList.toggle('pcs-sticky-ref-hidden', !!(en && en.isIntersecting && en.intersectionRatio > 0.15));
    }, { threshold: [0, 0.15, 0.35, 0.6, 1], rootMargin: '0px 0px -80px 0px' }).observe(target);
  }

  function init(data) {
    D = data;
    var posts = Object.keys(D.posts).sort();
    if (D.grades.indexOf(S.g) < 0) S.g = 'E-5';
    if (!D.posts[S.tgt]) S.tgt = 'Fort Bragg, NC';
    if (S.cur !== P.NONE_CURRENT && !D.posts[S.cur]) S.cur = 'Fort Campbell, KY';
    var depsLabel = function (n) { return n === 0 ? '0' : n === 5 ? '5+' : String(n); };
    var setBar = function () { var cb = $('bah_calc_barracks'); cb.disabled = S.d > 0; if (S.d > 0) cb.checked = false; };
    setupSelect('bah_calc_grade', D.grades.map(function (g) { return [g, g]; }), S.g, function (v) { S.g = v; render(); });
    setupSelect('bah_calc_deps_n', [0, 1, 2, 3, 4, 5].map(function (n) { return [String(n), depsLabel(n)]; }), S.d, function (v) { S.d = parseInt(v, 10) || 0; setBar(); S.bar = $('bah_calc_barracks').checked; render(); });
    var yos = []; for (var i = 0; i <= 40; i++) yos.push([String(i), String(i)]);
    setupSelect('bah_calc_yos', yos, S.y, function (v) { S.y = parseInt(v, 10) || 0; render(); });
    setupSelect('bah_calc_current', [[P.NONE_CURRENT, P.NONE_CURRENT]].concat(posts.map(function (p) { return [p, p]; })), S.cur, function (v) { S.cur = v; render(); });
    setupSelect('bah_calc_gaining', posts.map(function (p) { return [p, p]; }), S.tgt, function (v) { S.tgt = v; render(); });
    var cb = $('bah_calc_barracks'); cb.checked = S.bar; setBar(); S.bar = cb.checked;
    cb.addEventListener('change', function () { S.bar = cb.checked; render(); });
    render();
    if (/^#(find-a-home|pcs-referral|wayfinder)$/.test(location.hash)) { openGate(true); setTimeout(scrollToReferral, 60); }
  }

  readQuery();
  setupHelp(); setupSidebar(); setupSticky();
  $('referral_open_btn').addEventListener('click', function () { openGate(true); });
  $('pcs-ref-form').addEventListener('submit', submitReferral);
  window.addEventListener('hashchange', function () { if (D && /^#(find-a-home|pcs-referral|wayfinder)$/.test(location.hash)) { openGate(true); setTimeout(scrollToReferral, 60); } });
  var boot = window.__PCS_DATA__;
  if (boot) init(boot);
  else fetch('/assets/calc-data.json').then(function (r) { return r.json(); }).then(init).catch(function () {
    $('pcs-results').insertAdjacentHTML('afterbegin', '<div class="pcs-alert pcs-alert-warn">Could not load 2026 rate data. Refresh the page to try again.</div>');
  });
})();
