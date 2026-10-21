#!/usr/bin/env python3
"""21 Oct 2026: guard after PR #33 shipped a changed pcs.js under the old ?v= (iPhones kept stale JS, form opened without name/email).
Run against the deploy (main) tree before pushing: python3 _builder/check_cache_bust.py /path/to/main-checkout
Fails if index.html's ?v= for pcs.js / pcs.css is not the sha256[:10] of the file (same rule as gen_site.py)."""
import hashlib, re, sys
root = (sys.argv[1] if len(sys.argv) > 1 else '.').rstrip('/') + '/'
ix = open(root + 'index.html').read(); bad = 0
for a in ('pcs.js', 'pcs.css'):
    want = hashlib.sha256(open(root + 'assets/' + a, 'rb').read()).hexdigest()[:10]
    got = re.findall(r'/assets/' + re.escape(a) + r'\?v=([0-9a-f]+)', ix)
    ok = got and all(g == want for g in got); bad += not ok
    print(('OK  ' if ok else 'FAIL') + f' {a} index v={got} content={want}')
sys.exit(1 if bad else 0)
