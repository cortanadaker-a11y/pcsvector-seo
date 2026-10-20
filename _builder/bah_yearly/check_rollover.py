"""Number-diff after rollover.py. UNOFFICIAL / PERSONAL. Re-derives every $ figure on /bah/ pages from the DTMO ASCII files.
Usage: check_rollover.py <site_root> <new_ascii_dir> <prev_ascii_dir> <NEW_YEAR> <checked> <today> <home_sha256> [log]
Exit 0 only if 0 mismatches."""
import os, re, sys, json, glob, html, hashlib, subprocess
from collections import Counter
root, nd, pd, NY, CHECKED, TODAY, HOME = sys.argv[1:8]; NY = int(NY); PY = NY - 1
COLS = ['E1','E2','E3','E4','E5','E6','E7','E8','E9','W1','W2','W3','W4','W5','O1E','O2E','O3E','O1','O2','O3','O4','O5','O6','O7']; LBL = [c[0]+'-'+c[1:] for c in COLS]
def asc(d, k):
    p = [x for x in glob.glob(d + '/*') if re.fullmatch(rf'bah{k}\d\d\.txt', os.path.basename(x))][0]
    return {l.split(',')[0]: [int(float(v)) for v in l.strip().split(',')[1:25]] for l in open(p) if re.match(r'[A-Z]{2}\d{3},', l)}
NW, NWO, PW, PWO = asc(nd, 'w'), asc(nd, 'wo'), asc(pd, 'w'), asc(pd, 'wo')
res = []
NONRATE = {'fort-drum': {350}}  # static utility-bill remark (not a BAH figure), present before rollover
def ck(page, lab, got, exp): res.append((page, lab, got, exp, got == exp))
v = lambda s: int(s.replace('\u2212', '-').replace('+', '').replace('$', '').replace(',', ''))
TOK = re.compile(r'\u2212?\$[\d,]+')
ck('/', 'home index.html sha256 unchanged', hashlib.sha256(open(root + '/index.html', 'rb').read()).hexdigest(), HOME)
try:
    ch = subprocess.run(['git', '-C', root, 'status', '--porcelain'], capture_output=True, text=True).stdout.split('\n')
    bad = [l for l in ch if l.strip() and not re.match(r'^ ?M (bah/.*index\.html|sitemap\.xml)$', l.strip() if l.startswith(' ') else l)]
    ck('/', 'only bah/**/index.html + sitemap.xml changed', bad, [])
