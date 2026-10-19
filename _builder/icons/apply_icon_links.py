#!/usr/bin/env python3
"""Swap favicon link tags on an already-built site (no other change).
Sub-pages (bah/*, oha/*, 404): old '/favicon.svg' link -> full icon set (inline).
Home (index.html): ONLY the data-URI <link rel="icon"> line -> one tag per line. Hard rule: nothing else.
Usage: python3 apply_icon_links.py <site_root>
"""
import glob, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from icon_links import INLINE, HOME, HOME_OLD, SUB_OLD
root = sys.argv[1] if len(sys.argv) > 1 else '.'
home = os.path.join(root, 'index.html')
for f in sorted(glob.glob(os.path.join(root, '**/*.html'), recursive=True)):
    s = open(f, encoding='utf-8').read()
    if os.path.abspath(f) == os.path.abspath(home):
        if INLINE in s or HOME in s: print('ok (already)', f); continue
        lines = s.split('\n'); hits = [i for i, l in enumerate(lines) if l == HOME_OLD]
        assert len(hits) == 1 and s.count('rel="icon"') == 1, 'home: expected exactly one data-URI icon line'
        lines[hits[0]] = HOME; open(f, 'w', encoding='utf-8').write('\n'.join(lines)); print('home swapped', f)
    else:
        if INLINE in s: print('ok (already)', f); continue
        assert s.count(SUB_OLD) == 1 and s.count('rel="icon"') == 1, f'{f}: expected one /favicon.svg icon link'
        open(f, 'w', encoding='utf-8').write(s.replace(SUB_OLD, INLINE)); print('swapped', f)
