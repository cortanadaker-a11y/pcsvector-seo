import sys, json, random
sys.path.insert(0,'/workspace/pcs-vector-repo')
from services.housing_allowances import estimate_monthly_cola
from dtmo import cola
from concurrent.futures import ThreadPoolExecutor
IDX=json.load(open('dtmo_cola_index_2026-10-01.json'))
random.seed(7)
grades=['E-1','E-3','E-4','E-5','E-6','E-7','E-8','E-9','W-1','W-3','W-5','O-1','O-1E','O-2','O-3','O-3E','O-4','O-5','O-6','O-7']
locs=['PR080','HI009','AK049','AK029','AK005','DE700','KR025','KR177','JP045','IT073','DE355','DE231']
cases=[]
for i in range(260):
    l=random.choice(locs); g=random.choice(grades); y=random.choice([2,3,4,6,8,10,12,14,16,18,20,22,24,26,30,40]); dp=random.choice([0,0,1,2,3,4,5]); b=(dp==0 and random.random()<0.4)
    cases.append((l,g,y,dp,b))
def run(c):
    l,g,y,dp,b=c; r=cola(l,g,y,dp,b)
    p=estimate_monthly_cola(g,years_of_service=y,num_dependents=dp,cola_index=IDX[l]['index'],barracks_meal_card=b)['cola_monthly_usd']
    return c,r,p
with ThreadPoolExecutor(6) as ex: res=list(ex.map(run,cases))
bad=[(c,r.get('monthly'),p) for c,r,p in res if r.get('monthly') is None or abs(r['monthly']-p)>1.0]
json.dump([(c,r,p) for c,r,p in res],open('cola_check_results.json','w'))
print('cases',len(res),'mismatch >$1:',len(bad))
for b in bad[:40]: print(b)
