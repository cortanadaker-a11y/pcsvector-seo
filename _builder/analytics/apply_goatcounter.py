#!/usr/bin/env python3
"""Insert GoatCounter tag on its own line before </head> in every built page (idempotent, no other change).
Usage: python3 apply_goatcounter.py <site_root>"""
import glob, os, sys
TAG = '<script data-goatcounter="https://pcsvector.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>'
root = sys.argv[1] if len(sys.argv) > 1 else '.'
for f in sorted(glob.glob(os.path.join(root, '**/*.html'), recursive=True)):
    if '/_builder/' in f: continue
    s = open(f, encoding='utf-8').read()
    if TAG in s: print('ok (already)', f); continue
    assert s.count('</head>') == 1, f
    i = s.index('</head>'); pre = '' if i == 0 or s[i-1] == '\n' else '\n'
    open(f, 'w', encoding='utf-8').write(s[:i] + pre + TAG + '\n' + s[i:]); print('tagged', f)
