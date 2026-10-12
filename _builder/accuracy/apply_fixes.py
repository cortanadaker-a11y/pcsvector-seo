"""Apply DTMO-verified fixes (pulled 11 Oct 2026, pay period 1 Oct 2026) to pcs-vector data files."""
import json
R='/workspace/pcs-vector-repo/data/'
O=json.load(open('dtmo_oha_2026-10-01.json')); CI=json.load(open('dtmo_cola_index_2026-10-01.json'))
oc=json.load(open(R+'oconus_allowances_2026.json'))
def iso(d): return f"{d[:4]}-{d[4:6]}-{d[6:]}"
# --- OHA FX + PR080 ceilings
for name,v in oc['locations'].items():
    if v.get('housing_system')=='OHA':
        e5=O[v['oha_code']]['with']['E-5']
        roe=float(e5['roe'].split('/')[0])
        v['usd_per_local']=round(1/roe,10)
        v['fx_refreshed_on']='2026-10-01'
        v['oha_effective_date']='2026-10-01'
        if v['oha_code']=='PR080':
            v['oha_rent_local']={g:O['PR080']['with'][g]['rent_local'] for g in O['PR080']['with'] if g!='O-7'}
            v['oha_rent_local']['O-7+']=O['PR080']['with']['O-7']['rent_local']
            v['oha_util_local']=e5['util_local']; v['oha_miha_local']=e5['miha_local']
            v['currency_note']=("U.S. territory: OHA (not BAH) plus OCONUS COLA. DTMO OHA locality PR080 (San Juan incl Bayamon, Carolina, Fort Buchanan), "
                                "ceilings in USD, pay period 1 Oct 2026. Without dependents: 90% rent ceiling + 75% utility. OHA pays actual rent up to the ceiling.")
        else:
            cur=v.get('currency_code')
            v['currency_note']=(f"OHA ceilings in {cur}; USD uses DTMO rate 1 USD = {roe:g} {cur} (pay period 1 Oct 2026; DTMO refreshes the rate on the 1st and 16th). "
                                "Without dependents: 90% rent ceiling + 75% utility. OHA pays actual rent up to max.")
# --- COLA indices (DTMO Overseas COLA calculator, pay period 1-15 Oct 2026)
CODE={'Camp Humphreys, South Korea':'KR025','Camp Casey, South Korea':'KR177','Camp Zama, Japan':'JP045','USAG Bavaria, Germany':'DE231',
 'USAG Rheinland-Pfalz, Germany':'DE700','USAG Wiesbaden, Germany':'DE355','USAG Italy, Italy':'IT073','Fort Buchanan, PR':'PR080',
 'Schofield Barracks, HI':'HI009','Fort Shafter, HI':'HI009','Joint Base Elmendorf-Richardson, AK':'AK005','Fort Wainwright, AK':'AK049','Fort Greely, AK':'AK029'}
LOCN={'AK005':'Anchorage (incl Eagle River / JBER)','AK049':'Fairbanks','AK029':'Delta Junction (incl Fort Greely)'}
for name,code in CODE.items():
    v=oc['locations'][name]; c=CI[code]
    v['cola_code']=code; v['cola_index']=c['index']; v['cola_index_effective']=iso(c['eff'])
    if code in LOCN: v['locality']=LOCN[code]
oc['effective_date']='2026-10-01'
oc['notes']['COLA']='Monthly = spendable(DTMO annual-compensation bracket for grade x YOS x with/without dependents, # command-sponsored dependents 0-5) x (index-100)/100/12. Index can be null (no COLA).'
oc['source']=("OHA: DTMO OHA Rate Lookup (rent ceilings, utility, MIHA) and DTMO exchange rates, pay period 1 Oct 2026. "
              "COLA: DTMO Overseas COLA indices (pay period 1-15 Oct 2026) with the CY2026 spendable-income table and DTMO annual-compensation brackets. "
              "Verified against the DTMO calculators on 11 Oct 2026. Always verify on LES / DTMO.")
json.dump(oc,open(R+'oconus_allowances_2026.json','w'),indent=2); open(R+'oconus_allowances_2026.json','a').write('\n')
# --- COLA compensation brackets
ct=json.load(open(R+'oconus_cola_tables_2026.json'))
BR=json.load(open('cola_comp_brackets_2026.json'))
order=['1','2','3','4','6','8','10','12','14','16','18','20','22','24','26','28','30','32','34','36','38','40']
assert len(order)==len(ct['yos_breakpoints'])
ct['cola_compensation_min_usd']={g:{m:[BR[g][m][k] for k in order] for m in ('without','with')} for g in BR}
ct['cola_compensation_note']=("DTMO annual-compensation bracket (lower bound) per grade x YOS column (aligned with yos_breakpoints) for members without / with "
                              "dependents. Derived from the DTMO Overseas COLA calculator (1,584 queries, pay period 1 Oct 2026); spendable income is then read "
                              "from spendable_table for the member's dependent count. Barracks = without-dependent spendable x 0.63 (matches DTMO).")
ct['formula']=("Monthly COLA = round(annual_spendable x (index - 100) / 100 / 12). Spendable from the CY2026 table using the DTMO annual-compensation "
               "bracket for grade x YOS x (with/without dependents) and # dependents (0-5). Barracks + meal card (0 deps) = x0.63.")
ct['last_updated']='2026-10-11'
json.dump(ct,open(R+'oconus_cola_tables_2026.json','w'),indent=2); open(R+'oconus_cola_tables_2026.json','a').write('\n')
# --- BAH MHA fixes
cols=['E-1','E-2','E-3','E-4','E-5','E-6','E-7','E-8','E-9','W-1','W-2','W-3','W-4','W-5','O-1E','O-2E','O-3E','O-1','O-2','O-3','O-4','O-5','O-6','O-7+']
def load(f):
    t={}
    for line in open('bah26/'+f):
        p=line.strip().split(',')
        if len(p)>20: t[p[0]]={c:int(float(x)) for c,x in zip(cols,p[1:25])}
    return t
W,WO=load('bahw26.txt'),load('bahwo26.txt')
names=dict(l.strip().split(';',1) for l in open('bah26/mhanames26.txt') if ';' in l)
bah=json.load(open(R+'bah_2026.json'))
FIX={'Dugway Proving Ground, UT':'ZZ790','Fort Barfoot, VA':'ZZ710','Fort Hunter Liggett, CA':'CA392','Natick Soldier Systems Center, MA':'MA120','Sierra Army Depot, CA':'ZZ800'}
for k,code in FIX.items():
    v=bah['installations'][k]
    v['mha_code']=code; v['mha']=names[code]
    v['with_dependents']={**W[code],'Other':W[code]['E-5']}
    v['without_dependents']={**WO[code],'Other':WO[code]['E-5']}
txt=json.dumps(bah,indent=2)
open(R+'bah_2026.json','w').write(txt+'\n')
print('ok')
