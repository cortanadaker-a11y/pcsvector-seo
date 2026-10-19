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

BAH base pages, batch 2 (added 19 Oct 2026): /bah/{fort-stewart,fort-benning,joint-base-san-antonio,fort-riley,fort-knox,
fort-leonard-wood,fort-polk,fort-sill,fort-wainwright,fort-huachuca,fort-irwin,schofield-barracks}/ (same format as /bah/fort-bragg/)
  python3 bah_bases/pull_bah_live.py bah_bases/dtmo_bah_live_2026-10-19.json     # live DTMO BAH Rate Lookup, 12 anchor ZIPs x 24 grades (read-only)
  python3 bah_bases/gen_bah_bases.py <site_root> <ascii_dir> <pcs-vector repo>   # writes ONLY the 12 pages + /bah/ hub rows + sitemap URLs (idempotent)
  python3 bah_bases/check_bah_bases.py <site_root> <ascii_dir> <pcs-vector repo> bah_bases/dtmo_bah_live_2026-10-19.json <bah2026_with.pdf> <bah2026_without.pdf> [log]
        # every $ on each page re-derived from DTMO ASCII + PDF + live lookup + app bah_2026.json + calc-data.json + rent/util data (must be 0 mismatches)
  python3 bah_bases/links_local.py <site_root> http://127.0.0.1:<port>          # internal links + SEO basics
  node bah_bases/bah_browser.cjs http://127.0.0.1:<port>                        # 200, console errors, 390px overflow, tgt preselect, E-5 BAH in results
  Box paths used 19 Oct: ascii_dir=/workspace/scratch/bah2026, PDFs=/workspace/raw/pcs/bah2026_{with,without}.pdf, repo=/workspace/pcs-vector-repo.
  WARNING: build.py and gen_site.py regenerate index.html (home page). index.html must stay byte-identical (Zak's hard rule);
  do not run them against the served tree for page additions. gen_bah_bases.py and gen_oha.py never touch index.html.

BAH base pages, deepen the 8 original posts (added 19 Oct 2026): /bah/{fort-bragg,fort-hood,fort-campbell,fort-carson,joint-base-lewis-mcchord,fort-drum,fort-bliss,national-capital-region}/
  python3 bah_deepen/pull_bah_yoy.py bah_deepen/dtmo_bah_yoy_2026-10-19.json      # live DTMO BAH Rate Lookup, YEAR=25 and YEAR=26, 8 ZIPs x 24 grades (read-only)
  python3 bah_deepen/gen_bah_deepen.py <site_root> bah_deepen/dtmo_bah_yoy_2026-10-19.json   # as-of stamp, 2026 vs 2025 table, 19-base Other posts, dateModified/source, sitemap lastmod (idempotent; never touches index.html)
  python3 bah_deepen/check_bah_deepen.py <site_root> bah_deepen/dtmo_bah_yoy_2026-10-19.json /workspace/scratch/bah2026   # must be 0 mismatches
  node bah_deepen/deepen_browser.cjs http://127.0.0.1:<port>                      # 200, console, overflow 1280/390, yoy rows, other posts=19
  At the 2027 refresh, change YEAR to 26/27 and update TODAY/CHECKED in the generator.