except Exception as e: ck('/', 'git status', str(e), '')
bah = root + '/bah'; slugs = sorted(d for d in os.listdir(bah) if os.path.isdir(bah + '/' + d))
for s in slugs:
    t = open(f'{bah}/{s}/index.html', encoding='utf-8').read(); mha = re.search(r'\(code ([A-Z]{2}\d{3})\)', t).group(1)
    W, WO, Wp, WOp = NW[mha], NWO[mha], PW[mha], PWO[mha]
    yoy = re.search(r'<section id="yoy">(.*?)</section>', t, re.S); ck(s, 'one yoy section', t.count('<section id="yoy">'), 1)
    body = t.replace(yoy.group(0), '') if yoy else t
    main = re.findall(r'<tr><td>([EWO]-\dE?)</td><td>[^<]*</td><td>(\$[\d,]+)</td><td>(\$[\d,]+)</td></tr>', body)
    ck(s, 'main grades', [m[0] for m in main], LBL)
    ck(s, 'main with == DTMO new ASCII', [v(m[1]) for m in main], W); ck(s, 'main without == DTMO new ASCII', [v(m[2]) for m in main], WO)
    y = yoy.group(1); yr = re.findall(r'<tr><td>([EWO]-\dE?)</td>' + '<td>([^<]*)</td>' * 6 + '</tr>', y)
    ck(s, 'yoy grades', [r[0] for r in yr], LBL)
    ck(s, 'yoy cells', [[v(x) for x in r[1:]] for r in yr], [[Wp[i], W[i], W[i]-Wp[i], WOp[i], WO[i], WO[i]-WOp[i]] for i in range(24)])
    ck(s, 'yoy headers', re.findall(r'<th>(\d{4}) (?:with dep\.|without)</th>', y), [str(PY), str(NY), str(PY), str(NY)])
    m = re.search(rf'gets (\$[\d,]+) in {NY}, vs (\$[\d,]+) in {PY} \(([^/]+)/month, ([^%]+)%\)', y)
    ck(s, 'yoy E5 sentence', m and (v(m[1]), v(m[2]), v(m[3])), (W[4], Wp[4], W[4]-Wp[4]))
    ck(s, 'yoy pct', m and abs(float(m[4].replace('\u2212', '-')) - (W[4]-Wp[4])*100/Wp[4]) < 0.051, True)
    c = re.search(r'rent</strong> near .*? about <strong>\$([\d,]+)\u2013\$([\d,]+)/month</strong>.*? run about <strong>\$([\d,]+)\u2013\$([\d,]+)/month</strong>\. That puts all-in housing at roughly <strong>\$([\d,]+)\u2013\$([\d,]+)/month', body)
    r1, r2, u1, u2, c1, c2 = [v('$' + x) for x in c.groups()]; ck(s, 'cost = rent + utilities', (c1, c2), (r1 + u1, r2 + u2))
    gp = re.findall(r'<tr><td>([EWO]-\d) [^<]*</td><td>(\$[\d,]+)</td><td>(\u2212?\$[\d,]+) to (\u2212?\$[\d,]+)</td></tr>', body)
    GAP = ['E-4','E-5','E-6','E-7','W-2','O-3']; ck(s, 'gap grades', [g[0] for g in gp], GAP)
    for g in gp:
        b = W[LBL.index(g[0])]; ck(s, f'gap {g[0]}', (v(g[1]), v(g[2]), v(g[3])), (b, b - c2, b - c1))
    fs = re.findall(r'a Sergeant \(E-5\) with dependents \((\$[\d,]+)\) lands between (\u2212?\$[\d,]+) and (\u2212?\$[\d,]+) a month', t)
    ck(s, 'FAQ E5 sentence (visible + JSON-LD)', [tuple(v(x) for x in f) for f in fs], [(W[4], W[4]-c2, W[4]-c1)] * 2)
    # every $ token outside the tables must be explained
    allowed = {r1, r2, u1, u2, c1, c2, W[4], W[4]-c2, W[4]-c1} | NONRATE.get(s, set())
    prose = re.sub(r'<table.*?</table>', '', body, flags=re.S)
    stray = [x for x in TOK.findall(prose) if v(x) not in allowed]; ck(s, 'no unexplained $ in prose', stray, [])
    ld = [json.loads(x) for x in re.findall(r'<script type="application/ld\+json">(.*?)</script>', t)]
    fq = [(q['name'], q['acceptedAnswer']['text']) for q in [x for x in ld if x['@type'] == 'FAQPage'][0]['mainEntity']]
    vis = [(html.unescape(q), html.unescape(a)) for q, a in re.findall(r'<h3>(.*?)</h3><p>(.*?)</p>', t)]; ck(s, 'FAQ JSON-LD == visible', fq, vis)
    ck(s, 'dateModified', [x for x in ld if x['@type'] == 'WebPage'][0]['dateModified'], TODAY)
    ck(s, 'as-of stamp', f'Calendar-year {NY} rates (effective 1 Jan {NY}). Rates checked against DTMO {CHECKED}.' in t, True)
    ck(s, 'title/H1 year', (str(NY) in re.search(r'<title>(.*?)</title>', t)[1], f'({NY})</h1>' in t), (True, True))
    left = re.sub(r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d{4}|\d{4}-\d\d-\d\d|\d{4} planning|from \d{4} to \d{4}|DTMO\u2019s \d{4} ASCII', '', body)
    ck(s, f'no stale {PY} rate-year label outside yoy', re.findall(rf'.{{30}}\b{PY}\b.{{20}}', left), [])
    ck(s, "'Military-approved agents' kept", 'Military-approved agents' in t, True)
h = open(bah + '/index.html', encoding='utf-8').read()
for s in slugs:
    mha = re.search(r'\(code ([A-Z]{2}\d{3})\)', open(f'{bah}/{s}/index.html').read()).group(1)
    r = re.search(rf'<tr><td><a href="/bah/{s}/">[^<]+</a></td><td>({mha})</td><td>(\$[\d,]+)</td><td>(\$[\d,]+)</td>', h)
    ck('hub', f'row {s}', r and (v(r[2]), v(r[3])), (NW[mha][4], NWO[mha][4]))
ck('hub', 'title year', f'BAH {NY}' in re.search(r'<title>(.*?)</title>', h)[1], True)
sm = open(root + '/sitemap.xml').read()
ck('sitemap', '/bah/ lastmod', sorted(set(re.findall(r'<loc>https://pcsvector.com/bah/[^<]*</loc><lastmod>([^<]*)', sm))), [TODAY])
bad = [r for r in res if not r[4]]
with open(sys.argv[8] if len(sys.argv) > 8 else 'check_rollover.log', 'w') as f:
    for r in res: f.write(f'{"PASS" if r[4] else "FAIL"} | {r[0]} | {r[1]} | got={r[2]} | exp={r[3]}\n')
print(f'checks {len(res)} mismatches {len(bad)}')
for r in bad[:30]: print('FAIL', r)
sys.exit(1 if bad else 0)
