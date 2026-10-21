"""IndexNow (Bing/Yandex/etc no-login submit), added 20 Oct 2026. UNOFFICIAL / PERSONAL.
apply: copies the key file to <site_root>/<key>.txt (never touches index.html).
submit: POSTs every sitemap URL to https://api.indexnow.org/indexnow (run only after the key file is live).
Usage: python3 apply_indexnow.py <site_root> [--submit]"""
import glob, json, os, re, sys, urllib.request
here = os.path.dirname(os.path.abspath(__file__))
kf = [f for f in glob.glob(here + '/*.txt')][0]; key = open(kf).read().strip()
root = sys.argv[1].rstrip('/') + '/'
open(root + key + '.txt', 'w').write(key)
print('key file', key + '.txt')
if '--submit' in sys.argv:
    urls = re.findall(r'<loc>(.*?)</loc>', open(root + 'sitemap.xml').read())
    body = json.dumps({'host': 'pcsvector.com', 'key': key, 'keyLocation': f'https://pcsvector.com/{key}.txt', 'urlList': urls}).encode()
    req = urllib.request.Request('https://api.indexnow.org/indexnow', data=body, headers={'Content-Type': 'application/json; charset=utf-8'})
    try:
        r = urllib.request.urlopen(req, timeout=30); print('HTTP', r.status, r.read()[:300], len(urls), 'urls')
    except urllib.error.HTTPError as e: print('HTTP', e.code, e.read()[:300], len(urls), 'urls')
