"""Topical pin: how old the classic emo and pop punk albums are now, against the US drinking age of 21. Photo-free.

Release dates (Wikipedia album pages and contemporaneous coverage):
  Bleed American, Jimmy Eat World: July 24, 2001 -> 25 in Nov 2026
  Tell All Your Friends, Taking Back Sunday: March 26, 2002 -> 24
  Ocean Avenue, Yellowcard: July 22, 2003 -> 23
  Three Cheers for Sweet Revenge, My Chemical Romance: June 8, 2004 -> 22
  From Under the Cork Tree, Fall Out Boy: May 3, 2005 -> 21
  The Black Parade, My Chemical Romance: October 23, 2006 -> 20 (21 in October 2027)
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1000, 1500
F = 'assets/fonts/'
FIELD = (21, 27, 44)        # faded black band tee, cold navy
BONE = (236, 228, 212)      # headline and album names
AMBER = (228, 168, 64)      # the one accent: the legal bars and the 21 line
DIM = (146, 152, 170)       # band names, small text
UNDER = (70, 80, 106)       # the bar that is still under 21
TRACK = (31, 39, 62)        # faint bar track

im = Image.new('RGBA', (W, H), FIELD + (255,))
d = ImageDraw.Draw(im)


def font(name, size):
    return ImageFont.truetype(F + name, size)


M = 64
anton = lambda s: font('anton-latin-400-normal.woff', s)
nar7 = font('archivo-narrow-latin-700-normal.woff', 38)
inter4 = font('inter-latin-400-normal.woff', 30)
inter5 = font('inter-latin-500-normal.woff', 30)

# Logo, top left
mono = Image.open('assets/hh-monogram-white-140.png').convert('RGBA')
mono = mono.resize((int(mono.width * 52 / mono.height), 52), Image.LANCZOS)
tint = Image.new('RGBA', mono.size, DIM + (255,))
tint.putalpha(mono.getchannel('A'))
im.alpha_composite(tint, (M, M))
d.text((M + mono.width + 14, M + 26), 'Hex & Hollow', font=inter5, fill=DIM, anchor='lm')
d.text((W - M, M + 26), 'Age in years, 2026', font=inter4, fill=DIM, anchor='rm')

albums = [
    ('Bleed American', 'Jimmy Eat World', 2001, 25),
    ('Tell All Your Friends', 'Taking Back Sunday', 2002, 24),
    ('Ocean Avenue', 'Yellowcard', 2003, 23),
    ('Three Cheers for Sweet Revenge', 'My Chemical Romance', 2004, 22),
    ('From Under the Cork Tree', 'Fall Out Boy', 2005, 21),
    ('The Black Parade', 'My Chemical Romance', 2006, 20),
]

# Bars from zero: full width = 26 years, leaving room for the number at the end
X0 = M
NUMW = 92
XMAX = W - M - NUMW - 30
scale = (XMAX - X0) / 25.0
x21 = X0 + 21 * scale

TOP = 170
ROW = 158
BAR = 30
NUMX = W - M  # numbers right-aligned in their own column
for i, (title, band, year, age) in enumerate(albums):
    y = TOP + i * ROW
    legal = age >= 21
    d.text((X0, y), title, font=nar7, fill=BONE, anchor='lt')
    d.text((X0, y + 46), f'{band}, {year}', font=inter4, fill=DIM, anchor='lt')
    by = y + 90
    x1 = X0 + age * scale
    d.rectangle((X0, by, x1, by + BAR), fill=AMBER if legal else UNDER)
    d.text((NUMX, by + BAR / 2), str(age), font=anton(50), fill=AMBER if legal else DIM, anchor='rm')

# The legal line at 21, dashed, from the first bar to below the last
LY0 = TOP + 90 - 16
LY1 = TOP + 5 * ROW + 90 + BAR + 24
y = LY0
while y < LY1:
    d.line((x21, y, x21, min(y + 14, LY1)), fill=BONE, width=3)
    y += 24
LB = LY1 + 40
d.text((x21, LB), '21', font=anton(48), fill=BONE, anchor='mm')
d.text((x21 - 40, LB), 'US drinking age', font=inter4, fill=DIM, anchor='rm')

# Headline, flush left, anchored low
hf = anton(150)
lines = ['YOUR EMO ALBUMS', 'CAN LEGALLY DRINK']
# fit the longer line to the grid
size = 150
while max(d.textlength(t, font=anton(size)) for t in lines) > W - 2 * M:
    size -= 2
hf = anton(size)
lh = int(size * 1.06)
HB = H - M  # baseline of the last line
for k, t in enumerate(lines):
    d.text((M - 2, HB - (len(lines) - 1 - k) * lh), t, font=hf, fill=BONE, anchor='ls')

im.convert('RGB').save(os.environ.get('PIN_OUT', 'pins/out.jpg'), 'JPEG', quality=82, optimize=True)
print('headline size', size)
