"""PCS Vector static SEO site builder. UNOFFICIAL / PERSONAL (Zak Daker). Builds + number-checks from DTMO 2026 files."""
import re, json, html, subprocess, sys, datetime, os
sys.path.insert(0, '/workspace/pcs-vector-repo')
from services import utility_costs as U
D = '/workspace/scratch/bah2026/'
OUT = '/workspace/site_v2/'
REPO = '/workspace/pcs-vector-repo/'
TODAY = '2026-10-11'
APP = '/'
COLS = ['E1','E2','E3','E4','E5','E6','E7','E8','E9','W1','W2','W3','W4','W5','O1E','O2E','O3E','O1','O2','O3','O4','O5','O6','O7','O8','O9','O10']
G24 = COLS[:24]
TITLES = {'E1':'Private (PV1)','E2':'Private (PV2)','E3':'Private First Class','E4':'Specialist / Corporal','E5':'Sergeant','E6':'Staff Sergeant','E7':'Sergeant First Class','E8':'Master Sgt / First Sgt','E9':'Sergeant Major','W1':'Warrant Officer 1','W2':'Chief Warrant Officer 2','W3':'Chief Warrant Officer 3','W4':'Chief Warrant Officer 4','W5':'Chief Warrant Officer 5','O1E':'2LT, 4+ yrs prior enlisted/WO','O2E':'1LT, 4+ yrs prior enlisted/WO','O3E':'CPT, 4+ yrs prior enlisted/WO','O1':'Second Lieutenant','O2':'First Lieutenant','O3':'Captain','O4':'Major','O5':'Lieutenant Colonel','O6':'Colonel','O7':'Brigadier General and up'}
def g(c): return c[0]+'-'+c[1:]
BASES = [
 dict(slug='fort-bragg', name='Fort Bragg', st='NC', mha='NC182', zip='28310', app='Fort Bragg, NC', alias='Fort Liberty',
      h1='BAH at Fort Bragg, NC (2026)', title='Fort Bragg BAH 2026 (formerly Fort Liberty): Rates by Rank | PCS Vector',
      aliasq=('Is Fort Liberty BAH different from Fort Bragg BAH?', 'No. Fort Liberty was the post\u2019s name from 2023 to 2025. Same post, same housing area (NC182), same rates.')),
 dict(slug='fort-hood', name='Fort Hood', st='TX', mha='TX286', zip='76544', app='Fort Hood, TX', alias='Fort Cavazos',
      h1='BAH at Fort Hood, TX (2026)', title='Fort Hood BAH 2026 (formerly Fort Cavazos): Rates by Rank | PCS Vector',
      aliasq=('Is Fort Cavazos BAH different from Fort Hood BAH?', 'No. Fort Cavazos was the post\u2019s name from 2023 to 2025. Same post, same housing area (TX286), same rates. Killeen, Harker Heights and Copperas Cove are all in it.')),
 dict(slug='fort-campbell', name='Fort Campbell', st='KY', mha='KY106', zip='42223', app='Fort Campbell, KY', alias=None,
      h1='BAH at Fort Campbell, KY (2026)', title='Fort Campbell BAH 2026: Rates by Rank (KY/TN) | PCS Vector',
      aliasq=('Do I get a different rate if I live in Clarksville, TN?', 'No. Fort Campbell straddles Kentucky and Tennessee, but BAH follows your duty-station ZIP (housing area KY106), not which side of the state line you rent on. State taxes and utilities do differ, so check those before you sign.')),
 dict(slug='fort-carson', name='Fort Carson', st='CO', mha='CO046', zip='80913', app='Fort Carson, CO', alias=None,
      h1='BAH at Fort Carson, CO (2026)', title='Fort Carson BAH 2026 (Colorado Springs): Rates by Rank | PCS Vector',
      aliasq=('Why does DTMO call it Colorado Springs?', 'DTMO sets BAH by Military Housing Area, and Fort Carson sits in the COLORADO SPRINGS, CO area (CO046). Peterson SFB, Schriever SFB and the Air Force Academy share the same area and the same rates.')),
 dict(slug='joint-base-lewis-mcchord', name='Joint Base Lewis-McChord', st='WA', mha='WA311', zip='98433', app='Joint Base Lewis-McChord, WA', alias='JBLM',
      h1='BAH at Joint Base Lewis-McChord (JBLM), WA (2026)', title='JBLM BAH 2026 (Joint Base Lewis-McChord, Tacoma): Rates by Rank | PCS Vector',
      aliasq=('Is JBLM BAH the same as Tacoma BAH?', 'Yes. DTMO places Joint Base Lewis-McChord in the TACOMA, WA housing area (WA311), so Lewis Main, Lewis North and McChord Field all use these rates.')),
 dict(slug='fort-drum', name='Fort Drum', st='NY', mha='NY225', zip='13602', app='Fort Drum, NY', alias=None,
      h1='BAH at Fort Drum, NY (2026)', title='Fort Drum BAH 2026 (Watertown): Rates by Rank | PCS Vector',
      aliasq=('Why do Fort Drum utilities matter so much?', 'Winter heat. In the North Country, propane, oil or gas heat can push a 3-bedroom\u2019s monthly utilities past $350 in the coldest months. Ask a landlord for last winter\u2019s bills before you sign.')),
 dict(slug='fort-bliss', name='Fort Bliss', st='TX', mha='TX279', zip='79916', app='Fort Bliss, TX', alias=None,
      h1='BAH at Fort Bliss, TX (2026)', title='Fort Bliss BAH 2026 (El Paso): Rates by Rank | PCS Vector',
      aliasq=('Does living in New Mexico change my Fort Bliss BAH?', 'No. Chaparral, NM (88081) sits in a different DTMO housing area (NM209), but that doesn\u2019t matter: BAH follows your duty-station ZIP, and Fort Bliss is in the EL PASO, TX area (TX279). You get the El Paso rate wherever you rent.')),
 dict(slug='national-capital-region', name='National Capital Region', st='DC/VA/MD', mha='DC053', zip='22202', app='Pentagon / National Capital Region, VA', alias='Pentagon, Fort Belvoir, Fort Myer, Fort McNair',
      h1='BAH in the National Capital Region: Pentagon, Fort Belvoir, Fort Myer (2026)', title='Pentagon & Fort Belvoir BAH 2026 (Washington DC Metro): Rates by Rank | PCS Vector',
      aliasq=('Do the Pentagon, Fort Belvoir, Fort Myer and Fort McNair all get the same BAH?', 'Yes. ZIPs 22202 (Pentagon), 22060 (Fort Belvoir), 22211 (Fort Myer) and 20319 (Fort McNair) all map to the WASHINGTON, DC METRO AREA (DC053). Fort Meade and Fort Detrick are separate housing areas with different rates.')),
]
def row(f, mha):
    for l in open(D+f):
        p = l.strip().split(',')
        if p[0] == mha:
            assert len(p) == 28
            return dict(zip(COLS, [int(float(x)) for x in p[1:]]))
