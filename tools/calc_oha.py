#!/usr/bin/env python3
"""Sync the OHA numbers and COLA indexes in assets/calc-data.json with this pay period.

OHA pages are refreshed from DTMO each pay period; the calculator must show the same dollars.
For every calculator post that has an OHA page table, rent ceilings (with / without dependents, per grade) and
utilities are read from that page, to the cent.  USAG Italy has no page: its EUR ceilings (DTMO, unchanged
local-currency amounts, from pcs-vector data/oconus_allowances_2026.json) are converted at the EUR rate the
Germany page shows, using the rule the pages follow (with = local / rate; without = 90% rent, 75% utilities of
the with-dependents dollars).  That rule is asserted against every page-backed value first.

Fort Buchanan (PR080) without-dependents OHA is an estimate: 90% of the on-file with-dependents
rent and 75% of the utility, to the cent. DTMO's lookup was not reachable when this was checked
(HTTP 403), so no grade, including O grades, was re-verified. Do not int(round()): 0.9 * 2222 is
1999.80, and rounding to the dollar makes it 2000.

COLA indexes are the same pay-period refresh. COLA_INDEX is the source; calc-data.json "ci" is written from
it. --check fails if a post's index drifts, a COLA post is missing from the table, or COLA_AS_OF is more
than 45 days old. Update COLA_INDEX from the DTMO Overseas COLA Rate Lookup in the same pass as the OHA pages.

Idempotent: re-running with unchanged pages and an unchanged COLA table changes nothing. Also refreshes the
?v= cache-busting hashes (same scheme as .github/scripts/refresh_gas.py). The calculator's math is not in
this file.

usage:  python3 tools/calc_oha.py            # write
        python3 tools/calc_oha.py --check    # exit 1 if calc-data.json is out of date
"""
import datetime, hashlib, json, re, sys
from pathlib import Path
from zoneinfo import ZoneInfo

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

# Fort Buchanan / San Juan (PR080). ESTIMATE, not a fresh DTMO read.
# On 23 Nov 2026 the DTMO OHA Rate Lookup (https://www.travel.dod.mil/Allowances/Overseas-Housing-Allowance/OHA-Rate-Lookup/)
# returned HTTP 403 from this environment, so none of these grades were re-verified, including every
# O grade this calculator stores (O-1 through O-7+) and the O-1E / O-2E / O-3E rows DTMO publishes
# separately (those three are not their own rows here). With-dependents rent ceilings and the $1,223
# utility are the USD figures already on file. Without-dependents is derived, not copied from DTMO:
# 90% of the with-dependents rent and 75% of the utility, to the cent. Do not int(round()):
# 0.9 * 2222 is 1999.80, and rounding to the dollar makes it 2000.
BUCHANAN = "Fort Buchanan, PR"
BUCHANAN_OHA_BASIS = "estimate"
BUCHANAN_RENT_WITH = {
    "E-1": 2222, "E-2": 2222, "E-3": 2222, "E-4": 2222, "E-5": 2222,
    "E-6": 2300, "E-7": 2300, "E-8": 2300, "E-9": 2715,
    "W-1": 2222, "W-2": 2300, "W-3": 2715, "W-4": 2715, "W-5": 4286,
    "O-1": 2222, "O-2": 2222, "O-3": 2300, "O-4": 2715, "O-5": 4286, "O-6": 4286, "O-7+": 4286,
}
BUCHANAN_UTIL_WITH = 1223

