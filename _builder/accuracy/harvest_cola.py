import json, sys
from concurrent.futures import ThreadPoolExecutor
from dtmo import cola, SVC
S=json.load(open('/workspace/pcs-vector-repo/data/oconus_cola_tables_2026.json'))['spendable_table']
GR=['E-1','E-2','E-3','E-4','E-5','E-6','E-7','E-8','E-9','W-1','W-2','W-3','W-4','W-5','O-1E','O-2E','O-3E','O-1','O-2','O-3','O-4','O-5','O-6','O-7']
B=list(SVC.keys())
jobs=[(g,y,m) for g in GR for y in B for m in ('without','with','barracks')]
def run(j):
    g,y,m=j; dp=1 if m=='with' else 0
    r=cola('PR080',g,y,dp,m=='barracks')
    if 'daily' not in r: return j,None,None
    sp=r['daily']*360*100/(r['index']-100)
    col=1 if m=='with' else 0; fac=0.63 if m=='barracks' else 1.0
    cand=[t for t in S if abs(t['spendable'][col]*fac-sp)<3]
    return j,round(sp,2),(cand[0]['minIncome'] if len(cand)==1 else [c['minIncome'] for c in cand])
with ThreadPoolExecutor(8) as ex: res=list(ex.map(run,jobs))
out={}
odd=[]
for (g,y,m),sp,br in res:
    out.setdefault(g,{}).setdefault(m,{})[str(y)]=br
    if not isinstance(br,int): odd.append((g,y,m,sp,br))
json.dump(out,open('cola_comp_brackets_2026.json','w'),indent=1)
print('jobs',len(res),'odd',len(odd)); print(odd[:30])
