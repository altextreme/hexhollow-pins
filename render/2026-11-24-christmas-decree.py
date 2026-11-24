"""Topical pin: the 1659 Massachusetts Bay law against Christmas, drawn as a posted decree. Photo-free, 1000x2100.

Facts (checked Nov 23 2026):
  1659: the Massachusetts Bay General Court fined anyone "observing any such day as Christmas or the like,
        either by forbearing of labor, feasting, or any other way" five shillings for every such offense.
        The law opens "For preventing disorders arising in several places within this jurisdiction".
        (Mass Moments, "Christmas Celebration Outlawed"; New England Today, "How the Puritans Banned
        Christmas", which quotes the law; History.com, "When Massachusetts Banned Christmas".)
  1681: repealed under pressure from the government in London (Mass Moments; History.com).
  Salem, 1679 (Mass Moments): "On the night of December 25th" four men entered farmer John Rowden's home,
        demanded the Rowdens' pear wine and were repeatedly refused; they pretended to leave, returned and
        demanded money; "Turned out again", they threw "stones, bones, and other things" at the house.
Icons: game-icons.net, CC BY 3.0 (Lorc, Delapouite); credited in the Buffer description.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
from lib.icons import icon
from PIL import Image, ImageDraw, ImageFont

W, H = 1000, 2100
F = 'assets/fonts/'
FIELD = (46, 31, 24)        # Puritan "sadd colour": deep walnut brown wool
LINEN = (238, 229, 212)     # headline
DIM = (178, 160, 144)       # deck, Salem captions, sources
PAPER = (233, 220, 194)     # the posted notice, flat
INK = (46, 31, 24)          # ink on the notice: the field's own brown
INK2 = (104, 82, 66)        # secondary ink on the notice
NAIL = (30, 20, 15)         # iron nail heads
SEAL = (150, 38, 30)        # the one accent: the 5s stamps

im = Image.new('RGBA', (W, H), FIELD + (255,))
d = ImageDraw.Draw(im)


def font(name, size):
    return ImageFont.truetype(F + name, size)


M = 72
gar6 = lambda s: font('eb-garamond-latin-600-normal.woff', s)
gar4 = lambda s: font('eb-garamond-latin-400-normal.woff', s)
inter = lambda w, s: font(f'inter-latin-{w}-normal.woff', s)

# Headline, top third: cap top on the margin
head = gar6(150)
cap_top = d.textbbox((0, 0), 'T', font=head, anchor='ls')[1]
LEAD = 134
base = M - cap_top
for ln in ['The Puritans', 'canceled', 'Christmas']:
    d.text((M - 4, base), ln, font=head, fill=LINEN, anchor='ls')
    last = base
    base += LEAD
d.text((M, last + 52), 'Massachusetts Bay, 1659 to 1681', font=inter(400, 34), fill=DIM, anchor='lt')

# The posted notice: a flat sheet, full width inside the margins, nailed at the corners
NX0, NX1 = M, W - M
NY0 = last + 150
NY1 = NY0 + 950
d.rectangle((NX0, NY0, NX1, NY1), fill=PAPER)
for nx, ny in ((NX0 + 30, NY0 + 30), (NX1 - 30, NY0 + 30), (NX0 + 30, NY1 - 30), (NX1 - 30, NY1 - 30)):
    d.ellipse((nx - 9, ny - 9, nx + 9, ny + 9), fill=NAIL)

P = NX0 + 64                       # text start inside the notice
y = NY0 + 78
caps = inter(600, 30)
label = 'BY ORDER OF THE GENERAL COURT'
x = P
for ch in label:                   # tracked caps, the smallest tier only
    d.text((x, y), ch, font=caps, fill=INK2, anchor='lt')
    x += d.textlength(ch, font=caps) + 4
y += 64
d.text((P, y), '“For preventing disorders”', font=gar6(60), fill=INK, anchor='lt')
y += 92
d.text((P, y), 'Anyone found observing Christmas by:', font=inter(400, 32), fill=INK2, anchor='lt')
y += 70
d.line((P, y, NX1 - 64, y), fill=INK2, width=2)

rows = [
    ('gi:axe-in-stump', '“Forbearing of labor”', 'Taking the day off'),
    ('gi:roast-chicken', '“Feasting”', 'Christmas dinner'),
    ('gi:sing', '“Or any other way”', 'Vibes, presumably'),
]
RH = 176
ICON = 116
STAMP = 132
for i, (ic_id, term, plain) in enumerate(rows):
    ry = y + i * RH
    cy = ry + RH // 2
    ic = icon(ic_id, ICON, INK)
    im.alpha_composite(ic, (P, cy - ICON // 2))
    tx = P + ICON + 36
    d.text((tx, cy - 6), term, font=gar6(46), fill=INK, anchor='ls')
    d.text((tx, cy + 16), plain, font=inter(400, 32), fill=INK2, anchor='lt')
    # the stamp: a flat seal-red ring with the fine
    sx = NX1 - 64 - STAMP // 2
    d.ellipse((sx - STAMP // 2, cy - STAMP // 2, sx + STAMP // 2, cy + STAMP // 2), outline=SEAL, width=6)
    d.text((sx, cy + 4), '5s', font=gar6(64), fill=SEAL, anchor='mm')
    d.line((P, ry + RH, NX1 - 64, ry + RH), fill=INK2, width=2)

fy = y + 3 * RH + 66
d.text((P, fy), 'Each offense: five shillings', font=gar6(48), fill=SEAL, anchor='ls')

# Salem, Christmas night 1679, in four steps
sy = NY1 + 96
d.text((M, sy), 'Salem, Christmas night 1679', font=gar6(52), fill=LINEN, anchor='ls')
steps = [
    ('gi:pear', 'Refused', 'pear wine'),
    ('gi:two-coins', 'Came back', 'for money'),
    ('gi:exit-door', 'Turned', 'out again'),
    ('gi:stone-pile', 'Pelted the', 'house'),
]
COLW = (W - 2 * M) / 4
SI = 104
iy = sy + 44
for i, (ic_id, a, b) in enumerate(steps):
    cx = M + COLW * i
    ic = icon(ic_id, SI, LINEN)
    im.alpha_composite(ic, (int(cx), iy))
    d.text((cx, iy + SI + 22), a, font=inter(400, 30), fill=DIM, anchor='lt')
    d.text((cx, iy + SI + 62), b, font=inter(400, 30), fill=DIM, anchor='lt')

# Footer
FY = H - M - 26
d.text((M, FY), 'Sources: Mass Moments, New England Today', font=inter(400, 30), fill=DIM, anchor='lm')
mono = Image.open('assets/hh-monogram-white-140.png').convert('RGBA')
mono = mono.resize((int(mono.width * 52 / mono.height), 52), Image.LANCZOS)
tint = Image.new('RGBA', mono.size, DIM + (255,))
tint.putalpha(mono.getchannel('A'))
im.alpha_composite(tint, (W - M - mono.width, FY - 26))

im.convert('RGB').save(os.environ['PIN_OUT'], 'JPEG', quality=82, optimize=True)