# DTMO Overseas COLA index. Re-read this on each pay period (the 1st and the 16th) from
# https://www.travel.dod.mil/Allowances/Overseas-Cost-of-Living-Allowance/Overseas-COLA-Rate-Lookup/
# COLA_AS_OF is the pay-period date of the indexes below. tools/calc_oha.py --check fails when
# that date is more than 45 days old, so a hand-maintained table cannot sit unchanged for a quarter.
COLA_LOOKUP = "https://www.travel.dod.mil/Allowances/Overseas-Cost-of-Living-Allowance/Overseas-COLA-Rate-Lookup/"
COLA_AS_OF = "2026-11-16"
COLA_MAX_AGE_DAYS = 45
COLA_INDEX = {
    "USAG Wiesbaden, Germany": 134,                 # DE355 was 138
    "USAG Rheinland-Pfalz, Germany": 126,           # DE700 was 130
    "USAG Bavaria, Germany": 116,                   # DE231 was 120
    "USAG Italy, Italy": 118,                       # IT073 was 122
    "Camp Zama, Japan": 104,                        # JP045 was 106
    "Camp Casey, South Korea": 106,                 # KR177 unchanged this period
    "Camp Humphreys, South Korea": 116,             # KR025 unchanged this period
    "Fort Buchanan, PR": 124,                       # PR080 unchanged this period
    "Fort Greely, AK": 134,                         # AK029 Delta Junction unchanged
    "Fort Wainwright, AK": 132,                     # Fairbanks AK049 unchanged
    "Joint Base Elmendorf-Richardson, AK": 128,     # Anchorage AK005 unchanged
    "Fort Shafter, HI": 120,                        # Oahu HI009 unchanged
    "Schofield Barracks, HI": 120,                  # Oahu HI009 unchanged
}
# E-5, 2 dependents, calculator default 4 years (same annual-compensation bracket as 6 years).
# spendable 40100 * (134-100) / 100 / 12 = 1136.1666... which is $1,136.17 before the calculator's
# existing integer round (it shows $1,136). The old index 138 produced $1,270.
WIESBADEN_COLA_RAW = 1136.1666666666667

money = lambda s: float(s.replace("$", "").replace(",", ""))
r2 = lambda x: round(x + 1e-9, 2)

def money_num(x):
    """Keep a whole dollar as an int so unchanged ceilings do not flip from 2070 to 2070.0."""
    x = r2(x)
    if abs(x - round(x)) < 1e-9:
        return int(round(x))
    return x

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

def _yos_index(yos, bps):
    yos = max(0, min(40, int(yos)))
    if yos < 2:
        return 0
    if yos >= 40:
        return len(bps) - 1
    idx = 0
    for i, b in enumerate(bps):
        if yos >= b:
            idx = i
    return idx

def cola_monthly_raw(cd, grade, yos, deps, index):
    """Same spendable-income steps as assets/pcs.js estimateMonthlyCola, before its integer round.
    This check does not change the calculator."""
    t = cd["cola"]
    bps = t["yos_breakpoints"]
    row = t["compensation"][grade]["with" if int(deps) > 0 else "without"]
    idx = min(_yos_index(yos, bps), len(row) - 1)
    comp = int(row[idx])
    deps_i = max(0, min(5, int(deps)))
    last = None
    spend = 0
    for bracket in t["spendable_table"]:
        last = bracket
        if bracket[0] <= comp <= bracket[1]:
            spend = int(bracket[2][deps_i])
            break
    else:
        spend = int(last[2][deps_i]) if last else 0
    return spend * (index - 100) / 100.0 / 12.0

def apply_cola(cd):
    posts = cd["posts"]
    missing = [p for p in COLA_INDEX if p not in posts]
    assert not missing, missing
    for post, idx in COLA_INDEX.items():
        posts[post]["ci"] = idx
    extra = sorted(p for p, row in posts.items() if row.get("ci") is not None and p not in COLA_INDEX)
    assert not extra, extra
    raw = cola_monthly_raw(cd, "E-5", 4, 2, COLA_INDEX["USAG Wiesbaden, Germany"])
    assert abs(raw - WIESBADEN_COLA_RAW) < 1e-9, raw
    assert abs(raw - 1136.17) < 0.01
    return raw

def apply_buchanan(cd, grades):
    assert set(BUCHANAN_RENT_WITH) == set(grades)
    util_wo = money_num(0.75 * BUCHANAN_UTIL_WITH)
    without = [[money_num(0.9 * BUCHANAN_RENT_WITH[g]), util_wo] for g in grades]
    with_deps = [[BUCHANAN_RENT_WITH[g], BUCHANAN_UTIL_WITH] for g in grades]
    cd["posts"][BUCHANAN]["oha"] = [without, with_deps]
    e5 = without[grades.index("E-5")]
    assert e5[0] == 1999.8 and e5[1] == 917.25, e5

