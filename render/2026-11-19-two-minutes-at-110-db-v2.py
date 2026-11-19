# "2 minutes at 110 dB can damage your hearing" (Elder Emo: Still Ready for the Pit mug, 4611544912). v2 after
# creative director round 2. Skeleton f: photo as a full-width strip on the top edge; a single statement led by a
# giant "2"; the hero visual is a tall vertical LED level meter (80 to 120 dB) on the right, labels centered on ticks.
# Facts: CDC Vital Signs, Feb 2017, "Too Loud! For Too Long!": 85 dB is about where extended exposure can cause hearing
# damage; rock concert 110 dB, 2 minutes can cause damage; siren 120 dB.
# Palette sampled from photos/4611544912-3.jpg: field = the blue-gray wall (#C8D5DB), headline and the 110 mark = the
# mug print's crimson (#932B2F), lit meter = the laptop's charcoal (#474247), text = the mug's near-black.
import os
from PIL import Image, ImageDraw, ImageFont

W, H, M = 1000, 1500, 64
FIELD = (200, 213, 219)    # wall, #C8D5DB
RED   = (147, 43, 47)      # print crimson, #932B2F
CHAR  = (71, 66, 71)       # laptop charcoal, #474247
INK   = (36, 34, 34)       # the mug, #242222
DIM   = (150, 164, 172)    # wall in deeper shade: unlit segments
SAFE  = (128, 132, 136)    # below 85 dB: lit but quiet

F = 'assets/fonts/'
zilla = lambda s: ImageFont.truetype(F + 'zilla-slab-latin-700-normal.woff', s)
plex  = lambda w, s: ImageFont.truetype(F + f'ibm-plex-sans-latin-{w}-normal.woff', s)

S = 2
im = Image.new('RGB', (W * S, H * S), FIELD)
d = ImageDraw.Draw(im)
def T(x, y, s, font, fill, anchor='ls'):
    d.text((x * S, y * S), s, font=font, fill=fill, anchor=anchor)
def R(x0, y0, x1, y1, fill):
    d.rectangle([round(x0 * S), round(y0 * S), round(x1 * S) - 1, round(y1 * S) - 1], fill=fill)

# Photo: full-width strip on the top edge, hard bottom edge in the desk
PH = 470
ph = Image.open('photos/4611544912-3.jpg').convert('RGB')
ph = ph.resize((W * S, round(ph.height * W * S / ph.width)), Image.LANCZOS)
top = 330 * S
im.paste(ph.crop((0, top, W * S, top + PH * S)), (0, 0))

# Statement, flush left, one color, no period
T(M, 826, '2', zilla(430 * S), RED)
T(M, 934, 'minutes', zilla(112 * S), RED)
body = zilla(52 * S)
for i, line in enumerate(['at 110 dB can', 'damage your', 'hearing']):
    T(M, 1018 + i * 62, line, body, RED)
T(M, 1236, 'Earplugs are still punk', plex(400, 36 * S), INK)

# Vertical LED meter, 80 dB at the bottom to 120 dB at the top, 2 dB a segment
mx0, mx1 = 712, W - M
my_top, my_bot = 597, 1290
n, gap = 20, 6
pitch = (my_bot - my_top + gap) / n
segh = pitch - gap
def seg_y(db):  # top y of the segment that starts at db
    i = (db - 80) // 2
    return my_bot - (i + 1) * pitch + gap
for db in range(80, 120, 2):
    y = seg_y(db)
    col = SAFE if db < 85 else CHAR
    if db == 110: col = RED
    if db > 110: col = DIM
    R(mx0, y, mx1, y + segh, col)
# ticks and labels, each label vertically centered on its tick
lab = plex(600, 30 * S)
def tick(level_y, text, color):
    d.line([(mx0 - 22) * S, level_y * S, (mx0 - 6) * S, level_y * S], fill=color, width=3 * S)
    T(mx0 - 32, level_y, text, lab, color, 'rm')
def mid(db): return seg_y(db) + segh / 2
tick(mid(118), '120 siren', INK)
tick(mid(110), '110 rock show', RED)
tick(mid(100), '100', INK)
tick(mid(90), '90', INK)
tick(seg_y(84) - gap / 2, '85 risk starts', INK)    # boundary between the 84 and 86 segments
tick(mid(80), '80 dB', INK)

# Source and logo, kept above the bottom 120 px
T(W - M, 1336, 'Source: CDC', plex(400, 30 * S), INK, 'rs')
logo = Image.open('assets/hh-monogram-white-140.png').convert('RGBA')
lh = 44 * S; lw = round(logo.width * lh / logo.height)
logo = logo.resize((lw, lh), Image.LANCZOS)
logo = Image.merge('RGBA', (*[Image.new('L', logo.size, c) for c in INK], logo.split()[3]))
word = plex(600, 30 * S)
ww = d.textlength('Hex & Hollow', font=word) / S
gx = (W - (lw / S + 14 + ww)) / 2
ly = 1306
im.paste(logo, (round(gx * S), ly * S), logo)
T(gx + lw / S + 14, ly + 22, 'Hex & Hollow', word, INK, 'lm')

im = im.resize((W, H), Image.LANCZOS)
im.save(os.environ.get('PIN_OUT', '/tmp/pin.jpg'), quality=82, optimize=True, progressive=True)
