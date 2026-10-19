// New BAH base pages + /bah/ hub: 200, no console errors, no horizontal overflow at 390px, calculator links preselect
// the post, results show that post's 2026 E-5 BAH, agents link lands on the Military-approved kicker. UNOFFICIAL / PERSONAL.
// Usage: node bah_browser.cjs <base_url>   (HRR env = --host-resolver-rules for local)
const puppeteer = require('/workspace/build_v2/tools/node_modules/puppeteer-core');
const B = require(__dirname + '/bases_built.json');
const BASE = process.argv[2] || 'http://127.0.0.1:18794';
let pass = 0, fail = 0; const ok = (c, m) => { if (c) pass++; else { fail++; console.log('FAIL', m); } };
(async () => {
  const b = await puppeteer.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'].concat(process.env.HRR ? ['--host-resolver-rules=' + process.env.HRR] : []), headless: 'new' });
  const links = [];
  for (const slug of [''].concat(Object.keys(B).map(s => s + '/'))) {
    for (const w of [1280, 390]) {
      const p = await b.newPage(); const errs = [], bad = [];
      p.on('pageerror', e => errs.push(String(e))); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
      p.on('response', r => { if (r.status() >= 400) bad.push(r.status() + ' ' + r.url()); });
      await p.setCacheEnabled(false); await p.setViewport({ width: w, height: 900, isMobile: w < 500, hasTouch: w < 500 });
      const r = await p.goto(BASE + '/bah/' + slug, { waitUntil: 'networkidle0' });
      ok(r.status() === 200, slug + ' status ' + r.status());
      ok(errs.length === 0, slug + ' console errors ' + errs); ok(bad.length === 0, slug + ' bad responses ' + bad);
      const ov = await p.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
      ok(ov <= 0, `${slug} horizontal overflow ${ov}px @${w}`);
      if (w === 1280 && slug) {
        const hs = await p.$$eval('a[href^="/?"]', as => as.map(a => a.getAttribute('href')));
        ok(hs.length === 3 && hs.every(h => h.includes('tgt=')), slug + ' 3 calculator links with tgt');
        links.push([slug.slice(0, -1), hs[0]], [slug.slice(0, -1), hs[2]]);
      }
      await p.close();
    }
  }
  for (const [slug, l] of links) {
    const tgt = new URLSearchParams(l.split('?')[1].split('#')[0]).get('tgt');
    const p = await b.newPage(); const errs = []; p.on('pageerror', e => errs.push(String(e)));
    await p.setViewport({ width: 1280, height: 900 });
    await p.goto(BASE + l, { waitUntil: 'networkidle0' }); await new Promise(r => setTimeout(r, 300));
    const v = await p.$eval('#bah_calc_gaining', s => s.value);
    const res = await p.$eval('#pcs-results', e => e.textContent);
    ok(v === tgt && tgt === B[slug].post, `tgt preselect ${tgt} got ${v}`);
    const e5 = [B[slug].W.E5, B[slug].WO.E5].map(x => '$' + x.toLocaleString('en-US'));
    ok(e5.some(x => res.includes(x)), `${slug} results show its E-5 BAH ${e5}`);
    if (['fort-wainwright', 'schofield-barracks'].includes(slug)) ok(/COLA/.test(res), slug + ' results include COLA');
    ok(errs.length === 0, slug + ' calc errors ' + errs);
    if (l.includes('#find-a-home')) { const k = await p.$eval('#pcs-way-kicker', e => e.textContent); ok(k.startsWith('Military-approved agents'), 'kicker ' + k); }
    await p.close();
  }
  console.log('pages', 1 + Object.keys(B).length, 'calc links tested', links.length, 'PASS', pass, 'FAIL', fail); await b.close(); process.exit(fail ? 1 : 0);
})();
