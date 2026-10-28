# tools/ — site maintenance scripts (stdlib + bs4/requests only)

| Script | What it does |
|---|---|
| `build_guides.py` | Idempotent post-processor. Adds PCS-guide sections, FAQ entries, "More for your move" blocks, the homepage "Browse by fort" section, `/guides/*` pages, 404 links, and `scope="col"` on table headers. Re-running replaces the blocks between `<!--pcsv:NAME-->` markers. |
| `sitemap.py` | Rebuilds `sitemap.xml`. `lastmod` = date the page's content hash last changed (ledger in `lastmod.json`, no git history needed). Also run by the weekly gas-refresh workflow. `--check` for CI. |
| `dup_check.py` | Duplicate-content metric (6-word shingles, numbers removed) for the BAH pages: `dup_check.py BASE_DIR HEAD_DIR`, or `--guide-section DIR` for the guide block only. |
| `check_site.py` | Local audit: self-canonical on `https://pcsvector.com`, one h1, GoatCounter once, OG/Twitter tags, JSON-LD parses (+ breadcrumbs), alt text, internal links + `#fragments`, sitemap coverage, homepage links to every BAH/OHA/guide page, `og:site_name` = PCS Vector, the tagline on every page, one WebSite JSON-LD node on the homepage, favicon link set and icon sizes, and no `streamlit` string anywhere in the published tree. `--external` also GETs external links. |

```
python3 tools/build_guides.py && python3 tools/sitemap.py && python3 tools/check_site.py
```

## Adding a per-installation guide (the template)
1. Read the installation's **official** housing/newcomers pages (garrison page on home.army.mil or Military OneSource "MilitaryINSTALLATIONS").
2. Add each page to `SOURCES` in `tools/guides/guide_data.py` (or `guide_data_batch2.py`, merged at import).
3. Copy an entry in `GUIDES` (key = the `/bah/<slug>/` folder). Every `checklist` / `housing` / `area` line is `(text, [source keys])`.
4. **Never type BAH/OHA dollar amounts.** The builder reads them from the page's existing DTMO table; `faq` templates take `{E5w}`, `{O6o}`, `{bah_line}` etc.
5. Set `AS_OF` to the date you read the sources, run the three commands above, open a PR.
Pages currently done: all 27 BAH pages (9 in `guide_data.py`, 18 in `guide_data_batch2.py`); OHA: Korea, Japan, Germany, Okinawa. Batch 2 sources are Military OneSource (MilitaryINSTALLATIONS) housing, temporary housing and check-in pages read on 28 Oct 2026. The JBER and Schofield pages live under `joint-base-elmendorf-richardson-jber` and `schofield-barracks-fort-shafter` there.

Housing-office pages change; re-read before bumping `AS_OF`. OHA tables on `/oha/*` are refreshed by hand from DTMO each pay period (1st and 16th).

## Rules the builder enforces
- `check_site.py` fails if an FAQPage JSON-LD question is not visible on the page; `build_guides.py` prunes hidden ones.
- `dateModified` and sitemap `lastmod` move only for pages with substantive content changes. For cosmetic-only changes (nav links) run `python3 tools/sitemap.py --keep-date=YYYY-MM-DD:/url/,/url2/` once.
- OHA pages carry an "As of <pay period>; OHA updates the 1st and 16th" note (`<!--pcsv:asof-->`). Spot-check at least E-5 with dependents per area against DTMO's OHA lookup before changing the date.
- MIHA on the OHA pages: DTMO returned the same MIHA with and without dependents for all 11 areas (16 Oct 2026 pay period, read 28 Oct 2026). On each refresh re-read both cases; `check_site.py` fails on a dash cell in a MIHA row.

## Brand and site name
- Tagline, exactly: `For Soldiers; By Soldiers`. It is in every footer and in the homepage copy. Keep the not-official disclaimer and "Military-approved" wording. `build_guides.py` (`build_brand`) writes both.
- The homepage JSON-LD has one `WebSite` node (name `PCS Vector`, url, alternateName) for Google's site-name feature; every page has `og:site_name` = `PCS Vector`. Google may take days to weeks to recrawl; request indexing of `https://pcsvector.com/` in Search Console.
