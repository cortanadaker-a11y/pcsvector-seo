# pcsvector-seo
PCS Vector static SEO pages (unofficial/personal) - BAH hub and fort pages

Maintenance scripts (sitemap lastmod, guide builder, site checker): see `tools/README.md`.

The calculator on the homepage matches `main`: its inputs, results, lead forms, and `assets/pcs.js`, `assets/pcs.css`, and `assets/calc-data.json` stay unchanged. Content beneath the calculator lives in `<!-- home-extra:start -->` … `<!-- home-extra:end -->`. `tools/build_guides.py` replaces only that block and does not write any other part of `index.html`. Styling for the block is `assets/home-extra.css`.
