"""Check the 8 deepened BAH pages: main 2026 table vs DTMO ASCII + live 2026; YoY table + sentence vs live 2025/2026; stamp; other-posts (19 links, no self);
JSON-LD dateModified; home untouched. Usage: check_bah_deepen.py <site_root> <yoy.json> <ascii_dir>. Prints mismatches (must be 0)."""
import json,re,sys,os
root,src,ad=sys.argv[1:4]; D=json.load(open(src))
COLS=['E1','E2','E3','E4','E5','E6','E7','E8','E9','W1','W2','W3','W4','W5','O1E','O2E','O3E','O1','O2','O3','O4','O5','O6','O7']
PAGES={'fort-bragg':'NC182','fort-hood':'TX286','fort-campbell':'KY106','fort-carson':'CO046','joint-base-lewis-mcchord':'WA311','fort-drum':'NY225','fort-bliss':'TX279','national-capital-region':'DC053'}
ALL=set(os.listdir(os.path.join(root,'bah')))-{'index.html'}
asc=lambda f:{l.split(',')[0]:[int(float(x)) for x in l.strip().split(',')[1:]] for l in open(os.path.join(ad,f))}
W,WO=asc('bahw26.txt'),asc('bahwo26.txt')
n=bad=0
def ck(c,msg):
    global n,bad; n+=1
    if not c: bad+=1; print('MISMATCH',msg)
v=lambda s:int(s.replace('$','').replace(',','').replace('+','').replace('−','-'))
for slug,mha in PAGES.items():
    t=open(os.path.join(root,'bah',slug,'index.html'),encoding='utf-8').read()
    a,b=D[mha]['2025']['cells'],D[mha]['2026']['cells']
    ck(D[mha]['2026']['area'].endswith(f'({mha})') and D[mha]['2025']['area'].endswith(f'({mha})'),f'{slug} area')
    main=re.findall(r'<tr><td>[EWO]-\dE?</td><td>[^<]*</td><td>(\$[\d,]+)</td><td>(\$[\d,]+)</td></tr>',t)
    ck(len(main)==24,f'{slug} main rows {len(main)}')
    for i,c in enumerate(COLS):
        ck(v(main[i][0])==b[c]['with']==W[mha][i],f'{slug} {c} with'); ck(v(main[i][1])==b[c]['without']==WO[mha][i],f'{slug} {c} without')
    y=re.search(r'<section id="yoy">(.*?)</section>',t,re.S).group(1)
    yr=re.findall(r'<tr><td>([EWO]-\dE?)</td>'+'<td>([^<]*)</td>'*6+'</tr>',y)
    ck(len(yr)==24,f'{slug} yoy rows')
    for i,c in enumerate(COLS):
        r=yr[i]
        for k,(yrv,key) in enumerate([(a,'with'),(b,'with'),(None,'with'),(a,'without'),(b,'without'),(None,'without')]):
            exp=yrv[c][key] if yrv else b[c][key]-a[c][key]
            ck(v(r[k+1])==exp,f'{slug} yoy {c} col{k} {r[k+1]} != {exp}')
    s=re.search(r'gets (\$[\d,]+) in 2026, vs (\$[\d,]+) in 2025 \(([^/]+)/month, ([^%]+)%\)',y)
    ck(s and v(s[1])==b['E5']['with'] and v(s[2])==a['E5']['with'] and v(s[3])==b['E5']['with']-a['E5']['with'],f'{slug} E5 sentence')
    ck(s and abs(float(s[4].replace('−','-'))-(b['E5']['with']-a['E5']['with'])*100/a['E5']['with'])<0.051,f'{slug} pct')
    ck(f'ZIP {D[mha]["zip"]}' in y and mha in y,f'{slug} yoy zip/mha')
    ck(t.count('Rates checked against DTMO 19 Oct 2026')==1 and 'effective 1 Jan 2026' in t,f'{slug} stamp')
    ck('"dateModified": "2026-10-19"' in t,f'{slug} dateModified')
    op=re.findall(r'<li><a href="/bah/([^/]+)/">',re.search(r'<h2>Other posts</h2><ul class="bases">(.*?)</ul>',t).group(1))
    ck(set(op)==ALL-{slug} and len(op)==19,f'{slug} other posts {sorted(ALL-{slug}-set(op))}')
    for w in ('rent vs buy','Rent/Buy','consent','privacy','endorse'): ck(w.lower() not in t.lower(),f'{slug} forbidden {w}')
sm=open(os.path.join(root,'sitemap.xml')).read()
for slug in PAGES: ck(f'/bah/{slug}/</loc><lastmod>2026-10-19<' in sm,f'sitemap {slug}')
print(f'checks {n} mismatches {bad}')
