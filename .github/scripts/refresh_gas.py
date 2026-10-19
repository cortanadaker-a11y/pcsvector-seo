"""Weekly gas refresh for pcsvector.com (static site).

Uses the same code as the original app: pcs-vector services/gas_prices.py
(EIA weekly retail regular gasoline, public page, no API key:
https://www.eia.gov/dnav/pet/pet_pri_gnd_a_epmr_pte_dpgal_w.htm).
Updates only the gas fields of assets/calc-data.json + assets/gas-table.json,
then refreshes the content-hash cache-busting (?v=) the same way the builder does.

usage: python refresh_gas.py <site_root> <pcs-vector checkout>
Exit 1 (and change nothing) if the live EIA fetch fails: never publish fallback data as "current".
"""
import hashlib, json, re, sys
from pathlib import Path

site, app = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(app))
from services import gas_prices as GP  # noqa: E402

live = GP._fetch_eia_table()
if not live or len(live.get('prices') or {}) < 8 or not live.get('as_of'):
    print('EIA weekly fetch failed or incomplete; leaving site data unchanged.', file=sys.stderr)
    sys.exit(1)
table = dict(live)
table.setdefault('oconus_estimates', GP._load_fallback().get('oconus_estimates') or {})  # same as GP._eia_table()
GP._eia_table = lambda: table

cdp, gtp = site / 'assets/calc-data.json', site / 'assets/gas-table.json'
raw = cdp.read_text(encoding='utf-8')
cd = json.loads(raw)
changed = []
for post, rec in cd['posts'].items():
    lab = GP.get_gas_price_for_installation(post).get('label') or '\u2014'  # == _builder/export_calc.py
    if rec.get('gas') != lab:
        changed.append((post, rec.get('gas'), lab)); rec['gas'] = lab
old_asof = cd.get('gas_as_of')
cd['gas_as_of'], cd['gas_source'] = table.get('as_of'), table.get('source')
out = json.dumps(cd, separators=(',', ':'), ensure_ascii=False) + ('\n' if raw.endswith('\n') else '')
gt = json.dumps(table)
if out == raw and gtp.exists() and gtp.read_text(encoding='utf-8') == gt:
    print('No change (EIA as of %s).' % table.get('as_of')); sys.exit(0)
cdp.write_text(out, encoding='utf-8'); gtp.write_text(gt, encoding='utf-8')

h = lambda b: hashlib.sha256(b).hexdigest()[:10]  # == _builder/gen_site.py
cd_h = h(out.encode('utf-8'))
jsp, ixp = site / 'assets/pcs.js', site / 'index.html'
js = re.sub(r"/assets/calc-data\.json\?v=[0-9a-f]+", '/assets/calc-data.json?v=' + cd_h, jsp.read_text(encoding='utf-8'))
jsp.write_text(js, encoding='utf-8')
ix = ixp.read_text(encoding='utf-8')
ix = re.sub(r'/assets/calc-data\.json(\?v=[0-9a-f]+)?"', '/assets/calc-data.json?v=' + cd_h + '"', ix)
ix = re.sub(r'/assets/pcs\.js(\?v=[0-9a-f]+)?"', '/assets/pcs.js?v=' + h(js.encode('utf-8')) + '"', ix)
ix = re.sub(r'/assets/pcs\.css(\?v=[0-9a-f]+)?"', '/assets/pcs.css?v=' + h((site / 'assets/pcs.css').read_bytes()) + '"', ix)
ixp.write_text(ix, encoding='utf-8')
print('EIA as of %s (was %s); %d post labels changed' % (table.get('as_of'), old_asof, len(changed)))
for c in changed[:80]: print('  %s: %s -> %s' % c)
