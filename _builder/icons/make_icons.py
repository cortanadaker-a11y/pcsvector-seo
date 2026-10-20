#!/usr/bin/env python3
"""Render the PCS Vector favicon set from the logo mark pcs_icon_A_512.png
(gold compass star + arrow on #121E16, 512x512, PCS Vector's own artwork).
Needs: Pillow.   Usage: python3 make_icons.py <site_root>
"""
import base64, io, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'pcs_icon_A_512.png')
out = sys.argv[1] if len(sys.argv) > 1 else '.'
src = Image.open(SRC).convert('RGBA')
def r(px): return src.resize((px, px), Image.LANCZOS)
r(48).save(os.path.join(out, 'favicon.ico'), format='ICO', sizes=[(16, 16), (32, 32), (48, 48)], append_images=[r(16), r(32)])
r(48).save(os.path.join(out, 'favicon-48x48.png'), optimize=True)
r(192).save(os.path.join(out, 'favicon-192x192.png'), optimize=True)
r(180).convert('RGB').save(os.path.join(out, 'apple-touch-icon.png'), optimize=True)  # opaque bg already
b = io.BytesIO(); r(192).convert('RGB').save(b, 'PNG', optimize=True)
svg = ('<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 192 192" width="192" height="192">'
       '<!-- PCS Vector logo mark (raster embedded) -->'
       '<image width="192" height="192" href="data:image/png;base64,%s" xlink:href="data:image/png;base64,%s"/></svg>\n')
d = base64.b64encode(b.getvalue()).decode()
open(os.path.join(out, 'favicon.svg'), 'w').write(svg % (d, d))
open(os.path.join(out, 'favicon-LICENSE.txt'), 'w').write(
    'favicon.ico, favicon.svg, favicon-48x48.png, favicon-192x192.png, apple-touch-icon.png\n'
    'are rendered from the PCS Vector logo mark (original artwork, 2026). No third-party assets.\n')
print('icons written to', out)