names = dict(l.strip().split(';',1) for l in open(D+'mhanames26.txt') if ';' in l)
zipmap = [l.split() for l in open(D+'sorted_zipmha26.txt') if len(l.split()) == 2]
pdftxt = {lab: subprocess.run(['pdftotext','-layout',p,'-'],capture_output=True,text=True).stdout for lab,p in (('with','/workspace/raw/pcs/bah2026_with.pdf'),('without','/workspace/raw/pcs/bah2026_without.pdf'))}
appbah = json.load(open(REPO+'data/bah_2026.json'))['installations']
rent = json.load(open(REPO+'data/local_costs_2026.json'))
live = json.load(open('dtmo_live_2026-10-11.json')) if os.path.exists('dtmo_live_2026-10-11.json') else {}
GAP_RANKS = ['E4','E5','E6','E7','W2','O3']
checks = []
def chk(base, label, a, b): checks.append((base, label, a, b, a == b))
for B in BASES:
    m = B['mha']
    W, WO = row('bahw26.txt', m), row('bahwo26.txt', m)
    Wold, WOold = row('bahw26 - old.txt', m), row('bahwo26 - old.txt', m)
    B.update(W=W, WO=WO, area=names[m], zips=[z for z, mm in zipmap if mm == m])
    # 1) ASCII vs DTMO PDF tables
    for lab, ref in (('with', W), ('without', WO)):
        line = [l for l in pdftxt[lab].splitlines() if l.startswith(m)][0]
        nums = [int(x) for x in re.findall(r'\b\d{3,4}\b', re.split(r', [A-Z]{2}\b', line, maxsplit=1)[1])][-24:]
        assert len(nums) == 24, (m, nums)
        for c, v in zip(G24, nums): chk(B['slug'], f'ASCII vs DTMO PDF {lab} {g(c)}', ref[c], v)
    # 2) ASCII vs live app data
    a = appbah[B['app'] if B['app'] in appbah else 'Fort Belvoir, VA']
    chk(B['slug'], 'app mha_code', a['mha_code'], m)
    for c in G24:
        chk(B['slug'], f'ASCII vs app bah_2026.json with {g(c)}', W[c], a['with_dependents'][g(c) if c!='O7' else 'O-7+'])
        chk(B['slug'], f'ASCII vs app bah_2026.json without {g(c)}', WO[c], a['without_dependents'][g(c) if c!='O7' else 'O-7+'])
    # 3) ASCII vs live DTMO Rate Lookup today
    L = live.get(m, {}).get('cells', {})
    for c in G24:
        v = L.get(c)
        if v: chk(B['slug'], f'ASCII vs LIVE DTMO lookup {B["zip"]} {g(c)} with/without', (W[c], WO[c]), (v['with'], v['without']))
        else: checks.append((B['slug'], f'LIVE DTMO lookup {g(c)} not retrieved', None, None, None))
    # 4) misc
    chk(B['slug'], 'row unchanged vs pre-Abilene-update file', (W, WO) == (Wold, WOold), True)
    chk(B['slug'], 'O-8..O-10 equal O-7 (both columns)', W['O7']==W['O8']==W['O9']==W['O10'] and WO['O7']==WO['O8']==WO['O9']==WO['O10'], True)
    zr = [mm for z, mm in zipmap if z == B['zip']]
    chk(B['slug'], f'anchor ZIP {B["zip"]} maps once to {m}', zr, [m])
    # rent / utilities
    lc = rent['installations'][B['app']]
    ut = U.get_utility_costs_for_installation(B['app'])
    ar = ut['areas'][0]
    B.update(rent=lc['rent_3br'], util=(ar['total_utilities_usd_mo']['low'], ar['total_utilities_usd_mo']['high']), util_area=ar['name'], util_note=ar.get('season_note',''), util_asof=ut.get('as_of',''))
    lo, hi = B['rent'][0]+B['util'][0], B['rent'][1]+B['util'][1]
    B['cost'] = (lo, hi)
    B['gap'] = {c: (W[c]-hi, W[c]-lo) for c in GAP_RANKS}
