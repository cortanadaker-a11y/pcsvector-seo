"""Live DTMO BAH Rate Lookup pull (public neorates endpoint, read-only): 2025 (YEAR=25) and 2026 (YEAR=26)
for the 8 original base pages, 24 grades x with/without. UNOFFICIAL / PERSONAL.  Usage: python3 pull_bah_yoy.py <out.json>"""
import re, json, time, subprocess, sys
COLS=['E1','E2','E3','E4','E5','E6','E7','E8','E9','W1','W2','W3','W4','W5','O1E','O2E','O3E','O1','O2','O3','O4','O5','O6','O7']
ZIPS={'NC182':'28310','TX286':'76544','KY106':'42223','CO046':'80913','WA311':'98433','NY225':'13602','TX279':'79916','DC053':'22202'}
def q(y,z,i):
    for a in range(4):
        r=subprocess.run(['curl','-s','-m','25','-X','POST','https://www.defensetravel.dod.mil/neorates/report/index.php','-F','report=bah','-F',f'YEAR={y}','-F',f'Zipcode={z}','-F',f'Rank={i+1}'],capture_output=True,text=True).stdout
        t=re.sub(r'\s+',' ',re.sub(r'<[^>]*>',' ',re.sub(r'(?s)<(script|style).*?</\1>','',r)))
        m=re.search(r'MILITARY HOUSING AREA: (.*?) MONTHLY ALLOWANCE: .*? without DEPENDENTS: \$ ([\d.]+) \$ ([\d.]+)',t)
        if m: return m.group(1),m.group(2),m.group(3)
        time.sleep(2)
out={}
for mha,z in ZIPS.items():
    out[mha]={'zip':z}
    for y in ('25','26'):
        cells={};area=None
        for i,c in enumerate(COLS):
            r=q(y,z,i)
            if r: area=r[0]; cells[c]={'with':int(float(r[1])),'without':int(float(r[2])),'with_raw':r[1],'without_raw':r[2]}
            else: cells[c]=None
            time.sleep(0.3)
        out[mha]['20'+y]={'area':area,'cells':cells}
        print(mha,y,area,sum(v is not None for v in cells.values()),flush=True)
out['_pulled']=time.strftime('%Y-%m-%d %H:%M %Z'); out['_source']='https://www.defensetravel.dod.mil/neorates/report/index.php (report=bah, YEAR=25 and YEAR=26)'
json.dump(out,open(sys.argv[1],'w'),indent=1)
