"""Topical pin: the 1659 Massachusetts Bay law against Christmas, set as a price list. Photo-free.

Facts (checked Nov 23 2026):
  1659: the Massachusetts Bay General Court fined anyone "observing any such day as Christmas or the like,
        either by forbearing of labor, feasting, or any other way" five shillings for every such offense.
        (Mass Moments, "Christmas Celebration Outlawed"; History.com, "When Massachusetts Banned Christmas";
        New England Today, "How the Puritans Banned Christmas", which quotes the law.)
  1681: repealed under pressure from the government in London (Mass Moments; History.com).
  1856: Christmas became a Massachusetts state holiday (Mass Moments; History.com).
  No records of any prosecution under the law (History.com, citing historian Stephen Nissenbaum).
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1000, 1500
F = 'assets/fonts/'
FIELD = (27, 48, 52)        # colonial blue-green, a cold New England winter
LINEN = (236, 230, 216)     # headline and the law's words
DIM = (154, 170, 168)       # translations, notes, sources
RULE = (62, 86, 88)         # hairlines and leader dots
AMBER = (230, 164, 82)      # the one accent: the price

im = Image.new('RGBA', (W, H), FIELD + (255,))
d = ImageDraw.Draw(im)


def font(name, size):
    return ImageFont.truetype(F + name, size)


M = 72
gar6 = lambda s: font('eb-garamond-latin-600-normal.woff', s)
gar4 = lambda s: font('eb-garamond-latin-400-normal.woff', s)
inter4 = font('inter-latin-400-normal.woff', 32)
inter5 = font('inter-latin-500-normal.woff', 30)
src = font('inter-latin-400-normal.woff', 30)

# Headline, three lines, as large as the width allows
head = gar6(150)
lines = ['The Puritans', 'canceled', 'Christmas']
y = 96
LEAD = 138
for ln in lines:
    d.text((M - 4, y), ln, font=head, fill=LINEN, anchor='lt')
    y += LEAD

# Subline
y += 34
d.text((M, y), 'Massachusetts Bay law, 1659. Its own words,', font=inter4, fill=DIM, anchor='lt')
d.text((M, y + 46), 'and the fine for each one:', font=inter4, fill=DIM, anchor='lt')

# The price list
items = [
    ('“Forbearing of labor”', 'Taking the day off'),
    ('“Feasting”', 'Christmas dinner'),
    ('“Or any other way”', 'Vibes, presumably'),
]
TOP = y + 138
ROW = 170
phrase = gar6(64)
price = gar6(76)
d.line((M, TOP, W - M, TOP), fill=RULE, width=2)
for i, (law, plain) in enumerate(items):
    ry = TOP + i * ROW
    base = ry + 86          # baseline of the law's words
    d.text((M, base), law, font=phrase, fill=LINEN, anchor='ls')
    d.text((W - M, base), '5s', font=price, fill=AMBER, anchor='rs')
    # leader dots between the phrase and the price
    x0 = M + d.textlength(law, font=phrase) + 26
    x1 = W - M - d.textlength('5s', font=price) - 26
    x = x0
    while x < x1:
        d.ellipse((x, base - 12, x + 5, base - 7), fill=RULE)
        x += 16
    d.text((M, base + 26), plain, font=inter4, fill=DIM, anchor='lt')
    d.line((M, ry + ROW, W - M, ry + ROW), fill=RULE, width=2)

# The note
ny = TOP + 3 * ROW + 50
note = ['Five shillings per offense. Repealed in 1681.',
        'Christmas became a state holiday in 1856.']
for j, t in enumerate(note):
    d.text((M, ny + j * 46), t, font=inter4, fill=LINEN, anchor='lt')

# Footer: sources bottom left, logo bottom right
FY = H - M - 26
d.text((M, FY), 'Sources: Mass Moments, History.com', font=src, fill=DIM, anchor='lm')
mono = Image.open('assets/hh-monogram-white-140.png').convert('RGBA')
mono = mono.resize((int(mono.width * 52 / mono.height), 52), Image.LANCZOS)
tint = Image.new('RGBA', mono.size, DIM + (255,))
tint.putalpha(mono.getchannel('A'))
word = 'Hex & Hollow'
ww = d.textlength(word, font=inter5)
lx = W - M - ww - 14 - mono.width
im.alpha_composite(tint, (int(lx), FY - 26))
d.text((W - M, FY), word, font=inter5, fill=DIM, anchor='rm')

im.convert('RGB').save(os.environ['PIN_OUT'], 'JPEG', quality=82, optimize=True)
