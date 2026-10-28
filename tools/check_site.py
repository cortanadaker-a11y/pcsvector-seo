#!/usr/bin/env python3
"""Local checks for the static site.  usage: python3 tools/check_site.py [--external]
Checks every page: single self-canonical on https://pcsvector.com, exactly one h1, GoatCounter snippet once,
title/description/og/twitter tags, valid JSON-LD (+BreadcrumbList on non-home pages), images have alt,
internal links and #fragments resolve, no duplicate ids, sitemap lists every page with a lastmod.
--external also GETs every external link (some government sites block bots: 403 is reported as 'blocked', not broken)."""
import json, re, sys, collections
from pathlib import Path
from urllib.parse import urlparse, urldefrag
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://pcsvector.com"
TAGLINE = "For Soldiers; By Soldiers"
errs, warns = [], []
pages = {}
for p in sorted(ROOT.rglob("*.html")):
    rel = p.relative_to(ROOT)
    if rel.parts[0] in (".git", "tools", "node_modules", "_pcs_vector", "_builder"): continue
    url = "/" + str(rel)
    if rel.name == "index.html": url = "/" + "/".join(rel.parts[:-1]) + ("/" if len(rel.parts) > 1 else "")
    pages[url] = (rel, BeautifulSoup(p.read_text(encoding="utf-8"), "lxml"))
ids = {u: {t.get("id") for t in s.find_all(id=True)} for u, (_, s) in pages.items()}
ext = collections.defaultdict(set)

def e(u, m): errs.append("%s: %s" % (u, m))

for u, (rel, s) in pages.items():
    is404 = rel.name == "404.html"
    can = [l.get("href") for l in s.find_all("link", rel="canonical")]
    if is404:
        if can: e(u, "404 page should not carry a canonical")
    elif can != [BASE + u]: e(u, "canonical %r != %r" % (can, BASE + u))
    if len(s.find_all("h1")) != 1: e(u, "h1 count %d" % len(s.find_all("h1")))
    if len(s.find_all("script", attrs={"data-goatcounter": True})) != 1: e(u, "GoatCounter snippet count != 1")
    if not s.title or not s.title.string: e(u, "no title")
    if not s.find("meta", attrs={"name": "description"}): e(u, "no meta description")
    for k in ("og:title", "og:description", "og:url", "og:image"):
        if not s.find("meta", attrs={"property": k}): e(u, "missing " + k)
    for k in ("twitter:card", "twitter:image"):
        if not s.find("meta", attrs={"name": k}): e(u, "missing " + k)
    ou = s.find("meta", attrs={"property": "og:url"})
    if ou and not is404 and ou.get("content") != BASE + u: e(u, "og:url mismatch")
    if not s.find("meta", attrs={"name": "viewport"}): e(u, "no viewport")
    types = []
    vis = None
    for sc in s.find_all("script", type="application/ld+json"):
        try:
            j = json.loads(sc.string); types.append(j.get("@type"))
            if j.get("@type") == "FAQPage":     # FAQPage markup must match visible questions
                if vis is None:
                    import copy
                    s2 = copy.copy(s)
                    for t in s2.find_all(["script", "style"]): t.decompose()
                    vis = " ".join(s2.get_text(" ").split())
                for q in j.get("mainEntity", []):
                    if " ".join(q["name"].split()) not in vis: e(u, "FAQPage JSON-LD question not visible on page: %s" % q["name"][:70])
        except Exception as ex: e(u, "bad JSON-LD: %s" % ex)
    # --- brand / site-name signals (Google site name): consistent name, tagline, WebSite markup on the homepage
    osn = s.find("meta", attrs={"property": "og:site_name"})
    if not osn or osn.get("content") != "PCS Vector": e(u, "og:site_name != 'PCS Vector'")
    if s.title and s.title.string and "PCS Vector" not in s.title.string: e(u, "title does not contain 'PCS Vector'")
    if TAGLINE not in " ".join(s.get_text(" ").split()): e(u, "tagline %r not on page" % TAGLINE)
    if u == "/":
        nodes = []
        for sc in s.find_all("script", type="application/ld+json"):
            j = json.loads(sc.string); nodes += j.get("@graph", [j])
        ws = [n for n in nodes if n.get("@type") == "WebSite"]
        if len(ws) != 1: e(u, "homepage needs exactly one WebSite JSON-LD node (found %d)" % len(ws))
        elif ws[0].get("name") != "PCS Vector" or ws[0].get("url") != BASE + "/" or not ws[0].get("alternateName"):
            e(u, "WebSite JSON-LD must have name 'PCS Vector', url %s/ and alternateName" % BASE)
        rels = {(l.get("rel") or [""])[0] + ":" + (l.get("sizes") or "") + ":" + (l.get("href") or "") for l in s.find_all("link") if "icon" in " ".join(l.get("rel") or [])}
        for need in ("icon::/favicon.ico", "icon::/favicon.svg", "icon:48x48:/favicon-48x48.png", "icon:192x192:/favicon-192x192.png"):
            if not any(r.endswith(need) or r == need or (need.startswith("icon:") and need.split(":", 1)[1] in r) for r in rels): e(u, "missing icon link " + need)
        if not any("apple-touch-icon" in r for r in rels): e(u, "missing apple-touch-icon link")
    if u != "/" and not is404 and "BreadcrumbList" not in types: e(u, "no BreadcrumbList JSON-LD")
    for tr in s.find_all("tr", attrs={"data-k": "miha"}):
        if any(td.get_text(strip=True) in ("\u2014", "-") for td in tr.find_all("td")): e(u, "MIHA row has an empty/dash cell")
    if "did not return a MIHA" in s.get_text(): e(u, "stale 'DTMO did not return a MIHA figure' sentence")
    for im in s.find_all("img"):
        if im.get("alt") is None: e(u, "img without alt: %s" % im.get("src"))
    seen = collections.Counter(t.get("id") for t in s.find_all(id=True))
    for k, n in seen.items():
        if n > 1: e(u, "duplicate id %r x%d" % (k, n))
    for a in s.find_all("a", href=True):
        h = a["href"]
        if h.startswith(("mailto:", "tel:", "javascript:")): continue
        if h.startswith("http"):
            if urlparse(h).netloc in ("pcsvector.com", "www.pcsvector.com"): e(u, "absolute internal link %s" % h)
            ext[urldefrag(h)[0]].add(u); continue
        if h.startswith("//"): continue
        tgt, frag = urldefrag(h); tgt = tgt.split("?")[0]
        if tgt == "": tgt = u
        elif not tgt.startswith("/"): e(u, "relative link %s" % h); continue
        t2 = tgt if (tgt.endswith("/") or "." in tgt.split("/")[-1]) else tgt + "/"
        if t2 not in pages and not (ROOT / tgt.lstrip("/")).exists(): e(u, "broken internal link %s" % h); continue
        if frag and t2 in ids and frag not in ids[t2]: e(u, "missing fragment #%s on %s" % (frag, t2))
