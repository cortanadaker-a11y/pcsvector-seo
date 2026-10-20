"""Build pcsvector.com static app (exact port of the Streamlit UI) into /workspace/site_v2. UNOFFICIAL / PERSONAL (Zak Daker)."""
import json, html, re, os, glob, shutil, subprocess, sys
B = '/workspace/build_v2/'; OUT = '/workspace/site_v2/'; TODAY = '2026-10-11'
sys.path.insert(0, B + 'test'); sys.path.insert(0, '/workspace/pcs-vector-repo')
D = json.load(open(OUT + 'assets/calc-data.json'))
FAQ = json.load(open(B + 'faq.json'))
for d in ('calculator', 'find-a-home'):
    shutil.rmtree(OUT + d, ignore_errors=True)
for f in ('app.js',):
    if os.path.exists(OUT + 'assets/' + f): os.remove(OUT + 'assets/' + f)
# --- assets
js = open(B + 'src/pcs.js').read() + '\n' + open(B + 'src/app.js').read()
def _clean(t): return t.replace('the live Streamlit app', 'the original app').replace('Streamlit app', 'original app').replace('the Streamlit HTML', 'the original HTML').replace('match Streamlit', 'match the original')
js = _clean(js)
open(OUT + 'assets/pcs.js', 'w').write(js)
open(OUT + 'assets/pcs.css', 'w').write(_clean(open(B + 'src/pcs.css').read()))
# --- SSR of the default state via the REAL Python renderer (same HTML the Streamlit app emits)
import fake_st
from services import gas_prices as GP
table = json.load(open(OUT + 'assets/gas-table.json')); GP._eia_table = lambda: table
from components import bah_calculator as BC
fake_st.st.session_state.update(bah_calc_grade='E-5', bah_calc_deps_n=0, bah_calc_yos=4, bah_calc_current='Fort Campbell, KY', bah_calc_gaining='Fort Bragg, NC', bah_calc_barracks=False)
BC.render_bah_calculator()
ssr = re.sub(r'>\s+<', '><', ''.join(fake_st.CAP['html'])).strip()
e = lambda s: html.escape(s, quote=True)
posts = sorted(D['posts'])
def sel(id_, label, opts, value, gold=False, help_=None):
    o = ''.join(f'<option value="{e(v)}"{" selected" if v == value else ""}>{e(t)}</option>' for v, t in opts)
    h = (f'<button type="button" class="pcs-help" aria-label="Help: {e(help_)}">{QSVG}<span class="pcs-tip" role="tooltip">{e(help_)}</span></button>') if help_ else ''
    return (f'<div class="pcs-field"><label class="pcs-label{" gold" if gold else ""}" for="{id_}"><span>{label}</span>{h}</label>'
            f'<div class="pcs-select"><span class="val">{e(dict(opts).get(value, value))}</span><select id="{id_}" name="{id_}">{o}</select>{CHEV}</div></div>')
CHEV = '<svg class="chev" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M7.41 8.59 12 13.17l4.59-4.58L18 10l-6 6-6-6z"/></svg>'
QSVG = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M11 18h2v-2h-2v2zm1-16C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm0-14c-2.21 0-4 1.79-4 4h2c0-1.1.9-2 2-2s2 .9 2 2c0 2-3 1.75-3 5h2c0-2.25 3-2.5 3-5 0-2.21-1.79-4-4-4z"/></svg>'
DBL_R = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M6.41 6 5 7.41 9.58 12 5 16.59 6.41 18l6-6z"/><path fill="currentColor" d="m13 6-1.41 1.41L16.17 12l-4.58 4.59L13 18l6-6z"/></svg>'
DBL_L = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M17.59 18 19 16.59 14.42 12 19 7.41 17.59 6l-6 6z"/><path fill="currentColor" d="m11 18 1.41-1.41L7.83 12l4.58-4.59L11 6l-6 6z"/></svg>'
ARR_R = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M8.59 16.59 13.17 12 8.59 7.41 10 6l6 6-6 6z"/></svg>'
grades = [(g, g) for g in D['grades']]
deps = [(str(n), '5+' if n == 5 else str(n)) for n in range(6)]
yos = [(str(n), str(n)) for n in range(41)]
NONE = '\u2014 Skip \u2014'
TITLE = 'PCS Vector \u2014 Free Army PCS BAH Calculator (2026) | OHA, COLA, Housing'
DESC = 'Free Army PCS calculator: compare 2026 BAH, OHA, COLA, rent, utilities, and gas between duty stations. Built for Soldiers. Not affiliated with DoD.'
URL = 'https://pcsvector.com/'
FAQ_TITLE = 'Army PCS FAQ \u2014 BAH, OHA, COLA, DLA, and housing pay'
ld = {"@context": "https://schema.org", "@graph": [
    {"@type": "WebApplication", "name": "PCS Vector", "url": URL, "applicationCategory": "FinanceApplication", "operatingSystem": "Web",
     "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "description": DESC,
     "audience": {"@type": "Audience", "audienceType": "U.S. Army Soldiers and military families"}},
    {"@type": "FAQPage", "name": FAQ_TITLE, "url": URL, "mainEntity": [{"@type": "Question", "name": i['q'], "acceptedAnswer": {"@type": "Answer", "text": i['a']}} for i in FAQ['items']]},
    {"@type": "WebSite", "name": "PCS Vector", "url": URL}]}
