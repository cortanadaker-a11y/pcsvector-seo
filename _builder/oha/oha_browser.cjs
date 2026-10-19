// OHA pages: CTA links preselect the target post in the calculator; no console errors; no horizontal overflow at 390px. UNOFFICIAL / PERSONAL.
const puppeteer = require('/workspace/build_v2/tools/node_modules/puppeteer-core');
const BASE = process.argv[2] || 'http://127.0.0.1:18793';
let pass = 0, fail = 0; const ok = (c, m) => { if (c) pass++; else { fail++; console.log('FAIL', m); } };
(async () => {
  const b = await puppeteer.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'].concat(process.env.HRR ? ['--host-resolver-rules=' + process.env.HRR] : []), headless: 'new' });
  const seen = new Set();
  for (const slug of ['', 'korea/', 'japan/', 'okinawa/', 'germany/']) {
    for (const w of [1280, 390]) {
      const p = await b.newPage(); const errs = [];
      p.on('pageerror', e => errs.push(String(e))); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
      await p.setViewport({ width: w, height: 900 });
      const r = await p.goto(BASE + '/oha/' + slug, { waitUntil: 'networkidle0' });
      ok(r.status() === 200, slug + ' status ' + r.status());
      ok(errs.length === 0, slug + ' console errors ' + errs);
      const ov = await p.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
      ok(ov <= 0, `${slug} horizontal overflow ${ov}px @${w}`);
      if (w === 1280) {
        const links = await p.$$eval('a[href^="/?"]', as => as.map(a => a.getAttribute('href')));
        for (const l of links) if (l.includes('tgt=')) seen.add(l);
      }
      await p.close();
    }
  }
  for (const l of seen) {
    const tgt = new URLSearchParams(l.split('?')[1].split('#')[0]).get('tgt');
    const p = await b.newPage(); await p.setViewport({ width: 1280, height: 900 });
    await p.goto(BASE + l, { waitUntil: 'networkidle0' }); await new Promise(r => setTimeout(r, 300));
    const v = await p.$eval('#bah_calc_gaining', s => s.value);
    const res = await p.$eval('#pcs-results', e => e.textContent);
    ok(v === tgt, `tgt preselect ${tgt} got ${v}`);
    ok(/OHA/.test(res), `results show OHA for ${tgt}`);
    if (l.includes('#find-a-home')) { const k = await p.$eval('#pcs-way-kicker', e => e.textContent); ok(k.startsWith('Military-approved agents'), 'kicker ' + k); }
    await p.close();
  }
  console.log('links tested', seen.size, 'PASS', pass, 'FAIL', fail); await b.close(); process.exit(fail ? 1 : 0);
})();
