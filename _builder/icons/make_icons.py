#!/usr/bin/env python3
"""Render the compass emoji (U+1F9ED) favicon set from the Noto Color Emoji SVG.
Source: googlefonts/noto-emoji @ e20cbc2bbec1926686be9f9bee7d1d2cfa1fea0e, 2D/svg/emoji_u1f9ed.svg
License: Apache-2.0 (2D/svg/LICENSE, copied here as NOTO_EMOJI_SVG_LICENSE.txt).
Needs: rsvg-convert (librsvg2-bin), Pillow.   Usage: python3 make_icons.py <site_root>
"""
import os, subprocess, sys, tempfile
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'noto_emoji_u1f9ed.svg')
out = sys.argv[1] if len(sys.argv) > 1 else '.'
tmp = tempfile.mkdtemp()
def render(px):
    p = os.path.join(tmp, f'r{px}.png')
    subprocess.run(['rsvg-convert', '-w', str(px), '-h', str(px), SRC, '-o', p], check=True)
    return Image.open(p).convert('RGBA')
# favicon.ico: 16/32/48, each rendered natively from the vector (transparent)
r16, r32, r48 = render(16), render(32), render(48)
r48.save(os.path.join(out, 'favicon.ico'), format='ICO', sizes=[(16, 16), (32, 32), (48, 48)], append_images=[r16, r32])
r48.save(os.path.join(out, 'favicon-48x48.png'), optimize=True)
render(192).save(os.path.join(out, 'favicon-192x192.png'), optimize=True)
# apple-touch-icon: iOS fills transparency with black, so white square with ~8% padding
bg = Image.new('RGBA', (180, 180), (255, 255, 255, 255)); bg.alpha_composite(render(150), (15, 15))
bg.convert('RGB').save(os.path.join(out, 'apple-touch-icon.png'), optimize=True)
# favicon.svg: the Noto vector itself, with attribution
svg = open(SRC, encoding='utf-8').read()
svg = svg.replace('<!-- Generator: Adobe Illustrator 25.2.3, SVG Export Plug-In . SVG Version: 6.00 Build 0)  -->',
                  '<!-- Compass emoji U+1F9ED from Noto Emoji (github.com/googlefonts/noto-emoji), Copyright 2013 Google LLC, Apache License 2.0: https://www.apache.org/licenses/LICENSE-2.0 (see /favicon-LICENSE.txt) -->')
open(os.path.join(out, 'favicon.svg'), 'w', encoding='utf-8').write(svg)
lic = ('favicon.ico, favicon.svg, favicon-48x48.png, favicon-192x192.png, apple-touch-icon.png\n'
       'are rendered from the Noto Emoji compass (U+1F9ED) SVG, https://github.com/googlefonts/noto-emoji\n'
       '(2D/svg/emoji_u1f9ed.svg), Copyright 2013 Google LLC, licensed under the Apache License 2.0.\n'
       'Modifications: rasterized to PNG/ICO sizes; white background added to apple-touch-icon.\n\n')
open(os.path.join(out, 'favicon-LICENSE.txt'), 'w').write(lic + open(os.path.join(HERE, 'NOTO_EMOJI_SVG_LICENSE.txt')).read())
print('icons written to', out)
