#!/usr/bin/env python3
"""Check icon URLs (status, content-type, dimensions) and icon links on every page.
Usage: python3 check_icons.py https://pcsvector.com   (or http://localhost:8765)"""
import io, re, sys, urllib.request
from PIL import Image
base = sys.argv[1].rstrip('/')
def get(p):
    r = urllib.request.urlopen(urllib.request.Request(base + p, headers={'User-Agent': 'Mozilla/5.0 icon-check', 'Cache-Control': 'no-cache'}), timeout=30)
    return r.status, r.headers.get('Content-Type', ''), r.read()
fails = 0
exp = {'/favicon.ico': ('image/', [(16, 16), (32, 32), (48, 48)]), '/favicon.svg': ('image/svg+xml', None),
       '/favicon-48x48.png': ('image/png', [(48, 48)]), '/favicon-192x192.png': ('image/png', [(192, 192)]),
       '/apple-touch-icon.png': ('image/png', [(180, 180)]), '/favicon-LICENSE.txt': ('text/plain', None)}
for p, (ct, sz) in exp.items():
    st, c, b = get(p); ok = st == 200 and c.startswith(ct)
    if sz:
        im = Image.open(io.BytesIO(b)); got = sorted(im.info['sizes']) if p.endswith('.ico') else [im.size]
        ok = ok and sorted(got) == sorted(sz)
    else: got = len(b)
    print('PASS' if ok else 'FAIL', p, st, c, got); fails += not ok
sm = get('/sitemap.xml')[2].decode()
pages = [re.sub(r'^https://pcsvector\.com', '', u) for u in re.findall(r'<loc>([^<]+)</loc>', sm)] + ['/404.html']
for p in pages:
    s = get(p)[2].decode('utf-8')
    hrefs = re.findall(r'<link rel="(?:icon|apple-touch-icon)" href="([^"]+)"', s)
    ok = hrefs == ['/favicon.ico', '/favicon.svg', '/favicon-48x48.png', '/favicon-192x192.png', '/apple-touch-icon.png'] and 'data:image' not in ''.join(hrefs)
    print('PASS' if ok else 'FAIL', 'links', p, hrefs if not ok else ''); fails += not ok
print('ICON CHECK', 'PASS' if not fails else f'FAIL ({fails})', f'{len(exp)} files, {len(pages)} pages'); sys.exit(1 if fails else 0)
