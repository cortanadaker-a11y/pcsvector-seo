"""Export every calculator input from the pcs-vector Python services (main) -> static JSON.
Python stays the single source of truth; JS only does lookups + the COLA arithmetic (parity-tested)."""
import sys, json, re
sys.path.insert(0, '/workspace/pcs-vector-repo')
from services import gas_prices as GP
from services.housing_allowances import get_housing_package, get_oconus_record, _oha_amounts, _load_cola_tables
from services.installation_data import SUPPORTED_INSTALLATIONS as POSTS, get_family_market_rent
from services.utility_costs import get_utility_costs_for_installation
from services.dla_rates import get_dla_rate
OUT = sys.argv[1] if len(sys.argv) > 1 else '/workspace/site_v2/assets/calc-data.json'
GRADES = ["E-1","E-2","E-3","E-4","E-5","E-6","E-7","E-8","E-9","W-1","W-2","W-3","W-4","W-5","O-1","O-2","O-3","O-4","O-5","O-6","O-7+"]
def util_mid(areas):  # == components/bah_calculator._util_mid (main)
    lows, highs = [], []
    for a in areas or []:
        tot = a.get('total_utilities_usd_mo') or {}
        if tot.get('low') is not None and tot.get('high') is not None:
            lows.append(int(tot['low'])); highs.append(int(tot['high']))
    return int(round((sum(lows)/len(lows) + sum(highs)/len(highs)) / 2)) if lows else None
table = GP._eia_table()  # live EIA weekly if reachable, else repo fallback (same as the app)
GP._eia_table = lambda: table
ct = _load_cola_tables()
out = {'grades': GRADES, 'posts': {}, 'dla': {}, 'gas_as_of': table.get('as_of'), 'gas_source': table.get('source'),
       'cola': {'base_pay_monthly': ct['base_pay_monthly'], 'yos_breakpoints': ct.get('yos_breakpoints') or [0,2,3,4,6,8,10,12,14,16,18,20],
                'spendable_table': [[r['minIncome'], r['maxIncome'], r['spendable']] for r in ct['spendable_table']],
                'compensation': ct.get('cola_compensation_min_usd') or {}}}
for g in GRADES:
    out['dla'][g] = []
    for w in (False, True):
        d = get_dla_rate(g, with_dependents=w)
        out['dla'][g].append(round(float(d['dla_usd']), 2) if d.get('found') else None)
for p in POSTS:
    base = get_housing_package(p, 'E-5', with_dependents=True, years_of_service=4, num_dependents=1)
    sysn = base.get('housing_system') or 'BAH'
    oc = get_oconus_record(p)
    rec = {'sys': sysn, 'ci': (oc or {}).get('cola_index') if sysn in ('OHA', 'BAH_PLUS_COLA') else None}
    if sysn == 'OHA': rec['loc'] = base.get('locality')
    if sysn == 'OHA':
        rec['oha'] = [[list(_oha_amounts(oc, g, with_dependents=w)[:2]) for g in GRADES] for w in (False, True)]
    else:
        rec['h'] = [[get_housing_package(p, g, with_dependents=w, years_of_service=4, num_dependents=1 if w else 0)['housing_monthly_usd'] for g in GRADES] for w in (False, True)]
    rec['rent'] = [[get_family_market_rent(p, num_dependents=d)[k] for k in ('low_usd', 'high_usd', 'mid_usd', 'bedrooms')] for d in range(6)]
    oco = sysn in ('OHA', 'BAH_PLUS_COLA')
    rec['util'] = util_mid((get_utility_costs_for_installation(p, is_oconus=oco) or {}).get('areas'))
    rec['gas'] = GP.get_gas_price_for_installation(p).get('label') or '—'
    out['posts'][p] = rec
json.dump(out, open(OUT, 'w'), separators=(',', ':'), ensure_ascii=False)
json.dump(table, open(OUT.replace('calc-data.json', 'gas-table.json'), 'w'))
print(len(POSTS), 'posts', {s: sum(1 for r in out['posts'].values() if r['sys'] == s) for s in ('BAH', 'BAH_PLUS_COLA', 'OHA')}, 'gas', table.get('source'), table.get('as_of'))
