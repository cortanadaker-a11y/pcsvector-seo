import sys, json
sys.path.insert(0,'/workspace/build_v2/test'); import fake_st
sys.path.insert(0,'/workspace/pcs-vector-repo')
from services.referral_lead import build_referral_row, build_prefill_url, format_rank_label
import importlib
d=json.load(open('/workspace/site_v2/assets/calc-data.json'))
m=None
for mod in ['components.form_options','components.bah_calculator','services.housing_allowances']:
    try:
        x=importlib.import_module(mod)
        if hasattr(x,'PAY_GRADE_TO_RANK'): m=x.PAY_GRADE_TO_RANK;break
    except Exception as e: pass
names=[("Zak","zak@example.com"),("José María","a+b@x.co"),("O'Neil & Co","  t.e@st.io "),("李","x@y.org")]
cases=[]
grades=list(d['grades']) if isinstance(d['grades'],list) else list(d['grades'].keys())
posts=list(d['posts'].keys())
for gi,g in enumerate(grades):
  for pi,p in enumerate(posts):
    n=(gi+pi)%7; f,e=names[(gi*3+pi)%4]
    row=build_referral_row(destination=p,first_name=f,rank=format_rank_label(g,(m or {}).get(g)),num_dependents=n,email_address=e.strip())
    cases.append(dict(g=g,p=p,n=n,f=f,e=e,url=build_prefill_url(row)))
json.dump(cases,open('prefill_cases.json','w'))
print(len(cases), 'rankmap' if m else 'NO RANKMAP', cases[0]['url'])
