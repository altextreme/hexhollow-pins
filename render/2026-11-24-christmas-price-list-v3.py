"""Topical pin: the 1659 Massachusetts Bay law against Christmas, set as a price list. Photo-free. v3.

Facts (checked Nov 23 2026):
  1659: the Massachusetts Bay General Court fined anyone "observing any such day as Christmas or the like,
        either by forbearing of labor, feasting, or any other way" five shillings for every such offense.
        (Mass Moments, "Christmas Celebration Outlawed"; History.com, "When Massachusetts Banned Christmas";
        New England Today, "How the Puritans Banned Christmas", which quotes the law.)
  1681: repealed under pressure from the government in London (Mass Moments; History.com).
  Salem, 1679: four men entered farmer John Rowden's home at Christmas, demanded his pear wine, then
        threw "stones, bones, and other things" at the house (Mass Moments).
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1000, 1500
F = 'assets/fonts/'
FIELD = (46, 31, 24)        # Puritan "sadd colour": deep walnut brown wool
LINEN = (238, 229, 212)     # headline and the law's words
GLOSS = (214, 202, 186)     # the modern translations and the Salem story
DIM = (178, 160, 144)       # subline, sources
RULE = (84, 64, 52)         # hairlines
AMBER = (232, 166, 84)      # the one accent: candlelight, on the fine

im = Image.new('RGBA', (W, H), FIELD + (255,))
d = ImageDraw.Draw(im)


def font(name, size):
    return ImageFont.truetype(F + name, size)


M = 72
gar6 = lambda s: font('eb-garamond-latin-600-normal.woff', s)
inter = lambda w, s: font(f'inter-latin-{w}-normal.woff', s)

# Headline: cap top of the first line sits on the top margin
head = gar6(130)
cap_top = d.textbbox((0, 0), 'T', font=head, anchor='ls')[1]   # negative: cap height above baseline
LEAD = 120
base = M - cap_top
for ln in ['The Puritans', 'canceled', 'Christmas']:
    d.text((M - 4, base), ln, font=head, fill=LINEN, anchor='ls')
    last_base = base
    base += LEAD

# Subline
sub = inter(400, 34)
y = last_base + 62
d.text((M, y), 'Massachusetts Bay law, 1659 to 1681.', font=sub, fill=DIM, anchor='lt')
d.text((M, y + 48), 'It set a fine for anyone caught observing it by:', font=sub, fill=DIM, anchor='lt')

# The list
items = [
    ('“Forbearing of labor”', 'Taking the day off'),
    ('“Feasting”', 'Christmas dinner'),
    ('“Or any other way”', 'Vibes, presumably'),
]
TOP = y + 128
ROW = 152
phrase = gar6(62)
gloss = inter(400, 40)
d.line((M, TOP, W - M, TOP), fill=RULE, width=2)
for i, (law, plain) in enumerate(items):
    ry = TOP + i * ROW
    d.text((M, ry + 64), law, font=phrase, fill=LINEN, anchor='ls')
    d.text((M, ry + 130), plain, font=gloss, fill=GLOSS, anchor='ls')
    d.line((M, ry + ROW, W - M, ry + ROW), fill=RULE, width=2)

# The fine, once, as the accent
fy = TOP + 3 * ROW + 84
d.text((M, fy), 'Any of the above: 5 shillings', font=gar6(64), fill=AMBER, anchor='ls')

# The dark part: what Christmas actually looked like
note = inter(400, 36)
ny = fy + 56
lines = ['Salem, Christmas 1679: refused pear wine,',
         'four men came back and pelted the house',
         'with “stones, bones, and other things.”']
for j, t in enumerate(lines):
    d.text((M, ny + j * 50), t, font=note, fill=GLOSS, anchor='lt')

# Footer: sources bottom left, logo bottom right
FY = H - M - 26
d.text((M, FY), 'Sources: Mass Moments, History.com', font=inter(400, 30), fill=DIM, anchor='lm')
mono = Image.open('assets/hh-monogram-white-140.png').convert('RGBA')
mono = mono.resize((int(mono.width * 52 / mono.height), 52), Image.LANCZOS)
tint = Image.new('RGBA', mono.size, DIM + (255,))
tint.putalpha(mono.getchannel('A'))
word = 'Hex & Hollow'
w5 = inter(500, 30)
ww = d.textlength(word, font=w5)
im.alpha_composite(tint, (int(W - M - ww - 14 - mono.width), FY - 26))
d.text((W - M, FY), word, font=w5, fill=DIM, anchor='rm')

im.convert('RGB').save(os.environ['PIN_OUT'], 'JPEG', quality=82, optimize=True)
