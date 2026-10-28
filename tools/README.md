# tools/ — site maintenance scripts (stdlib + bs4/requests only)

| Script | What it does |
|---|---|
| `build_guides.py` | Idempotent post-processor. Adds PCS-guide sections, FAQ entries, "More for your move" blocks, the homepage "Browse by fort" section, `/guides/*` pages, 404 links, and `scope="col"` on table headers. Re-running replaces the blocks between `<!--pcsv:NAME-->` markers. |
| `sitemap.py` | Rebuilds `sitemap.xml`. `lastmod` = date the page's content hash last changed (ledger in `lastmod.json`, no git history needed). Also run by the weekly gas-refresh workflow. `--check` for CI. |
| `check_site.py` | Local audit: self-canonical on `https://pcsvector.com`, one h1, GoatCounter once, OG/Twitter tags, JSON-LD parses (+ breadcrumbs), alt text, internal links + `#fragments`, sitemap coverage, homepage links to every BAH/OHA/guide page. `--external` also GETs external links. |

```
python3 tools/build_guides.py && python3 tools/sitemap.py && python3 tools/check_site.py
```

## Adding a per-installation guide (the template)
1. Read the installation's **official** housing/newcomers pages (garrison page on home.army.mil or Military OneSource "MilitaryINSTALLATIONS").
2. Add each page to `SOURCES` in `tools/guides/guide_data.py`.
3. Copy an entry in `GUIDES` (key = the `/bah/<slug>/` folder). Every `checklist` / `housing` / `area` line is `(text, [source keys])`.
4. **Never type BAH/OHA dollar amounts.** The builder reads them from the page's existing DTMO table; `faq` templates take `{E5w}`, `{O6o}`, `{bah_line}` etc.
5. Set `AS_OF` to the date you read the sources, run the three commands above, open a PR.
Pages currently done: Fort Sill, NCR/Fort Belvoir, JBSA, Fort Bliss, Fort Riley, Fort Campbell, Fort Bragg, Fort Hood, Fort Drum; OHA: Korea, Japan, Germany. The other 18 BAH pages only get the related-links block until someone adds their facts.

Housing-office pages change; re-read before bumping `AS_OF`. OHA tables on `/oha/*` are refreshed by hand from DTMO each pay period (1st and 16th).

## Rules the builder enforces
- `check_site.py` fails if an FAQPage JSON-LD question is not visible on the page; `build_guides.py` prunes hidden ones.
- `dateModified` and sitemap `lastmod` move only for pages with substantive content changes. For cosmetic-only changes (nav links) run `python3 tools/sitemap.py --keep-date=YYYY-MM-DD:/url/,/url2/` once.
- OHA pages carry an "As of <pay period>; OHA updates the 1st and 16th" note (`<!--pcsv:asof-->`). Spot-check at least E-5 with dependents per area against DTMO's OHA lookup before changing the date.
- MIHA on the OHA pages: DTMO returned the same MIHA with and without dependents for all 11 areas (16 Oct 2026 pay period, read 28 Oct 2026). On each refresh re-read both cases; `check_site.py` fails on a dash cell in a MIHA row.
