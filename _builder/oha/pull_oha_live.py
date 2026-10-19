"""Read-only live pull of DTMO OHA (public neorates endpoint), pay period 16 Oct 2026. UNOFFICIAL / PERSONAL."""
import json, datetime
from concurrent.futures import ThreadPoolExecutor
import sys; sys.path.insert(0, __import__('os').path.join(__import__('os').path.dirname(__file__), '..', 'accuracy'))
from dtmo import oha, OHA_RANK
LOCS=['KR025','KR177','JP045','JP065','JP061','JP027','DE355','DE231','DE700','DE055','DE228']
jobs=[(l,g,d) for l in LOCS for g in OHA_RANK for d in (True,False)]
with ThreadPoolExecutor(6) as ex: res=list(ex.map(lambda j:(j,oha(j[0],j[1],j[2],2026,10,'16')),jobs))
out={'_meta':{'pulled_at':datetime.datetime.now().astimezone().isoformat(timespec='seconds'),'source':'https://www.defensetravel.dod.mil/neorates/report/index.php (report=oha)','pay_period':'2026-10-16'}}
for (l,g,d),r in res: out.setdefault(l,{}).setdefault('with' if d else 'without',{})[g]=r
json.dump(out,open('dtmo_oha_live_2026-10-19.json','w'),indent=1)
bad=[j for j,r in res if r['rent'] is None]
print('n',len(res),'missing',len(bad),bad[:5])
for l in LOCS: e=out[l]['with']['E-5']; print(l,e['loc'],e['eff'],e['roe'],e['rent'],e['rent_local'],e['util'],e['miha'])
