"""Render the real Streamlit calculator HTML for N cases (JSON lines in -> JSON lines out)."""
import sys, json, re
sys.path.insert(0, '/workspace/build_v2/test'); sys.path.insert(0, '/workspace/pcs-vector-repo')
import fake_st
from services import gas_prices as GP
table = json.load(open('/workspace/site_v2/assets/gas-table.json')); GP._eia_table = lambda: table
from components import bah_calculator as BC
cases = json.load(open(sys.argv[1])); out = []
for c in cases:
    ss = fake_st.st.session_state; ss.clear()
    ss.update(bah_calc_grade=c['g'], bah_calc_deps_n=c['d'], bah_calc_yos=c['y'], bah_calc_current=c['cur'] or BC._NONE_CURRENT, bah_calc_gaining=c['tgt'], bah_calc_barracks=c['bar'])
    fake_st.CAP['html'].clear(); fake_st.CAP['warn'].clear()
    BC.render_bah_calculator()
    snap = ss.get('bah_calc_snapshot') or {}
    out.append({'html': ''.join(fake_st.CAP['html']), 'warn': list(fake_st.CAP['warn']), 'snap': {k: snap.get(k) for k in ('pay_grade','num_dependents','gaining_installation','current_installation','total_monthly_usd','arrive_cash_net_usd')}})
json.dump(out, open(sys.argv[2], 'w'))
print(len(out))
