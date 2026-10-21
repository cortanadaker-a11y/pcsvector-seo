#!/usr/bin/env python3
"""21 Oct 2026 go-live fixes (Zak-approved 7:16 AM ET). Idempotent. Usage: python3 apply_golive.py <site_root> [YYYY-MM-DD]
 1) Post renames: Fort Barfoot, VA -> Fort Pickett, VA (MHA ZZ710); Fort Walker, VA -> Fort A.P. Hill, VA (MHA VA368). Rates unchanged.
 2) 'PCS Wayfinder' -> 'Military-approved agent'; 'typical rent' -> 'avg rent' (home FAQ + JSON-LD + button).
 3) og:image / twitter:summary_large_image on every page (copies og-card-2026-10-21.png into assets/).
 6) aria-labels on the two home post inputs; 'Other posts' links 20 older BAH pages -> 7 newer; sitemap lastmod for changed pages.
Then re-versions calc-data.json in pcs.js and pcs.js/pcs.css in index.html (sha256[:10], same rule as gen_site.py).
Run after any generator (gen_site.py/build.py/gen_bah_*): those re-emit the old strings/tags."""
import sys, os, re, json, glob, hashlib, shutil
R = sys.argv[1].rstrip('/') + '/'; TODAY = sys.argv[2] if len(sys.argv) > 2 else '2026-10-21'
HERE = os.path.dirname(os.path.abspath(__file__)) + '/'
BASE = 'https://pcsvector.com'
OG = '/assets/og-card-2026-10-21.png'
ALT = 'PCS Vector — Know your BAH before you PCS — free, 2026 rates'
REN = {'Fort Barfoot, VA': 'Fort Pickett, VA', 'Fort Walker, VA': 'Fort A.P. Hill, VA'}
TXT = [('Connecting with a PCS Wayfinder for housing help is also free.', 'Connecting with a Military-approved agent for housing help is also free.'),
       ('What is a PCS Wayfinder?', 'What is a Military-approved agent?'),
       ('PCS Wayfinders are military-approved local housing agents at your new duty station.', 'Military-approved agents are local housing agents at your new duty station.'),
       ('then tap Connect With A PCS Wayfinder and enter your first name and email.', 'then enter your first name and email and tap Find a home — Free to connect with a Military-approved agent.'),
       ('Connect with a PCS Wayfinder ➔', 'Connect with a Military-approved agent ➔'),
       ('then shows typical rent, utilities', 'then shows avg rent, utilities'),
       ('compares typical rent plus utilities', 'compares avg rent plus utilities'),
       ('Typical rent and utilities are local planning estimates', 'Avg rent and utilities are local planning estimates')]
# 21 Oct 7:33 AM ET (Zak-approved): no 'formerly'/'also called'/'briefly called' rename mentions anywhere; strip any re-emitted ones.
STRIP = ['Fort Pickett and Fort A.P. Hill were briefly called Fort Barfoot and Fort Walker (2023–2025); '
         'the calculator uses Fort Pickett, VA and Fort A.P. Hill, VA. ', ' (Fort Bragg, not Fort Liberty)']
NEW7 = [('fort-gordon', 'Fort Gordon'), ('fort-jackson', 'Fort Jackson'), ('fort-rucker', 'Fort Rucker'), ('fort-lee', 'Fort Lee'),
        ('joint-base-langley-eustis', 'Joint Base Langley-Eustis'), ('fort-leavenworth', 'Fort Leavenworth'),
        ('joint-base-elmendorf-richardson', 'Joint Base Elmendorf-Richardson')]
h10 = lambda b: hashlib.sha256(b).hexdigest()[:10]
changed = set()
def rw(p, s):
    if open(p).read() != s: open(p, 'w').write(s); changed.add(p)
os.makedirs(R + 'assets', exist_ok=True)
if not os.path.exists(R + OG[1:]) or open(R + OG[1:], 'rb').read() != open(HERE + 'og-card-2026-10-21.png', 'rb').read():
    shutil.copy(HERE + 'og-card-2026-10-21.png', R + OG[1:])
# 1) calc-data keys (order preserved)
cp = R + 'assets/calc-data.json'; raw = open(cp).read(); cd = json.loads(raw)
if any(k in cd['posts'] for k in REN):
    cd['posts'] = {REN.get(k, k): v for k, v in cd['posts'].items()}
    rw(cp, json.dumps(cd, separators=(',', ':'), ensure_ascii=False))
