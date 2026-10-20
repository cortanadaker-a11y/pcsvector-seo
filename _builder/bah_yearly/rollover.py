"""BAH calendar-year rollover for the served /bah/ pages (hub + every base page). UNOFFICIAL / PERSONAL.
Rewrites, from the DTMO ASCII rate files only:
  - main rate table (24 grades, with/without) -> new year
  - gap table BAH column + "left after rent + utilities" (rent/utility planning ranges on the page are kept)
  - FAQ E-5 sentence (visible + FAQPage JSON-LD)
  - <section id="yoy">: "{NEW} vs {PREV}" table for all 24 grades (replaces any older yoy section)
  - rate-year labels (title, meta, og, H1, H2, FAQ, JSON-LD names), as-of stamp, source line, dateModified
  - /bah/ hub rows (E-5 with/without) + labels; sitemap <lastmod> for /bah/ URLs
NEVER opens index.html at the site root.
Usage: rollover.py <site_root> <new_ascii_dir> <prev_ascii_dir> <NEW_YEAR> <checked "DD Mon YYYY"> <today YYYY-MM-DD> [--expect-prev]
  --expect-prev: assert the page tables currently equal the PREV ASCII (normal rollover). Dry-run with a stand-in skips this."""
import os, re, sys, json, glob
root, nd, pd, NY, CHECKED, TODAY = sys.argv[1:7]; NY = int(NY); PY = NY - 1
EXPECT_PREV = '--expect-prev' in sys.argv
COLS = ['E1','E2','E3','E4','E5','E6','E7','E8','E9','W1','W2','W3','W4','W5','O1E','O2E','O3E','O1','O2','O3','O4','O5','O6','O7']
LBL = [c[0] + '-' + c[1:] for c in COLS]
def find(d, pat):
    f = [p for p in glob.glob(os.path.join(d, '*')) if re.fullmatch(pat, os.path.basename(p))]
    assert len(f) == 1, (d, pat, f); return f[0]
def asc(d, kind):
    yy = None
    p = find(d, rf'bah{kind}\d\d\.txt'); out = {}
    for l in open(p):
        x = l.strip().split(',')
        if len(x) >= 25 and re.fullmatch(r'[A-Z]{2}\d{3}', x[0]): out[x[0]] = [int(float(v)) for v in x[1:25]]
    return out, os.path.basename(p)
