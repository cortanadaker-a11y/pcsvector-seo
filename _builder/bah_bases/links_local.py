import os,re,sys,urllib.request,urllib.parse,html,json
ROOT=sys.argv[1]; BASE=sys.argv[2]
pages=[]
for d,_,fs in os.walk(ROOT):
  for f in fs:
    if f.endswith('.html'): pages.append(os.path.relpath(os.path.join(d,f),ROOT))
internal=set(); external=set(); issues=[]
for p in pages:
  s=open(os.path.join(ROOT,p)).read()
  url='/'+p.replace('index.html','')
  for attr,v in re.findall(r'\b(href|src|content)="([^"]+)"',s):
    v=html.unescape(v)
    if attr=='content' and not v.startswith('http'): continue
    if v.startswith(('mailto:','tel:','data:','#','javascript:')): continue
    if v.startswith('http'): 
      if 'pcsvector.com' in urllib.parse.urlparse(v).netloc: internal.add((p,urllib.parse.urlparse(v).path or '/'))
      else: external.add(v)
    else: internal.add((p,urllib.parse.urljoin(url,v.split('#')[0])))
  # basic SEO
  t=re.findall(r'<title>(.*?)</title>',s); md=re.findall(r'<meta name="description" content="([^"]*)"',s); cn=re.findall(r'<link rel="canonical" href="([^"]+)"',s)
  h1=len(re.findall(r'<h1[\s>]',s))
  for blk in re.findall(r'<script type="application/ld\+json">(.*?)</script>',s,re.S):
    try: json.loads(blk)
    except Exception as e: issues.append(f'{p}: bad JSON-LD {e}')
  if p!='404.html':
    if len(t)!=1: issues.append(f'{p}: title count {len(t)}')
    if len(md)!=1 or not (50<=len(md[0])<=170): issues.append(f'{p}: meta desc {[len(x) for x in md]}')
    if len(cn)!=1: issues.append(f'{p}: canonical {cn}')
    if h1!=1: issues.append(f'{p}: h1 count {h1}')
    if 'lang="en"' not in s[:300]: issues.append(f'{p}: no lang')
    if 'name="viewport"' not in s: issues.append(f'{p}: no viewport')
  print(f'{p:40} title={len(t[0]) if t else 0} desc={len(md[0]) if md else 0} canon={cn[0] if cn else None} h1={h1}')
  if re.search(r'streamlit',s,re.I): issues.append(f'{p}: mentions streamlit')
bad=[]
for p,u in sorted(internal):
  try:
    r=urllib.request.urlopen(BASE+u); 
  except Exception as e: bad.append((p,u,str(e)))
print('internal links',len(internal),'broken',bad)
for e in sorted(external):
  try:
    req=urllib.request.Request(e,headers={'User-Agent':'Mozilla/5.0'},method='GET'); r=urllib.request.urlopen(req,timeout=20); st=r.status
  except Exception as ex: st=str(ex)[:60]
  print('EXT',st,e[:110])
print('ISSUES',issues)
