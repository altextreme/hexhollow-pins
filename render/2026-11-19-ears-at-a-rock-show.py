# "How long your ears last at a rock show" (Emotionally at the Show, Physically in Bed by 9 sweatshirt, 4618209079)
# Skeleton f: photo as a full-width strip on the top edge, single big number (2 MIN) under a drawn decibel gauge.
# Facts: CDC Vital Signs, Feb 2017 ("Too Loud! For Too Long!"): rock concert 110 dB, 2 minutes can cause damage;
# 85 dB is about where extended exposure can cause damage. Palette sampled from photos/4618209079-1.jpg.
import os, math
from PIL import Image, ImageDraw, ImageFont

W, H, M = 1000, 1500, 64
FIELD = (237, 228, 223)    # the wall behind her, #EDE4DF
RED   = (148, 50, 41)      # "EMOTIONALLY AT THE SHOW" print red, #943229
INK   = (44, 34, 27)       # latte deepened to espresso, for text and the needle
MUTED = (108, 94, 84)      # her denim shorts, warmed; secondary text
ARC   = (205, 193, 182)    # wall in shadow, the quiet part of the gauge
ARC2  = (160, 144, 131)    # mid zone, shorts gray

F = 'assets/fonts/'
bebas = lambda s: ImageFont.truetype(F + 'bebas-neue-latin-400-normal.woff', s)
grot  = lambda w, s: ImageFont.truetype(F + f'space-grotesk-latin-{w}-normal.woff', s)

S = 2  # supersample for clean arcs
im = Image.new('RGB', (W * S, H * S), FIELD)
d = ImageDraw.Draw(im)

# Photo strip: full width, top edge, hard bottom edge inside the black sweatshirt
PH = 450
ph = Image.open('photos/4618209079-1.jpg').convert('RGB')
ph = ph.resize((W * S, round(ph.height * W * S / ph.width)), Image.LANCZOS)
top = 268 * S
im.paste(ph.crop((0, top, W * S, top + PH * S)), (0, 0))

def text(x, y, s, font, fill, anchor='la'):
    d.text((x * S, y * S), s, font=font, fill=fill, anchor=anchor)

# Headline, flush left, red, no period
hf = bebas(104 * S)
y = 498
for line in ['How long your ears', 'last at a rock show']:
    text(M, y, line.upper(), hf, RED, 'lt')
    y += 90
# headline ends ~670

# Gauge: 80 to 120 dB across a half circle
cx, cy, R, T = 500, 1072, 300, 54
def ang(db):  # 80 dB at the left (180 deg), 120 dB at the right (0 deg)
    return 180 - (db - 80) / 40 * 180
def arc(db0, db1, col):
    a0, a1 = ang(db1), ang(db0)   # PIL draws clockwise from 3 o'clock with y down; use negative angles
    box = [(cx - R) * S, (cy - R) * S, (cx + R) * S, (cy + R) * S]
    d.arc(box, start=-a1, end=-a0, fill=col, width=T * S)
arc(80, 85, ARC)
arc(85, 110, ARC2)
arc(110, 120, RED)
# hairline gaps between zones
for db in (85, 110):
    a = math.radians(ang(db))
    x0, y0 = cx + (R - T - 2) * math.cos(a), cy - (R - T - 2) * math.sin(a)
    x1, y1 = cx + (R + 2) * math.cos(a), cy - (R + 2) * math.sin(a)
    d.line([x0 * S, y0 * S, x1 * S, y1 * S], fill=FIELD, width=6 * S)

# tick labels outside the ring
lf = grot(500, 32 * S)
for db, lab in [(90, '90'), (100, '100'), (110, '110'), (120, '120 dB')]:
    a = math.radians(ang(db))
    rx, ry = cx + (R + 40) * math.cos(a), cy - (R + 40) * math.sin(a)
    anchor = 'mm' if db != 120 else 'rm'
    if db == 120:
        rx, ry = cx + R, cy + 30
    text(rx, ry, lab, lf, INK if db != 110 else RED, anchor)
text(cx - R, cy + 30, '80', lf, MUTED, 'lm')

# needle to 110 dB, hub
a = math.radians(ang(110))
nx, ny = cx + (R - T - 24) * math.cos(a), cy - (R - T - 24) * math.sin(a)
d.line([cx * S, cy * S, nx * S, ny * S], fill=INK, width=12 * S)
r = 22
d.ellipse([(cx - r) * S, (cy - r) * S, (cx + r) * S, (cy + r) * S], fill=INK)

# Big number under the gauge, then the one-line payoff
text(cx, 1140, '2 MIN', bebas(150 * S), INK, 'mt')
sub = grot(400, 34 * S)
text(cx, 1262, 'at 110 dB before damage can start', sub, INK, 'mt')

# Footer, kept above the bottom 120 px
logo = Image.open('assets/hh-monogram-white-140.png').convert('RGBA')
lh = 56 * S; lw = round(logo.width * lh / logo.height)
logo = logo.resize((lw, lh), Image.LANCZOS)
logo = Image.merge('RGBA', (*[Image.new('L', logo.size, c) for c in INK], logo.split()[3]))
ly = 1322
im.paste(logo, (M * S, ly * S), logo)
text(M + lw // S + 16, ly + 28, 'Hex & Hollow', grot(500, 30 * S), INK, 'lm')
text(W - M, ly + 28, 'Earplugs are still punk', grot(400, 30 * S), MUTED, 'rm')

im = im.resize((W, H), Image.LANCZOS)
im.save(os.environ.get('PIN_OUT', '/tmp/pin.jpg'), quality=82, optimize=True, progressive=True)
