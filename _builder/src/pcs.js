/*! PCS Vector static app (pcsvector.com). Port of the Streamlit app (pcs-vector main):
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
      leftRent = money(curRentLo) + '\u2013' + money(curRentHi);
      leftUtil = money(curUtilN || 0) + '/mo';
      leftGas = D.posts[current].gas || '\u2014';
    } else {
      arrow = '<div class="pcs-partner-arrow pcs-partner-arrow-solo"><div class="pcs-partner-arrow-col pcs-partner-arrow-col-new"><div class="pcs-partner-arrow-loc">Target \u00b7 ' +
        safeHtml(chip) + '</div><span class="pcs-partner-arrow-amt">' + money(total) + '</span></div></div>' +
        '<div class="pcs-partner-delta-row"><span>' + safeHtml(gaining) + '</span><span class="pcs-bah-delta-badge pcs-delta-flat">' + money(total) + '/mo total</span></div>';
      leftRent = leftUtil = leftGas = '\u2014';
    }
    var rightRent = money(m.low) + '\u2013' + money(m.high), rightUtil = utilN ? money(utilN) + '/mo' : '\u2014', rightGas = P.gas || '\u2014';
    function row(l, label, r, emph, cls) {
      return '<div class="pcs-est-row' + (emph ? ' pcs-est-row-emph' : '') + (cls ? ' ' + cls : '') + '"><span class="pcs-est-side">' + l + '</span><span class="pcs-est-label">' + label +
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
      row(leftRent, 'Avg ' + m.br + 'BR rent', rightRent, false, 'pcs-est-row-rent') + row(leftUtil, 'Utilities', rightUtil) + row(leftGas, 'Avg gas', rightGas) +
      row('\u2014', 'DLA (one-time)', dlaHtml) + rollup + '</div></div>';
    return { html: html, warn: null, snap: { pay_grade: grade, num_dependents: deps, years_of_service: yos, gaining_installation: gaining,
      current_installation: current, barracks_meal_card: barracks, total_monthly_usd: total } };
  }

  /* ---- views/home.py + services/referral_lead.py (Wayfinder) ---- */
  var FORM_VIEW = 'https://docs.google.com/forms/d/e/1FAIpQLSeok5DcRqIU9QhzOGXCGAVd8UbW21LNK_S601kzOwb4FJ1Wyg/viewform';
  var ENTRIES = [['Email address', 'entry.1162277939'], ['Destination', 'entry.159372216'], ['First Name', 'entry.1546051705'],
    ['Rank', 'entry.1001940560'], ['Number of Dependents', 'entry.1983274092']];
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
  /* One-tap Find a home (21 Oct 2026, Zak OK): form prefilled from calculator only (rank, destination, dependents); plain form if nothing picked */
  function onetapUrl(snap) {
    var c = calcFields(snap || {}), q = [];
    if (c.rank) q.push('entry.1001940560=' + quotePlus(c.rank));
    if (c.destination) q.push('entry.159372216=' + quotePlus(c.destination));
    if (c.destination && snap && snap.num_dependents != null) q.push('entry.1983274092=' + quotePlus(String(c.num_dependents)));
    return q.length ? FORM_VIEW + '?usp=pp_url&' + q.join('&') : FORM_VIEW;
  }
  function onetapLabel(snap) {
    var c = calcFields(snap || {}), g = String((snap && snap.pay_grade) || '');
    return [g, c.destination].filter(Boolean).join(' \u00b7 ');
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
    renderResults: renderResults, calcFields: calcFields, shortDest: shortDest, rankLabel: rankLabel, referralRow: referralRow, prefillUrl: prefillUrl, onetapUrl: onetapUrl, onetapLabel: onetapLabel,
    validate: validate, safeHtml: safeHtml, escAttr: escAttr, cleanEmail: cleanEmail };
});