for slug,z,m in [('fort-carson','80914','CO046'),('fort-carson','80912','CO046'),('fort-carson','80840','CO046'),('joint-base-lewis-mcchord','98438','WA311'),('fort-bliss','88081','NM209'),('fort-campbell','37042','KY106'),('fort-campbell','37040','KY106'),('fort-hood','76541','TX286'),('fort-hood','76522','TX286')]:
    chk(slug, f'Q&A claim: ZIP {z} maps to {m}', [mm for zz, mm in zipmap if zz == z], [m])
# NCR extra ZIP checks
for z in ('22060','22211','20319','20301'):
    chk('national-capital-region', f'ZIP {z} maps to DC053', [mm for zz, mm in zipmap if zz == z], ['DC053'])

def money(v): return ('\u2212$' if v < 0 else '$') + f'{abs(v):,}'
def cta(slug, medium='organic'): return f'{APP}?utm_source=bahpage&amp;utm_medium={medium}&amp;utm_campaign={slug}'
CSS = open('style.css').read()
def head(title, desc, url, ld):
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website"><meta property="og:site_name" content="PCS Vector">
<meta property="og:title" content="{html.escape(title.split(' | ')[0])}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{url}">
<meta name="twitter:card" content="summary">
<style>{CSS}</style>
{''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld)}
<script data-goatcounter="https://pcsvector.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>
</head><body><main>'''
FOOT = f'''<p class="src">PCS Vector is an independent planning tool built by Soldiers. It is not an official Army, DoW or DTMO site. Confirm your rate with your finance office. Page updated {datetime.date(2026,10,11):%b %Y}.</p>
</main></body></html>
'''
for B in BASES:
    s, n, W, WO = B['slug'], B['name'], B['W'], B['WO']
    url = f'https://pcsvector.com/bah/{s}/'
    alias = f' (also {B["alias"]})' if B['alias'] and s != 'national-capital-region' else ''
    desc = f'2026 BAH at {n}{alias} for every pay grade, with and without dependents, vs local rent and utilities. Official DTMO rates.'
    faqs = [B['aliasq'],
            (f'Does 2026 BAH at {n} cover rent and utilities?', f'It depends on rank. With avg 3-bedroom rent of ${B["rent"][0]:,}\u2013${B["rent"][1]:,} and utilities of about ${B["util"][0]:,}\u2013${B["util"][1]:,} a month, a Sergeant (E-5) with dependents (${W["E5"]:,}) lands between {money(B["gap"]["E5"][0])} and {money(B["gap"]["E5"][1])} a month after housing. These are planning estimates, not official figures.'),
            ('Do I get a different rate if I live in a nearby town?', 'No. BAH follows your permanent duty-station ZIP, not your home address.'),
            ('When do these rates apply?', 'These are the calendar-year 2026 rates. Rate protection keeps your rate from dropping while you stay at the same post with the same status; a PCS, a reduction in grade or a change in dependency status resets it. DTMO usually publishes the next year\u2019s rates in mid-December.')]
    ld = [{"@context":"https://schema.org","@type":"WebPage","name":B['title'].split(' | ')[0],"url":url,"dateModified":TODAY,"isBasedOn":"https://www.travel.dod.mil/Allowances/Basic-Allowance-for-Housing/BAH-Rate-Lookup/"},
          {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"PCS Vector","item":"https://pcsvector.com/"},{"@type":"ListItem","position":2,"name":"BAH by post","item":"https://pcsvector.com/bah/"},{"@type":"ListItem","position":3,"name":n,"item":url}]},
          {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q, a in faqs]}]
    p = [head(B['title'], desc, url, ld)]
    p.append(f'<nav class="crumb"><a href="/">PCS Vector</a> \u203a <a href="/bah/">BAH by post</a> \u203a {html.escape(n)}</nav>')
    p.append(f'<div class="kick">Military-approved agents \u00b7 {html.escape(n)}, {B["st"]}</div>')
    p.append(f'<h1>{html.escape(B["h1"])}</h1>')
    aka = f' (also searched as {html.escape(B["alias"])})' if B['alias'] else ''
    p.append(f'<p>Monthly Basic Allowance for Housing for Soldiers stationed at {html.escape(n)}{aka}. DTMO lists this housing area as <strong>{html.escape(B["area"])}</strong> (code {B["mha"]}). Your rate depends on three things only: pay grade, with or without dependents, and your duty-station ZIP. Where you choose to live does not change it.</p>')
    p.append(f'<a class="cta" href="{cta(s)}">Compare {html.escape(n)} with your current post (free calculator) \u2192</a>')
    p.append(f'<h2>2026 {html.escape(n)} BAH by pay grade</h2>')
    p.append('<div class="tw"><table><thead><tr><th>Grade</th><th>Rank</th><th>With dependents</th><th>Without</th></tr></thead><tbody>' + ''.join(f'<tr><td>{g(c)}</td><td>{html.escape(TITLES[c])}</td><td>${W[c]:,}</td><td>${WO[c]:,}</td></tr>' for c in G24) + '</tbody></table></div>')
    p.append('<p class="note">\u201cWith dependents\u201d is yes or no: one child and four children get the same rate. O-1E to O-3E are officers with more than four years of prior enlisted or warrant service.</p>')
    # Rent / utilities gap
    p.append(f'<h2>BAH vs rent and utilities at {html.escape(n)}</h2>')
    p.append(f'<p>BAH is a flat monthly amount; rent and utilities are not. Avg off-post <strong>3-bedroom rent</strong> near {html.escape(n)} runs about <strong>${B["rent"][0]:,}\u2013${B["rent"][1]:,}/month</strong>, and utilities for that home (electric, heat, water/trash, internet; {html.escape(B["util_area"])}) run about <strong>${B["util"][0]:,}\u2013${B["util"][1]:,}/month</strong>. That puts all-in housing at roughly <strong>${B["cost"][0]:,}\u2013${B["cost"][1]:,}/month</strong>.</p>')
    p.append('<div class="tw"><table class="gap"><thead><tr><th>Grade</th><th>BAH (with dep.)</th><th>Left after rent + utilities</th></tr></thead><tbody>' + ''.join(f'<tr><td>{g(c)} {html.escape(TITLES[c].split(" /")[0])}</td><td>${W[c]:,}</td><td>{money(B["gap"][c][0])} to {money(B["gap"][c][1])}</td></tr>' for c in GAP_RANKS) + '</tbody></table></div>')
    p.append(f'<p class="note"><strong>Gap note:</strong> a negative number means out-of-pocket each month at the high end of the local market; a positive number means BAH covers it with money left over. {html.escape(B["util_note"])} Rent and utility ranges are PCS Vector planning estimates (rent as of Sep 2026; utilities: {html.escape(B["util_asof"])}), not DTMO figures. DTMO itself says BAH is not meant to cover every housing cost.</p>')
    p.append(f'<a class="cta" href="{cta(s)}">See your exact rent gap for your rank and family size \u2192</a>')
    # ZIPs
    if s == 'national-capital-region':
        st_groups = {}
        for z in B['zips']:
            k = 'DC' if z.startswith('20') and int(z[:3]) <= 205 else ('MD' if z[:2] in ('20','21') else ('VA' if z[:2] in ('22','23','24') else ('WV' if z[:2] in ('25','26') else 'Other')))
            st_groups.setdefault(k, []).append(z)
        p.append(f'<h2>ZIP codes in the Washington, DC Metro housing area ({len(B["zips"])})</h2>')
        for k in ('DC','VA','MD','WV','Other'):
            if k in st_groups: p.append(f'<details><summary>{k} ZIPs ({len(st_groups[k])})</summary><p class="zips">{" ".join(st_groups[k])}</p></details>')
        p.append('<p class="note">State grouping is by ZIP prefix (approximate near borders). The ZIP-to-housing-area mapping itself is DTMO\u2019s.</p>')
    else:
        p.append(f'<h2>ZIP codes in the {html.escape(n)} housing area ({len(B["zips"])})</h2><p class="zips">{" ".join(B["zips"])}</p>')
    p.append('<h2>Quick answers</h2>' + ''.join(f'<h3>{html.escape(q)}</h3><p>{html.escape(a)}</p>' for q, a in faqs))
    # Agents CTA
    p.append(f'<section class="agents"><h2>Military-approved agents at {html.escape(n)}</h2><p>Want local help finding a place that fits your BAH? PCS Vector can connect you with one of our <strong>military-approved agents</strong>: local housing agents at your new duty station. The intro is free and does not change your BAH.</p><a class="cta cta2" href="{cta(s, "agents")}">Run your numbers and get a free intro to a military-approved agent \u2192</a></section>')
    others = [o for o in BASES if o is not B]
    p.append('<h2>Other posts</h2><ul class="bases">' + ''.join(f'<li><a href="/bah/{o["slug"]}/">{html.escape(o["name"])}</a></li>' for o in others) + '</ul>')
    p.append(f'<p class="src">Source: Defense Travel Management Office (DTMO), 2026 BAH rates, all locations and all pay grades (ASCII rate file, MHA {B["mha"]}, downloaded 4 Oct 2026); checked against DTMO\u2019s 2026 PDF rate tables and the DTMO BAH Rate Lookup for ZIP {B["zip"]} on 11 Oct 2026.</p>')
    p.append(FOOT)
    os.makedirs(OUT+f'bah/{s}', exist_ok=True)
    open(OUT+f'bah/{s}/index.html','w').write('\n'.join(p))

# hub
url = 'https://pcsvector.com/bah/'
ld = [{"@context":"https://schema.org","@type":"CollectionPage","name":"Army BAH 2026 by post","url":url,"dateModified":TODAY},
      {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"PCS Vector","item":"https://pcsvector.com/"},{"@type":"ListItem","position":2,"name":"BAH by post","item":url}]}]
h = [head('Army BAH 2026 by Post: Rates, Rent and Utilities | PCS Vector', '2026 BAH for the biggest Army posts, side by side with typical 3-bedroom rent and utilities. From official DTMO tables. Free PCS calculator.', url, ld)]
h.append('<nav class="crumb"><a href="/">PCS Vector</a> \u203a BAH by post</nav><div class="kick">PCS Vector \u00b7 free BAH tables</div><h1>Army BAH 2026 by post</h1>')
h.append('<p>2026 Basic Allowance for Housing for the largest Army posts, from official DTMO tables, next to what a typical 3-bedroom off post actually costs with utilities. Pick a post for every pay grade, the ZIPs covered and the rent gap by rank.</p>')
h.append(f'<a class="cta" href="{APP}?utm_source=bahhub&amp;utm_medium=organic&amp;utm_campaign=bah-hub">Compare any two posts (free calculator) \u2192</a>')
h.append('<div class="tw"><table><thead><tr><th>Post</th><th>Housing area</th><th>E-5 with dep.</th><th>E-5 without</th><th>3BR rent + utilities</th></tr></thead><tbody>' + ''.join(f'<tr><td><a href="/bah/{B["slug"]}/">{html.escape(B["name"])}</a></td><td>{B["mha"]}</td><td>${B["W"]["E5"]:,}</td><td>${B["WO"]["E5"]:,}</td><td>${B["cost"][0]:,}\u2013${B["cost"][1]:,}</td></tr>' for B in BASES) + '</tbody></table></div>')
h.append('<p class="note">Rent + utilities = typical off-post 3-bedroom rent plus monthly utilities, PCS Vector planning estimates (Sep 2026), not DTMO figures. More posts coming; the calculator already covers 68+ Army posts, CONUS and OCONUS.</p>')
h.append(f'<section class="agents"><h2>Military-approved agents</h2><p>After you run your numbers, PCS Vector can connect you with one of our military-approved agents at your new post for free local housing help.</p><a class="cta cta2" href="{APP}?utm_source=bahhub&amp;utm_medium=agents&amp;utm_campaign=bah-hub">Run your numbers \u2192</a></section>')
h.append('<p class="src">Source: DTMO 2026 BAH rates (ASCII and PDF rate tables) and the DTMO BAH Rate Lookup, checked 11 Oct 2026.</p>')
h.append(FOOT)
os.makedirs(OUT+'bah', exist_ok=True)
open(OUT+'bah/index.html','w').write('\n'.join(h))

# landing
url = 'https://pcsvector.com/'
ld = [{"@context":"https://schema.org","@type":"WebSite","name":"PCS Vector","url":url},
      {"@context":"https://schema.org","@type":"WebApplication","name":"PCS Vector BAH Calculator","url":APP,"applicationCategory":"FinanceApplication","operatingSystem":"Web","offers":{"@type":"Offer","price":"0","priceCurrency":"USD"}}]
L = [head('PCS Vector: Free Army PCS BAH Calculator (2026)', 'Free Army PCS calculator: compare 2026 BAH, OHA, COLA, rent, utilities and gas between duty stations. Built by Soldiers. Not affiliated with DoW.', url, ld)]
L.append('<div class="center"><div class="kick">For Soldiers; by Soldiers</div><h1 class="big">PCS Vector</h1>')
L.append('<p>See your 2026 BAH at your current post and your next one, side by side, plus typical rent, utilities, gas and DLA.</p>')
L.append(f'<a class="cta" id="go" href="{APP}?utm_source=pcsvector&amp;utm_medium=home&amp;utm_campaign=landing">Open the free calculator \u2192</a><p class="note">New: loads instantly, right here on pcsvector.com. Still being built, so some figures (rent, utilities, gas, OCONUS) are coming soon.</p></div>')
L.append('<ul class="feat"><li>68+ Army posts, CONUS and OCONUS</li><li>2026 BAH from official DTMO tables, plus OHA, COLA and DLA planning figures</li><li>BAH vs local rent and utilities, so you see the gap before you sign a lease</li><li>Optional free intro to our military-approved agents at your new post</li></ul>')
L.append('<h2>2026 BAH by post</h2><ul class="bases">' + ''.join(f'<li><a href="/bah/{B["slug"]}/">{html.escape(B["name"])}</a></li>' for B in BASES) + '<li><a href="/bah/">All posts \u2192</a></li></ul>')
L.append(FOOT)
open(OUT+'index.html','w').write('\n'.join(L))

# robots + sitemap
open(OUT+'robots.txt','w').write('User-agent: *\nAllow: /\n\nSitemap: https://pcsvector.com/sitemap.xml\n')
urls = ['https://pcsvector.com/', 'https://pcsvector.com/bah/'] + [f'https://pcsvector.com/bah/{B["slug"]}/' for B in BASES]
open(OUT+'sitemap.xml','w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{u}</loc><lastmod>{TODAY}</lastmod></url>\n' for u in urls) + '</urlset>\n')
open(OUT+'404.html','w').write(head('Page not found | PCS Vector','Page not found.','https://pcsvector.com/404.html',[]).replace('<meta name="viewport"','<meta name="robots" content="noindex"><meta name="viewport"') + '<h1>Page not found</h1><p><a href="/">PCS Vector home</a> \u00b7 <a href="/bah/">BAH by post</a></p>' + FOOT)

# log
ok = sum(1 for c in checks if c[4] is True); bad = [c for c in checks if c[4] is False]; miss = [c for c in checks if c[4] is None]
with open('/workspace/build_v2/number_check.log','w') as f:
    for c in checks: f.write(f'{ {True:"PASS",False:"FAIL",None:"MISS"}[c[4]] } | {c[0]} | {c[1]} | file={c[2]} | ref={c[3]}\n')
    f.write(f'TOTAL PASS {ok} / FAIL {len(bad)} / MISSING {len(miss)} (of {len(checks)})\n')
json.dump({B['slug']:{k:B[k] for k in ('mha','area','zip','rent','util','cost','gap')} | {'nzips':len(B['zips']),'E5':(B['W']['E5'],B['WO']['E5'])} for B in BASES}, open('/workspace/build_v2/summary.json','w'), indent=1)
print(f'PASS {ok} FAIL {len(bad)} MISS {len(miss)}')
for c in bad[:20]: print('FAIL', c)
