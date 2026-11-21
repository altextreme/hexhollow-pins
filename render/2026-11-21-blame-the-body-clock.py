# Hex & Hollow pin: Elder Emo, Now With Earlier Bedtime sweatshirt (listing 4618215666)
# Concept: the teen body clock runs up to 2 hours later at puberty (AAP, 2014),
# then rhythms creep earlier with age (Sleep Foundation). Drawn night dial as the hero.
import math
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1000, 1500
M = 64

# Palette sampled from the product mockup (photos/4618215666-3.jpg)
PRINT_RED = (158, 16, 33)      # heart, moon and bolts in the print
BONE = (232, 222, 206)         # the print's lettering
FIELD = (52, 10, 17)           # print red, darkened: deep crimson field
DIM = (196, 168, 160)          # bone dimmed into the field, for small text
LINE = (122, 66, 70)           # hairlines on the dial

F = 'assets/fonts/'
display = lambda s: ImageFont.truetype(F + 'archivo-black-latin-400-normal.woff', s)
sans = lambda s, w=400: ImageFont.truetype(F + f'dm-sans-latin-{w}-normal.woff', s)

im = Image.new('RGB', (W, H), FIELD)
d = ImageDraw.Draw(im)

# --- Product cutout from the plain-background mockup -------------------------
src = Image.open('photos/4618215666-3.jpg').convert('RGB')
arr = np.asarray(src).astype(np.int16)
bright = arr.min(axis=2)
# Light pixels are candidate background; flood fill from the border so the
# cream print inside the garment is never touched.
cand = Image.fromarray(np.where(bright > 200, 255, 0).astype(np.uint8), 'L').copy()
sw, sh = cand.size
for pt in [(0, 0), (sw - 1, 0), (0, sh - 1), (sw - 1, sh - 1), (sw // 2, 0), (sw // 2, sh - 1), (0, sh // 2), (sw - 1, sh // 2)]:
    if cand.getpixel(pt) == 255:
        ImageDraw.floodfill(cand, pt, 128)
bg = np.asarray(cand) == 128
mask = Image.fromarray(np.where(bg, 0, 255).astype(np.uint8), 'L')
# Pull the edge in 2 px so no white or soft shadow survives, then antialias 1 px.
mask = mask.filter(ImageFilter.MinFilter(5)).filter(ImageFilter.GaussianBlur(1.2))
bbox = Image.fromarray(np.where(bg, 0, 255).astype(np.uint8), 'L').getbbox()
garment = src.crop(bbox)
gmask = mask.crop(bbox)

GW = 520
GH = round(garment.height * GW / garment.width)
garment = garment.resize((GW, GH), Image.LANCZOS)
gmask = gmask.resize((GW, GH), Image.LANCZOS)
gx, gy = (W - GW) // 2, 60
im.paste(garment, (gx, gy), gmask)

# --- Headline -----------------------------------------------------------------
hy = gy + GH + 44
hf = display(112)
d.text((M, hy), 'Blame the', font=hf, fill=BONE)
lh = 118
d.text((M, hy + lh), 'body clock', font=hf, fill=BONE)

# Support line
sf = sans(34)
sy = hy + 2 * lh + 34
d.text((M, sy), 'It runs up to 2 hours later at puberty,', font=sf, fill=DIM)
d.text((M, sy + 46), 'then creeps earlier as you age.', font=sf, fill=DIM)

# --- Night dial: 8 PM (left) through midnight (top) to 4 AM (right) -----------
cx = W // 2
R_OUT, R_IN = 330, 262
cy = sy + 92 + 44 + R_OUT
DEG_PER_H = 180 / 8  # 22.5 degrees per hour


def ang(hours_from_8pm):
    # 0 h = 8 PM at the left (180 deg), 8 h = 4 AM at the right (0 deg)
    return math.radians(180 - hours_from_8pm * DEG_PER_H)


def pt(r, a):
    return cx + r * math.cos(a), cy - r * math.sin(a)


# Supersample the dial for smooth curves
S = 3
dial = Image.new('RGBA', (W * S, H * S), (0, 0, 0, 0))
dd = ImageDraw.Draw(dial)


def spt(r, a):
    x, y = pt(r, a)
    return x * S, y * S


def sband(h0, h1, fill, r_out=R_OUT, r_in=R_IN, steps=160):
    pts = [spt(r_out, ang(h0 + (h1 - h0) * i / steps)) for i in range(steps + 1)]
    pts += [spt(r_in, ang(h0 + (h1 - h0) * i / steps)) for i in range(steps, -1, -1)]
    dd.polygon(pts, fill=fill)


sband(0, 8, (30, 6, 10, 255))          # the night: darker than the field
sband(4, 6, PRINT_RED + (255,))         # teen shift: midnight to 2 AM
# hour ticks across the band
for h in range(0, 9):
    a = ang(h)
    w = 3 if h in (2, 4, 6) else 2
    dd.line([spt(R_IN, a), spt(R_OUT, a)], fill=LINE + (255,) if h not in (4, 6) else BONE + (255,), width=w * S)
dial = dial.resize((W, H), Image.LANCZOS)
im.paste(dial, (0, 0), dial)
d = ImageDraw.Draw(im)

# Hour labels inside the arc
lf = sans(30, 500)


def label_at(h, text, r, font, fill):
    x, y = pt(r, ang(h))
    bb = d.textbbox((0, 0), text, font=font)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    d.text((x - tw / 2 - bb[0], y - th / 2 - bb[1]), text, font=font, fill=fill)


label_at(2, '10 PM', R_IN - 58, lf, DIM)
label_at(4, 'midnight', R_IN - 40, lf, BONE)
label_at(6, '2 AM', R_IN - 58, lf, BONE)

# Callout under the dial's centre
cf = sans(34, 700)
t = 'Teen body clock: up to +2 h'
bb = d.textbbox((0, 0), t, font=cf)
d.text((cx - (bb[2] - bb[0]) / 2 - bb[0], cy - 104), t, font=cf, fill=BONE)

# --- Footer -------------------------------------------------------------------
logo = Image.open('assets/hh-monogram-white-140.png').convert('RGBA')
lh_ = 44
logo = logo.resize((round(logo.width * lh_ / logo.height), lh_), Image.LANCZOS)
tint = Image.new('RGBA', logo.size, DIM + (255,))
tint.putalpha(logo.getchannel('A'))
fy = H - 64 - lh_
ff = sans(30, 500)
word = 'Hex & Hollow'
bb = d.textbbox((0, 0), word, font=ff)
ww = bb[2] - bb[0]
lx = W - M - ww - 14 - logo.width
im.paste(tint, (lx, fy), tint)
d.text((lx + logo.width + 14, fy + (lh_ - (bb[3] - bb[1])) / 2 - bb[1]), word, font=ff, fill=DIM)
sfn = sans(30)
src_t = 'Sources: AAP, Sleep Foundation'
bb = d.textbbox((0, 0), src_t, font=sfn)
d.text((M, fy + (lh_ - (bb[3] - bb[1])) / 2 - bb[1]), src_t, font=sfn, fill=DIM)

out = os.environ.get('PIN_OUT', 'out.jpg')
im.save(out, 'JPEG', quality=82, optimize=True, progressive=False)