NW, nwf = asc(nd, 'w'); NWO, _ = asc(nd, 'wo'); PW, _ = asc(pd, 'w'); PWO, _ = asc(pd, 'wo')
money = lambda n: ('\u2212$' if n < 0 else '$') + f'{abs(n):,}'
def chg(a, b): d = b - a; return '$0' if d == 0 else ('+' if d > 0 else '\u2212') + f'${abs(d):,}'
def pct(a, b): return '{:+.1f}%'.format((b - a) * 100 / a).replace('-', '\u2212')
PROTECT = [r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d{4}', r'\d{4}-\d\d-\d\d', r'\d{4} planning', r'from \d{4} to \d{4}']
def relabel(t):
    """rate-year label PY -> NY outside protected date phrases (also handles re-runs: NY stays NY)."""
    keep = []
    def stash(m): keep.append(m.group(0)); return f'\x00{len(keep)-1}\x00'
    for p in PROTECT: t = re.sub(p, stash, t)
    t = re.sub(rf'\b{PY}\b', str(NY), t)
    return re.sub(r'\x00(\d+)\x00', lambda m: keep[int(m.group(1))], t)
log = []
bah = os.path.join(root, 'bah'); slugs = sorted(d for d in os.listdir(bah) if os.path.isdir(os.path.join(bah, d)))
for s in slugs:
    p = os.path.join(bah, s, 'index.html'); t = open(p, encoding='utf-8').read()
    mha = re.search(r'\(code ([A-Z]{2}\d{3})\)', t).group(1)
    W, WO, Wp, WOp = NW[mha], NWO[mha], PW[mha], PWO[mha]
    head, sep, rest = t.partition('</table></div>')  # first table = main rate table
    rows = re.findall(r'<tr><td>([EWO]-\dE?)</td><td>([^<]*)</td><td>\$([\d,]+)</td><td>\$([\d,]+)</td></tr>', head)
    assert [r[0] for r in rows] == LBL, (s, 'main rows')
    if EXPECT_PREV:
        assert [int(r[2].replace(',', '')) for r in rows] == Wp and [int(r[3].replace(',', '')) for r in rows] == WOp, (s, 'page != prev ASCII')
    i = iter(range(24))
    head = re.sub(r'<tr><td>([EWO]-\dE?)</td><td>([^<]*)</td><td>\$[\d,]+</td><td>\$[\d,]+</td></tr>',
                  lambda m: (lambda k: f'<tr><td>{m.group(1)}</td><td>{m.group(2)}</td><td>{money(W[k])}</td><td>{money(WO[k])}</td></tr>')(LBL.index(m.group(1))), head)
    t = head + sep + rest
    # gap table + FAQ sentence
    cm = re.search(r'all-in housing at roughly <strong>\$([\d,]+)\u2013\$([\d,]+)/month</strong>', t)
    lo, hi = int(cm.group(1).replace(',', '')), int(cm.group(2).replace(',', ''))
    def gaprow(m):
        k = LBL.index(m.group(1)); b = W[k]
        return f'<tr><td>{m.group(1)} {m.group(2)}</td><td>{money(b)}</td><td>{money(b - hi)} to {money(b - lo)}</td></tr>'
    t, ng = re.subn(r'<tr><td>([EWO]-\d) ([^<]*)</td><td>\$[\d,]+</td><td>\u2212?\$[\d,]+ to \u2212?\$[\d,]+</td></tr>', gaprow, t)
    assert ng == 6, (s, 'gap rows', ng)
    e5 = W[4]
    t, nf = re.subn(r'a Sergeant \(E-5\) with dependents \(\$[\d,]+\) lands between \u2212?\$[\d,]+ and \u2212?\$[\d,]+ a month',
                    f'a Sergeant (E-5) with dependents ({money(e5)}) lands between {money(e5 - hi)} and {money(e5 - lo)} a month', t)
    assert nf == 2, (s, 'faq e5', nf)
    # labels
    t = re.sub(r'<p class="note" id="asof">.*?</p>\n', '', t)
    t = re.sub(r'<p class="note">Calendar-year \d{4} rates \(effective 1 Jan \d{4}\)\. Rates checked against DTMO [^<]*</p>\n', '', t)
    t = re.sub(r'<section id="yoy">.*?</section>\n', '', t, flags=re.S)
    t = relabel(t)
    stamp = f'<p class="note" id="asof">Calendar-year {NY} rates (effective 1 Jan {NY}). Rates checked against DTMO {CHECKED}.</p>\n'
    t, k = re.subn(rf'(<h2>{NY} [^<]*BAH by pay grade</h2>\n)', lambda m: m.group(1) + stamp, t, count=1); assert k == 1, (s, 'h2')
    name = re.search(rf'<h2>{NY} (.*?) BAH by pay grade</h2>', t).group(1)
    yrows = ''.join(f'<tr><td>{LBL[i]}</td><td>{money(Wp[i])}</td><td>{money(W[i])}</td><td>{chg(Wp[i], W[i])}</td><td>{money(WOp[i])}</td><td>{money(WO[i])}</td><td>{chg(WOp[i], WO[i])}</td></tr>' for i in range(24))
    yoy = (f'<section id="yoy">\n<h2>{name} BAH: {NY} vs {PY}</h2>\n'
           f'<p>Official DTMO rates for the same housing area ({mha}). A Sergeant (E-5) with dependents gets {money(W[4])} in {NY}, vs {money(Wp[4])} in {PY} ({chg(Wp[4], W[4])}/month, {pct(Wp[4], W[4])}).</p>\n'
           f'<div class="tw"><table><thead><tr><th>Grade</th><th>{PY} with dep.</th><th>{NY} with dep.</th><th>Change</th><th>{PY} without</th><th>{NY} without</th><th>Change</th></tr></thead><tbody>{yrows}</tbody></table></div>\n'
           f'<p class="note">{PY} and {NY} rates from the DTMO BAH ASCII rate files (MHA {mha}), checked {CHECKED}. If your area\u2019s rate went down, rate protection keeps your {PY} rate while you stay at the same post with the same status.</p>\n</section>\n')
    t, k = re.subn(r'(</table></div>\n<p class="note">\u201cWith dependents\u201d.*?</p>\n)', lambda m: m.group(1) + yoy, t, count=1, flags=re.S); assert k == 1, (s, 'yoy anchor')
    src = (f'<p class="src">Source: Defense Travel Management Office (DTMO), {NY} BAH rates, all locations and all pay grades (ASCII rate file {nwf}, MHA {mha}), '
           f'compared with DTMO\u2019s {PY} ASCII rate file; checked {CHECKED}.</p>')
    t, k = re.subn(r'<p class="src">Source: Defense Travel Management Office.*?</p>', src, t, count=1, flags=re.S); assert k == 1, (s, 'src')
    t = re.sub(r'"dateModified": "[^"]*"', f'"dateModified": "{TODAY}"', t, count=1)
    t = re.sub(r'Page updated [A-Z][a-z]{2} \d{4}', 'Page updated ' + ' '.join(CHECKED.split()[1:]), t)
    for need in ('id="asof"', 'id="yoy"'): assert t.count(need) == 1, (s, need)
    open(p, 'w', encoding='utf-8').write(t); log.append((s, mha, Wp[4], W[4]))
# hub
hp = os.path.join(bah, 'index.html'); h = open(hp, encoding='utf-8').read()
h, nh = re.subn(r'<tr><td><a href="/bah/([^/]+)/">([^<]+)</a></td><td>([A-Z]{2}\d{3})</td><td>\$[\d,]+</td><td>\$[\d,]+</td><td>([^<]*)</td></tr>',
                lambda m: f'<tr><td><a href="/bah/{m.group(1)}/">{m.group(2)}</a></td><td>{m.group(3)}</td><td>{money(NW[m.group(3)][4])}</td><td>{money(NWO[m.group(3)][4])}</td><td>{m.group(4)}</td></tr>', h)
assert nh == len(slugs), ('hub rows', nh, len(slugs))
h = relabel(h)
h, k = re.subn(r'<p class="src">Source: DTMO .*?</p>', f'<p class="src">Source: DTMO {NY} BAH rates (ASCII rate file {nwf}), checked {CHECKED}.</p>', h, count=1, flags=re.S); assert k == 1
h = re.sub(r'"dateModified": "[^"]*"', f'"dateModified": "{TODAY}"', h, count=1)
h = re.sub(r'Page updated [A-Z][a-z]{2} \d{4}', 'Page updated ' + ' '.join(CHECKED.split()[1:]), h)
open(hp, 'w', encoding='utf-8').write(h)
sm = os.path.join(root, 'sitemap.xml'); x = open(sm).read()
x = re.sub(r'(<loc>https://pcsvector.com/bah/(?:[^<]*/)?</loc><lastmod>)[^<]*', rf'\g<1>{TODAY}', x); open(sm, 'w').write(x)
for r in log: print('ok', *r)
print('pages', len(log), '+ hub')
