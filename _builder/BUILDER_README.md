# PCS Vector static site builder (branch `builder-src`, NOT served)

Pages serves `main` (root). This branch only holds the generator + tests used to produce it (11 Oct 2026).
Paths in scripts assume the box layout: builder at /workspace/build_v2, output /workspace/site_v2,
pcs-vector checkout at /workspace/pcs-vector-repo (source of truth for rates/logic).

Rebuild:
  python3 export_calc.py   # calc-data.json + gas-table.json from pcs-vector services (live EIA gas)
  python3 build.py         # BAH hub + post pages (+ number check: PASS 1005)
  python3 gen_site.py      # index.html (Streamlit-identical UI), assets, sitemap, favicon

Validate:
  python3 test/gen_cases.py && node test/parity.js test/cases.json test/expected.json   # 98,582 cases vs real Python renderer
  node test/prefill_js.js                                                               # Google Form prefill URL vs Python (1,428)
  node tools/func.cjs http://localhost:8765/                                            # 67 browser checks
  python3 tools/links.py                                                                # links + SEO basics
  node tools/rects.cjs 1280|390                                                         # layout vs live Streamlit
Deploy: push site_v2/* to main (keep CNAME).

Accuracy audit vs DTMO (added 11 Oct 2026, run from /workspace/accuracy_audit with these scripts):
  accuracy/dtmo.py         # read-only scrapers for the public DTMO neorates OHA + Overseas COLA calculators
  accuracy/pull.py         # all OHA cells (8 localities x 24 grades x with/without) + COLA indices for 12 codes
  accuracy/harvest_cola.py # DTMO annual-compensation bracket per grade x YOS x with/without/barracks (1,584 queries)
  accuracy/cola_check.py   # 260 random COLA cases vs DTMO calculator
  accuracy/apply_fixes.py  # writes pcs-vector data/*.json from the pulls + DTMO BAH ASCII (BAH-ASCII-2026.zip)
Refresh cadence: OHA FX + foreign COLA indices change on the 1st and 16th of each month (DTMO). Re-run pull.py + apply_fixes.py, then rebuild.

OHA pages (added 19 Oct 2026): /oha/ hub + /oha/{korea,japan,okinawa,germany}/
  python3 oha/pull_oha_live.py                                        # live DTMO OHA pull (11 localities x 24 grades x with/without), pay period set in the script
  python3 oha/gen_oha.py <site_root> oha/dtmo_oha_live_2026-10-19.json  # run AFTER build.py/gen_site.py; idempotently re-adds the /bah/ hub OHA link + sitemap URLs
  python3 oha/check_numbers.py <site_root> oha/dtmo_oha_live_2026-10-19.json   # every number on the OHA pages vs DTMO JSON + calc-data (must be 0 mismatches)
  node oha/oha_browser.cjs http://127.0.0.1:<port>                    # tgt preselect, console errors, 390px overflow
  gen_oha.py never touches index.html. Update TODAY/CHECKED in gen_oha.py on each refresh (1st/16th).
