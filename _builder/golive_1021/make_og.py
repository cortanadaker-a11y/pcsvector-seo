"""PCS Vector 1200x630 share card (og:image). UNOFFICIAL/PERSONAL. Usage: python3 make_og.py <icon_512.png> <out.png>"""
import sys
from PIL import Image, ImageDraw, ImageFont
F='/usr/share/fonts/truetype/sand-box/google/Inter/Inter-VariableFont_opsz,wght.ttf'
def font(sz, w):
    f=ImageFont.truetype(F, sz); f.set_variation_by_name(w); return f
BG=(0x12,0x1E,0x16); FG=(0xE8,0xEE,0xEA); GOLD=(0xD4,0xAF,0x37)
im=Image.new('RGB',(1200,630),BG); d=ImageDraw.Draw(im)
ic=Image.open(sys.argv[1]).convert('RGB').resize((300,300),Image.LANCZOS)
im.paste(ic,(90,165))
wb=font(104,'ExtraBold'); x=420; y=200
d.text((x,y),'PCS',font=wb,fill=FG); x2=x+d.textlength('PCS ',font=wb)
d.text((x2,y),'VECTOR',font=wb,fill=GOLD)
tf=font(38,'SemiBold')
d.text((426,345),'Know your BAH before you PCS',font=tf,fill=FG)
d.text((426,395),'— free, 2026 rates',font=tf,fill=GOLD)
d.rectangle((0,618,1200,630),fill=GOLD)
sf=font(24,'Medium'); d.text((426,470),'pcsvector.com · Unofficial — not affiliated with the Army or DoW',font=sf,fill=(0x9F,0xB0,0xA6))
im.save(sys.argv[2],optimize=True)
