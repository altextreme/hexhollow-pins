# Hex & Hollow pin: Still Here Somehow cracked heart tee (listing 4611527727)
# Concept: the heart on the shirt is cracked and pinned, and still going.
# Big-number pin: your heart beats about 100,000 times a day and more than
# 2.5 billion times in a lifetime (Cleveland Clinic: "about 100,000 times per
# day", "more than 2.6 billion times" in an average lifetime).
# Skeleton: type-led, headline and huge number top, clean product cutout low.
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1000, 1500
M = 64

# Palette sampled from the plain mockup (photos/4611527727-5.jpg)
CREAM = (234, 223, 206)        # the print's cracked heart and lettering: field
RED = (145, 30, 33)            # the print's dripping red: the number
INK = (39, 36, 36)             # the tee, warmed a touch: headline
DIM = (96, 86, 80)             # ink lifted toward the cream, for small text

F = 'assets/fonts/'
display = lambda s: ImageFont.truetype(F + 'dm-serif-display-latin-400-normal.woff', s)
sans = lambda s, w=400: ImageFont.truetype(F + f'inter-latin-{w}-normal.woff', s)

im = Image.new('RGB', (W, H), CREAM)
d = ImageDraw.Draw(im)


def text_top(x, y, s, font, fill):
    """Draw text so its ink top sits at y; return the ink bottom."""
    bb = d.textbbox((0, 0), s, font=font)
    d.text((x - bb[0], y - bb[1]), s, font=font, fill=fill)
    return y + bb[3] - bb[1]


# --- Headline -----------------------------------------------------------------
hf = display(118)
y = text_top(M, 72, 'Still beating,', hf, INK)
y = text_top(M, y + 34, 'somehow', hf, INK)

# --- The number ---------------------------------------------------------------
nf = display(268)
ny = y + 56
nb = text_top(M - 6, ny, '100,000', nf, RED)

sf = sans(38, 500)
y = text_top(M, nb + 40, 'times your heart beats in a day,', sf, INK)
y = text_top(M, y + 18, 'without anyone asking it to', sf, INK)
tf = sans(34)
y = text_top(M, y + 34, 'More than 2.5 billion in a lifetime.', tf, DIM)
text_bottom = y

# --- Product cutout from the plain-background mockup -------------------------
src = Image.open('photos/4611527727-5.jpg').convert('RGB')
arr = np.asarray(src).astype(np.int16)
cand = Image.fromarray(np.where(arr.min(axis=2) > 200, 255, 0).astype(np.uint8), 'L').copy()
sw, sh = cand.size
for pt in [(0, 0), (sw - 1, 0), (0, sh - 1), (sw - 1, sh - 1), (sw // 2, 0), (sw // 2, sh - 1), (0, sh // 2), (sw - 1, sh // 2)]:
    if cand.getpixel(pt) == 255:
        ImageDraw.floodfill(cand, pt, 128)
bg = np.asarray(cand) == 128
hard = Image.fromarray(np.where(bg, 0, 255).astype(np.uint8), 'L')
mask = hard.filter(ImageFilter.MinFilter(5)).filter(ImageFilter.GaussianBlur(1.2))
bbox = hard.getbbox()
garment = src.crop(bbox)
gmask = mask.crop(bbox)

# --- Footer -------------------------------------------------------------------
logo = Image.open('assets/hh-monogram-white-140.png').convert('RGBA')
LH = 44
logo = logo.resize((round(logo.width * LH / logo.height), LH), Image.LANCZOS)
tint = Image.new('RGBA', logo.size, DIM + (255,))
tint.putalpha(logo.getchannel('A'))
fy = H - 64 - LH

# Tee fills the space between the text block and the footer, centered.
gap = 56
avail = (fy - gap) - (text_bottom + gap)
GH = avail
GW = round(garment.width * GH / garment.height)
garment = garment.resize((GW, GH), Image.LANCZOS)
gmask = gmask.resize((GW, GH), Image.LANCZOS)
gx, gy = (W - GW) // 2, text_bottom + gap
im.paste(garment, (gx, gy), gmask)
d = ImageDraw.Draw(im)

ff = sans(30, 500)
word = 'Hex & Hollow'
bb = d.textbbox((0, 0), word, font=ff)
ww = bb[2] - bb[0]
lx = W - M - ww - 14 - logo.width
im.paste(tint, (lx, fy), tint)
d.text((lx + logo.width + 14, fy + (LH - (bb[3] - bb[1])) / 2 - bb[1]), word, font=ff, fill=DIM)
sfn = sans(30)
src_t = 'Source: Cleveland Clinic'
bb = d.textbbox((0, 0), src_t, font=sfn)
d.text((M, fy + (LH - (bb[3] - bb[1])) / 2 - bb[1]), src_t, font=sfn, fill=DIM)

print('text_bottom', text_bottom, 'tee', GW, GH, gy)
out = os.environ.get('PIN_OUT', 'out.jpg')
im.save(out, 'JPEG', quality=84, optimize=True)
