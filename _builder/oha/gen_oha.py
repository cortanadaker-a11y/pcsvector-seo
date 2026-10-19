"""PCS Vector: OHA hub + country pages (static). UNOFFICIAL / PERSONAL.
Data: live DTMO OHA pull (neorates, pay period 16 Oct 2026) in dtmo_oha_live_2026-10-19.json.
Usage: python3 gen_oha.py <site_root> <dtmo_json>"""
import json, html, os, re, sys, datetime
from urllib.parse import quote_plus
OUT = sys.argv[1].rstrip('/') + '/'; SRC = json.load(open(sys.argv[2]))
TODAY = '2026-10-19'; CHECKED = '19 Oct 2026'
GR = ['E-1','E-2','E-3','E-4','E-5','E-6','E-7','E-8','E-9','W-1','W-2','W-3','W-4','W-5','O-1E','O-2E','O-3E','O-1','O-2','O-3','O-4','O-5','O-6','O-7']
TITLES = {'E-1':'Private (PV1)','E-2':'Private (PV2)','E-3':'Private First Class','E-4':'Specialist / Corporal','E-5':'Sergeant','E-6':'Staff Sergeant','E-7':'Sergeant First Class','E-8':'Master Sgt / First Sgt','E-9':'Sergeant Major','W-1':'Warrant Officer 1','W-2':'Chief Warrant Officer 2','W-3':'Chief Warrant Officer 3','W-4':'Chief Warrant Officer 4','W-5':'Chief Warrant Officer 5','O-1E':'2LT, 4+ yrs prior enlisted/WO','O-2E':'1LT, 4+ yrs prior enlisted/WO','O-3E':'CPT, 4+ yrs prior enlisted/WO','O-1':'Second Lieutenant','O-2':'First Lieutenant','O-3':'Captain','O-4':'Major','O-5':'Lieutenant Colonel','O-6':'Colonel','O-7':'Brigadier General'}
CUR = {'KR': ('KRW', '\u20a9', 0), 'JP': ('JPY', '\u00a5', 0), 'DE': ('EUR', '\u20ac', 0)}
# locality -> (display name, area label, calculator post name or None)
LOC = {
 'KR025': ('Camp Humphreys', 'Camp Humphreys (Pyeongtaek)', 'Camp Humphreys, South Korea'),
 'KR177': ('Camp Casey', 'Camp Casey (Dongducheon)', 'Camp Casey, South Korea'),
 'JP045': ('Camp Zama', 'Camp Zama', 'Camp Zama, Japan'),
 'JP065': ('Yokota', 'Yokota Air Base', None),
 'JP061': ('Yokosuka', 'Yokosuka', None),
 'JP027': ('Okinawa', 'Okinawa', None),
 'DE355': ('Wiesbaden', 'USAG Wiesbaden', 'USAG Wiesbaden, Germany'),
 'DE231': ('Grafenwoehr / Vilseck', 'USAG Bavaria (Grafenwoehr, Vilseck)', 'USAG Bavaria, Germany'),
 'DE700': ('Kaiserslautern', 'Kaiserslautern Military Community (USAG Rheinland-Pfalz)', 'USAG Rheinland-Pfalz, Germany'),
 'DE055': ('Stuttgart', 'Stuttgart Military Community (USAG Stuttgart)', None),
 'DE228': ('Ansbach', 'USAG Ansbach', None),
}
PAGES = [
 dict(slug='korea', name='South Korea', locs=['KR025','KR177'], h1='OHA in South Korea: Camp Humphreys and Camp Casey (2026)',
      title='Korea OHA 2026: Camp Humphreys & Camp Casey Rent Ceilings by Rank | PCS Vector',
      desc='2026 OHA rent ceilings for Camp Humphreys and Camp Casey, every rank, with and without dependents, plus utility and move-in allowance. DTMO rates, 16 Oct 2026.',
      intro='Overseas Housing Allowance for Soldiers who rent off post in South Korea. DTMO sets a separate OHA locality for each area: Camp Humphreys falls under OSAN AB (INCL CAMP HUMPHREYS) and Camp Casey under DONGDUCHEON (INCL CAMP CASEY).',
      extra=('Do Camp Humphreys and Osan AB get the same OHA?', 'Yes. DTMO puts Camp Humphreys in the OSAN AB (INCL CAMP HUMPHREYS) locality (KR025), so the same rent ceilings and utility allowance apply. Camp Casey is a different locality, DONGDUCHEON (INCL CAMP CASEY) (KR177), with lower ceilings.')),
 dict(slug='japan', name='Japan (mainland)', locs=['JP045','JP065','JP061'], h1='OHA in Japan: Camp Zama, Yokota and Yokosuka (2026)',
      title='Japan OHA 2026: Camp Zama, Yokota & Yokosuka Rent Ceilings by Rank | PCS Vector',
      desc='2026 OHA rent ceilings for Camp Zama, Yokota and Yokosuka, every rank, with and without dependents, plus utility and move-in allowance. DTMO rates, 16 Oct 2026.',
      intro='Overseas Housing Allowance for service members who rent off post on mainland Japan. Each area has its own DTMO OHA locality: CAMP ZAMA (KA), YOKOTA (TO) and YOKOSUKA (KA). Okinawa has its own page.',
      extra=('Is the Japan utility allowance the same at every base?', 'For these three localities, yes as of this pay period: DTMO lists the same utility/recurring maintenance allowance and the same move-in housing allowance for Camp Zama, Yokota and Yokosuka. Rent ceilings differ by locality and grade.')),
 dict(slug='okinawa', name='Okinawa', locs=['JP027'], h1='OHA on Okinawa, Japan (2026)',
      title='Okinawa OHA 2026: Rent Ceilings by Rank (Japan) | PCS Vector',
      desc='2026 Okinawa OHA rent ceilings for every rank, with and without dependents, plus utility and move-in allowance, in yen and dollars. DTMO rates, 16 Oct 2026.',
      intro='Overseas Housing Allowance for service members who rent off post on Okinawa. DTMO\u2019s OHA locality is OKINAWA (OK), code JP027. Confirm your locality with your housing office before you sign a lease.',
      extra=('Is Okinawa OHA higher than mainland Japan?', 'At this pay period the Okinawa rent ceilings are higher than Camp Zama, Yokota and Yokosuka for the same grade; the utility allowance is the same. See the Japan page for the mainland localities.')),
 dict(slug='germany', name='Germany', locs=['DE355','DE231','DE700','DE055','DE228'], h1='OHA in Germany: Wiesbaden, Grafenwoehr/Vilseck, Kaiserslautern, Stuttgart, Ansbach (2026)',
      title='Germany OHA 2026: Wiesbaden, Grafenwoehr, Stuttgart & More by Rank | PCS Vector',
      desc='2026 Germany OHA rent ceilings by rank for Wiesbaden, Grafenwoehr/Vilseck, Kaiserslautern, Stuttgart and Ansbach, plus utilities. DTMO rates, 16 Oct 2026.',
      intro='Overseas Housing Allowance for Soldiers who rent off post in Germany. DTMO sets ceilings in euros for each OHA locality: WIESBADEN (H), VILSECK/GRAFENWOEHR, KAISERSLAUTERN MILITARY COMMUNITY (RP), STUTTGART MILITARY COMMUNITY (BW) and ANSBACH (B).',
      extra=('Do Grafenwoehr and Vilseck get the same OHA?', 'Yes. DTMO uses one locality, VILSECK/GRAFENWOEHR (DE231), for both. Other Bavarian areas such as Ansbach (DE228) have their own ceilings.')),
]
e = lambda s: html.escape(s, quote=True)
def clean_loc(s): return re.sub(r'\s*\d+/\s*$|\s*/\d+\s*$', '', s).strip()
def usd(v): return f'${v:,.2f}'
def loc_money(code, v):
    c, sym, _ = CUR[code[:2]]; return f'{sym}{int(v + 0.5):,}'
