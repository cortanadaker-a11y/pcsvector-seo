#!/usr/bin/env python3
"""Regenerate sitemap.xml with accurate <lastmod>.

How lastmod is decided (no git history needed, so it also works in CI with a shallow checkout):
  tools/lastmod.json stores, per sitemap URL, the sha256 of the page's source files and the date that
  hash was first seen.  If a page's hash changed since the last run, lastmod becomes today (UTC);
  otherwise the stored date is kept.  The home page hash also covers assets/ (calc data, JS, CSS)
  because those change what visitors see on "/".

usage:
  python3 tools/sitemap.py                  # update ledger + sitemap.xml
  python3 tools/sitemap.py --seed-from-git  # first run only: seed dates from `git log` (no 'today' bump)
  python3 tools/sitemap.py --check          # exit 1 if sitemap.xml / ledger are out of date
  python3 tools/sitemap.py --keep-date=YYYY-MM-DD:/url/,/url2/   # cosmetic-only change (e.g. nav links): record the new hash, keep the old lastmod
"""
import hashlib, json, subprocess, sys, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEDGER = ROOT / "tools" / "lastmod.json"
BASE = "https://pcsvector.com"
HOME_EXTRA = ["assets/calc-data.json", "assets/gas-table.json", "assets/pcs.js", "assets/pcs.css"]

def pages():
    out = []
    for p in sorted(ROOT.rglob("index.html")):
        rel = p.relative_to(ROOT)
        if rel.parts[0] in (".git", "tools", "_builder", "_pcs_vector", "node_modules"):
            continue
        url = "/" if rel.parts == ("index.html",) else "/" + "/".join(rel.parts[:-1]) + "/"
        out.append((url, rel))
    return out

def order(url):
    # home, hubs, then everything else alphabetically (stable, diff-friendly)
    return (0 if url == "/" else 1 if url in ("/bah/", "/oha/", "/guides/") else 2, url)

def digest(rel):
    h = hashlib.sha256()
    files = [rel] + ([Path(x) for x in HOME_EXTRA] if rel.parts == ("index.html",) else [])
    for f in files:
        h.update((ROOT / f).read_bytes())
    return h.hexdigest()

def git_date(rel):
    files = [rel] + ([Path(x) for x in HOME_EXTRA] if rel.parts == ("index.html",) else [])
    ds = []
    for f in files:
        r = subprocess.run(["git", "log", "-1", "--format=%cs", "--", str(f)], cwd=ROOT, capture_output=True, text=True)
        if r.stdout.strip():
            ds.append(r.stdout.strip())
    return max(ds) if ds else datetime.datetime.now(datetime.timezone.utc).date().isoformat()

def build(seed=False, keep=None):
    """keep = {url: date}: when the page's hash changed only cosmetically, record the new hash but keep this date."""
    keep = keep or {}
    today = datetime.datetime.now(datetime.timezone.utc).date().isoformat()
    led = json.loads(LEDGER.read_text()) if LEDGER.exists() else {}
    new = {}
    for url, rel in pages():
        d = digest(rel)
        old = led.get(url)
        if seed:
            new[url] = {"sha256": d, "lastmod": git_date(rel)}
        elif old and old["sha256"] == d:
            new[url] = old
        elif url in keep:
            new[url] = {"sha256": d, "lastmod": keep[url]}
        else:
            new[url] = {"sha256": d, "lastmod": today}
    urls = sorted(new, key=order)
    xml = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        xml.append(f'  <url><loc>{BASE}{u}</loc><lastmod>{new[u]["lastmod"]}</lastmod></url>')
    xml.append('</urlset>')
    return new, "\n".join(xml) + "\n"

def main():
    seed = "--seed-from-git" in sys.argv
    keep = {}
    for a in sys.argv:
        if a.startswith("--keep-date="):           # --keep-date=2026-10-21:/bah/fort-lee/,/bah/fort-knox/
            d, urls = a.split("=", 1)[1].split(":", 1)
            keep.update({x: d for x in urls.split(",") if x})
    new, xml = build(seed, keep)
    led_txt = json.dumps(new, indent=1, sort_keys=True) + "\n"
    if "--check" in sys.argv:
        ok = (ROOT / "sitemap.xml").read_text() == xml and LEDGER.exists() and LEDGER.read_text() == led_txt
        print("sitemap OK" if ok else "sitemap/ledger OUT OF DATE (run tools/sitemap.py)")
        sys.exit(0 if ok else 1)
    LEDGER.write_text(led_txt)
    (ROOT / "sitemap.xml").write_text(xml)
    print(f"wrote sitemap.xml ({len(new)} URLs) and tools/lastmod.json")

if __name__ == "__main__":
    main()
