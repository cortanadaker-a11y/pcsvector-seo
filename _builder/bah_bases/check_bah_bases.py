"""Number-diff for the 12 new BAH base pages + /bah/ hub rows. UNOFFICIAL / PERSONAL.
Every number on each new page is re-derived independently from the sources and compared:
  DTMO 2026 BAH ASCII (with/without), DTMO 2026 PDF rate tables, live DTMO BAH Rate Lookup JSON,
  app data/bah_2026.json, site assets/calc-data.json, app rent/utility planning data, DTMO ZIP->MHA map.
Usage: python3 check_bah_bases.py <site_root> <ascii_dir> <pcs-vector repo> <live_json> <pdf_with> <pdf_without>"""
import json, re, sys, html, subprocess
from collections import Counter
from urllib.parse import unquote_plus
OUT, D, REPO, LIVE, PW, PWO = [a.rstrip('/') + '/' if i < 3 else a for i, a in enumerate(sys.argv[1:7])]
sys.path.insert(0, REPO)
from services import utility_costs as U
COLS = ['E1','E2','E3','E4','E5','E6','E7','E8','E9','W1','W2','W3','W4','W5','O1E','O2E','O3E','O1','O2','O3','O4','O5','O6','O7','O8','O9','O10']
G24 = COLS[:24]; GAP = ['E4','E5','E6','E7','W2','O3']
CALC21 = ['E1','E2','E3','E4','E5','E6','E7','E8','E9','W1','W2','W3','W4','W5','O1','O2','O3','O4','O5','O6','O7']
g = lambda c: c[0] + '-' + c[1:]
SPEC = {  # slug: (mha, anchor zip, app/calculator name, alias that must appear in title+H1+body)
 'fort-stewart': ('GA080','31314','Fort Stewart, GA',None), 'fort-benning': ('GA075','31905','Fort Benning, GA','Fort Moore'),
 'joint-base-san-antonio': ('TX285','78234','Joint Base San Antonio, TX','JBSA'), 'fort-riley': ('KS100','66442','Fort Riley, KS',None),
 'fort-knox': ('KY110','40121','Fort Knox, KY',None), 'fort-leonard-wood': ('MO163','65473','Fort Leonard Wood, MO',None),
 'fort-polk': ('LA115','71459','Fort Polk, LA','Fort Johnson'), 'fort-sill': ('OK237','73503','Fort Sill, OK',None),
 'fort-wainwright': ('AK405','99703','Fort Wainwright, AK',None), 'fort-huachuca': ('AZ014','85613','Fort Huachuca, AZ',None),
 'fort-irwin': ('CA028','92310','Fort Irwin, CA',None), 'schofield-barracks': ('HI408','96857','Schofield Barracks, HI',None)}
res = []
def chk(page, label, a, b): res.append((page, label, a, b, a == b))
def row(f, m):
    for l in open(D + f):
        p = l.strip().split(',')
        if p[0] == m: return dict(zip(COLS, [int(float(x)) for x in p[1:]]))