def roe(code): return float(SRC[code]['with']['E-5']['roe'].split('/')[0])
def fx_txt(code):
    c = CUR[code[:2]][0]; r = roe(code)
    return f'1 USD = {r:,.4f} {c}' if r < 10 else f'1 USD = {r:,.2f} {c}'
def eff(code): d = SRC[code]['with']['E-5']['eff']; return datetime.date(int(d[:4]), int(d[4:6]), int(d[6:]))
def dfmt(d): return f'{d.day} {d:%b %Y}'
def rec(code, k, g): return SRC[code][k][g]
def calc(post, slug, medium='organic'):
    pre = ('tgt=' + quote_plus(post) + '&amp;') if post else ''
    return f'/?{pre}utm_source=ohapage&amp;utm_medium={medium}&amp;utm_campaign={slug}' + ('#find-a-home' if medium == 'agents' else '')
CSS = re.search(r'<style>(.*?)</style>', open(OUT + 'bah/fort-bragg/index.html').read(), re.S).group(1)
CSS += '.stamp{display:inline-block;background:var(--card);border:1px solid #2c3f34;border-radius:8px;padding:4px 10px;font-size:.85rem;color:var(--mute)}\n.loc{color:var(--mute);font-size:.8rem}\n'
def head(title, desc, url, ld):
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<link rel="icon" href="/favicon.svg" type="image/svg+xml"><meta name="viewport" content="width=device-width, initial-scale=1">
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
</head><body><main>'''
FOOT = '''<p class="src">PCS Vector is an independent planning tool built by Soldiers. It is not an official Army, DoD or DTMO site. Confirm your rate with your finance office. Page updated Oct 2026.</p>
</main></body></html>
'''
DTMO_URL = 'https://www.travel.dod.mil/Allowances/Overseas-Housing-Allowance/OHA-Rate-Lookup/'
HOW = ('<h2>How OHA works</h2><p>OHA has three parts. <strong>Rent:</strong> you are reimbursed your actual monthly rent, up to a <strong>rent ceiling</strong> set by DTMO for your grade, '
       'dependency status and locality. <strong>Utilities:</strong> a flat monthly <strong>utility/recurring maintenance allowance</strong> for the locality, paid on top of rent. '
       '<strong>Move-in:</strong> a one-time <strong>Move-In Housing Allowance (MIHA)</strong> toward the costs of setting up a private rental.</p>'
       '<p>Ceilings are set in the local currency. Your rent is in local currency, and finance converts it to dollars at the DTMO exchange rate, so the dollar amount moves with the exchange rate even when your rent does not. '
       'DTMO can update exchange rates and OHA rates every pay period, on the 1st and 16th of each month. Members without dependents get 90% of the with-dependents rent ceiling and 75% of the utility allowance.</p>')
def sources(codes):
    parts = []
    for c in codes:
        parts.append(f'{clean_loc(rec(c,"with","E-5")["loc"])} ({c}) effective {dfmt(eff(c))}, {fx_txt(c)}')
    return (f'<p class="src">Source: Defense Travel Management Office (DTMO) OHA Rate Lookup, queried for the pay period starting 16 Oct 2026 '
            f'(rates as of 16 Oct 2026; DTMO effective dates: {e("; ".join(parts))}). Rates checked {CHECKED}. '
            f'Official lookup: <a href="{DTMO_URL}">DTMO OHA Rate Lookup</a>.</p>')
def section(code, slug):
    nm, area, post = LOC[code]; W = SRC[code]['with']; WO = SRC[code]['without']; c3 = CUR[code[:2]][0]
    p = [f'<h2 id="{code.lower()}">{e(area)} OHA by pay grade</h2>',
         f'<p class="loc">DTMO locality: {e(clean_loc(W["E-5"]["loc"]))} ({code}) \u00b7 ceilings in {c3} \u00b7 {fx_txt(code)} \u00b7 effective {dfmt(eff(code))}</p>']
    p.append('<div class="tw"><table><thead><tr><th>Grade</th><th>Rank</th><th>Rent ceiling, with dependents</th><th>Rent ceiling, without</th></tr></thead><tbody>' +
             ''.join(f'<tr data-g="{g}"><td>{g}</td><td>{e(TITLES[g])}</td><td>{usd(W[g]["rent"])} <span class="loc">{loc_money(code, W[g]["rent_local"])}</span></td><td>{usd(WO[g]["rent"])} <span class="loc">{loc_money(code, WO[g]["rent_local"])}</span></td></tr>' for g in GR) +
             '</tbody></table></div>')
    u, uo = W['E-5'], WO['E-5']
    p.append(f'<div class="tw"><table class="gap"><thead><tr><th>Allowance (monthly unless noted)</th><th>With dependents</th><th>Without</th></tr></thead><tbody>'
             f'<tr data-k="util"><td>Utility / recurring maintenance</td><td>{usd(u["util"])} <span class="loc">{loc_money(code, u["util_local"])}</span></td><td>{usd(uo["util"])} <span class="loc">{loc_money(code, uo["util_local"])}</span></td></tr>'
             f'<tr data-k="miha"><td>Move-In Housing Allowance (one-time)</td><td>{usd(u["miha"])} <span class="loc">{loc_money(code, u["miha_local"])}</span></td><td>\u2014</td></tr></tbody></table></div>')
    p.append(f'<p class="note">Example: a Sergeant (E-5) with dependents at {e(nm)} can receive up to <strong>{usd(round(u["rent"] + u["util"], 2))}/month</strong> ({usd(u["rent"])} rent ceiling + {usd(u["util"])} utilities), if rent is at or above the ceiling. '
             'The MIHA figure is what DTMO\u2019s calculator shows for a member with dependents; DTMO did not return a MIHA figure for the without-dependents query, so check with your housing office. Dollar figures are DTMO\u2019s conversion at the rate shown; local-currency amounts are rounded to whole units.</p>')
    if post:
        p.append(f'<a class="cta" href="{calc(post, slug)}">See {e(nm)} OHA, COLA and costs for your rank (free calculator) \u2192</a>')
    return p
def faqs_for(P):
    c0 = P['locs'][0]; nm = LOC[c0][0]; u = rec(c0, 'with', 'E-5'); uo = rec(c0, 'without', 'E-5')
    return [(f'How much OHA does an E-5 get at {nm}?', f'As of 16 Oct 2026 DTMO lists a rent ceiling of {usd(u["rent"])} ({loc_money(c0, u["rent_local"])}) for a Sergeant (E-5) with dependents and {usd(uo["rent"])} without, plus a utility allowance of {usd(u["util"])} with dependents and {usd(uo["util"])} without. With dependents that is up to {usd(round(u["rent"] + u["util"], 2))} a month.'),
            P['extra'],
            ('Why does my OHA change in dollars when my rent stays the same?', 'Ceilings and your lease are in local currency. Finance pays you in dollars at the DTMO exchange rate, which DTMO can update every pay period (the 1st and 16th), so the dollar amount rises or falls with the exchange rate.'),
            ('Do Soldiers without dependents get OHA?', 'Yes, if they are authorized to live off post. The without-dependents rent ceiling is 90% of the with-dependents ceiling and the utility allowance is 75%. Soldiers in government quarters or the barracks do not get OHA.')]
def page(P):
    s, n = P['slug'], P['name']; url = f'https://pcsvector.com/oha/{s}/'
    faqs = faqs_for(P);     desc = P['desc']; assert 50 <= len(desc) <= 165, (s, len(desc))
    ld = [{"@context": "https://schema.org", "@type": "WebPage", "name": P['title'].split(' | ')[0], "url": url, "dateModified": TODAY, "isBasedOn": DTMO_URL},
          {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "PCS Vector", "item": "https://pcsvector.com/"}, {"@type": "ListItem", "position": 2, "name": "OHA by country", "item": "https://pcsvector.com/oha/"}, {"@type": "ListItem", "position": 3, "name": n, "item": url}]},
          {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}]
    p = [head(P['title'], desc, url, ld)]
    p.append(f'<nav class="crumb"><a href="/">PCS Vector</a> \u203a <a href="/oha/">OHA by country</a> \u203a {e(n)}</nav>')
    has_calc = any(LOC[c][2] for c in P['locs'])
    p.append(f'<div class="kick">{"Military-approved agents" if has_calc else "PCS Vector"} \u00b7 {e(n)} OHA</div>')
    p.append(f'<h1>{e(P["h1"])}</h1>')
    p.append(f'<p class="stamp">Rates checked {CHECKED} \u00b7 DTMO rates as of 16 Oct 2026</p>')
    p.append(f'<p>{e(P["intro"])}</p>')
    first = next((LOC[c][2] for c in P['locs'] if LOC[c][2]), None)
    if first: p.append(f'<a class="cta" href="{calc(first, s)}">Compare {e(LOC[next(c for c in P["locs"] if LOC[c][2])][0])} with your current post (free calculator) \u2192</a>')
    else: p.append(f'<a class="cta" href="{calc(None, s)}">Open the free PCS calculator \u2192</a><p class="note">Okinawa is not in the calculator yet; the calculator covers Camp Zama for Japan.</p>')
    if len(P['locs']) > 1:
        p.append('<h2>At a glance: E-5 with dependents</h2><div class="tw"><table><thead><tr><th>Area</th><th>DTMO code</th><th>Rent ceiling</th><th>Utilities</th></tr></thead><tbody>' +
                 ''.join(f'<tr data-c="{c}"><td><a href="#{c.lower()}">{e(LOC[c][0])}</a></td><td>{c}</td><td>{usd(rec(c,"with","E-5")["rent"])}</td><td>{usd(rec(c,"with","E-5")["util"])}</td></tr>' for c in P['locs']) + '</tbody></table></div>')
    for c in P['locs']: p += section(c, s)
    p.append('<p class="note">\u201cWith dependents\u201d is yes or no for the rent ceiling. O-1E to O-3E are officers with more than four years of prior enlisted or warrant service. OHA pays your actual rent up to the ceiling, never more.</p>')
    p.append(HOW)
    p.append('<h2>Quick answers</h2>' + ''.join(f'<h3>{e(q)}</h3><p>{e(a)}</p>' for q, a in faqs))
    if has_calc:
        p.append(f'<section class="agents"><h2>Military-approved agents in {e(n)}</h2><p>Want local help finding a rental that fits your OHA? PCS Vector can connect you with one of our <strong>military-approved agents</strong> at your new duty station. The intro is free and does not change your OHA.</p><a class="cta cta2" href="{calc(first, s, "agents")}">Run your numbers and get a free intro to a military-approved agent \u2192</a></section>')
    others = [o for o in PAGES if o is not P]
    p.append('<h2>Other OHA pages</h2><ul class="bases">' + ''.join(f'<li><a href="/oha/{o["slug"]}/">{e(o["name"])}</a></li>' for o in others) + '<li><a href="/oha/">All OHA \u2192</a></li><li><a href="/bah/">BAH by post (U.S.)</a></li></ul>')
    p.append(sources(P['locs']))
    p.append(FOOT)
    os.makedirs(OUT + f'oha/{s}', exist_ok=True)
    open(OUT + f'oha/{s}/index.html', 'w').write('\n'.join(p))
for P in PAGES: page(P)
# hub
url = 'https://pcsvector.com/oha/'
hub_faq = [('What is OHA?', 'Overseas Housing Allowance (OHA) is the overseas counterpart of BAH for members who rent private housing off post. It reimburses actual rent up to a DTMO rent ceiling, plus a flat utility/recurring maintenance allowance and a one-time Move-In Housing Allowance.'),
           ('How often do OHA rates change?', 'DTMO can update OHA exchange rates and rates every pay period, on the 1st and 16th of each month. The rates on these pages are for the pay period starting 16 Oct 2026.')]
ld = [{"@context": "https://schema.org", "@type": "CollectionPage", "name": "OHA 2026 by country", "url": url, "dateModified": TODAY, "isBasedOn": DTMO_URL},
      {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "PCS Vector", "item": "https://pcsvector.com/"}, {"@type": "ListItem", "position": 2, "name": "OHA by country", "item": url}]},
      {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in hub_faq]}]
h = [head('OHA 2026 by Country: Japan, Okinawa, Germany, Korea Rent Ceilings | PCS Vector', '2026 OHA rent ceilings, utility and move-in allowance for Army areas in Japan, Okinawa, Germany and South Korea, by rank. DTMO rates as of 16 Oct 2026.', url, ld)]
h.append('<nav class="crumb"><a href="/">PCS Vector</a> \u203a OHA by country</nav><div class="kick">PCS Vector \u00b7 free OHA tables</div><h1>Overseas Housing Allowance (OHA) 2026 by country</h1>')
h.append(f'<p class="stamp">Rates checked {CHECKED} \u00b7 DTMO rates as of 16 Oct 2026</p>')
h.append('<p>OHA rent ceilings, utility allowance and move-in allowance for the main Army areas in Japan, Okinawa, Germany and South Korea, from the DTMO OHA Rate Lookup. Pick a country for every pay grade, with and without dependents.</p>')
h.append('<a class="cta" href="/?utm_source=ohahub&amp;utm_medium=organic&amp;utm_campaign=oha-hub">Compare any two posts, CONUS or OCONUS (free calculator) \u2192</a>')
rows = []
for P in PAGES:
    for c in P['locs']:
        u = rec(c, 'with', 'E-5'); uo = rec(c, 'without', 'E-5')
        rows.append(f'<tr data-c="{c}"><td><a href="/oha/{P["slug"]}/#{c.lower()}">{e(LOC[c][0])}</a> <span class="loc">{e(P["name"])}</span></td><td>{c}</td><td>{usd(u["rent"])}</td><td>{usd(uo["rent"])}</td><td>{usd(u["util"])}</td></tr>')
h.append('<h2>E-5 rent ceilings and utilities by area</h2><div class="tw"><table><thead><tr><th>Area</th><th>DTMO code</th><th>E-5 with dep.</th><th>E-5 without</th><th>Utilities (with dep.)</th></tr></thead><tbody>' + ''.join(rows) + '</tbody></table></div>')
h.append('<ul class="bases">' + ''.join(f'<li><a href="/oha/{P["slug"]}/">{e(P["name"])}</a></li>' for P in PAGES) + '<li><a href="/bah/">BAH by post (U.S.)</a></li></ul>')
h.append(HOW)
h.append('<h2>Quick answers</h2>' + ''.join(f'<h3>{e(q)}</h3><p>{e(a)}</p>' for q, a in hub_faq))
h.append('<section class="agents"><h2>Military-approved agents</h2><p>After you run your numbers, PCS Vector can connect you with one of our military-approved agents at your new post for free local housing help.</p><a class="cta cta2" href="/?utm_source=ohahub&amp;utm_medium=agents&amp;utm_campaign=oha-hub#find-a-home">Run your numbers \u2192</a></section>')
h.append(sources([c for P in PAGES for c in P['locs']]))
h.append(FOOT)
os.makedirs(OUT + 'oha', exist_ok=True)
open(OUT + 'oha/index.html', 'w').write('\n'.join(h))
# BAH hub: add OHA link (idempotent)
bh = OUT + 'bah/index.html'; s = open(bh).read()
LINK = '<p class="note">Stationed overseas? <a href="/oha/">OHA by country: Japan, Okinawa, Germany, Korea \u2192</a></p>'
if '/oha/' not in s:
    s = s.replace('<p class="src">Source: DTMO 2026 BAH', LINK + '\n<p class="src">Source: DTMO 2026 BAH', 1); open(bh, 'w').write(s)
# sitemap: add OHA URLs (true lastmod = today), bump /bah/ hub lastmod (changed today)
sm = OUT + 'sitemap.xml'; t = open(sm).read()
t = t.replace('<loc>https://pcsvector.com/bah/</loc><lastmod>2026-10-11</lastmod>', f'<loc>https://pcsvector.com/bah/</loc><lastmod>{TODAY}</lastmod>')
new = ['https://pcsvector.com/oha/'] + [f'https://pcsvector.com/oha/{P["slug"]}/' for P in sorted(PAGES, key=lambda x: x['slug'])]
add = ''.join(f'  <url><loc>{u}</loc><lastmod>{TODAY}</lastmod></url>\n' for u in new if f'<loc>{u}</loc>' not in t)
t = t.replace('</urlset>', add + '</urlset>'); open(sm, 'w').write(t)
print('built', [P['slug'] for P in PAGES], '+ hub')
