"""PCS Vector: 12 additional BAH base pages (static), same format as /bah/fort-bragg/. UNOFFICIAL / PERSONAL.
Data (all BAH numbers): DTMO 2026 BAH ASCII rate files (bahw26.txt / bahwo26.txt, MHA names, ZIP->MHA map),
cross-checked by check_bah_bases.py against DTMO's 2026 PDF rate tables, the live DTMO BAH Rate Lookup pull
(pull_bah_live.py) and the calculator's data. Rent/utility ranges are the app's own planning estimates
(pcs-vector data/local_costs_2026.json + services/utility_costs.py), labelled on the page as not DTMO figures.
Writes ONLY bah/<slug>/index.html for the new slugs, adds rows to the /bah/ hub table, and adds sitemap URLs.
NEVER touches index.html.
Usage: python3 gen_bah_bases.py <site_root> <ascii_dir> <pcs-vector repo>"""
import json, html, os, re, sys
from urllib.parse import quote_plus
OUT = sys.argv[1].rstrip('/') + '/'; D = sys.argv[2].rstrip('/') + '/'; REPO = sys.argv[3].rstrip('/') + '/'
sys.path.insert(0, REPO)
from services import utility_costs as U
TODAY = '2026-10-19'; CHECKED = '19 Oct 2026'
COLS = ['E1','E2','E3','E4','E5','E6','E7','E8','E9','W1','W2','W3','W4','W5','O1E','O2E','O3E','O1','O2','O3','O4','O5','O6','O7','O8','O9','O10']
G24 = COLS[:24]
TITLES = {'E1':'Private (PV1)','E2':'Private (PV2)','E3':'Private First Class','E4':'Specialist / Corporal','E5':'Sergeant','E6':'Staff Sergeant','E7':'Sergeant First Class','E8':'Master Sgt / First Sgt','E9':'Sergeant Major','W1':'Warrant Officer 1','W2':'Chief Warrant Officer 2','W3':'Chief Warrant Officer 3','W4':'Chief Warrant Officer 4','W5':'Chief Warrant Officer 5','O1E':'2LT, 4+ yrs prior enlisted/WO','O2E':'1LT, 4+ yrs prior enlisted/WO','O3E':'CPT, 4+ yrs prior enlisted/WO','O1':'Second Lieutenant','O2':'First Lieutenant','O3':'Captain','O4':'Major','O5':'Lieutenant Colonel','O6':'Colonel','O7':'Brigadier General and up'}
GAP_RANKS = ['E4','E5','E6','E7','W2','O3']
def g(c): return c[0] + '-' + c[1:]
R = '\u2019'
COLA_Q = lambda n, st: (f'Do I get COLA on top of BAH at {n}?', f'Yes. {st} duty stations get BAH plus a cost-of-living allowance (COLA), which DTMO sets separately by rank, years of service and dependents. This page shows BAH only; the calculator adds COLA for {n}.')
NEW = [
 dict(slug='fort-stewart', name='Fort Stewart', st='GA', mha='GA080', zip='31314', app='Fort Stewart, GA', alias=None,
      h1='BAH at Fort Stewart, GA (2026)', title='Fort Stewart BAH 2026 (Hinesville): Rates by Rank | PCS Vector',
      zipq=[('31313','GA080'),('31409','GA077')],
      aliasq=('Does Hunter Army Airfield get Fort Stewart BAH?', 'No. Hunter Army Airfield (ZIP 31409) is in Savannah, which DTMO puts in a separate housing area, SAVANNAH, GA (GA077), with its own rates. Fort Stewart and Hinesville (31313) are in FORT STEWART, GA (GA080).')),
 dict(slug='fort-benning', name='Fort Benning', st='GA', mha='GA075', zip='31905', app='Fort Benning, GA', alias='Fort Moore',
      h1='BAH at Fort Benning (formerly Fort Moore), GA (2026)', title='Fort Benning BAH 2026 (formerly Fort Moore): Rates by Rank | PCS Vector',
      zipq=[('36867','GA075'),('36869','GA075')],
      aliasq=('Is Fort Moore BAH different from Fort Benning BAH?', f'No. Fort Moore was the post{R}s name from 2023 to 2025. Same post, same housing area (GA075), same rates. Columbus, GA and Phenix City, AL (36867, 36869) are both in it.')),
 dict(slug='joint-base-san-antonio', name='Joint Base San Antonio', st='TX', mha='TX285', zip='78234', app='Joint Base San Antonio, TX', alias='JBSA, Fort Sam Houston, Lackland, Randolph', desc_alias='JBSA',
      h1='BAH at Joint Base San Antonio (JBSA), TX (2026)', title='JBSA BAH 2026 (Joint Base San Antonio, Fort Sam Houston): Rates by Rank | PCS Vector',
      who='service members', zipq=[('78236','TX285'),('78150','TX285')],
      aliasq=('Do Fort Sam Houston, Lackland and Randolph all get the same BAH?', 'Yes. ZIPs 78234 (JBSA-Fort Sam Houston), 78236 (JBSA-Lackland) and 78150 (JBSA-Randolph) all map to the SAN ANTONIO, TX housing area (TX285), so all three use these rates.')),
 dict(slug='fort-riley', name='Fort Riley', st='KS', mha='KS100', zip='66442', app='Fort Riley, KS', alias=None,
      h1='BAH at Fort Riley, KS (2026)', title='Fort Riley BAH 2026 (Junction City, Manhattan): Rates by Rank | PCS Vector',
      zipq=[('66441','KS100'),('66502','KS100')],
      aliasq=('Do Junction City and Manhattan get the same BAH?', 'Yes. Junction City (66441) and Manhattan (66502) are both in the FORT RILEY, KS housing area (KS100). BAH follows your duty-station ZIP anyway, not the town you rent in.')),
 dict(slug='fort-knox', name='Fort Knox', st='KY', mha='KY110', zip='40121', app='Fort Knox, KY', alias=None,
      h1='BAH at Fort Knox, KY (2026)', title='Fort Knox BAH 2026 (Radcliff, Elizabethtown): Rates by Rank | PCS Vector',
      zipq=[('40160','KY110'),('42701','KY110')],
      aliasq=('Do Radcliff and Elizabethtown get the same BAH?', 'Yes. Radcliff (40160) and Elizabethtown (42701) are both in the FORT KNOX, KY housing area (KY110). BAH follows your duty-station ZIP anyway, not the town you rent in.')),
 dict(slug='fort-leonard-wood', name='Fort Leonard Wood', st='MO', mha='MO163', zip='65473', app='Fort Leonard Wood, MO', alias=None,
      h1='BAH at Fort Leonard Wood, MO (2026)', title='Fort Leonard Wood BAH 2026 (St. Robert, Waynesville): Rates by Rank | PCS Vector',
      zipq=[('65584','MO163'),('65583','MO163'),('65401','MO163')],
      aliasq=('Do St. Robert, Waynesville and Rolla get the same BAH?', 'Yes. St. Robert (65584), Waynesville (65583) and Rolla (65401) are all in the FORT LEONARD WOOD, MO housing area (MO163). BAH follows your duty-station ZIP anyway, not the town you rent in.')),
 dict(slug='fort-polk', name='Fort Polk', st='LA', mha='LA115', zip='71459', app='Fort Polk, LA', alias='Fort Johnson',
      h1='BAH at Fort Polk (formerly Fort Johnson), LA (2026)', title='Fort Polk BAH 2026 (formerly Fort Johnson): Rates by Rank | PCS Vector',
      zipq=[('71446','LA115'),('70634','LA115')],
      aliasq=('Is Fort Johnson BAH different from Fort Polk BAH?', f'No. Fort Johnson was the post{R}s name from 2023 to 2025. Same post, same housing area (LA115), same rates. Leesville (71446) and DeRidder (70634) are both in it.')),
 dict(slug='fort-sill', name='Fort Sill', st='OK', mha='OK237', zip='73503', app='Fort Sill, OK', alias=None,
      h1='BAH at Fort Sill, OK (2026)', title='Fort Sill BAH 2026 (Lawton): Rates by Rank | PCS Vector',
      zipq=[('73505','OK237')],
      aliasq=('Why does DTMO call it Fort Sill/Lawton?', 'DTMO sets BAH by Military Housing Area, and Fort Sill and the city of Lawton share one area, FORT SILL/LAWTON, OK (OK237). Lawton ZIPs such as 73505 use the same rates.')),
 dict(slug='fort-wainwright', name='Fort Wainwright', st='AK', mha='AK405', zip='99703', app='Fort Wainwright, AK', alias=None,
      h1='BAH at Fort Wainwright, AK (2026)', title='Fort Wainwright BAH 2026 (Fairbanks, Alaska): Rates by Rank | PCS Vector',
      zipq=[('99705','AK405'),('99702','AK405')], cola='Alaska',
      aliasq=('Why does DTMO call it Fairbanks?', 'DTMO sets BAH by Military Housing Area, and Fort Wainwright sits in the FAIRBANKS, AK area (AK405). North Pole (99705) and Eielson AFB (99702) are in the same area and use the same rates.')),
 dict(slug='fort-huachuca', name='Fort Huachuca', st='AZ', mha='AZ014', zip='85613', app='Fort Huachuca, AZ', alias=None,
      h1='BAH at Fort Huachuca, AZ (2026)', title='Fort Huachuca BAH 2026 (Sierra Vista): Rates by Rank | PCS Vector',
      zipq=[('85635','AZ014')],
      aliasq=('Is Fort Huachuca BAH the same in Sierra Vista?', 'Yes. Sierra Vista (85635) is in the FORT HUACHUCA, AZ housing area (AZ014). BAH follows your duty-station ZIP anyway, not the town you rent in.')),
 dict(slug='fort-irwin', name='Fort Irwin', st='CA', mha='CA028', zip='92310', app='Fort Irwin, CA', alias='National Training Center (NTC)',
      h1='BAH at Fort Irwin, CA (2026)', title='Fort Irwin BAH 2026 (Barstow, NTC): Rates by Rank | PCS Vector',
      zipq=[('92311','CA028')],
      aliasq=('Why does DTMO call it Barstow/Fort Irwin?', 'DTMO places Fort Irwin and the National Training Center in the BARSTOW/FORT IRWIN, CA housing area (CA028), so Barstow (92311) rentals use the same rates.')),
 dict(slug='schofield-barracks', name='Schofield Barracks', st='HI', mha='HI408', zip='96857', app='Schofield Barracks, HI', alias=None,
      h1='BAH at Schofield Barracks, HI (2026)', title='Schofield Barracks BAH 2026 (Oahu, Hawaii): Rates by Rank | PCS Vector',
      zipq=[('96786','HI408'),('96858','HI408'),('96853','HI408'),('96860','HI408'),('96863','HI408')], cola='Hawaii',
      aliasq=('Do all Oahu posts get the same BAH?', 'Yes. Schofield Barracks (96857), Wahiawa (96786), Fort Shafter (96858), Joint Base Pearl Harbor-Hickam (96853, 96860) and Marine Corps Base Hawaii (96863) all map to HONOLULU COUNTY, HI (HI408).')),
]
def row(f, mha):
    for l in open(D + f):
        p = l.strip().split(',')
        if p[0] == mha:
            assert len(p) == 28
            return dict(zip(COLS, [int(float(x)) for x in p[1:]]))
    raise KeyError(mha)
