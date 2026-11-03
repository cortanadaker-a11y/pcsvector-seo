#!/usr/bin/env python3
"""Sync the OHA numbers in assets/calc-data.json with the /oha/* pages (the pages are refreshed from DTMO
each pay period; the calculator must show the same dollars).

For every calculator post that has an OHA page table, rent ceilings (with / without dependents, per grade) and
utilities are read from that page, to the cent.  USAG Italy has no page: its EUR ceilings (DTMO, unchanged
local-currency amounts, from pcs-vector data/oconus_allowances_2026.json) are converted at the EUR rate the
Germany page shows, using the rule the pages follow (with = local / rate; without = 90% rent, 75% utilities of
the with-dependents dollars).  That rule is asserted against every page-backed value first.
Fort Buchanan (PR) is paid in USD and is left as is.

Idempotent: re-running with unchanged pages changes nothing.  Also refreshes the ?v= cache-busting hashes
(same scheme as .github/scripts/refresh_gas.py).

usage:  python3 tools/calc_oha.py            # write
        python3 tools/calc_oha.py --check    # exit 1 if calc-data.json is out of date
"""
import hashlib, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CD = ROOT / "assets" / "calc-data.json"

# calculator post -> (page, DTMO locality code)
PAGE_POSTS = {
    "Camp Humphreys, South Korea": ("oha/korea/index.html", "kr025"),
    "Camp Casey, South Korea": ("oha/korea/index.html", "kr177"),
    "Camp Zama, Japan": ("oha/japan/index.html", "jp045"),
    "USAG Bavaria, Germany": ("oha/germany/index.html", "de231"),
    "USAG Rheinland-Pfalz, Germany": ("oha/germany/index.html", "de700"),
    "USAG Wiesbaden, Germany": ("oha/germany/index.html", "de355"),
}
# USAG Italy (IT073 Vicenza) EUR ceilings, with dependents (DTMO; pcs-vector oconus_allowances_2026.json).
ITALY_EUR = {"E-1": 1450, "E-2": 1450, "E-3": 1450, "E-4": 1450, "E-5": 1600, "E-6": 1600, "E-7": 1600, "E-8": 1600,
             "E-9": 2000, "W-1": 1600, "W-2": 1600, "W-3": 2000, "W-4": 2000, "W-5": 2200, "O-1": 1600, "O-2": 1600,
             "O-3": 1600, "O-4": 2000, "O-5": 2200, "O-6": 2200, "O-7+": 2200}
ITALY_UTIL_EUR = 1404

money = lambda s: float(s.replace("$", "").replace(",", ""))
r2 = lambda x: round(x + 1e-9, 2)

def section(html, code):
    i = html.index('id="%s"' % code)
    j = html.find("<h2", i + 10)
    return html[i:j if j > 0 else len(html)]

def parse(sec):
    rent = {}
    for g, a, b in re.findall(r'<tr data-g="([^"]+)"><td>[^<]*</td><td>[^<]*</td><td>(\$[\d,\.]+)[^<]*<span[^>]*>[^<]*</span></td><td>(\$[\d,\.]+)', sec):
        rent["O-7+" if g == "O-7" else g] = (money(b), money(a))   # (without, with)
    u = re.search(r'<tr data-k="util"><td>[^<]*</td><td>(\$[\d,\.]+)[^<]*<span[^>]*>([^<]*)</span></td><td>(\$[\d,\.]+)', sec)
    loc = {g: int(re.sub(r"\D", "", v)) for g, v in re.findall(r'<tr data-g="([^"]+)"><td>[^<]*</td><td>[^<]*</td><td>\$[\d,\.]+ <span[^>]*>([^<]*)</span>', sec)}
    rate = float(re.search(r"1 USD = ([\d,\.]+) [A-Z]{3}", sec).group(1).replace(",", ""))
    return rent, (money(u.group(3)), money(u.group(1))), int(re.sub(r"\D", "", u.group(2))), loc, rate

def build():
    raw = CD.read_text(encoding="utf-8")
    cd = json.loads(raw)
    grades = cd["grades"]
    eur_rate = None
    for post, (page, code) in PAGE_POSTS.items():
        rent, util, util_loc, loc, rate = parse(section((ROOT / page).read_text(encoding="utf-8"), code))
        missing = [g for g in grades if g not in rent]
        assert not missing, (post, missing)
        # the conversion rule (used for Italy) must reproduce every page value
        for g in grades:
            lg = loc["O-7" if g == "O-7+" else g]
            w = r2(lg / rate)
            assert abs(w - rent[g][1]) <= 0.011, (post, g, w, rent[g])
            assert abs(r2(0.9 * rent[g][1]) - rent[g][0]) <= 0.011, (post, g, rent[g])
        assert abs(r2(util_loc / rate) - util[1]) <= 0.011 and abs(r2(0.75 * util[1]) - util[0]) <= 0.011, (post, util)
        cd["posts"][post]["oha"] = [[[rent[g][0], util[0]] for g in grades], [[rent[g][1], util[1]] for g in grades]]
        if code.startswith("de"): eur_rate = rate
    w = {g: r2(ITALY_EUR[g] / eur_rate) for g in grades}
    uw = r2(ITALY_UTIL_EUR / eur_rate)
    cd["posts"]["USAG Italy, Italy"]["oha"] = [[[r2(0.9 * w[g]), r2(0.75 * uw)] for g in grades], [[w[g], uw] for g in grades]]
    out = json.dumps(cd, separators=(",", ":"), ensure_ascii=False) + ("\n" if raw.endswith("\n") else "")
    return raw, out

def bust(out):
    h = lambda b: hashlib.sha256(b).hexdigest()[:10]
    cd_h = h(out.encode("utf-8"))
    jsp, ixp = ROOT / "assets/pcs.js", ROOT / "index.html"
    js = re.sub(r"/assets/calc-data\.json\?v=[0-9a-f]+", "/assets/calc-data.json?v=" + cd_h, jsp.read_text(encoding="utf-8"))
    ix = ixp.read_text(encoding="utf-8")
    ix = re.sub(r'/assets/calc-data\.json(\?v=[0-9a-f]+)?"', "/assets/calc-data.json?v=" + cd_h + '"', ix)
    ix = re.sub(r'/assets/pcs\.js(\?v=[0-9a-f]+)?"', "/assets/pcs.js?v=" + h(js.encode("utf-8")) + '"', ix)
    ix = re.sub(r'/assets/pcs\.css(\?v=[0-9a-f]+)?"', "/assets/pcs.css?v=" + h((ROOT / "assets/pcs.css").read_bytes()) + '"', ix)
    return js, ix

def main():
    raw, out = build()
    js, ix = bust(out)
    same = raw == out and (ROOT / "assets/pcs.js").read_text(encoding="utf-8") == js and (ROOT / "index.html").read_text(encoding="utf-8") == ix
    if "--check" in sys.argv:
        print("calc-data OK" if same else "calc-data OUT OF DATE (run tools/calc_oha.py)")
        sys.exit(0 if same else 1)
    if not same:
        CD.write_text(out, encoding="utf-8")
        (ROOT / "assets/pcs.js").write_text(js, encoding="utf-8")
        (ROOT / "index.html").write_text(ix, encoding="utf-8")
    print("calc-data OHA synced with /oha/* pages" + ("" if not same else " (no change)"))

if __name__ == "__main__":
    main()
