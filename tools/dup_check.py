#!/usr/bin/env python3
"""Duplicate-content metric used in the PCS Vector PRs (same method as the Devil review script).

For each page: take the visible text (scripts, styles, nav, header, footer removed), lowercase it, drop numbers
and $ amounts, cut it into overlapping 6-word shingles.  "overlap" = share of the page's shingles that also
appear on at least one other page in the same set.  Lower is better.

usage:
  python3 tools/dup_check.py BASE_DIR HEAD_DIR          # whole-page overlap for the 27 BAH pages, base vs head
  python3 tools/dup_check.py --guide-section HEAD_DIR   # overlap of only the PCS-guide section + its FAQ block
BASE_DIR / HEAD_DIR are checked-out site trees (for example `git archive <sha> | tar -x -C dir`).
"""
import re, sys, glob, os, collections, statistics
from bs4 import BeautifulSoup

def words(html):
    s = BeautifulSoup(html, "lxml")
    for t in s(["script", "style", "noscript", "nav", "header", "footer"]): t.decompose()
    t = (s.body or s).get_text(" ").lower().replace("\u2019", "'")
    t = re.sub(r"[\u2212-]?\$[\d,.]+|[\u20a9\u00a5\u20ac][\d,.]+|\b\d[\d,./:-]*\b", " ", t)
    return re.sub(r"[^a-z' ]", " ", t).split()

def shingles(w, k=6): return {" ".join(w[i:i + k]) for i in range(len(w) - k + 1)}

def overlap(texts):
    S = {k: shingles(w) for k, w in texts.items()}; c = collections.Counter()
    for s in S.values(): c.update(s)
    return {k: (len(texts[k]), round(100 * sum(1 for x in s if c[x] > 1) / len(s), 1) if s else 0.0) for k, s in S.items()}

def bah_pages(root, guide_only=False):
    out = {}
    for f in sorted(glob.glob(root + "/bah/*/index.html")):
        k = f.split("/")[-2]; h = open(f, encoding="utf-8").read()
        if guide_only:
            g = BeautifulSoup(h, "lxml").find("section", id="pcs-guide")
            if not g: continue
            m = re.search(r"<!--pcsv:faq-->(.*?)<!--/pcsv:faq-->", h, re.S)
            h = str(g) + (m.group(1) if m else "")
        out[k] = words(h)
    return out

if __name__ == "__main__":
    if sys.argv[1] == "--guide-section":
        r = overlap(bah_pages(sys.argv[2], True))
        print("guide sections: %d | mean words %.0f | mean overlap %.1f%% | max %.1f%%" % (len(r), statistics.mean(v[0] for v in r.values()), statistics.mean(v[1] for v in r.values()), max(v[1] for v in r.values())))
    else:
        rb, rh = overlap(bah_pages(sys.argv[1])), overlap(bah_pages(sys.argv[2]))
        print("BAH pages: base %d, head %d | mean overlap base %.1f%% -> head %.1f%% | mean words %.0f -> %.0f" % (
            len(rb), len(rh), statistics.mean(v[1] for v in rb.values()), statistics.mean(v[1] for v in rh.values()),
            statistics.mean(v[0] for v in rb.values()), statistics.mean(v[0] for v in rh.values())))
        for k in sorted(rh): print("  %-36s words %5d -> %5d   overlap %5.1f -> %5.1f" % (k, rb.get(k, (0, 0))[0], rh[k][0], rb.get(k, (0, 0))[1], rh[k][1]))
