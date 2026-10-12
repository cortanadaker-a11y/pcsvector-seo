import json, itertools
from concurrent.futures import ThreadPoolExecutor
from dtmo import oha, cola, OHA_RANK
LOCS=['KR025','KR177','JP045','DE231','DE700','DE355','IT073','PR080']
jobs=[(l,g,d) for l in LOCS for g in OHA_RANK for d in (True,False)]
with ThreadPoolExecutor(6) as ex: res=list(ex.map(lambda j: (j,oha(*j)), jobs))
out={}
for (l,g,d),r in res: out.setdefault(l,{}).setdefault('with' if d else 'without',{})[g]=r
json.dump(out,open('dtmo_oha_2026-10-01.json','w'),indent=1)
bad=[(j,r) for j,r in res if r['rent'] is None]; print('oha done',len(res),'missing',len(bad),bad[:3])
CL={'KR025':0,'KR177':0,'JP045':0,'DE231':0,'DE700':0,'DE355':0,'IT073':0,'PR080':0,'HI009':0,'AK005':0,'AK049':0,'AK029':0}
with ThreadPoolExecutor(6) as ex: ci=dict(zip(CL, ex.map(lambda l: cola(l,'E-5',8,1), CL)))
json.dump(ci,open('dtmo_cola_index_2026-10-01.json','w'),indent=1)
for k,v in ci.items(): print(k,v.get('index'),v.get('eff'),v.get('city'))