names = dict(l.strip().split(';', 1) for l in open(D + 'mhanames26.txt') if ';' in l)
zipmap = [l.split() for l in open(D + 'sorted_zipmha26.txt') if len(l.split()) == 2]
rent = json.load(open(REPO + 'data/local_costs_2026.json'))['installations']
calc_posts = json.load(open(OUT + 'assets/calc-data.json'))['posts']
for B in NEW:
    m = B['mha']
    B.update(W=row('bahw26.txt', m), WO=row('bahwo26.txt', m), area=names[m], zips=[z for z, mm in zipmap if mm == m])
    lc = rent[B['app']]; ut = U.get_utility_costs_for_installation(B['app']); ar = ut['areas'][0]
    B.update(rent=lc['rent_3br'], util=(ar['total_utilities_usd_mo']['low'], ar['total_utilities_usd_mo']['high']), util_area=ar['name'], util_note=ar.get('season_note', ''), util_asof=ut.get('as_of', ''))
    B['cost'] = (B['rent'][0] + B['util'][0], B['rent'][1] + B['util'][1])
    B['gap'] = {c: (B['W'][c] - B['cost'][1], B['W'][c] - B['cost'][0]) for c in GAP_RANKS}
    B['post'] = B['app'] if B['app'] in calc_posts else None
