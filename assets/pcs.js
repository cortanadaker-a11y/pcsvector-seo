/*! PCS Vector static app (pcsvector.com). Port of the original app (pcs-vector main):
    components/bah_calculator.py + services/housing_allowances.py + views/home.py (Wayfinder) + faq.
    Data in /assets/calc-data.json is exported from the Python services at build time (Python = source of truth).
    UNOFFICIAL / PERSONAL. Not affiliated with the U.S. Army, DoD or DTMO. */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.PCS = factory();
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';
  var NONE_CURRENT = '\u2014 Skip \u2014';
  var GRADE_ALIASES = { 'O-7+': 'O-7', 'O7+': 'O-7', 'Other': 'E-5' };
  var PAY_GRADE_TO_RANK = { 'E-1': 'Private', 'E-2': 'Private', 'E-3': 'Private First Class', 'E-4': 'Specialist',
    'E-5': 'Sergeant', 'E-6': 'Staff Sergeant', 'E-7': 'Sergeant First Class', 'E-8': 'Master Sergeant', 'E-9': 'Sergeant Major',
    'W-1': 'Warrant Officer 1', 'W-2': 'Chief Warrant Officer 2', 'W-3': 'Chief Warrant Officer 3', 'W-4': 'Chief Warrant Officer 4',
    'W-5': 'Chief Warrant Officer 5', 'O-1': 'Second Lieutenant', 'O-2': 'First Lieutenant', 'O-3': 'Captain', 'O-4': 'Major',
    'O-5': 'Lieutenant Colonel', 'O-6': 'Colonel', 'O-7+': 'General Officer' };

  /* Python round(): round half to even (for exact .5 binary values). */
  function pyRound(x) {
    var f = Math.floor(x), d = x - f;
    if (d > 0.5) return f + 1;
    if (d < 0.5) return f;
    return (f % 2 === 0) ? f : f + 1;
  }
  function intTrunc(x) { return x < 0 ? Math.ceil(x) : Math.floor(x); }
  function commas(n) { return String(n).replace(/\B(?=(\d{3})+(?!\d))/g, ','); }
  function money(n) { if (n === null || n === undefined) return '\u2014'; return (n < 0 ? '-' : '') + '$' + commas(Math.abs(n)); }
  /* components/html_utils.safe_html: html.escape(quote=False) + $ -> &#36; */
  function safeHtml(t) { return String(t).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/\$/g, '&#36;'); }
  function escAttr(t) { return String(t).replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }

  /* ---- services/housing_allowances.py ---- */
  function normGrade(g) { g = (g || 'E-5').trim(); return GRADE_ALIASES[g] || g; }
  function yosPayIndex(yos, bps) {
    yos = Math.max(0, Math.min(40, intTrunc(yos)));
    if (yos < 2) return 0;
    if (yos >= 40) return bps.length - 1;
    var idx = 0;
    for (var i = 0; i < bps.length; i++) if (yos >= bps[i]) idx = i;
    return idx;
  }
  function monthlyBasePay(D, grade, yos) {
    var t = D.cola, row = t.base_pay_monthly[normGrade(grade)] || t.base_pay_monthly['E-5'];
    if (!row) return null;
    var idx = yosPayIndex(yos, t.yos_breakpoints || [0, 2, 3, 4, 6, 8, 10, 12, 14, 16, 18, 20]);
    if (idx >= row.length) idx = row.length - 1;
    var pay = +(row[idx] || 0);
    return pay > 0 ? pay : null;
  }
  function colaCompensation(D, grade, yos, withDeps) {
    var t = D.cola, c = t.compensation || {}, r = c[normGrade(grade)];
    var row = r ? r[withDeps ? 'with' : 'without'] : null;
    if (!row) return null;
    var idx = Math.min(yosPayIndex(yos, t.yos_breakpoints || [0, 2, 3, 4, 6, 8, 10, 12, 14, 16, 18, 20]), row.length - 1);
    return intTrunc(row[idx]);
  }
  function annualSpendable(D, annual, deps) {
    deps = Math.max(0, Math.min(5, intTrunc(deps)));
    var rows = D.cola.spendable_table, last = null;
    for (var i = 0; i < rows.length; i++) {
      last = rows[i];
      if (rows[i][0] <= annual && annual <= rows[i][1]) return intTrunc(rows[i][2][deps]);
    }
    return last ? intTrunc(last[2][deps]) : 0;
  }
  function estimateMonthlyCola(D, grade, yos, deps, index, barracks) {
    if (index === null || index === undefined) return 0;
    index = +index;
    if (index <= 100) return 0;
    var comp = colaCompensation(D, grade, yos, intTrunc(deps) > 0);
    var monthly = monthlyBasePay(D, grade, yos);
    if (comp === null && monthly === null) return 0;
    /* DTMO picks spendable income by an annual-compensation bracket (grade x YOS x with/without deps), not base pay alone. */
    var spendable = annualSpendable(D, comp !== null ? comp : (monthly || 0) * 12, deps);
    var cola = spendable * (index - 100) / 100.0 / 12.0;
    if (barracks && intTrunc(deps) === 0) cola *= 0.63;
    var c = pyRound(cola);
    return c < 0 ? 0 : c;
  }
  /* get_housing_package(installation, pay_grade, num_dependents=deps, years_of_service=yos, barracks_meal_card=bar) */
  function housingPackage(D, post, grade, deps, yos, barracks) {
    var P = D.posts[post];
    if (!P) return { found: false, housing_system: 'BAH', total_monthly_usd: null };
    var gi = D.grades.indexOf(grade), wd = deps > 0 ? 1 : 0, inGov = !!barracks && deps === 0;
    var cola = 0, out = { housing_system: P.sys, cola_index: P.sys === 'BAH' ? null : P.ci, in_government_quarters: inGov,
      oha_rent_max_usd: null, oha_utility_usd: null, locality: P.loc || null };
    if (P.sys === 'OHA') {
      var ru = gi >= 0 ? P.oha[wd][gi] : [null, null];
      var rent = ru[0], util = ru[1], ohaTotal = (rent === null) ? null : rent + util;
      cola = estimateMonthlyCola(D, grade, yos, deps, P.ci, barracks);
      out.found = ohaTotal !== null;
      if (inGov && out.found) { rent = 0; util = 0; ohaTotal = 0; }
      out.oha_rent_max_usd = rent; out.oha_utility_usd = util; out.housing_monthly_usd = ohaTotal;
      out.cola_monthly_usd = cola; out.total_monthly_usd = ohaTotal === null ? null : ohaTotal + cola;
      return out;
    }
    var bah = gi >= 0 ? P.h[wd][gi] : null;
    if (P.sys === 'BAH_PLUS_COLA') cola = estimateMonthlyCola(D, grade, yos, deps, P.ci, barracks);
    out.found = bah !== null;
    if (inGov && out.found) bah = 0;
    out.housing_monthly_usd = bah; out.cola_monthly_usd = cola;
    out.total_monthly_usd = bah === null ? null : bah + cola;
    return out;
  }
  function marketRent(D, post, deps) { var r = D.posts[post].rent[Math.max(0, Math.min(5, deps))]; return { low: r[0], high: r[1], mid: r[2], br: r[3] }; }
  function systemChip(sys, barracks, cola) {
    if (barracks) return (cola || 0) > 0 ? 'Barracks + COLA' : 'Barracks';
    if (sys === 'OHA') return 'OHA + COLA';
    if (sys === 'BAH_PLUS_COLA') return 'BAH + COLA';
    return 'BAH';
  }

  /* ---- components/bah_calculator.render_bah_calculator (results block) ---- */
  function renderResults(D, s) {
    var grade = s.g, deps = Math.max(0, Math.min(5, s.d | 0)), yos = s.y | 0;
    var withDeps = deps > 0, barracks = withDeps ? false : !!s.bar;
    var gaining = s.tgt, current = (s.cur && s.cur !== NONE_CURRENT) ? s.cur : null;
    var pkg = housingPackage(D, gaining, grade, deps, yos, barracks);
    var cur = current ? housingPackage(D, current, grade, deps, yos, barracks) : null;
    if (!pkg.found || pkg.total_monthly_usd === null) {
      var warn;
      if (pkg.housing_system === 'OHA') {
        var loc = pkg.locality || gaining, idx = pkg.cola_index;
        warn = gaining + ' uses OHA (Overseas Housing Allowance), not BAH. This locality\'s OHA table isn\'t loaded yet, so get your exact rent ceiling and utility allowance from the DTMO OHA Rate Lookup (' + loc + ').' +
          (idx !== null && idx !== undefined ? ' COLA index: ' + idx + '.' : '');
        return { html: '', warn: warn, kind: 'info', snap: { pay_grade: grade } };
      } else warn = 'No 2026 rates for ' + grade + ' at ' + gaining + '. Try another post or ask finance.';
      return { html: '', warn: warn, kind: 'warn', snap: { pay_grade: grade } };
    }
    var system = pkg.housing_system || 'BAH', housing = pkg.housing_monthly_usd | 0, cola = pkg.cola_monthly_usd | 0, total = pkg.total_monthly_usd;
    var P = D.posts[gaining], utilN = P.util || 0;
    var ohaRent = pkg.oha_rent_max_usd;
    var m = marketRent(D, gaining, deps);
    var hasCompare = !!(current && cur && cur.found);
    var curRentLo = null, curRentHi = null, curUtilN = null, curMid = null;
    if (hasCompare) {
      curUtilN = D.posts[current].util || 0;
      var cm = marketRent(D, current, deps); curRentLo = cm.low; curRentHi = cm.high; curMid = cm.mid;
    }
    var tgtBarracks = !!pkg.in_government_quarters, curBarracks = !!(hasCompare && cur.in_government_quarters);
    var curSys = hasCompare ? (cur.housing_system || 'BAH') : null;
    var curColaPreview = hasCompare ? (cur.cola_monthly_usd | 0) : 0;
    var chip = systemChip(system, tgtBarracks, cola), curChip = curSys ? systemChip(curSys, curBarracks, curColaPreview) : '';
    var curTotal = (hasCompare && cur.total_monthly_usd !== null) ? cur.total_monthly_usd : null;
    var curOhaRent = null, curOhaUtil = null, curBah = null, curCola = 0;
    if (hasCompare) {
      if (curSys === 'OHA') { if (cur.oha_rent_max_usd !== null) curOhaRent = cur.oha_rent_max_usd; if (cur.oha_utility_usd !== null) curOhaUtil = cur.oha_utility_usd; }
      else if (cur.housing_monthly_usd !== null) curBah = cur.housing_monthly_usd;
      curCola = cur.cola_monthly_usd | 0;
    }
    var ohaUtil = pkg.oha_utility_usd, colaIdx = pkg.cola_index;
    var tgtBah = system !== 'OHA' ? housing : null, tgtOhaRent = system === 'OHA' ? ohaRent : null;
    var arrow, rollup = '', leftRent, leftUtil, leftGas;
    if (hasCompare && curTotal !== null) {
      var d = total - curTotal, dc, dt;
      if (d > 0) { dc = 'pcs-delta-up'; dt = '+' + money(d) + '/mo'; }
      else if (d < 0) { dc = 'pcs-delta-down'; dt = '-' + money(Math.abs(d)) + '/mo'; }
      else { dc = 'pcs-delta-flat'; dt = '$0/mo'; }
      arrow = '<div class="pcs-partner-arrow"><div class="pcs-partner-arrow-col"><div class="pcs-partner-arrow-loc">Current \u00b7 ' + safeHtml(curChip) +
        '</div><span class="pcs-partner-arrow-amt muted">' + money(curTotal) + '</span></div><span class="pcs-partner-arrow-glyph">\u2794</span>' +
        '<div class="pcs-partner-arrow-col pcs-partner-arrow-col-new"><div class="pcs-partner-arrow-loc">Target \u00b7 ' + safeHtml(chip) +
        '</div><span class="pcs-partner-arrow-amt">' + money(total) + '</span></div></div>' +
        '<div class="pcs-partner-delta-row"><span>Monthly total package</span><span class="pcs-bah-delta-badge ' + dc + '">' + dt + '</span></div>';
      var curCol = (curMid || 0) + (curUtilN || 0), tgtCol = (m.mid || 0) + (utilN || 0);
      if (curCol > 0) {
        var pct = pyRound(((tgtCol - curCol) / curCol) * 100), rc, rt;
        if (pct < 0) { rc = 'pcs-roll-down'; rt = Math.abs(pct) + '% lower'; }
        else if (pct > 0) { rc = 'pcs-roll-up'; rt = pct + '% higher'; }
        else { rc = 'pcs-roll-flat'; rt = 'about the same'; }
        rollup = '<div class="pcs-partner-rollup"><span>New Cost of Living Index</span><span class="pcs-partner-rollup-mids">' + money(curCol) +
          ' \u2192 ' + money(tgtCol) + '</span><span class="pcs-partner-rollup-badge ' + rc + '">' + rt + '</span></div>';
      }
      leftRent = money(curRentLo) + ' \u2013 ' + money(curRentHi);
      leftUtil = money(curUtilN || 0) + '/mo';
      leftGas = D.posts[current].gas || '\u2014';
    } else {
      arrow = '<div class="pcs-partner-arrow pcs-partner-arrow-solo"><div class="pcs-partner-arrow-col pcs-partner-arrow-col-new"><div class="pcs-partner-arrow-loc">Target \u00b7 ' +
        safeHtml(chip) + '</div><span class="pcs-partner-arrow-amt">' + money(total) + '</span></div></div>' +
        '<div class="pcs-partner-delta-row"><span>' + safeHtml(gaining) + '</span><span class="pcs-bah-delta-badge pcs-delta-flat">' + money(total) + '/mo total</span></div>';
      leftRent = leftUtil = leftGas = '\u2014';
    }
    var rightRent = money(m.low) + ' \u2013 ' + money(m.high), rightUtil = utilN ? money(utilN) + '/mo' : '\u2014', rightGas = P.gas || '\u2014';
    function row(l, label, r, emph) {
      return '<div class="pcs-est-row' + (emph ? ' pcs-est-row-emph' : '') + '"><span class="pcs-est-side">' + l + '</span><span class="pcs-est-label">' + label +
        '</span><span class="pcs-est-side pcs-est-side-new">' + r + '</span></div>';
    }
    var rows = '', eitherOha = curSys === 'OHA' || system === 'OHA';
    var eitherBah = (curSys ? (curSys === 'BAH' || curSys === 'BAH_PLUS_COLA') : false) || system === 'BAH' || system === 'BAH_PLUS_COLA';
    if (eitherOha) {
      rows += row(curOhaRent !== null ? money(curOhaRent) : '\u2014', 'OHA rent max', tgtOhaRent !== null ? money(tgtOhaRent) : '\u2014');
      rows += row(curOhaUtil !== null ? money(curOhaUtil) : '\u2014', 'OHA utilities', (ohaUtil !== null && ohaUtil !== undefined) ? money(ohaUtil) : '\u2014');
    }
    if (eitherBah) rows += row(curBah !== null ? money(curBah) : '\u2014', 'BAH', tgtBah !== null ? money(tgtBah) : '\u2014');
    if (eitherOha || system === 'BAH_PLUS_COLA' || curSys === 'BAH_PLUS_COLA' || cola > 0 || curCola > 0) {
      var note = '';
      if ((system === 'OHA' || system === 'BAH_PLUS_COLA') && colaIdx !== null && colaIdx !== undefined) note = ' \u00b7 index ' + colaIdx;
      else if (system === 'BAH' && cola === 0 && (curCola > 0 || curSys === 'OHA')) note = ' \u00b7 none at target';
      else if (system === 'OHA' && cola === 0) note = ' \u00b7 none at this location';
      var leftCola = (hasCompare && (curSys === 'OHA' || curSys === 'BAH_PLUS_COLA')) ? money(curCola) : (hasCompare && curCola > 0) ? money(curCola) : '\u2014';
      rows += row(leftCola, 'COLA' + safeHtml(note), money(cola) + '/mo');
    }
    rows += row(curTotal !== null ? money(curTotal) : '\u2014', 'Total package', money(total) + '/mo', true);
    var dlaV = D.dla[grade] ? D.dla[grade][withDeps ? 1 : 0] : null;
    var dlaHtml = (dlaV === null || dlaV === undefined) ? '\u2014' : money(pyRound(dlaV));
    var html = '<div class="pcs-face-section pcs-face-section-results pcs-partner-results">' + arrow +
      '<div class="pcs-partner-breakdown"><div class="pcs-est-heads-live"><span>Current</span><span></span><span>Target</span></div>' +
      '<div class="pcs-partner-breakdown-title">Allowances (official tables)</div>' + rows +
      '<div class="pcs-partner-breakdown-title">Local costs &amp; move-in (estimates)</div>' +
      row(leftRent, 'Typical ' + m.br + 'BR rent', rightRent) + row(leftUtil, 'Utilities', rightUtil) + row(leftGas, 'Avg gas', rightGas) +
      row('\u2014', 'DLA (one-time)', dlaHtml) + rollup + '</div></div>';
    return { html: html, warn: null, snap: { pay_grade: grade, num_dependents: deps, years_of_service: yos, gaining_installation: gaining,
      current_installation: current, barracks_meal_card: barracks, total_monthly_usd: total } };
  }

  /* ---- views/home.py + services/referral_lead.py (Wayfinder) ---- */
  var FORM_VIEW = 'https://docs.google.com/forms/d/e/1FAIpQLSeok5DcRqIU9QhzOGXCGAVd8UbW21LNK_S601kzOwb4FJ1Wyg/viewform';
  var ENTRIES = [['Email address', 'entry.1162277939'], ['Destination', 'entry.159372216'], ['First Name', 'entry.1546051705'], ['Last Name', 'entry.1445033394'],
    ['Rank', 'entry.1001940560'], ['Number of Dependents', 'entry.1983274092'], ['Rent/Buy/Not Sure', 'entry.1608004035']];
  var EMAIL_RE = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;
  function cleanEmail(raw) { return String(raw || '').trim().replace(/[\u200b\u200c\u200d\ufeff\u00a0]/g, '').trim(); }
  function rankLabel(grade) { var n = PAY_GRADE_TO_RANK[grade] || ''; return grade && n && n !== grade ? grade + ' \u2014 ' + n : (grade || n || ''); }
  function depsShort(n) { n = Math.max(0, n | 0); if (n === 0) return '0 dependents'; if (n >= 5) return '5+ dependents'; return n + ' dependent' + (n !== 1 ? 's' : ''); }
  function shortDest(dest, max) { max = max || 28; dest = String(dest || '').trim(); if (dest.length <= max) return dest; return dest.slice(0, max - 1).replace(/\s+$/, '') + '\u2026'; }
  function calcFields(snap) {
    var g = String(snap.pay_grade || ''), n = snap.num_dependents | 0;
    return { destination: String(snap.gaining_installation || '').trim(), rank: g ? rankLabel(g) : '', dependents_short: depsShort(n), num_dependents: n };
  }
  function referralRow(o) {
    var n = Math.max(0, o.num_dependents | 0);
    return { 'Destination': (o.destination || '').trim(), 'First Name': (o.first_name || '').trim(), 'Last Name': (o.last_name || '').trim(),
      'Rank': (o.rank || '').trim(), 'Number of Dependents': String(n), 'Rent/Buy/Not Sure': 'Not sure', 'Email address': (o.email_address || '').trim() };
  }
  /* urllib.parse.urlencode -> quote_plus (safe: A-Za-z0-9_.-~) */
  function quotePlus(v) { return encodeURIComponent(v).replace(/[!'()*]/g, function (c) { return '%' + c.charCodeAt(0).toString(16).toUpperCase(); }).replace(/%20/g, '+'); }
  function prefillUrl(row) {
    var q = ['usp=pp_url'];
    ENTRIES.forEach(function (e) { q.push(e[1] + '=' + quotePlus(row[e[0]] || '')); });
    return FORM_VIEW + '?' + q.join('&');
  }
  function validate(snap, first, email) {
    var c = calcFields(snap || {});
    var row = referralRow({ destination: c.destination, first_name: first, rank: c.rank, num_dependents: snap ? snap.num_dependents : 0, email_address: cleanEmail(email) });
    if (!c.destination) return { error: 'Set New post in the calculator above first.' };
    if (!row['First Name'].trim()) return { error: 'Enter your first name.' };
    if (!EMAIL_RE.test(cleanEmail(row['Email address']))) return { error: 'Enter a valid email address (example: name@email.com).' };
    return { row: row, url: prefillUrl(row) };
  }
  return { NONE_CURRENT: NONE_CURRENT, pyRound: pyRound, money: money, housingPackage: housingPackage, estimateMonthlyCola: estimateMonthlyCola,
    renderResults: renderResults, calcFields: calcFields, shortDest: shortDest, rankLabel: rankLabel, referralRow: referralRow, prefillUrl: prefillUrl,
    validate: validate, safeHtml: safeHtml, escAttr: escAttr, cleanEmail: cleanEmail };
});

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

  /* ---------- select widgets (native select; custom list on fine pointers to match the original) ---------- */
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
  else fetch('/assets/calc-data.json?v=9ac86d1f28').then(function (r) { return r.json(); }).then(init).catch(function () {
    $('pcs-results').insertAdjacentHTML('afterbegin', '<div class="pcs-alert pcs-alert-warn">Could not load 2026 rate data. Refresh the page to try again.</div>');
  });
})();
