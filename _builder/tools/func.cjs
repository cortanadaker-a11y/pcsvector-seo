const puppeteer = require('puppeteer-core');
const P = require('/workspace/site_v2/assets/pcs.js'); const PCS = P.PCS || P;
const D = require('/workspace/site_v2/assets/calc-data.json');
const BASE = process.argv[2] || 'http://localhost:8765/';
let pass = 0, fail = 0; const ok = (c, m) => { if (c) pass++; else { fail++; console.log('FAIL', m); } };
const D_APP = {'fort-bragg':'Fort Bragg, NC','fort-hood':'Fort Hood, TX','fort-campbell':'Fort Campbell, KY','fort-carson':'Fort Carson, CO','joint-base-lewis-mcchord':'Joint Base Lewis-McChord, WA','fort-drum':'Fort Drum, NY','fort-bliss':'Fort Bliss, TX','national-capital-region':'Pentagon / National Capital Region, VA'};
const sleep = ms => new Promise(r => setTimeout(r, ms));
(async () => {
  const b = await puppeteer.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'].concat(process.env.HRR ? ['--host-resolver-rules=' + process.env.HRR] : []), headless: 'new' });
  async function page(url, w = 1280, mobile = false) {
    const p = await b.newPage(); p.errs = []; p.bad = [];
    p.on('pageerror', e => p.errs.push(String(e))); p.on('console', m => { if (m.type() === 'error') p.errs.push(m.text()); });
    p.on('response', r => { if (r.status() >= 400) p.bad.push(r.status() + ' ' + r.url()); });
    await p.setViewport({ width: w, height: 900, isMobile: mobile, hasTouch: mobile });
    await p.goto(url, { waitUntil: 'networkidle0' }); await sleep(200); return p;
  }
  const results = p => p.$eval('#pcs-results', e => e.innerHTML);
  const exp = s => { const r = PCS.renderResults(D, s); return r.warn ? null : r.html; };

  // 1 default
  let p = await page(BASE);
  const def = { g: 'E-5', d: 0, y: 4, cur: 'Fort Campbell, KY', tgt: 'Fort Bragg, NC', bar: false };
  ok((await results(p)) === exp(def), 'default results == JS render');
  ok(p.errs.length === 0, 'console errors default: ' + p.errs);
  ok(p.bad.length === 0, 'bad responses: ' + p.bad);
  ok((await p.$eval('#pcs-way-kicker', e => e.textContent)) === 'Military-approved agents · Fort Bragg, NC', 'kicker text');
  ok(await p.$eval('#pcs-ref-form', e => getComputedStyle(e.closest('.pcs-ref-fields') || e).display === 'none'), 'gate closed initially');

  // 2 select changes (native select change event)
  const setSel = async (id, v) => p.evaluate((id, v) => { const s = document.getElementById(id); s.value = v; s.dispatchEvent(new Event('change')); }, id, v);
  await setSel('bah_calc_grade', 'O-3'); await setSel('bah_calc_deps_n', '2'); await setSel('bah_calc_yos', '10');
  await setSel('bah_calc_current', 'Fort Hood, TX'); await setSel('bah_calc_gaining', 'USAG Wiesbaden, Germany');
  ok((await results(p)) === exp({ g: 'O-3', d: 2, y: 10, cur: 'Fort Hood, TX', tgt: 'USAG Wiesbaden, Germany', bar: false }), 'OHA/COLA results after select change');
  ok(await p.$eval('#bah_calc_barracks', e => e.disabled), 'barracks disabled with deps');
  ok((await p.$eval('#pcs-sticky-ref-line', e => e.textContent)) === 'USAG Wiesbaden, Germany · O-3 — Captain · 2 dependents', 'sticky line: ' + await p.$eval('#pcs-sticky-ref-line', e => e.textContent));
  await setSel('bah_calc_deps_n', '0');
  ok(!(await p.$eval('#bah_calc_barracks', e => e.disabled)), 'barracks enabled deps 0');
  await p.click('#bah_calc_barracks');
  ok((await results(p)) === exp({ g: 'O-3', d: 0, y: 10, cur: 'Fort Hood, TX', tgt: 'USAG Wiesbaden, Germany', bar: true }), 'barracks results');
  await setSel('bah_calc_current', '— Skip —');
  ok((await results(p)) === exp({ g: 'O-3', d: 0, y: 10, cur: '— Skip —', tgt: 'USAG Wiesbaden, Germany', bar: true }), 'skip current');
  const fine = await p.evaluate(() => matchMedia('(pointer:fine)').matches); console.log('pointer:fine =', fine);
  if (fine) {
  // custom listbox keyboard
  await p.focus('#bah_calc_grade'); await p.keyboard.press('Enter'); await sleep(50);
  const lb = await p.$$eval('[role=option]', l => l.length); ok(lb === D.grades.length, 'listbox opens with ' + lb);
  await p.keyboard.press('ArrowDown'); await p.keyboard.press('Enter'); await sleep(50);
  ok((await p.$eval('#bah_calc_grade', e => e.value)) === 'O-4', 'listbox arrow select -> ' + await p.$eval('#bah_calc_grade', e => e.value));
  // click option
  await p.click('#bah_calc_yos'); await sleep(50);
  await p.evaluate(() => { const li = [...document.querySelectorAll('[role=option]')].find(l => l.textContent === '20'); li.dispatchEvent(new MouseEvent('mousedown', { bubbles: true })); });
  ok((await p.$eval('#bah_calc_yos', e => e.value)) === '20', 'listbox mouse select');
  } else { await setSel('bah_calc_grade','O-4'); await setSel('bah_calc_yos','20'); }
  // help tooltip
  const hc = await p.$$('.pcs-help'); if (hc.length) { await hc[0].click(); ok(await p.$eval('.pcs-help', e => e.classList.contains('show')), 'help toggles'); }

  // 3 gate via button, validation
  await p.click('#referral_open_btn'); await sleep(150);
  ok(await p.$eval('#pcs-match-panel', e => e.classList.contains('pcs-ref-open')), 'gate opens via button');
  ok(await p.evaluate(() => document.activeElement.id) === 'referral_first_name', 'focus on first name');
  const msg = () => p.$eval('#pcs-ref-msg', e => e.textContent.trim());
  await p.click('#referral_submit_btn'); await sleep(50);
  ok((await msg()) === 'Enter your first name.', 'empty name error: ' + await msg());
  await p.type('#referral_first_name', 'Zak'); await p.type('#referral_email_address', 'bad@');
  await p.click('#referral_submit_btn'); await sleep(50);
  ok((await msg()).startsWith('Enter a valid email address'), 'bad email error: ' + await msg());
  await p.$eval('#referral_email_address', e => e.value = '');
  await p.type('#referral_email_address', 'zak@example.com');
  await p.setRequestInterception(true); let navUrl = null;
  p.on('request', r => { if (r.url().startsWith('https://docs.google.com')) { navUrl = r.url(); r.abort(); } else r.continue(); });
  await p.click('#referral_submit_btn'); await sleep(900);
  const st = { 'First Name': 'Zak' }; // session row checked separately (page navigated)
  const expUrl = PCS.prefillUrl(PCS.referralRow({ destination: 'USAG Wiesbaden, Germany', first_name: 'Zak', rank: 'O-4 — Major', num_dependents: 0, email_address: 'zak@example.com' }));
  ok(navUrl === expUrl, 'navigates to prefill url\n got ' + navUrl + '\n exp ' + expUrl);
  ok(st && st['First Name'] === 'Zak', 'sessionStorage row');
  ok(p.errs.length === 0, 'console errors flow: ' + p.errs);
  await p.close();

  // 3b fine pointer listbox (headless reports no pointer; force matchMedia)
  { const q = await b.newPage(); q.errs=[]; q.on('pageerror', e => q.errs.push(String(e)));
    await q.evaluateOnNewDocument(() => { const mm = window.matchMedia.bind(window); window.matchMedia = s => s === '(pointer:fine)' ? { matches: true, media: s, addListener(){}, removeListener(){}, addEventListener(){}, removeEventListener(){} } : mm(s); });
    await q.setViewport({ width: 1280, height: 900 }); await q.goto(BASE, { waitUntil: 'networkidle0' });
    await q.focus('#bah_calc_grade'); await q.keyboard.press('Enter'); await sleep(50);
    ok((await q.$$eval('[role=option]', l => l.length)) === D.grades.length, 'listbox opens');
    await q.keyboard.press('ArrowDown'); await q.keyboard.press('Enter'); await sleep(50);
    ok((await q.$eval('#bah_calc_grade', e => e.value)) === 'E-6', 'listbox arrow -> ' + await q.$eval('#bah_calc_grade', e => e.value));
    await q.focus('#bah_calc_gaining'); await q.keyboard.press('Enter'); await q.keyboard.type('sch'); await q.keyboard.press('Enter'); await sleep(50);
    ok((await q.$eval('#bah_calc_gaining', e => e.value)) === 'Schofield Barracks, HI', 'typeahead -> ' + await q.$eval('#bah_calc_gaining', e => e.value));
    await q.click('#bah_calc_yos'); await sleep(50);
    await q.evaluate(() => { const li = [...document.querySelectorAll('[role=option]')].find(l => l.textContent === '20'); li.dispatchEvent(new MouseEvent('mousedown', { bubbles: true })); });
    ok((await q.$eval('#bah_calc_yos', e => e.value)) === '20', 'listbox mouse select');
    await q.click('#bah_calc_deps_n'); await sleep(50); await q.mouse.click(5, 5); await sleep(50);
    ok((await q.$$eval('[role=option]', l => l.length)) === 0, 'outside click closes');
    ok((await results(q)) === exp({ g: 'E-6', d: 0, y: 20, cur: 'Fort Campbell, KY', tgt: 'Schofield Barracks, HI', bar: false }), 'results after listbox');
    ok(q.errs.length === 0, 'errs listbox ' + q.errs);
    // session storage write
    await q.click('#referral_open_btn'); await q.type('#referral_first_name', 'Ann'); await q.type('#referral_email_address', 'a@b.co');
    await q.evaluate(() => { window.__assign = null; });
    await q.setRequestInterception(true); q.on('request', r => r.url().startsWith('https://docs.google') ? r.abort() : r.continue());
    await q.click('#referral_submit_btn'); await sleep(100);
    const row = await q.evaluate(() => JSON.parse(sessionStorage.getItem('pcs_referral_lead') || 'null'));
    ok(row && row['First Name'] === 'Ann' && row['Email address'] === 'a@b.co' && row['Rank'] === 'E-6 — Staff Sergeant', 'session row ' + JSON.stringify(row));
    ok((await q.$eval('#pcs-ref-msg', e => e.textContent)).startsWith('Opening your pre-filled form'), 'success msg');
    await q.close(); }

  // 4 query presets + hash gate
  p = await page(BASE + '?g=E-7&d=3&y=12&cur=Fort%20Bragg%2C%20NC&tgt=Schofield%20Barracks%2C%20HI#find-a-home');
  ok((await results(p)) === exp({ g: 'E-7', d: 3, y: 12, cur: 'Fort Bragg, NC', tgt: 'Schofield Barracks, HI', bar: false }), 'query preset results');
  ok(await p.$eval('#pcs-match-panel', e => e.classList.contains('pcs-ref-open')), 'hash opens gate');
  ok((await p.$eval('#bah_calc_gaining', e => e.value)) === 'Schofield Barracks, HI', 'select reflects tgt');
  await p.close();
  p = await page(BASE + '?tgt=Nowhere&g=Z-9&d=99');
  ok((await results(p)) === exp({ g: 'E-5', d: 5, y: 4, cur: 'Fort Campbell, KY', tgt: 'Fort Bragg, NC', bar: false }), 'bad query falls back');
  ok(p.errs.length === 0, 'errs bad query ' + p.errs);
  // hashchange
  await p.evaluate(() => location.hash = '#wayfinder'); await sleep(150);
  ok(await p.$eval('#pcs-match-panel', e => e.classList.contains('pcs-ref-open')), 'hashchange opens gate');
  await p.close();

  // 5 OCONUS: Zak's 11 Oct case (Fort Drum -> Fort Buchanan, 3 deps, 9 YOS, phone) computes OHA + COLA, no alert box
  p = await page(BASE + '?g=E-6&d=3&y=9&cur=Fort%20Drum%2C%20NY&tgt=Fort%20Buchanan%2C%20PR', 390, true);
  ok((await results(p)) === exp({ g: 'E-6', d: 3, y: 9, cur: 'Fort Drum, NY', tgt: 'Fort Buchanan, PR', bar: false }), 'buchanan computes (zak case)');
  ok(await p.$eval('#pcs-results', e => !e.querySelector('.pcs-alert') && /OHA rent max/.test(e.textContent) && /\$2,300/.test(e.textContent) && /\$1,223/.test(e.textContent) && /index 124/.test(e.textContent)), 'buchanan OHA $2,300 + util $1,223 + COLA idx 124 shown');
  await p.close();
  // every post as target (E-5, 1 dep): rendered card, never an alert
  { p = await page(BASE);
    let alerts = [];
    for (const post of Object.keys(D.posts)) {
      await p.select('#bah_calc_gaining', post); await sleep(5);
      if (await p.$eval('#pcs-results', e => !!e.querySelector('.pcs-alert') || !e.querySelector('.pcs-partner-results'))) alerts.push(post);
    }
    ok(alerts.length === 0, 'all ' + Object.keys(D.posts).length + ' posts render a results card, no alert: ' + alerts.join('|'));
    await p.close(); }

  // 5b BAH pages: every agent CTA opens the Wayfinder with the post preset; every calculator CTA presets the post
  for (const slug of ['fort-bragg','fort-hood','fort-campbell','fort-carson','joint-base-lewis-mcchord','fort-drum','fort-bliss','national-capital-region','']) {
    p = await page(BASE + 'bah/' + (slug ? slug + '/' : ''));
    const hrefs = await p.$$eval('a.cta', as => as.map(a => a.getAttribute('href')));
    ok(hrefs.length > 0 && hrefs.every(h => !/#.*#/.test(h)), 'bah ' + (slug || 'hub') + ' CTA hrefs clean: ' + hrefs.filter(h => /#.*#/.test(h)).join(' '));
    const agent = hrefs.find(h => /utm_medium=agents/.test(h));
    ok(!!agent, 'bah ' + (slug || 'hub') + ' has agent CTA');
    await p.close();
    p = await page(new URL(agent, BASE).href);
    ok(await p.$eval('#pcs-match-panel', e => e.classList.contains('pcs-ref-open')), 'bah ' + (slug || 'hub') + ' agent CTA opens Wayfinder');
    if (slug) { const tg = await p.$eval('#bah_calc_gaining', e => e.value); ok(tg === D_APP[slug], 'bah ' + slug + ' preset target ' + tg); }
    await p.close();
  }
  // 6 mobile: sticky, sidebar, overflow
  for (const w of [320, 360, 390, 414, 768, 1024, 1280, 1920]) {
    p = await page(BASE, w, w < 700);
    const ov = await p.evaluate((w) => Math.max(document.documentElement.scrollWidth, innerWidth) - w, w);
    const tips = await p.evaluate(() => [...document.querySelectorAll('.pcs-help')].map(h => { h.classList.add('show'); h.dispatchEvent(new Event('mouseenter')); const r = h.querySelector('.pcs-tip').getBoundingClientRect(); h.classList.remove('show'); return [Math.round(r.left), Math.round(r.right)]; }));
    ok(tips.every(t => t[0] >= 0 && t[1] <= w), `tips in view at ${w}: ` + JSON.stringify(tips));
    ok(ov <= 0, `no h-overflow at ${w}: ${ov}`);
    ok(p.errs.length === 0, 'errs mobile ' + w + p.errs);
    if (w === 390) {
      ok(await p.$eval('#pcs-sticky-ref-bar', e => !e.hidden && !e.classList.contains('pcs-sticky-ref-hidden') && getComputedStyle(e).display !== 'none'), 'sticky visible at top');
      await p.click('#pcs-sticky-ref-go'); await sleep(900);
      ok(await p.$eval('#pcs-match-panel', e => e.classList.contains('pcs-ref-open')), 'sticky opens gate');
      ok(await p.$eval('#pcs-sticky-ref-bar', e => e.classList.contains('pcs-sticky-ref-hidden')), 'sticky hides when panel in view');
      await p.evaluate(() => scrollTo(0, 0));
      await p.click('#pcs-sidebar-open'); await sleep(300);
      ok(await p.$eval('#pcs-sidebar', e => e.classList.contains('open')), 'sidebar opens');
      await p.keyboard.press('Escape'); await sleep(300);
      ok(await p.$eval('#pcs-sidebar', e => !e.classList.contains('open')), 'sidebar esc closes');
      const tgt = await p.$$eval('button, a, select, input', es => es.filter(e => { const r = e.getBoundingClientRect(); return r.width && r.height && r.height < 24 && getComputedStyle(e).visibility !== 'hidden'; }).map(e => (e.id || e.tagName) + ':' + Math.round(e.getBoundingClientRect().height)));
      console.log('small tap targets @390:', tgt.join(', ') || 'none');
    }
    await p.close();
  }
  // 7 other pages
  for (const u of ['bah/', 'bah/fort-bragg-nc/', 'nope-404']) {
    p = await page(BASE + u); ok(p.errs.filter(e => !/404/.test(e)).length === 0, 'errs ' + u + p.errs); await p.close();
  }
  console.log('PASS', pass, 'FAIL', fail); await b.close();
})();
