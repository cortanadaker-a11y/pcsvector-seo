"""Deepen the 8 original BAH base pages (19 Oct 2026). UNOFFICIAL / PERSONAL.
Adds: as-of stamp, 'Change vs 2025' table (official DTMO 2025 vs 2026, live BAH Rate Lookup), full 'Other posts' list (19 base pages),
dateModified + source line, sitemap lastmod. Idempotent. Never touches index.html (home).
Usage: python3 gen_bah_deepen.py <site_root> dtmo_bah_yoy_2026-10-19.json"""
import json,re,sys,os,html
root,src=sys.argv[1],sys.argv[2]; D=json.load(open(src))
TODAY='2026-10-19'; CHECKED='19 Oct 2026'
COLS=['E1','E2','E3','E4','E5','E6','E7','E8','E9','W1','W2','W3','W4','W5','O1E','O2E','O3E','O1','O2','O3','O4','O5','O6','O7']
LBL=['E-1','E-2','E-3','E-4','E-5','E-6','E-7','E-8','E-9','W-1','W-2','W-3','W-4','W-5','O-1E','O-2E','O-3E','O-1','O-2','O-3','O-4','O-5','O-6','O-7']
PAGES={'fort-bragg':'NC182','fort-hood':'TX286','fort-campbell':'KY106','fort-carson':'CO046','joint-base-lewis-mcchord':'WA311','fort-drum':'NY225','fort-bliss':'TX279','national-capital-region':'DC053'}
ALL=[('fort-bragg','Fort Bragg'),('fort-hood','Fort Hood'),('fort-campbell','Fort Campbell'),('fort-carson','Fort Carson'),('joint-base-lewis-mcchord','Joint Base Lewis-McChord'),('fort-drum','Fort Drum'),('fort-bliss','Fort Bliss'),('national-capital-region','National Capital Region'),
 ('fort-stewart','Fort Stewart'),('fort-benning','Fort Benning'),('joint-base-san-antonio','Joint Base San Antonio'),('fort-riley','Fort Riley'),('fort-knox','Fort Knox'),('fort-leonard-wood','Fort Leonard Wood'),('fort-polk','Fort Polk'),('fort-sill','Fort Sill'),('fort-wainwright','Fort Wainwright'),('fort-huachuca','Fort Huachuca'),('fort-irwin','Fort Irwin'),('schofield-barracks','Schofield Barracks')]
money=lambda n:'${:,}'.format(n)
def chg(a,b):
    d=b-a
    return '$0' if d==0 else ('+' if d>0 else '−')+money(abs(d))
def pct(a,b): return '{:+.1f}%'.format((b-a)*100/a).replace('-','−')
for slug,mha in PAGES.items():
    p=os.path.join(root,'bah',slug,'index.html'); t=open(p,encoding='utf-8').read()
    c25=D[mha]['2025']['cells']; c26=D[mha]['2026']['cells']; z=D[mha]['zip']
    assert all(c25[c] and c26[c] for c in COLS)
    name=re.search(r'<h2>2026 (.*?) BAH by pay grade</h2>',t).group(1)
    # 1 stamp
    stamp=f'<p class="note" id="asof">Calendar-year 2026 rates (effective 1 Jan 2026). Rates checked against DTMO {CHECKED}.</p>'
    t=re.sub(r'<p class="note" id="asof">.*?</p>\n','',t)
    t=re.sub(r'(<h2>2026 .*? BAH by pay grade</h2>\n)',lambda m:m.group(1)+stamp+'\n',t,count=1)
    # 2 yoy
    t=re.sub(r'<section id="yoy">.*?</section>\n','',t,flags=re.S)
    rows=''.join(f'<tr><td>{LBL[i]}</td><td>{money(c25[c]["with"])}</td><td>{money(c26[c]["with"])}</td><td>{chg(c25[c]["with"],c26[c]["with"])}</td><td>{money(c25[c]["without"])}</td><td>{money(c26[c]["without"])}</td><td>{chg(c25[c]["without"],c26[c]["without"])}</td></tr>' for i,c in enumerate(COLS))
    e5a,e5b=c25['E5']['with'],c26['E5']['with']
    yoy=(f'<section id="yoy">\n<h2>{name} BAH: 2026 vs 2025</h2>\n'
         f'<p>Official DTMO rates for the same housing area ({mha}). A Sergeant (E-5) with dependents gets {money(e5b)} in 2026, vs {money(e5a)} in 2025 ({chg(e5a,e5b)}/month, {pct(e5a,e5b)}).</p>\n'
         f'<div class="tw"><table><thead><tr><th>Grade</th><th>2025 with dep.</th><th>2026 with dep.</th><th>Change</th><th>2025 without</th><th>2026 without</th><th>Change</th></tr></thead><tbody>{rows}</tbody></table></div>\n'
         f'<p class="note">2025 and 2026 rates from the DTMO BAH Rate Lookup (ZIP {z}), checked {CHECKED}. If your area’s rate went down, rate protection keeps your 2025 rate while you stay at the same post with the same status.</p>\n</section>\n')
    t=re.sub(r'(</table></div>\n<p class="note">“With dependents”.*?</p>\n)',lambda m:m.group(1)+yoy,t,count=1,flags=re.S)
    # 3 other posts
    ul='<h2>Other posts</h2><ul class="bases">'+''.join(f'<li><a href="/bah/{s}/">{n}</a></li>' for s,n in ALL if s!=slug)+'</ul>'
    t,k=re.subn(r'<h2>Other posts</h2><ul class="bases">.*?</ul>',ul,t,count=1); assert k==1
    # 4 dateModified + source
    t=re.sub(r'"dateModified": "[^"]*"',f'"dateModified": "{TODAY}"',t,count=1)
    t=re.sub(r' 2026 rates re-checked and 2025 rates read on the DTMO BAH Rate Lookup.*?\.(?=</p>)','',t)
    t=re.sub(r'(<p class="src">Source: Defense Travel Management Office.*?)(</p>)',lambda m:m.group(1)+f' 2026 rates re-checked and 2025 rates read on the DTMO BAH Rate Lookup (ZIP {z}) on {CHECKED}.'+m.group(2),t,count=1)
    for need in ('id="asof"','id="yoy"'): assert t.count(need)==1,(slug,need)
    open(p,'w',encoding='utf-8').write(t); print('ok',slug,name)
sm=os.path.join(root,'sitemap.xml'); s=open(sm).read()
for slug in PAGES: s=re.sub(rf'(<loc>https://pcsvector.com/bah/{slug}/</loc><lastmod>)[^<]*',rf'\g<1>{TODAY}',s)
open(sm,'w').write(s)
