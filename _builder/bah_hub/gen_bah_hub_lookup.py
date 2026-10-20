"""/bah/ hub: rank + dependents + home-size lookup (Zak request 20 Oct 2026). Idempotent; edits ONLY <root>/bah/index.html.
Data: BAH from assets/calc-data.json (DTMO 2026 BAH tables, verified cell-for-cell vs BAH-ASCII-2026), rent from the same
calc-data 'rent' rows the calculator uses (shown as 'Avg nBR rent' = midpoint, as in the calculator). No other sources.
Usage: python3 gen_bah_hub_lookup.py <site_root>"""
import json, re, sys, html
root = sys.argv[1].rstrip('/') + '/'
P = root + 'bah/index.html'; s = open(P).read()
D = json.load(open(root + 'assets/calc-data.json'))
PICK = {'national-capital-region': 'Pentagon / National Capital Region, VA', 'joint-base-san-antonio': 'Joint Base San Antonio, TX',
        'fort-wainwright': 'Fort Wainwright, AK', 'schofield-barracks': 'Schofield Barracks, HI'}
rows = re.findall(r'<a href="/bah/([a-z0-9-]+)/">([^<]+)</a></td><td>([A-Z]{2}\d{3})</td>', s)
assert len(rows) >= 20, rows
def post_for(slug, name):
    if slug in PICK: return PICK[slug]
    c = [p for p in D['posts'] if p.split(',')[0] == name]
    assert len(c) == 1, (slug, name, c); return c[0]
G = D['grades']; posts = []
for slug, name, code in rows:
    p = post_for(slug, name); v = D['posts'][p]; assert v['sys'] != 'OHA'
    rent = {}
    for lo, hi, mid, br in v['rent']: rent.setdefault(str(br), mid)
    posts.append({'s': slug, 'n': name, 'c': code, 'p': p, 'wo': v['h'][0], 'w': v['h'][1], 'r': rent})
SIZES = sorted({k for x in posts for k in x['r']}, key=int)
money = lambda n: ('-' if n < 0 else '') + '$' + f'{abs(n):,}'
def diff(n): return ('+' if n > 0 else '\u2212' if n < 0 else '') + '$' + f'{abs(n):,}'
DEF_G, DEF_W, DEF_SZ = 'E-5', 1, '3'
def body(g, w, sz):
    gi = G.index(g); out = []
    for x in posts:
        b = (x['w'] if w else x['wo'])[gi]; r = x['r'][sz]; d = b - r
        out.append(f'<tr><td><a href="/bah/{x["s"]}/">{html.escape(x["n"])}</a></td><td>{x["c"]}</td><td>{money(b)}</td><td>{money(r)}</td>'
                   f'<td class="{"pos" if d >= 0 else "neg"}">{diff(d)}</td></tr>')
    return ''.join(out)