# existing pages (names read from their H1/breadcrumb) for the "Other posts" list
existing = []
for s in sorted(os.listdir(OUT + 'bah')):
    f = OUT + f'bah/{s}/index.html'
    if os.path.isdir(OUT + f'bah/{s}') and s not in [B['slug'] for B in NEW]:
        existing.append((s, re.search(r'"position": 3, "name": "(.*?)"', open(f).read()).group(1)))
HUB_ORDER = ['fort-bragg','fort-hood','fort-campbell','fort-carson','joint-base-lewis-mcchord','fort-drum','fort-bliss','national-capital-region']
existing.sort(key=lambda x: HUB_ORDER.index(x[0]) if x[0] in HUB_ORDER else 99)
ALL = existing + [(B['slug'], B['name']) for B in NEW]
e = lambda s: html.escape(s)
def money(v): return ('\u2212$' if v < 0 else '$') + f'{abs(v):,}'
def cta(B, medium='organic'):
    pre = ('tgt=' + quote_plus(B['post']) + '&amp;') if B['post'] else ''
    return f'/?{pre}utm_source=bahpage&amp;utm_medium={medium}&amp;utm_campaign={B["slug"]}' + ('#find-a-home' if medium == 'agents' else '')
TPL = open(OUT + 'bah/fort-bragg/index.html').read()
CSS = re.search(r'<style>(.*?)</style>', TPL, re.S).group(1)
def head(title, desc, url, ld):
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<link rel="icon" href="/favicon.ico" sizes="any"><link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="icon" href="/favicon-48x48.png" type="image/png" sizes="48x48"><link rel="icon" href="/favicon-192x192.png" type="image/png" sizes="192x192"><link rel="apple-touch-icon" href="/apple-touch-icon.png" sizes="180x180"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website"><meta property="og:site_name" content="PCS Vector">
<meta property="og:title" content="{e(title.split(' | ')[0])}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta name="twitter:card" content="summary">
<style>{CSS}</style>
{''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld)}
<script data-goatcounter="https://pcsvector.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>
</head><body><main>'''
FOOT = '''<p class="src">PCS Vector is an independent planning tool built by Soldiers. It is not an official Army, DoW or DTMO site. Confirm your rate with your finance office. Page updated Oct 2026.</p>
</main></body></html>
'''
for B in NEW:
    s, n, W, WO = B['slug'], B['name'], B['W'], B['WO']
    url = f'https://pcsvector.com/bah/{s}/'
    alias = f' (also {B.get("desc_alias", B["alias"])})' if B['alias'] else ''
    desc = f'2026 BAH at {n}{alias} for every pay grade, with and without dependents, vs local rent and utilities. Official DTMO rates.'
    faqs = [B['aliasq']]
    if B.get('cola'): faqs.append(COLA_Q(n, B['cola']))
    faqs += [(f'Does 2026 BAH at {n} cover rent and utilities?', f'It depends on rank. With avg 3-bedroom rent of ${B["rent"][0]:,}\u2013${B["rent"][1]:,} and utilities of about ${B["util"][0]:,}\u2013${B["util"][1]:,} a month, a Sergeant (E-5) with dependents (${W["E5"]:,}) lands between {money(B["gap"]["E5"][0])} and {money(B["gap"]["E5"][1])} a month after housing. These are planning estimates, not official figures.'),
             ('Do I get a different rate if I live in a nearby town?', 'No. BAH follows your permanent duty-station ZIP, not your home address.'),
             ('When do these rates apply?', f'These are the calendar-year 2026 rates. Rate protection keeps your rate from dropping while you stay at the same post with the same status; a PCS, a reduction in grade or a change in dependency status resets it. DTMO usually publishes the next year{R}s rates in mid-December.')]
    ld = [{"@context": "https://schema.org", "@type": "WebPage", "name": B['title'].split(' | ')[0], "url": url, "dateModified": TODAY, "isBasedOn": "https://www.travel.dod.mil/Allowances/Basic-Allowance-for-Housing/BAH-Rate-Lookup/"},
          {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "PCS Vector", "item": "https://pcsvector.com/"}, {"@type": "ListItem", "position": 2, "name": "BAH by post", "item": "https://pcsvector.com/bah/"}, {"@type": "ListItem", "position": 3, "name": n, "item": url}]},
          {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}]
    p = [head(B['title'], desc, url, ld)]
    p.append(f'<nav class="crumb"><a href="/">PCS Vector</a> \u203a <a href="/bah/">BAH by post</a> \u203a {e(n)}</nav>')
    p.append(f'<div class="kick">Military-approved agents \u00b7 {e(n)}, {B["st"]}</div>')
    p.append(f'<h1>{e(B["h1"])}</h1>')
    aka = f' (also searched as {e(B["alias"])})' if B['alias'] else ''
    p.append(f'<p>Monthly Basic Allowance for Housing for {B.get("who", "Soldiers")} stationed at {e(n)}{aka}. DTMO lists this housing area as <strong>{e(B["area"])}</strong> (code {B["mha"]}). Your rate depends on three things only: pay grade, with or without dependents, and your duty-station ZIP. Where you choose to live does not change it.</p>')
    p.append(f'<a class="cta" href="{cta(B)}">Compare {e(n)} with your current post (free calculator) \u2192</a>')
    p.append(f'<h2>2026 {e(n)} BAH by pay grade</h2>')
    p.append(f'<p class="note">Calendar-year 2026 rates (effective 1 Jan 2026). Rates checked against DTMO {CHECKED}.</p>')
    p.append('<div class="tw"><table><thead><tr><th>Grade</th><th>Rank</th><th>With dependents</th><th>Without</th></tr></thead><tbody>' + ''.join(f'<tr><td>{g(c)}</td><td>{e(TITLES[c])}</td><td>${W[c]:,}</td><td>${WO[c]:,}</td></tr>' for c in G24) + '</tbody></table></div>')
    p.append('<p class="note">\u201cWith dependents\u201d is yes or no: one child and four children get the same rate. O-1E to O-3E are officers with more than four years of prior enlisted or warrant service.</p>')
    if B.get('cola'):
        p.append(f'<p class="note">{B["cola"]} duty stations also get a cost-of-living allowance (COLA) on top of BAH. It is not included in this table; the calculator adds it.</p>')
    p.append(f'<h2>BAH vs rent and utilities at {e(n)}</h2>')
    p.append(f'<p>BAH is a flat monthly amount; rent and utilities are not. Avg off-post <strong>3-bedroom rent</strong> near {e(n)} runs about <strong>${B["rent"][0]:,}\u2013${B["rent"][1]:,}/month</strong>, and utilities for that home (electric, heat, water/trash, internet; {e(B["util_area"])}) run about <strong>${B["util"][0]:,}\u2013${B["util"][1]:,}/month</strong>. That puts all-in housing at roughly <strong>${B["cost"][0]:,}\u2013${B["cost"][1]:,}/month</strong>.</p>')
    p.append('<div class="tw"><table class="gap"><thead><tr><th>Grade</th><th>BAH (with dep.)</th><th>Left after rent + utilities</th></tr></thead><tbody>' + ''.join(f'<tr><td>{g(c)} {e(TITLES[c].split(" /")[0])}</td><td>${W[c]:,}</td><td>{money(B["gap"][c][0])} to {money(B["gap"][c][1])}</td></tr>' for c in GAP_RANKS) + '</tbody></table></div>')
    p.append(f'<p class="note"><strong>Gap note:</strong> a negative number means out-of-pocket each month at the high end of the local market; a positive number means BAH covers it with money left over. {e(B["util_note"])} Rent and utility ranges are PCS Vector planning estimates (rent as of Sep 2026; utilities: {e(B["util_asof"])}), not DTMO figures. DTMO itself says BAH is not meant to cover every housing cost.</p>')
    p.append(f'<a class="cta" href="{cta(B)}">See your exact rent gap for your rank and family size \u2192</a>')
    p.append(f'<h2>ZIP codes in the {e(n)} housing area ({len(B["zips"])})</h2><p class="zips">{" ".join(B["zips"])}</p>')
    p.append('<h2>Quick answers</h2>' + ''.join(f'<h3>{e(q)}</h3><p>{e(a)}</p>' for q, a in faqs))
    p.append(f'<section class="agents"><h2>Military-approved agents at {e(n)}</h2><p>Want local help finding a place that fits your BAH? PCS Vector can connect you with one of our <strong>military-approved agents</strong>: local housing agents at your new duty station. The intro is free and does not change your BAH.</p><a class="cta cta2" href="{cta(B, "agents")}">Run your numbers and get a free intro to a military-approved agent \u2192</a></section>')
    p.append('<h2>Other posts</h2><ul class="bases">' + ''.join(f'<li><a href="/bah/{os_}/">{e(on)}</a></li>' for os_, on in ALL if os_ != s) + '</ul>')
    p.append(f'<p class="src">Source: Defense Travel Management Office (DTMO), 2026 BAH rates, all locations and all pay grades (ASCII rate file, MHA {B["mha"]}, downloaded 4 Oct 2026); checked against DTMO{R}s 2026 PDF rate tables and the DTMO BAH Rate Lookup for ZIP {B["zip"]} on {CHECKED}.</p>')
    p.append(FOOT)
    os.makedirs(OUT + f'bah/{s}', exist_ok=True)
    open(OUT + f'bah/{s}/index.html', 'w').write('\n'.join(p))
# hub: append rows (idempotent), bump dateModified + source line
bh = OUT + 'bah/index.html'; t = open(bh).read()
rows = ''.join(f'<tr><td><a href="/bah/{B["slug"]}/">{e(B["name"])}</a></td><td>{B["mha"]}</td><td>${B["W"]["E5"]:,}</td><td>${B["WO"]["E5"]:,}</td><td>${B["cost"][0]:,}\u2013${B["cost"][1]:,}</td></tr>' for B in NEW if f'href="/bah/{B["slug"]}/"' not in t)
if rows:
    i = t.index('</tbody></table></div>'); t = t[:i] + rows + t[i:]
t = t.replace('"url": "https://pcsvector.com/bah/", "dateModified": "2026-10-11"', f'"url": "https://pcsvector.com/bah/", "dateModified": "{TODAY}"')
old_src = '<p class="src">Source: DTMO 2026 BAH rates (ASCII and PDF rate tables) and the DTMO BAH Rate Lookup, checked 11 Oct 2026.</p>'
if old_src in t: t = t.replace(old_src, f'<p class="src">Source: DTMO 2026 BAH rates (ASCII and PDF rate tables) and the DTMO BAH Rate Lookup, checked 11 Oct 2026 (Fort Stewart through Schofield Barracks: checked {CHECKED}).</p>')
open(bh, 'w').write(t)
# sitemap
sm = OUT + 'sitemap.xml'; t = open(sm).read()
t = re.sub(r'(<loc>https://pcsvector.com/bah/</loc><lastmod>)[\d-]+(</lastmod>)', rf'\g<1>{TODAY}\g<2>', t)
add = ''.join(f'  <url><loc>https://pcsvector.com/bah/{B["slug"]}/</loc><lastmod>{TODAY}</lastmod></url>\n' for B in NEW if f'<loc>https://pcsvector.com/bah/{B["slug"]}/</loc>' not in t)
t = t.replace('</urlset>', add + '</urlset>'); open(sm, 'w').write(t)
json.dump({B['slug']: {'mha': B['mha'], 'area': B['area'], 'zip': B['zip'], 'post': B['post'], 'W': B['W'], 'WO': B['WO'], 'rent': B['rent'], 'util': B['util'], 'cost': B['cost'], 'gap': B['gap'], 'nzips': len(B['zips']), 'zipq': B['zipq']} for B in NEW}, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bases_built.json'), 'w'), indent=1)
print('built', [B['slug'] for B in NEW], 'calc posts missing:', [B['slug'] for B in NEW if not B['post']])
