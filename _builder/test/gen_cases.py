import json, random, sys
D = json.load(open('/workspace/site_v2/assets/calc-data.json'))
posts = sorted(D['posts']); G = D['grades']; random.seed(int(sys.argv[2]) if len(sys.argv) > 2 else 7)
cases = []
cola_posts = [p for p in posts if D['posts'][p]['sys'] != 'BAH']
# systematic: every target x every grade x deps {0,1,3,5} x bar, vs Fort Campbell and Skip; yos sweep for COLA posts
for t in posts:
    for g in G:
        for d in (0, 1, 3, 5):
            for bar in (False, True):
                cases.append(dict(g=g, d=d, y=4, cur='Fort Campbell, KY', tgt=t, bar=bar))
for t in cola_posts:
    for g in G:
        for d in range(6):
            for y in range(0, 41):
                cases.append(dict(g=g, d=d, y=y, cur='', tgt=t, bar=(y % 2 == 1)))
# random pairs incl. OHA<->BAH, skip, same post
for _ in range(int(sys.argv[3]) if len(sys.argv) > 3 else 20000):
    cases.append(dict(g=random.choice(G), d=random.randint(0, 5), y=random.randint(0, 40), cur=random.choice(posts + ['']), tgt=random.choice(posts), bar=random.random() < .3))
json.dump(cases, open(sys.argv[1], 'w'))
print(len(cases))
