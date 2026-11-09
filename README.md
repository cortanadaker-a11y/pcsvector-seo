# pcsvector-seo
PCS Vector static SEO pages (unofficial/personal) - BAH hub and fort pages

Maintenance scripts (sitemap lastmod, guide builder, site checker): see `tools/README.md`.

The homepage (`index.html`) and every file it loads are frozen to match `main`. `tools/build_guides.py` skips `index.html` and will not add links to it. Because of that freeze, `tools/check_site.py` does not require `/bah/by-zip/` or `/guides/tle-vs-tla/` to be linked from the homepage. Those two “not linked from the homepage” results are expected.
