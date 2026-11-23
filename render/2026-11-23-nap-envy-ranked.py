"""Topical pin: average hours of sleep a day, ranked on one 24-hour scale. Photo-free.

Source: Neuroscience for Kids, University of Washington (Chudler), "Animal Sleep" table, adapted from
Siegel 2022, Campbell and Tobler 1984, Gravett et al. 2017 and others: brown bat 19.9 h, tiger 15.8 h,
cat 12.1 h, adult human 8 h, wild African elephant 2.1 h.
"""
import os
from PIL import Image, ImageDraw, ImageFont
from lib.icons import icon

W, H = 1000, 1500
F = 'assets/fonts/'
FIELD = (222, 214, 232)     # pale 3 AM lilac
INK = (44, 30, 58)          # aubergine ink, headline and icons
VIOLET = (98, 64, 140)      # the one accent: the numbers
MUTED = (100, 88, 116)      # small text
RULE = (160, 146, 178)      # scale ticks

im = Image.new('RGBA', (W, H), FIELD + (255,))
d = ImageDraw.Draw(im)


def font(name, size):
    return ImageFont.truetype(F + name, size)


M = 64
# Headline, flush left
hf = font('fraunces-latin-900-normal.woff', 132)
d.text((M, 64), 'Your nap', font=hf, fill=INK)
d.text((M, 204), 'envy, ranked', font=hf, fill=INK)
sf = font('inter-latin-400-normal.woff', 36)
d.text((M, 380), 'Average hours of sleep in a day', font=sf, fill=MUTED)

# One vertical 24-hour scale
RX = 176
Y24, Y0 = 500, 1310
PPH = (Y0 - Y24) / 24


def yh(h):
    return Y0 - h * PPH


d.rectangle([RX - 2, Y24, RX + 2, Y0], fill=INK)
tf = font('inter-latin-500-normal.woff', 30)
for h in (0, 6, 12, 18, 24):
    y = yh(h)
    d.rectangle([RX - 16, y - 1, RX + 2, y + 1], fill=INK)
    lab = f'{h} h'
    d.text((RX - 28, y), lab, font=tf, fill=MUTED, anchor='rm')

items = [
    ('gi:bat--delapouite', 19.9, 'Brown bat'),
    ('gi:tiger-head', 15.8, 'Tiger'),
    ('gi:cat', 12.1, 'House cat'),
    ('gi:person', 8, 'Adult human'),
    ('gi:elephant', 2.1, 'Wild elephant'),
]
IC = 112
IX = 236
NX = 384
nf = font('fraunces-latin-900-normal.woff', 76)
lf = font('inter-latin-500-normal.woff', 38)
for iid, hrs, name in items:
    y = yh(hrs)
    d.ellipse([RX - 9, y - 9, RX + 9, y + 9], fill=VIOLET)
    d.rectangle([RX + 9, y - 1, IX - 16, y + 1], fill=RULE)
    ic = icon(iid, IC, INK)
    bb = ic.getbbox()
    gw, gh = bb[2] - bb[0], bb[3] - bb[1]
    im.alpha_composite(ic, (int(IX + (IC - gw) / 2 - bb[0]), int(y - gh / 2 - bb[1])))
    num = f'{hrs:g}'
    # number: optical centre on the line
    nb = d.textbbox((0, 0), num, font=nf, anchor='ls')
    cap = -nb[1]
    d.text((NX, y + cap / 2), num, font=nf, fill=VIOLET, anchor='ls')
    nw = d.textlength(num, font=nf)
    hb = d.textbbox((0, 0), 'h', font=lf, anchor='ls')
    d.text((NX + nw + 12, y + cap / 2), 'h', font=lf, fill=VIOLET, anchor='ls')
    d.text((620, y), name, font=lf, fill=INK, anchor='lm')

# Footer
ff = font('inter-latin-400-normal.woff', 30)
FY = H - 64 - 64
d.text((M, FY + 32), 'Source: UW Neuroscience for Kids', font=ff, fill=MUTED, anchor='lm')
mono = Image.open('assets/hh-monogram-white-140.png').convert('RGBA')
mono = mono.resize((int(mono.width * 64 / mono.height), 64), Image.LANCZOS)
tint = Image.new('RGBA', mono.size, INK + (255,))
tint.putalpha(mono.getchannel('A'))
wf = font('inter-latin-600-normal.woff', 32)
word = 'Hex & Hollow'
ww = d.textlength(word, font=wf)
lx = int(W - M - ww - 14 - mono.width)
im.alpha_composite(tint, (lx, FY))
d.text((lx + mono.width + 14, FY + 32), word, font=wf, fill=INK, anchor='lm')

im.convert('RGB').save(os.environ['PIN_OUT'], 'JPEG', quality=82)