names = dict(l.strip().split(';', 1) for l in open(D + 'mhanames26.txt') if ';' in l)
zipmap = [l.split() for l in open(D + 'sorted_zipmha26.txt') if len(l.split()) == 2]
pdf = {k: subprocess.run(['pdftotext', '-layout', p, '-'], capture_output=True, text=True).stdout for k, p in (('with', PW), ('without', PWO))}
live = json.load(open(LIVE)); app = json.load(open(REPO + 'data/bah_2026.json'))['installations']
rent = json.load(open(REPO + 'data/local_costs_2026.json'))['installations']; calc = json.load(open(OUT + 'assets/calc-data.json'))
chk('_calc', 'calc-data grade order', calc['grades'], [g(c) if c != 'O7' else 'O-7+' for c in CALC21])
money = lambda v: ('\u2212$' if v < 0 else '$') + f'{abs(v):,}'
TOK = re.compile(r'\u2212?\$[\d,]+(?:\.\d+)?')
hub = open(OUT + 'bah/index.html').read()
for s, (m, z, post, alias) in SPEC.items():
    P = open(OUT + f'bah/{s}/index.html').read()
    W, WO = row('bahw26.txt', m), row('bahwo26.txt', m)
    # sources agree with each other
    for lab, ref in (('with', W), ('without', WO)):
        line = [l for l in pdf[lab].splitlines() if l.startswith(m)][0]
        nums = [int(x) for x in re.findall(r'\b\d{3,4}\b', re.split(r', [A-Z]{2}\b', line, maxsplit=1)[1])][-24:]
        for c, v in zip(G24, nums): chk(s, f'ASCII vs DTMO PDF {lab} {g(c)}', ref[c], v)
    chk(s, 'ASCII unchanged vs pre-update file', (W, WO), (row('bahw26 - old.txt', m), row('bahwo26 - old.txt', m)))
    chk(s, 'O-8..O-10 == O-7', all(R[c] == R['O7'] for R in (W, WO) for c in ('O8', 'O9', 'O10')), True)
    L = live[m]
    chk(s, 'live anchor zip', L['zip'], z); chk(s, 'live area name', L['area'], f'{names[m]} ({m})')
    for i, c in enumerate(G24):
        v = L['cells'][c]
        chk(s, f'LIVE DTMO lookup {g(c)} with/without', (v['with'], v['without']) if v else None, (W[c], WO[c]))
        if v: chk(s, f'LIVE raw is whole dollars {g(c)}', (v['with_raw'].endswith('.00'), v['without_raw'].endswith('.00')), (True, True))
        if v: chk(s, f'LIVE rank label {g(c)}', re.sub(r'\s', '', v['rank_shown']), {'O7':'O7/O7+'}.get(c, c))
    a = app[post]; chk(s, 'app mha_code', a['mha_code'], m)
    for c in G24:
        k = g(c) if c != 'O7' else 'O-7+'
        chk(s, f'app bah_2026.json {g(c)}', (a['with_dependents'][k], a['without_dependents'][k]), (W[c], WO[c]))
    cp = calc['posts'][post]
    for i, c in enumerate(CALC21): chk(s, f'calc-data.json {g(c)} with/without', (cp['h'][1][i], cp['h'][0][i]), (W[c], WO[c]))
    # page table
    rows = re.findall(r'<tr><td>([EWO]-\d+E?)</td><td>[^<]*</td><td>\$([\d,]+)</td><td>\$([\d,]+)</td></tr>', P)
    chk(s, 'page grade rows', [r[0] for r in rows], [g(c) for c in G24])
    for gr, w, wo in rows:
        c = gr.replace('-', ''); chk(s, f'page table {gr}', (int(w.replace(',', '')), int(wo.replace(',', ''))), (W[c], WO[c]))
    # rent/utilities/gap re-derived
    rr = rent[post]['rent_3br']; ar = U.get_utility_costs_for_installation(post)['areas'][0]['total_utilities_usd_mo']; uu = (ar['low'], ar['high'])
    cost = (rr[0] + uu[0], rr[1] + uu[1])
    gaprows = re.findall(r'<tr><td>([EWO]-\d) [^<]*</td><td>\$([\d,]+)</td><td>(\u2212?\$[\d,]+) to (\u2212?\$[\d,]+)</td></tr>', P)
    chk(s, 'gap rows', [x[0] for x in gaprows], [g(c) for c in GAP])
    for gr, b, lo, hi in gaprows:
        c = gr.replace('-', ''); chk(s, f'gap {gr}', (b, lo, hi), (f'{W[c]:,}', money(W[c] - cost[1]), money(W[c] - cost[0])))
    # every money token on the page must be explained, and multiset must match exactly
    exp = Counter()
    for c in G24: exp[f'${W[c]:,}'] += 1; exp[f'${WO[c]:,}'] += 1
    for c in GAP: exp[f'${W[c]:,}'] += 1; exp[money(W[c] - cost[1])] += 1; exp[money(W[c] - cost[0])] += 1
    for v in (rr[0], rr[1], uu[0], uu[1], cost[0], cost[1]): exp[f'${v:,}'] += 1
    for v in (rr[0], rr[1], uu[0], uu[1], W['E5']): exp[f'${v:,}'] += 2   # FAQ visible + FAQ JSON-LD
    for v in (W['E5'] - cost[1], W['E5'] - cost[0]): exp[money(v)] += 2
    got = Counter(TOK.findall(P))
    chk(s, 'all $ tokens on page == re-derived set (multiset)', dict(got), dict(exp))
    # ZIPs + area + FAQ claims
    zl = re.search(r'housing area \((\d+)\)</h2><p class="zips">([\d ]+)</p>', P)
    zips = [zz for zz, mm in zipmap if mm == m]
    chk(s, 'ZIP list == DTMO map', zl.group(2).split(), zips); chk(s, 'ZIP count', int(zl.group(1)), len(zips))
    chk(s, 'anchor ZIP maps once', [mm for zz, mm in zipmap if zz == z], [m])
    chk(s, 'area name on page', f'<strong>{html.escape(names[m])}</strong> (code {m})' in P, True)
    faq_txt = re.sub(r'<[^>]+>', ' ', P.split('<h2>Quick answers</h2>')[1].split('<section')[0])
    for zz in sorted(set(re.findall(r'\b(\d{5})\b', faq_txt))):
        mm = [x for y, x in zipmap if y == zz]
        codes = re.findall(r'\(([A-Z]{2}\d{3})\)', faq_txt)
        chk(s, f'FAQ ZIP {zz} maps to a code named on the page', len(mm) == 1 and mm[0] in codes, True)
    for code in set(re.findall(r'\b([A-Z]{2}\d{3})\b', faq_txt)): chk(s, f'FAQ MHA code {code} is a DTMO MHA and its DTMO name is on the page', code in names and html.escape(names[code]) in P, True)
    for nm, code in re.findall(r'([A-Z][A-Z .,/]+?, [A-Z]{2}) \(([A-Z]{2}\d{3})\)', html.unescape(faq_txt)): chk(s, f'FAQ "{nm.strip()} ({code})" matches DTMO name', nm.strip(), names[code])
    ld = [json.loads(x) for x in re.findall(r'<script type="application/ld\+json">(.*?)</script>', P)]
    fq = [(q['name'], q['acceptedAnswer']['text']) for q in [x for x in ld if x['@type'] == 'FAQPage'][0]['mainEntity']]
    vis = [(html.unescape(q), html.unescape(a)) for q, a in re.findall(r'<h3>(.*?)</h3><p>(.*?)</p>', P)]
    chk(s, 'FAQ JSON-LD == visible Q&A', fq, vis)
    # SEO + links
    url = f'https://pcsvector.com/bah/{s}/'
    chk(s, 'self canonical', re.search(r'<link rel="canonical" href="(.*?)">', P).group(1), url)
    title = html.unescape(re.search(r'<title>(.*?)</title>', P).group(1)); h1 = html.unescape(re.search(r'<h1>(.*?)</h1>', P).group(1))
    if alias: chk(s, f'alias {alias} in title/H1/body', (alias in title, alias in h1, alias in P.split('</h1>')[1]), (True, True, True))
    chk(s, 'dateModified', [x for x in ld if x['@type'] == 'WebPage'][0]['dateModified'], '2026-10-19')
    chk(s, 'as-of stamp visible', 'Rates checked against DTMO 19 Oct 2026' in P and f'ZIP {z} on 19 Oct 2026' in P, True)
    tg = re.findall(r'href="/\?tgt=([^&"]+)&amp;', P)
    chk(s, 'calculator links preselect this post (3)', [unquote_plus(x) for x in tg], [post] * 3)
    chk(s, 'post exists in calculator', post in calc['posts'], True)
    for bad in ('rent/buy', 'rent or buy', 'buy or rent', 'consent', 'privacy', 'endorse', 'approved by the army', 'approved by dod'):
        chk(s, f'forbidden text "{bad}" absent', bad.lower() in P.lower(), False)
    chk(s, "'Military-approved' label kept", 'Military-approved agents' in P, True)
    # hub row
    hr = re.search(rf'<tr><td><a href="/bah/{s}/">[^<]+</a></td><td>([A-Z]{{2}}\d{{3}})</td><td>\$([\d,]+)</td><td>\$([\d,]+)</td><td>\$([\d,]+)\u2013\$([\d,]+)</td></tr>', hub)
    chk(s, 'hub row', hr.groups() if hr else None, (m, f'{W["E5"]:,}', f'{WO["E5"]:,}', f'{cost[0]:,}', f'{cost[1]:,}'))
bad = [r for r in res if not r[4]]
with open(sys.argv[7] if len(sys.argv) > 7 else 'check_bah_bases.log', 'w') as f:
    for r in res: f.write(f'{"PASS" if r[4] else "FAIL"} | {r[0]} | {r[1]} | page/src={r[2]} | ref={r[3]}\n')
print(f'checks {len(res)} mismatches {len(bad)}')
for r in bad[:30]: print('FAIL', r)
sys.exit(1 if bad else 0)
