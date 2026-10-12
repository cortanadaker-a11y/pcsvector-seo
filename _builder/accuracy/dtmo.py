"""Read-only DTMO neorates scrapers (public endpoints): OHA + Overseas COLA, pay period 2026-10-01."""
import re, subprocess, time
def _post(fields):
    args=['curl','-s','-m','40','-X','POST','https://www.defensetravel.dod.mil/neorates/report/index.php']
    for k,v in fields.items(): args+=['-F',f'{k}={v}']
    for a in range(4):
        t=subprocess.run(args,capture_output=True,text=True).stdout
        t=re.sub(r'(?s)<script.*?</script>','',t);t=re.sub(r'(?s)<style.*?</style>','',t);t=re.sub(r'<[^>]+>',' ',t);t=re.sub(r'\s+',' ',t)
        if 'Query Results' in t or 'no data' in t.lower(): return t
        time.sleep(2)
    return t
OHA_RANK={'E-1':13,'E-2':14,'E-3':15,'E-4':16,'E-5':17,'E-6':18,'E-7':19,'E-8':20,'E-9':21,'W-1':22,'W-2':23,'W-3':24,'W-4':25,'W-5':26,'O-1E':27,'O-2E':28,'O-3E':29,'O-1':30,'O-2':31,'O-3':32,'O-4':33,'O-5':34,'O-6':35,'O-7':36}
def oha(loc, grade, deps=True, y=2026,m=10,d='01'):
    t=_post({'report':'oha','locode':loc,'locode2':'','rank':OHA_RANK[grade],'depend':'YES' if deps else 'NO','year':y,'month':m,'day':d})
    def g(lbl):
        r=re.search(lbl+r' (?:([\d.,]+) [A-Z ]+? )?\$ ([\d.,]+)',t)
        return (float(r.group(2).replace(',','')), float(r.group(1).replace(',','')) if r.group(1) else float(r.group(2).replace(',',''))) if r else (None,None)
    (ru,rl),(uu,ul),(mu,ml)=g('OHA Rental Allowance'),g('Utility/Recurring Maintenance Allowance'),g(r'Move-In-Housing Allowance \(MIHA\)')
    eff=(re.search(r'Effective: (\d+)',t) or [None,None])[1]
    return {'rent':ru,'rent_local':rl,'util':uu,'util_local':ul,'miha':mu,'miha_local':ml,'eff':eff,
            'roe':(re.search(r'Rate of Exchange \(ROE\): ([^ ]+ ?/? ?[^ ]*)',t) or [None,None])[1],'loc':(re.search(r'LOCATION: (.*?) , LOCATION CODE',t) or [None,None])[1],'raw':None if 'Query Results' in t else t[:300]}
COLA_RANK=lambda g: g.replace('-','')
SVC={1:'1',2:'2',3:'3',4:'4',6:'5',8:'6',10:'7',12:'8',14:'9',16:'10',18:'11',20:'12',22:'13',24:'14',26:'15',28:'16',30:'17',32:'18',34:'19',36:'20',38:'21',40:'22'}
def cola(loc, grade, yos, deps, barracks=False):
    t=_post({'report':'ocola','year':2026,'month':10,'day':'01','LOCCODE':'','LOCCODE2':loc,'CINDEX2':'','RANK':COLA_RANK(grade),'DEPEND':deps+2,'SERVICE':SVC[yos],'BARRACK':'YES' if barracks else 'NO'})
    r=re.search(r'COLA Index: ([\d.]+) Effective Date: (\d+) Daily COLA: \$ ([\d.]+)',t)
    city=(re.search(r'City: (.*?) Location Code',t) or [None,None])[1]
    if not r: return {'raw':t[:300]}
    return {'index':round(100+float(r.group(1))*100),'eff':r.group(2),'daily':float(r.group(3)),'monthly':round(float(r.group(3))*30,2),'city':city}