posts = sorted(cd['posts'])
# home
ip = R + 'index.html'; ix = open(ip).read()
for a, b in REN.items(): ix = ix.replace(f'<option value="{a}">{a}</option>', f'<option value="{b}">{b}</option>')
def resort(m):  # keep the static option order == JS Object.keys(D.posts).sort()
    opts = re.findall(r'<option value="([^"]*)"( selected)?>', m.group(2)); sel = {o for o, x in opts if x}
    head = [o for o, _ in opts if o not in cd['posts']]
    return m.group(1) + ''.join(f'<option value="{o}"{" selected" if o in sel else ""}>{o}</option>' for o in head + posts) + m.group(3)
ix = re.sub(r'(<select id="bah_calc_(?:current|gaining)" name="bah_calc_(?:current|gaining)"[^>]*>)(.*?)(</select>)', resort, ix, flags=re.S)
ix = ix.replace('<select id="bah_calc_current" name="bah_calc_current">', '<select id="bah_calc_current" name="bah_calc_current" aria-label="Current post">')
ix = ix.replace('<select id="bah_calc_gaining" name="bah_calc_gaining">', '<select id="bah_calc_gaining" name="bah_calc_gaining" aria-label="New post">')
for a, b in TXT: ix = ix.replace(a, b)
# no renamed-post mentions on the traditional-names FAQ answer (HTML + JSON-LD)
for k in STRIP: ix = ix.replace(k, '')
rw(ip, ix)
# pcs.js: aria-label on the generated combobox inputs; comment wording
jp = R + 'assets/pcs.js'; js = open(jp).read()
A = "inp.setAttribute('aria-controls', lid);"
if "inp.setAttribute('aria-label'" not in js:
    js = js.replace(A, "inp.setAttribute('aria-label', sel.getAttribute('aria-label') || (id === 'bah_calc_current' ? 'Current post' : 'New post')); " + A, 1)
js = js.replace('views/home.py (Wayfinder)', 'views/home.py (agent referral)').replace('services/referral_lead.py (Wayfinder)', 'services/referral_lead.py (agent referral)').replace('results + Wayfinder', 'results + agent referral')
js = re.sub(r"calc-data\.json\?v=[0-9a-f]+", 'calc-data.json?v=' + h10(open(cp, 'rb').read()), js)
rw(jp, js)
sp = R + 'assets/pcs.css'; rw(sp, open(sp).read().replace('/* wayfinder */', '/* agent referral */'))
# every page: og:image + twitter large card
TAGS = (f'<meta property="og:image" content="{BASE}{OG}">\n<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n'
        f'<meta property="og:image:alt" content="{ALT}">\n<meta name="twitter:card" content="summary_large_image">\n<meta name="twitter:image" content="{BASE}{OG}">')
pages = sorted(glob.glob(R + '**/*.html', recursive=True))
for p in pages:
    s = open(p).read()
    if 'property="og:image"' not in s:
        s2 = s.replace('<meta name="twitter:card" content="summary">', TAGS, 1)
        assert s2 != s, 'no twitter:card anchor in ' + p
        s = s2
    rw(p, s)
# Other posts: older 20 -> newer 7
for p in sorted(glob.glob(R + 'bah/*/index.html')):
    s = open(p).read(); slug = p.split('/')[-2]
    m = re.search(r'(<h2>Other posts</h2><ul class="bases">)(.*?)(</ul>)', s, re.S)
    if not m: continue
    add = ''.join(f'<li><a href="/bah/{sl}/">{nm}</a></li>' for sl, nm in NEW7 if sl != slug and f'href="/bah/{sl}/"' not in m.group(2))
    if add: s = s[:m.end(2)] + add + s[m.end(2):]
    rw(p, s)
# cache-bust index (same rule as gen_site.py / check_cache_bust.py)
ix = open(ip).read()
ix = re.sub(r'/assets/pcs\.js(\?v=[0-9a-f]+)?"', '/assets/pcs.js?v=' + h10(open(jp, 'rb').read()) + '"', ix)
ix = re.sub(r'/assets/pcs\.css(\?v=[0-9a-f]+)?"', '/assets/pcs.css?v=' + h10(open(sp, 'rb').read()) + '"', ix)
rw(ip, ix)
# sitemap lastmod for changed pages
smp = R + 'sitemap.xml'; sm = open(smp).read()
for p in sorted(changed):
    if not p.endswith('.html') or p.endswith('404.html'): continue
    u = BASE + '/' + p[len(R):].replace('index.html', '')
    sm = re.sub(r'(<loc>' + re.escape(u) + r'</loc><lastmod>)[^<]+', r'\g<1>' + TODAY, sm)
rw(smp, sm)
print('changed', len(changed), 'files:', *sorted(x[len(R):] for x in changed))