# no leftover 'Streamlit' anywhere in the published tree (the old app name Google may still show as the site name)
for f in sorted(ROOT.rglob("*")):
    rel = f.relative_to(ROOT)
    if not f.is_file() or rel.parts[0] in (".git", "tools", "node_modules"): continue
    try: txt = f.read_text(encoding="utf-8")
    except Exception: continue
    if "streamlit" in txt.lower(): e("/" + str(rel), "contains the string 'streamlit'")
# Google favicon rules: square, multiple of 48px, stable URL
try:
    from PIL import Image
    for fn, want in (("favicon-48x48.png", (48, 48)), ("favicon-192x192.png", (192, 192)), ("apple-touch-icon.png", (180, 180))):
        im = Image.open(ROOT / fn)
        if im.size != want: e("/" + fn, "size %s != %s" % (im.size, want))
    ico = Image.open(ROOT / "favicon.ico")
    if not any(w % 48 == 0 and w == h for w, h in ico.info.get("sizes", {ico.size})): e("/favicon.ico", "no square size that is a multiple of 48: %s" % sorted(ico.info.get("sizes", {ico.size})))
except ImportError:
    warns.append("PIL missing: favicon dimensions not checked")

# sitemap
sm = (ROOT / "sitemap.xml").read_text()
locs = re.findall(r"<loc>([^<]+)</loc><lastmod>(\d{4}-\d{2}-\d{2})</lastmod>", sm)
smu = {l.replace(BASE, "") for l, _ in locs}
for u, (rel, _) in pages.items():
    if rel.name != "404.html" and u not in smu: e(u, "missing from sitemap")
for l in smu:
    if l not in pages: e(l, "sitemap URL has no page")
# homepage links every BAH/OHA/guide page
home_links = {a["href"].split("?")[0] for a in pages["/"][1].find_all("a", href=True)}
for u in pages:
    if (u.startswith(("/bah/", "/oha/", "/guides/"))) and u not in home_links: e(u, "not linked from the homepage")
# fort pages link to /bah/ and /oha/
for u, (_, s) in pages.items():
    if u.startswith("/bah/") and u != "/bah/":
        hs = {a["href"].split("?")[0] for a in s.find_all("a", href=True)}
        for need in ("/bah/", "/oha/"):
            if need not in hs: e(u, "no link to " + need)

if "--external" in sys.argv:
    import requests
    from concurrent.futures import ThreadPoolExecutor
    H = {"User-Agent": "Mozilla/5.0 (compatible; pcsvector-linkcheck)"}
    def chk(url):
        try:
            r = requests.get(url, headers=H, timeout=25, allow_redirects=True, stream=True)
            return url, r.status_code
        except Exception as ex:
            return url, "ERR %s" % type(ex).__name__
    with ThreadPoolExecutor(8) as ex:
        res = list(ex.map(chk, sorted(ext)))
    for url, c in res:
        tag = "ok" if c == 200 else ("blocked" if c in (401, 403, 429) else "BAD")
        print("%-8s %s  %s" % (tag, c, url))
        if tag == "BAD": errs.append("external link %s -> %s (on %s)" % (url, c, sorted(ext[url])[:2]))
print("pages checked: %d | sitemap URLs: %d | %s | errors: %d" % (len(pages), len(smu), "internal links + external URLs fetched (--external)" if "--external" in sys.argv else "internal links only (add --external to fetch external URLs)", len(errs)))
for x in errs: print("ERROR", x)
sys.exit(1 if errs else 0)
