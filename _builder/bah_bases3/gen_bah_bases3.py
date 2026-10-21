"""PCS Vector: 7 batch-3 BAH base pages (static), same format as /bah/fort-bragg/. UNOFFICIAL / PERSONAL.
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
TODAY = '2026-10-20'; CHECKED = '20 Oct 2026'
COLS = ['E1','E2','E3','E4','E5','E6','E7','E8','E9','W1','W2','W3','W4','W5','O1E','O2E','O3E','O1','O2','O3','O4','O5','O6','O7','O8','O9','O10']
G24 = COLS[:24]
TITLES = {'E1':'Private (PV1)','E2':'Private (PV2)','E3':'Private First Class','E4':'Specialist / Corporal','E5':'Sergeant','E6':'Staff Sergeant','E7':'Sergeant First Class','E8':'Master Sgt / First Sgt','E9':'Sergeant Major','W1':'Warrant Officer 1','W2':'Chief Warrant Officer 2','W3':'Chief Warrant Officer 3','W4':'Chief Warrant Officer 4','W5':'Chief Warrant Officer 5','O1E':'2LT, 4+ yrs prior enlisted/WO','O2E':'1LT, 4+ yrs prior enlisted/WO','O3E':'CPT, 4+ yrs prior enlisted/WO','O1':'Second Lieutenant','O2':'First Lieutenant','O3':'Captain','O4':'Major','O5':'Lieutenant Colonel','O6':'Colonel','O7':'Brigadier General and up'}
GAP_RANKS = ['E4','E5','E6','E7','W2','O3']
def g(c): return c[0] + '-' + c[1:]
R = '\u2019'
COLA_Q = lambda n, st: (f'Do I get COLA on top of BAH at {n}?', f'Yes. {st} duty stations get BAH plus a cost-of-living allowance (COLA), which DTMO sets separately by rank, years of service and dependents. This page shows BAH only; the calculator adds COLA for {n}.')
NEW = [
 dict(slug='fort-gordon', name='Fort Gordon', st='GA', mha='GA073', zip='30905', app='Fort Gordon, GA', alias='Fort Eisenhower',
      h1='BAH at Fort Gordon (formerly Fort Eisenhower), GA (2026)', title='Fort Gordon BAH 2026 (formerly Fort Eisenhower, Augusta): Rates by Rank | PCS Vector',
      zipq=[('30907','GA073'),('30809','GA073'),('29841','GA073')],
      aliasq=('Is Fort Eisenhower BAH different from Fort Gordon BAH?', f'No. Fort Eisenhower was the post{R}s name from 2023 to 2025. Same post, same housing area (GA073), same rates. Augusta (30907), Evans (30809) and North Augusta, SC (29841) are all in it. DTMO{R}s rate file labels this area FORT GORDON, AL; the DTMO BAH Rate Lookup shows FORT GORDON, GA. Same code, same rates.')),
 dict(slug='fort-jackson', name='Fort Jackson', st='SC', mha='SC260', zip='29207', app='Fort Jackson, SC', alias=None,
      h1='BAH at Fort Jackson, SC (2026)', title='Fort Jackson BAH 2026 (Columbia, SC): Rates by Rank | PCS Vector',
      zipq=[('29229','SC260'),('29223','SC260')],
      aliasq=('Why does DTMO call it Columbia/Fort Jackson?', 'DTMO sets BAH by Military Housing Area, and Fort Jackson shares one area with the city of Columbia: COLUMBIA/FORT JACKSON, SC (SC260). Northeast Columbia ZIPs such as 29229 and 29223 use the same rates.')),
 dict(slug='fort-rucker', name='Fort Rucker', st='AL', mha='AL002', zip='36362', app='Fort Rucker, AL', alias='Fort Novosel',
      h1='BAH at Fort Rucker (formerly Fort Novosel), AL (2026)', title='Fort Rucker BAH 2026 (formerly Fort Novosel, Enterprise): Rates by Rank | PCS Vector',
      zipq=[('36330','AL002'),('36360','AL002'),('36301','AL002')],
      aliasq=('Is Fort Novosel BAH different from Fort Rucker BAH?', f'No. Fort Novosel was the post{R}s name from 2023 to 2025. Same post, same housing area (AL002), same rates. Enterprise (36330), Ozark (36360) and Dothan (36301) are all in it.')),
 dict(slug='fort-lee', name='Fort Lee', st='VA', mha='VA301', zip='23801', app='Fort Lee, VA', alias='Fort Gregg-Adams',
      h1='BAH at Fort Lee (formerly Fort Gregg-Adams), VA (2026)', title='Fort Lee BAH 2026 (formerly Fort Gregg-Adams, Petersburg): Rates by Rank | PCS Vector',
      zipq=[('23805','VA301'),('23860','VA301'),('23803','VA301')],
      aliasq=('Is Fort Gregg-Adams BAH different from Fort Lee BAH?', f'No. Fort Gregg-Adams was the post{R}s name from 2023 to 2025. Same post, same housing area (VA301), same rates. Petersburg (23805, 23803) and Hopewell (23860) are in it; DTMO calls the area RICHMOND/FORT LEE, VA.')),
 dict(slug='joint-base-langley-eustis', name='Joint Base Langley-Eustis', st='VA', mha='VA297', zip='23604', app='Joint Base Langley-Eustis, VA', alias='Fort Eustis', desc_alias='Fort Eustis',
      h1='BAH at Joint Base Langley-Eustis (Fort Eustis), VA (2026)', title='Fort Eustis BAH 2026 (Joint Base Langley-Eustis, Newport News): Rates by Rank | PCS Vector',
      who='service members', zipq=[('23665','VA297'),('23606','VA297'),('23185','VA297')],
      aliasq=('Do Fort Eustis and Langley get the same BAH?', 'Yes. Fort Eustis (23604) and Langley (23665) both map to the HAMPTON/NEWPORT NEWS, VA housing area (VA297), as do Newport News (23606) and Williamsburg (23185).')),
 dict(slug='fort-leavenworth', name='Fort Leavenworth', st='KS', mha='KS102', zip='66027', app='Fort Leavenworth, KS', alias=None,
      h1='BAH at Fort Leavenworth, KS (2026)', title='Fort Leavenworth BAH 2026 (Leavenworth, Kansas City area): Rates by Rank | PCS Vector',
      zipq=[('66048','KS102'),('64079','KS102')],
      aliasq=('Do Leavenworth and Platte City get the same BAH?', 'Yes. The city of Leavenworth (66048) and Platte City, MO (64079) are both in the FORT LEAVENWORTH, KS housing area (KS102). BAH follows your duty-station ZIP anyway, not the town you rent in.')),
 dict(slug='joint-base-elmendorf-richardson', name='Joint Base Elmendorf-Richardson', st='AK', mha='AK404', zip='99506', app='Joint Base Elmendorf-Richardson, AK', alias='JBER, Fort Richardson', desc_alias='JBER',
      h1='BAH at Joint Base Elmendorf-Richardson (JBER), AK (2026)', title='JBER BAH 2026 (Joint Base Elmendorf-Richardson, Anchorage): Rates by Rank | PCS Vector',
      who='service members', zipq=[('99505','AK404'),('99501','AK404'),('99577','AK404'),('99654','AK404')], cola='Alaska',
      aliasq=('Why does DTMO call it Anchorage?', 'DTMO sets BAH by Military Housing Area, and JBER (99506, 99505) sits in the ANCHORAGE, AK area (AK404). Anchorage (99501), Eagle River (99577) and Wasilla (99654) are in the same area and use the same rates.')),
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
old_src = '(Fort Stewart through Schofield Barracks: checked 19 Oct 2026)'
if old_src in t and 'Fort Gordon through' not in t: t = t.replace(old_src, f'(Fort Stewart through Schofield Barracks: checked 19 Oct 2026; Fort Gordon through JBER: checked {CHECKED})')
open(bh, 'w').write(t)
# sitemap
sm = OUT + 'sitemap.xml'; t = open(sm).read()
t = re.sub(r'(<loc>https://pcsvector.com/bah/</loc><lastmod>)[\d-]+(</lastmod>)', rf'\g<1>{TODAY}\g<2>', t)
add = ''.join(f'  <url><loc>https://pcsvector.com/bah/{B["slug"]}/</loc><lastmod>{TODAY}</lastmod></url>\n' for B in NEW if f'<loc>https://pcsvector.com/bah/{B["slug"]}/</loc>' not in t)
t = t.replace('</urlset>', add + '</urlset>'); open(sm, 'w').write(t)
json.dump({B['slug']: {'mha': B['mha'], 'area': B['area'], 'zip': B['zip'], 'post': B['post'], 'W': B['W'], 'WO': B['WO'], 'rent': B['rent'], 'util': B['util'], 'cost': B['cost'], 'gap': B['gap'], 'nzips': len(B['zips']), 'zipq': B['zipq']} for B in NEW}, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bases_built3.json'), 'w'), indent=1)
print('built', [B['slug'] for B in NEW], 'calc posts missing:', [B['slug'] for B in NEW if not B['post']])
