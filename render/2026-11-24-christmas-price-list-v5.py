"""Topical pin: the 1659 Massachusetts Bay law against Christmas, set as a price list. Photo-free. v5.

Facts (checked Nov 23 2026):
  1659: the Massachusetts Bay General Court fined anyone "observing any such day as Christmas or the like,
        either by forbearing of labor, feasting, or any other way" five shillings for every such offense.
        (Mass Moments, "Christmas Celebration Outlawed"; History.com, "When Massachusetts Banned Christmas";
        New England Today, "How the Puritans Banned Christmas", which quotes the law.)
        The law opens "For preventing disorders arising in several places within this jurisdiction"
        (New England Today quotes the law).
  1681: repealed under pressure from the government in London (Mass Moments; History.com).
  Salem, 1679 (Mass Moments): "On the night of December 25th" four men entered farmer John Rowden's home,
        demanded the Rowdens' pear wine and were repeatedly refused; they pretended to leave, returned and
        demanded money; "Turned out again", they threw "stones, bones, and other things" at the house.
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
LEAD = 116
base = M - cap_top
for ln in ['The Puritans', 'canceled', 'Christmas']:
    d.text((M - 4, base), ln, font=head, fill=LINEN, anchor='ls')
    last_base = base
    base += LEAD

# Subline
sub = inter(400, 32)
y = last_base + 58
d.text((M, y), 'A 1659 Massachusetts Bay law “for preventing', font=sub, fill=DIM, anchor='lt')
d.text((M, y + 46), 'disorders” fined anyone found observing Christmas by:', font=sub, fill=DIM, anchor='lt')

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
fy = TOP + 3 * ROW + 80
d.text((M, fy), 'Any of the above: 5 shillings', font=gar6(64), fill=AMBER, anchor='ls')

# The disorders in question
note = inter(400, 34)
ny = fy + 50
lines = ['Salem, Christmas night 1679: four men were refused',
         'a farmer’s pear wine, came back demanding money,',
         'got turned out, then pelted his house with',
         '“stones, bones, and other things.”']
for j, t in enumerate(lines):
    d.text((M, ny + j * 46), t, font=note, fill=GLOSS, anchor='lt')

# Footer: sources bottom left, monogram bottom right
FY = H - M - 26
d.text((M, FY), 'Sources: Mass Moments, New England Today', font=inter(400, 30), fill=DIM, anchor='lm')
mono = Image.open('assets/hh-monogram-white-140.png').convert('RGBA')
mono = mono.resize((int(mono.width * 52 / mono.height), 52), Image.LANCZOS)
tint = Image.new('RGBA', mono.size, DIM + (255,))
tint.putalpha(mono.getchannel('A'))
im.alpha_composite(tint, (W - M - mono.width, FY - 26))   # monogram only: the sources line needs the width

im.convert('RGB').save(os.environ['PIN_OUT'], 'JPEG', quality=82, optimize=True)