opt = lambda vals, cur: ''.join(f'<option value="{v}"{" selected" if v == cur else ""}>{t}</option>' for v, t in vals)
data = {'g': G, 'sz': SIZES, 'p': [{k: x[k] for k in ('s', 'n', 'c', 'w', 'wo', 'r')} for x in posts]}
cap = lambda g, w, sz: f'Showing {g} {"with" if w else "without"} dependents, Avg {sz}BR rent'
block = f'''<!--hub-lookup-->
<style>.lk{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;margin:14px 0 8px}}.lk label{{display:block;color:var(--gold);font-size:.75rem;font-weight:700;text-transform:uppercase;letter-spacing:.04em;margin-bottom:4px}}
.lk select{{width:100%;min-height:44px;padding:8px 10px;background:var(--card);color:var(--ink);border:1px solid #3a5245;border-radius:8px;font:inherit}}
.lk select:focus{{outline:2px solid var(--gold);outline-offset:1px}}td.pos{{color:#7fd19b}}td.neg{{color:#f2a07b}}#hub-cap{{margin:4px 0 8px}}
@media (max-width:560px){{.lk{{grid-template-columns:1fr 1fr}}.lk div:first-child{{grid-column:1/-1}}#hub-t th:nth-child(2),#hub-t td:nth-child(2){{display:none}}#hub-t{{font-size:.84rem}}#hub-t th{{white-space:normal;font-size:.68rem}}#hub-t th,#hub-t td{{padding:7px 4px}}}}</style>
<div class="lk" id="hub-lk" hidden>
<div><label for="hub-g">Rank</label><select id="hub-g">{opt([(g, g) for g in G], DEF_G)}</select></div>
<div><label for="hub-d">Dependents</label><select id="hub-d">{opt([('1', 'With dependents'), ('0', 'Without dependents')], '1')}</select></div>
<div><label for="hub-sz">Home size</label><select id="hub-sz">{opt([(z, f'Avg {z}BR rent') for z in SIZES], DEF_SZ)}</select></div>
</div>
<p class="note" id="hub-cap" aria-live="polite">{cap(DEF_G, DEF_W, DEF_SZ)}</p>
<div class="tw"><table id="hub-t"><thead><tr><th>Post</th><th>Housing area</th><th>BAH (DTMO 2026)</th><th id="hub-rh">Avg {DEF_SZ}BR rent</th><th>Difference</th></tr></thead><tbody id="hub-tb">{body(DEF_G, DEF_W, DEF_SZ)}</tbody></table></div>
<p class="note">BAH = official DTMO 2026 rate for the post's housing area. Avg nBR rent = PCS Vector planning estimate of average off-post rent for that home size (the same figure the calculator uses), not a DTMO figure. Difference = BAH minus Avg rent. Every rank is built in: pick rank, dependents and home size above. More posts coming; the calculator already covers 68+ Army posts, CONUS and OCONUS.</p>
<script type="application/json" id="hub-data">{json.dumps(data, separators=(',', ':'))}</script>
<script>(function(){{var D=JSON.parse(document.getElementById('hub-data').textContent),$=function(i){{return document.getElementById(i)}};
function m(n){{return(n<0?'-':'')+'$'+Math.abs(n).toLocaleString('en-US')}}function df(n){{return(n>0?'+':n<0?'\\u2212':'')+'$'+Math.abs(n).toLocaleString('en-US')}}
function e(t){{return String(t).replace(/&/g,'&amp;').replace(/</g,'&lt;')}}
function r(){{var g=$('hub-g').value,w=$('hub-d').value==='1',z=$('hub-sz').value,gi=D.g.indexOf(g);
$('hub-rh').textContent='Avg '+z+'BR rent';$('hub-cap').textContent='Showing '+g+' '+(w?'with':'without')+' dependents, Avg '+z+'BR rent';
$('hub-tb').innerHTML=D.p.map(function(x){{var b=(w?x.w:x.wo)[gi],a=x.r[z],d=b-a;return '<tr><td><a href="/bah/'+x.s+'/">'+e(x.n)+'</a></td><td>'+x.c+'</td><td>'+m(b)+'</td><td>'+m(a)+'</td><td class="'+(d>=0?'pos':'neg')+'">'+df(d)+'</td></tr>'}}).join('')}}
['hub-g','hub-d','hub-sz'].forEach(function(i){{$(i).addEventListener('change',r)}});$('hub-lk').hidden=false;r();}})();</script>
<!--/hub-lookup-->'''
if '<!--hub-lookup-->' in s:
    s = re.sub(r'<!--hub-lookup-->.*?<!--/hub-lookup-->', lambda m: block, s, flags=re.S)
else:
    a = s.index('<div class="tw"><table><thead><tr><th>Post</th>'); b = s.index('</p>', s.index('<p class="note">', a)) + 4
    s = s[:a] + block + s[b:]
s = s.replace('next to what a typical 3-bedroom off post actually costs with utilities.', 'next to the average off-post rent for the home size you pick. Every rank is built in.')
s = s.replace('side by side with typical 3-bedroom rent and utilities.', 'next to average off-post rent by rank and home size.')
open(P, 'w').write(s); print('hub lookup:', len(posts), 'posts,', len(G), 'grades, sizes', SIZES)