def assert_cola_fresh():
    """Fail when the hand-kept COLA table is more than COLA_MAX_AGE_DAYS old."""
    as_of = datetime.date.fromisoformat(COLA_AS_OF)
    today = datetime.datetime.now(ZoneInfo("America/New_York")).date()
    age = (today - as_of).days
    if age > COLA_MAX_AGE_DAYS:
        raise SystemExit(
            "COLA_INDEX as of %s is %d days old (limit %d). Re-read %s and update COLA_AS_OF and COLA_INDEX."
            % (COLA_AS_OF, age, COLA_MAX_AGE_DAYS, COLA_LOOKUP))
    return age

def build():
    cola_age = assert_cola_fresh()
    raw = CD.read_text(encoding="utf-8")
    cd = json.loads(raw)
    grades = cd["grades"]
    eur_rate = None
    for post, (page, code) in PAGE_POSTS.items():
        rent, util, util_loc, loc, rate = parse(section((ROOT / page).read_text(encoding="utf-8"), code))
        missing = [g for g in grades if g not in rent]
        assert not missing, (post, missing)
        # the conversion rule (used for Italy and Buchanan) must reproduce every page value
        for g in grades:
            lg = loc["O-7" if g == "O-7+" else g]
            w = r2(lg / rate)
            assert abs(w - rent[g][1]) <= 0.011, (post, g, w, rent[g])
            assert abs(r2(0.9 * rent[g][1]) - rent[g][0]) <= 0.011, (post, g, rent[g])
        assert abs(r2(util_loc / rate) - util[1]) <= 0.011 and abs(r2(0.75 * util[1]) - util[0]) <= 0.011, (post, util)
        cd["posts"][post]["oha"] = [[[rent[g][0], util[0]] for g in grades], [[rent[g][1], util[1]] for g in grades]]
        if code.startswith("de"):
            eur_rate = rate
    w = {g: r2(ITALY_EUR[g] / eur_rate) for g in grades}
    uw = r2(ITALY_UTIL_EUR / eur_rate)
    cd["posts"]["USAG Italy, Italy"]["oha"] = [[[r2(0.9 * w[g]), r2(0.75 * uw)] for g in grades], [[w[g], uw] for g in grades]]
    apply_buchanan(cd, grades)
    cola_raw = apply_cola(cd)
    out = json.dumps(cd, separators=(",", ":"), ensure_ascii=False) + ("\n" if raw.endswith("\n") else "")
    return raw, out, cola_raw, cola_age

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
    raw, out, cola_raw, cola_age = build()
    js, ix = bust(out)
    same = raw == out and (ROOT / "assets/pcs.js").read_text(encoding="utf-8") == js and (ROOT / "index.html").read_text(encoding="utf-8") == ix
    if "--check" in sys.argv:
        print("calc-data OK" if same else "calc-data OUT OF DATE (run tools/calc_oha.py)")
        print("COLA %s (%d days old) Wiesbaden E-5 / 2 dependents raw monthly $%.2f (index %s); Buchanan without-dependents basis: %s" % (
            COLA_AS_OF, cola_age, round(cola_raw + 1e-9, 2), COLA_INDEX["USAG Wiesbaden, Germany"], BUCHANAN_OHA_BASIS))
        sys.exit(0 if same else 1)
    if not same:
        CD.write_text(out, encoding="utf-8")
        (ROOT / "assets/pcs.js").write_text(js, encoding="utf-8")
        (ROOT / "index.html").write_text(ix, encoding="utf-8")
    print("calc-data OHA + COLA synced" + ("" if not same else " (no change)")
          + "; Wiesbaden E-5 / 2 dep raw $%.2f" % round(cola_raw + 1e-9, 2))

if __name__ == "__main__":
    main()