sh = lambda t: html.escape(t, quote=False).replace('$', '&#36;')
faq_html = ''.join(f"<article class='pcs-seo-faq-item'><h3>{sh(i['q'])}</h3><div><p>{sh(i['a'])}</p></div></article>" for i in FAQ['items'])
bah_pages = sorted(p for p in os.listdir(OUT + 'bah') if os.path.isdir(OUT + 'bah/' + p))
names = {s: re.search(r'<h1>BAH (?:at|in the) (.*?)(?: \(20| \(JBLM|:)', open(OUT + f'bah/{s}/index.html').read()).group(1) for s in bah_pages}
side_links = ''.join(f'<li><a href="/bah/{s}/">{e(n)}</a></li>' for s, n in names.items()) + '<li><a href="/bah/">All posts \u2192</a></li>'
page = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(TITLE)}</title>
<meta name="description" content="{e(DESC)}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{URL}">
<meta name="theme-color" content="#121E16">
<meta property="og:type" content="website"><meta property="og:site_name" content="PCS Vector"><meta property="og:title" content="{e(TITLE)}">
<meta property="og:description" content="{e(DESC)}"><meta property="og:url" content="{URL}"><meta name="twitter:card" content="summary">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon-48x48.png" type="image/png" sizes="48x48">
<link rel="icon" href="/favicon-192x192.png" type="image/png" sizes="192x192">
<link rel="apple-touch-icon" href="/apple-touch-icon.png" sizes="180x180">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400..800&amp;family=Source+Sans+3:wght@200..900&amp;display=swap">
<link rel="preload" href="/assets/calc-data.json" as="fetch" crossorigin>
<link rel="stylesheet" href="/assets/pcs.css">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
<script src="/assets/pcs.js" defer></script>
</head><body>
<header class="pcs-header"><button type="button" class="pcs-icon-btn" id="pcs-sidebar-open" aria-label="Open sidebar" aria-controls="pcs-sidebar" aria-expanded="false">{DBL_R}</button></header>
<div class="pcs-scrim" id="pcs-scrim"></div>
<aside class="pcs-sidebar" id="pcs-sidebar" aria-hidden="true" inert aria-label="About PCS Vector">
<button type="button" class="pcs-icon-btn" id="pcs-sidebar-close" aria-label="Close sidebar">{DBL_L}</button>
<h2>PCS Vector</h2><p class="cap">Built For Soldiers; By Soldiers</p><hr>
<p><strong>Free</strong> PCS calculator for <strong>{len(posts)}+</strong> posts \u2014 BAH, OHA, COLA, utilities, DLA, then a free housing match.</p>
<p class="cap">Always confirm numbers with finance before you sign.</p>
<p class="cap" style="margin-top:24px;color:#F0D060;font-weight:700">2026 BAH by post</p><ul class="pcs-side-links">{side_links}</ul>
</aside>
<main class="pcs-main" id="main">
<div class="pcs-page-brand"><h1 class="pcs-brand-title">PCS Vector</h1><div class="pcs-face-tagline">For Soldiers; By Soldiers</div></div>
<div class="pcs-calc-face">
<div id="pcs-inputs-panel" class="pcs-face-section pcs-face-section-inputs">
<div class="pcs-row">{sel('bah_calc_grade', 'Rank', grades, 'E-5', gold=True)}{sel('bah_calc_deps_n', 'Dependents', deps, '0')}{sel('bah_calc_yos', 'Years of service', yos, '4')}</div>
<div class="pcs-row">{sel('bah_calc_current', 'Current Post', [(NONE, NONE)] + [(p, p) for p in posts], 'Fort Campbell, KY', gold=True, help_='Pick a post to compare. Use Skip compare for target only.')}{sel('bah_calc_gaining', 'Target Post', [(p, p) for p in posts], 'Fort Bragg, NC')}</div>
<div class="pcs-check-row"><label class="pcs-check"><input type="checkbox" id="bah_calc_barracks"><span class="box" aria-hidden="true"></span><span>Barracks + meal card (no BAH)</span></label><button type="button" class="pcs-help" aria-label="Help: barracks">{QSVG}<span class="pcs-tip" role="tooltip">Single Soldiers in the barracks do not get BAH or OHA. Meal card replaces BAS. OCONUS COLA is reduced.</span></button></div>
</div>
<div id="pcs-results" aria-live="polite">{ssr}</div>
<div id="pcs-match-panel" class="pcs-face-section pcs-face-section-match"><div id="pcs-referral"></div><span id="find-a-home"></span>
<p class="pcs-way-kicker" id="pcs-way-kicker">Military-approved agents \u00b7 Fort Bragg, NC</p>
<button type="button" class="pcs-btn" id="referral_open_btn">Find a home \u2014 Free \u2794</button>
<form class="pcs-ref-fields" id="pcs-ref-form" novalidate>
<div class="pcs-row"><div class="pcs-field"><label class="pcs-label gold" for="referral_first_name">First name</label><input class="pcs-text" id="referral_first_name" name="first_name" type="text" placeholder="First" autocomplete="given-name" maxlength="80"></div>
<div class="pcs-field"><label class="pcs-label" for="referral_email_address">Email</label><input class="pcs-text" id="referral_email_address" name="email" type="email" inputmode="email" placeholder="you@email.com" autocomplete="email" maxlength="120"></div></div>
<button type="submit" class="pcs-btn" id="referral_submit_btn">Connect with a PCS Wayfinder \u2794</button>
<p class="pcs-caption" id="pcs-ref-caption">Free \u00b7 no obligation</p>
<div id="pcs-ref-msg" aria-live="polite"></div>
</form>
</div>
</div>
<div class="pcs-footer"><span>Planning figures \u00b7 verify LES / finance / DTMO before you sign</span></div>
<div class="pcs-exp"><details id="pcs-faq-exp"><summary>{ARR_R}<span>FAQ \u2014 BAH, OHA, COLA &amp; more</span></summary><div class="body">
<section class="pcs-seo-faq" id="pcs-faq" aria-labelledby="pcs-faq-heading"><h2 id="pcs-faq-heading">{sh(FAQ_TITLE)}</h2><p class="pcs-seo-faq-lead">{sh(FAQ['lead'])}</p>{faq_html}</section>
</div></details></div>
<noscript><p>Turn on JavaScript to change rank, dependents and posts. The figures above are for an E-5 with no dependents, Fort Campbell to Fort Bragg.</p></noscript>
</main>
<div id="pcs-sticky-ref-bar" role="complementary" aria-label="Housing referral" hidden><div class="pcs-sticky-ref-meta"><div class="pcs-sticky-ref-kicker">Step 2 \u00b7 Free housing help</div><div class="pcs-sticky-ref-line" id="pcs-sticky-ref-line"></div></div><button type="button" class="pcs-sticky-ref-btn" id="pcs-sticky-ref-go">Get free help \u2192</button></div>
</body></html>
'''
open(OUT + 'index.html', 'w').write(page)
# --- BAH pages: CTAs -> the app on the domain (preset target post), agent CTAs -> open the Wayfinder
app_names = {'fort-bragg': 'Fort Bragg, NC', 'fort-hood': 'Fort Hood, TX', 'fort-campbell': 'Fort Campbell, KY', 'fort-carson': 'Fort Carson, CO',
             'joint-base-lewis-mcchord': 'Joint Base Lewis-McChord, WA', 'fort-drum': 'Fort Drum, NY', 'fort-bliss': 'Fort Bliss, TX',
             'national-capital-region': 'Pentagon / National Capital Region, VA'}
from urllib.parse import quote_plus
for f in glob.glob(OUT + 'bah/**/index.html', recursive=True) + [OUT + '404.html']:
    s = open(f).read(); slug = f.split('/')[-2]
    pre = ('tgt=' + quote_plus(app_names[slug]) + '&amp;') if slug in app_names else ''
    s = re.sub(r'href="/(?:calculator/)?\?(?:tgt=[^&"]*&amp;)?(utm_source=[^"#]*utm_medium=agents[^"#]*)(?:#find-a-home)*"', lambda m: f'href="/?{pre}{m.group(1)}#find-a-home"', s)
    s = re.sub(r'href="/(?:calculator/)?\?(?:tgt=[^&"]*&amp;)?(utm_source=[^"#]*)"', lambda m: f'href="/?{pre}{m.group(1)}"', s)
    s = s.replace('"url": "/calculator/"', '"url": "https://pcsvector.com/"')
    if f.endswith('404.html'): s = s.replace('<link rel="canonical" href="https://pcsvector.com/404.html">', '')
    open(f, 'w').write(s)
# favicon (live app uses the compass emoji as page_icon)
# 19 Oct 2026: real files (Google ignores data-URI favicons). Source: PCS Vector logo mark icons/pcs_icon_A_512.png (was Noto compass until 19 Oct 2026 PM); see icons/make_icons.py
import subprocess, sys as _sys
subprocess.run([_sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'icons', 'make_icons.py'), OUT], check=True)
ICON = '<link rel="icon" href="/favicon.ico" sizes="any"><link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="icon" href="/favicon-48x48.png" type="image/png" sizes="48x48"><link rel="icon" href="/favicon-192x192.png" type="image/png" sizes="192x192"><link rel="apple-touch-icon" href="/apple-touch-icon.png" sizes="180x180">'
for f in glob.glob(OUT + '**/*.html', recursive=True):
    s = open(f).read()
    if 'rel="icon"' not in s:
        s = s.replace('<meta name="viewport"', ICON + '<meta name="viewport"', 1); open(f, 'w').write(s)
# cache-busting: content-hash query on assets (GitHub Pages sends max-age=600)
import hashlib
_h = lambda b: hashlib.sha256(b).hexdigest()[:10]
_cd = _h(open(OUT + 'assets/calc-data.json', 'rb').read())
_js = open(OUT + 'assets/pcs.js').read()
if '/assets/calc-data.json?v=' not in _js:
    _js = _js.replace("fetch('/assets/calc-data.json')", "fetch('/assets/calc-data.json?v=" + _cd + "')"); open(OUT + 'assets/pcs.js', 'w').write(_js)
_jv, _cv = _h(_js.encode()), _h(open(OUT + 'assets/pcs.css', 'rb').read())
_ix = open(OUT + 'index.html').read()
_ix = re.sub(r'/assets/calc-data\.json(\?v=[0-9a-f]+)?"', '/assets/calc-data.json?v=' + _cd + '"', _ix)
_ix = re.sub(r'/assets/pcs\.js(\?v=[0-9a-f]+)?"', '/assets/pcs.js?v=' + _jv + '"', _ix)
_ix = re.sub(r'/assets/pcs\.css(\?v=[0-9a-f]+)?"', '/assets/pcs.css?v=' + _cv + '"', _ix)
open(OUT + 'index.html', 'w').write(_ix)
# sitemap
urls = [URL, URL + 'bah/'] + [f'{URL}bah/{s}/' for s in bah_pages]
open(OUT + 'sitemap.xml', 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{u}</loc><lastmod>{TODAY}</lastmod></url>\n' for u in urls) + '</urlset>\n')
missing = [v for v in app_names.values() if v not in D['posts']]
assert not missing, missing
print('built', len(page), 'bytes index;', len(js), 'bytes js')
