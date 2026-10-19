"""Diff every number on the OHA pages against the DTMO source JSON (and site calc-data). UNOFFICIAL / PERSONAL. Exit 1 on any mismatch."""
import json, re, sys, html
ROOT = sys.argv[1].rstrip('/') + '/'; S = json.load(open(sys.argv[2])); C = json.load(open(ROOT + 'assets/calc-data.json'))
sys.path.insert(0, '/workspace/oha_1019/gen')
PAGES = {'korea': ['KR025','KR177'], 'japan': ['JP045','JP065','JP061'], 'okinawa': ['JP027'], 'germany': ['DE355','DE231','DE700','DE055','DE228']}
PAGES['index'] = sum(PAGES.values(), [])
SYM = {'KR': '\u20a9', 'JP': '\u00a5', 'DE': '\u20ac'}
mism = []; checked = 0
def lm(c, v): return f'{SYM[c[:2]]}{int(v + 0.5):,}'
def allowed(codes):
    a = set()
    for c in codes:
        for k in ('with', 'without'):
            for g, r in S[c][k].items():
                for f in ('rent', 'util', 'miha'):
                    if r[f] is not None: a.add(f'${r[f]:,.2f}'); a.add(lm(c, r[f + '_local']))
        u = S[c]['with']['E-5']; a.add(f'${round(u["rent"] + u["util"], 2):,.2f}')
    return a
for slug, codes in PAGES.items():
    f = ROOT + ('oha/index.html' if slug == 'index' else f'oha/{slug}/index.html'); t = open(f).read()
    A = allowed(codes)
    # 1) every currency token anywhere in the page (visible text + JSON-LD) must be a source value
    for tok in re.findall(r'[$\u20a9\u00a5\u20ac][\d,]+(?:\.\d+)?', html.unescape(t)):
        checked += 1
        if tok not in A: mism.append((slug, 'unsourced currency token', tok))
    # 2) structured: each grade row in each locality table
    for c in codes:
        if slug == 'index':
            m = re.search(rf'<tr data-c="{c}">(.*?)</tr>', t).group(1); vals = re.findall(r'\$[\d,]+\.\d\d', m)
            exp = [f'${S[c]["with"]["E-5"]["rent"]:,.2f}', f'${S[c]["without"]["E-5"]["rent"]:,.2f}', f'${S[c]["with"]["E-5"]["util"]:,.2f}']
            checked += 1
            if vals != exp: mism.append((slug, c, 'hub row', vals, exp))
            continue
        sec = t.split(f'<h2 id="{c.lower()}">')[1].split('<h2')[0]
        for g in S[c]['with']:
            m = re.search(rf'<tr data-g="{g}">(.*?)</tr>', sec).group(1)
            vals = re.findall(r'[$\u20a9\u00a5\u20ac][\d,]+(?:\.\d+)?', html.unescape(m))
            W, O = S[c]['with'][g], S[c]['without'][g]
            exp = [f'${W["rent"]:,.2f}', lm(c, W['rent_local']), f'${O["rent"]:,.2f}', lm(c, O['rent_local'])]
            checked += 1
            if vals != exp: mism.append((slug, c, g, vals, exp))
        W, O = S[c]['with']['E-5'], S[c]['without']['E-5']
        u = re.findall(r'[$\u20a9\u00a5\u20ac][\d,]+(?:\.\d+)?', html.unescape(re.search(r'<tr data-k="util">(.*?)</tr>', sec).group(1)))
        mi = re.findall(r'[$\u20a9\u00a5\u20ac][\d,]+(?:\.\d+)?', html.unescape(re.search(r'<tr data-k="miha">(.*?)</tr>', sec).group(1)))
        checked += 2
        if u != [f'${W["util"]:,.2f}', lm(c, W['util_local']), f'${O["util"]:,.2f}', lm(c, O['util_local'])]: mism.append((slug, c, 'util', u))
        if mi != [f'${W["miha"]:,.2f}', lm(c, W['miha_local'])]: mism.append((slug, c, 'miha', mi))
        # FX + effective date + locality name
        r = float(W['roe'].split('/')[0]); fx = f'1 USD = {r:,.4f} EUR' if r < 10 else f'1 USD = {r:,.2f} ' + {'KR': 'KRW', 'JP': 'JPY'}[c[:2]]
        d = W['eff']; import datetime; dd = datetime.date(int(d[:4]), int(d[4:6]), int(d[6:])); ds = f'{dd.day} {dd:%b %Y}'
        checked += 2
        if fx not in sec: mism.append((slug, c, 'fx', fx))
        if f'effective {ds}' not in sec: mism.append((slug, c, 'eff', ds))
        # rounding consistency of the DTMO USD figure vs local/ROE
        for k in ('with', 'without'):
            for g, rr in S[c][k].items():
                for fld in ('rent', 'util'):
                    checked += 1
                    if abs(rr[fld + '_local'] / r - rr[fld]) > 0.011: mism.append((slug, c, k, g, fld, 'USD != local/ROE', rr[fld], rr[fld + '_local'] / r))
    # 3) stamps/dates/schema
    checked += 3
    if 'Rates checked 19 Oct 2026' not in t: mism.append((slug, 'stamp'))
    if '"dateModified": "2026-10-19"' not in t: mism.append((slug, 'dateModified'))
    if 'rates as of 16 Oct 2026' not in t: mism.append((slug, 'as-of'))
    # 4) FAQ schema text == visible text
    for blk in re.findall(r'<script type="application/ld\+json">(.*?)</script>', t):
        j = json.loads(blk)
        if j.get('@type') == 'FAQPage':
            for q in j['mainEntity']:
                checked += 1
                if f'<h3>{html.escape(q["name"])}</h3><p>{html.escape(q["acceptedAnswer"]["text"])}</p>' not in t: mism.append((slug, 'faq text mismatch', q['name']))
# 5) site calc-data (what the calculator shows) vs DTMO source, rounded dollars
CM = {'Camp Humphreys, South Korea': 'KR025', 'Camp Casey, South Korea': 'KR177', 'Camp Zama, Japan': 'JP045', 'USAG Wiesbaden, Germany': 'DE355', 'USAG Bavaria, Germany': 'DE231', 'USAG Rheinland-Pfalz, Germany': 'DE700'}
for p, c in CM.items():
    for di, k in ((1, 'with'), (0, 'without')):
        for i, g in enumerate(C['grades']):
            r = S[c][k]['O-7' if g == 'O-7+' else g]; checked += 1
            if C['posts'][p]['oha'][di][i] != [round(r['rent']), round(r['util'])]: mism.append(('calc-data', p, k, g))
print(f'checked {checked} | mismatches {len(mism)}')
for m in mism[:30]: print('MISMATCH', m)
sys.exit(1 if mism else 0)
