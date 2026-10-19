"""Live DTMO BAH Rate Lookup pull (public neorates endpoint, read-only) for the 12 new base pages.
24 grades x 12 anchor duty-station ZIPs, 2026 rates. UNOFFICIAL / PERSONAL.
Usage: python3 pull_bah_live.py <out.json>"""
import re, json, time, subprocess, sys
COLS=['E1','E2','E3','E4','E5','E6','E7','E8','E9','W1','W2','W3','W4','W5','O1E','O2E','O3E','O1','O2','O3','O4','O5','O6','O7']
ZIPS={'GA080':'31314','GA075':'31905','TX285':'78234','KS100':'66442','KY110':'40121','MO163':'65473','LA115':'71459','OK237':'73503','AK405':'99703','AZ014':'85613','CA028':'92310','HI408':'96857'}
out={}
for mha,z in ZIPS.items():
    out[mha]={'zip':z,'cells':{}}
    for i,c in enumerate(COLS):
        m=None
        for attempt in range(3):
            r=subprocess.run(['curl','-s','-m','25','-X','POST','https://www.defensetravel.dod.mil/neorates/report/index.php','-F','report=bah','-F','YEAR=26','-F',f'Zipcode={z}','-F',f'Rank={i+1}'],capture_output=True,text=True).stdout
            r=re.sub(r'(?s)<script.*?</script>','',r); r=re.sub(r'(?s)<style.*?</style>','',r)
            t=re.sub(r'\s+',' ',re.sub(r'<[^>]*>',' ',r))
            m=re.search(r'MILITARY HOUSING AREA: (.*?) MONTHLY ALLOWANCE: (.*?) with DEPENDENTS: .*? without DEPENDENTS: \$ ([\d.]+) \$ ([\d.]+)',t)
            if m: break
            time.sleep(2)
        if m:
            out[mha]['area']=m.group(1); out[mha]['cells'][c]={'rank_shown':m.group(2),'with':int(float(m.group(3))),'without':int(float(m.group(4))),'with_raw':m.group(3),'without_raw':m.group(4)}
        else: out[mha]['cells'][c]=None
        time.sleep(0.4)
    print(mha, out[mha].get('area'), sum(v is not None for v in out[mha]['cells'].values()), flush=True)
out['_pulled']=time.strftime('%Y-%m-%d %H:%M %Z'); out['_source']='https://www.defensetravel.dod.mil/neorates/report/index.php (report=bah, YEAR=26)'
json.dump(out,open(sys.argv[1],'w'),indent=1)
