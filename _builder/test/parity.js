const fs = require('fs'); const P = require('/workspace/build_v2/src/pcs.js'); const D = require('/workspace/site_v2/assets/calc-data.json');
const cases = JSON.parse(fs.readFileSync(process.argv[2])); const exp = JSON.parse(fs.readFileSync(process.argv[3]));
const ent = s => s.replace(/&#36;/g, '$').replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>');
const norm = s => ent(s).replace(/>\s+</g, '><').replace(/\s+/g, ' ').trim();
let bad = 0, warnN = 0;
cases.forEach((c, i) => {
  const r = P.renderResults(D, c), e = exp[i];
  const a = norm(r.html), b = norm(e.html);
  const wa = r.warn ? [r.warn] : [], wb = e.warn;
  if (wb.length) warnN++;
  const snapOk = (e.snap.gaining_installation || '') === (r.snap.gaining_installation || '') && (e.snap.total_monthly_usd ?? null) === (r.snap.total_monthly_usd ?? null);
  if (a !== b || JSON.stringify(wa) !== JSON.stringify(wb) || !snapOk) { if (bad < 5) { console.log('MISMATCH', JSON.stringify(c)); for (let k = 0; k < Math.max(a.length, b.length); k++) if (a[k] !== b[k]) { console.log(' js :', a.slice(k - 80, k + 120)); console.log(' py :', b.slice(k - 80, k + 120)); break; } console.log(wa, wb, r.snap, e.snap); } bad++; }
});
console.log(`cases ${cases.length}  mismatches ${bad}  (python warnings ${warnN})`);
process.exit(bad ? 1 : 0);
