"""Topical pin: the 1659 Massachusetts Bay law against Christmas, drawn as a posted decree. Photo-free, 1000x2100. v3: fines spelled out as stamps.

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
LEAD = 130
base = M - cap_top
for ln in ['The Puritans', 'canceled', 'Christmas']:
    d.text((M - 4, base), ln, font=head, fill=LINEN, anchor='ls')
    last = base
    base += LEAD
d.text((M, last + 52), 'Massachusetts Bay, 1659 to 1681', font=inter(400, 34), fill=DIM, anchor='lt')

# The posted notice: a flat sheet, full width inside the margins
NX0, NX1 = M, W - M
NY0 = last + 150
NY1 = NY0 + 940                    # set again below once the content height is known

P = NX0 + 64                       # text start inside the notice
RH = 176
FINE_GAP = 48                      # rule to the fine line's cap top, same as the rows get
fine_font = gar6(48)
fine_cap = -d.textbbox((0, 0), 'E', font=fine_font, anchor='ls')[1]
fine_desc = d.textbbox((0, 0), 'g', font=fine_font, anchor='ls')[3]
y0 = NY0 + 78
rows_top = y0 + 64 + 92 + 70
fine_base = rows_top + 3 * RH + FINE_GAP + fine_cap
NY1 = fine_base + fine_desc + 66   # bottom padding close to the top
d.rectangle((NX0, NY0, NX1, NY1), fill=PAPER)
y = y0
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
    ('gi:musical-notes', '“Or any other way”', 'Vibes, presumably'),
]
ICON = 104
SW, SH = 166, 120                  # the stamp: a flat seal-red frame with the fine spelled out
for i, (ic_id, term, plain) in enumerate(rows):
    ry = y + i * RH
    cy = ry + RH // 2
    ic = icon(ic_id, ICON, INK)
    im.alpha_composite(ic, (P, cy - ICON // 2))
    tx = P + ICON + 28
    d.text((tx, cy - 6), term, font=gar6(46), fill=INK, anchor='ls')
    d.text((tx, cy + 16), plain, font=inter(400, 32), fill=INK2, anchor='lt')
    sx1 = NX1 - 64
    sx0 = sx1 - SW
    d.rounded_rectangle((sx0, cy - SH // 2, sx1, cy + SH // 2), radius=12, outline=SEAL, width=5)
    scx = (sx0 + sx1) / 2
    d.text((scx, cy + 6), '5', font=gar6(64), fill=SEAL, anchor='ms')
    d.text((scx, cy + 16), 'shillings', font=inter(600, 30), fill=SEAL, anchor='mt')
    d.line((P, ry + RH, NX1 - 64, ry + RH), fill=INK2, width=2)

d.text((P, fine_base), 'Each offense: five shillings', font=fine_font, fill=SEAL, anchor='ls')

# Salem, Christmas night 1679, in four steps
sy = NY1 + 90
d.text((M, sy), 'Salem wassailers, Christmas night 1679', font=gar6(48), fill=LINEN, anchor='ls')
steps = [
    ('gi:pear', 'Denied the', 'pear wine'),
    ('gi:two-coins', 'Came back', 'for money'),
    ('gi:exit-door', 'Turned', 'out again'),
    ('gi:stone-pile', 'Pelted the', 'house'),
]
COLW = (W - 2 * M) / 4
SI = 108
iy = sy + 46
lab = inter(400, 34)
for i, (ic_id, a, b) in enumerate(steps):
    cx = M + COLW * i
    ic = icon(ic_id, SI, LINEN)
    ink = ic.getchannel('A').getbbox()          # align the visible ink, not the box, to the label edge
    im.alpha_composite(ic, (int(cx) - ink[0], iy))
    d.text((cx, iy + SI + 22), a, font=lab, fill=DIM, anchor='lt')
    d.text((cx, iy + SI + 66), b, font=lab, fill=DIM, anchor='lt')

# Footer
FY = H - M - 26
d.text((M, FY), 'Sources: Mass Moments, New England Today', font=inter(400, 30), fill=DIM, anchor='lm')
mono = Image.open('assets/hh-monogram-white-140.png').convert('RGBA')
mono = mono.resize((int(mono.width * 52 / mono.height), 52), Image.LANCZOS)
tint = Image.new('RGBA', mono.size, DIM + (255,))
tint.putalpha(mono.getchannel('A'))
im.alpha_composite(tint, (W - M - mono.width, FY - 26))

im.convert('RGB').save(os.environ['PIN_OUT'], 'JPEG', quality=82, optimize=True)
