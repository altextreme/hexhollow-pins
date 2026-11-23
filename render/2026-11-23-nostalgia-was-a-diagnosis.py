# Hex & Hollow pin: "In 1688, nostalgia was a diagnosis"
# Product: 4618215622 Running on Nostalgia & Holiday Snacks skeleton Christmas sweatshirt.
# Skeleton: light field, headline top left, the word "nostalgia" split and bracketed as a drawn etymology diagram,
# a clean cutout of the flat mockup (photos/4618215622-4.jpg) set low, source left and logo right at the foot.
# Palette sampled from the print: cream (235,221,204), cardigan red (179,20,29), garment ink.
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1000, 1500
M = 64

FIELD = (242, 234, 223)     # print cream, lifted
INK = (26, 22, 24)          # garment black
RED = (172, 22, 32)         # cardigan red, a touch deeper for contrast on cream
DIM = (112, 98, 90)         # warm gray from the cookie and shadows

def font(fam, w, s):
    return ImageFont.truetype(f'assets/fonts/{fam}-latin-{w}-normal.woff', s)

im = Image.new('RGB', (W, H), FIELD)
d = ImageDraw.Draw(im)

def text(s, x, y, f, fill, anchor='l'):
    bb = d.textbbox((0, 0), s, font=f)
    w = bb[2] - bb[0]
    if anchor == 'c':
        x = x - w / 2
    elif anchor == 'r':
        x = x - w
    d.text((x - bb[0], y - bb[1]), s, font=f, fill=fill)
    return x, y, x + w, y + (bb[3] - bb[1])

# --- Headline -------------------------------------------------------------------
HF = font('gloock', 400, 80)
y = 70
for line in ('In 1688, nostalgia', 'was a diagnosis'):
    box = text(line, M, y, HF, INK)
    y += 96
head_bottom = box[3]

# --- The word, split and bracketed -----------------------------------------------
WF = font('gloock', 400, 196)
wy = head_bottom + 48
a, b = 'nost', 'algia'
ba = d.textbbox((0, 0), a, font=WF)
bb_ = d.textbbox((0, 0), b, font=WF)
wa = ba[2] - ba[0]
wb = bb_[2] - bb_[0]
gap = 26
total = wa + gap + wb
x0 = (W - total) / 2
# shared baseline: draw both from the same y using the font's own offsets
d.text((x0 - ba[0], wy), a, font=WF, fill=INK)
d.text((x0 + wa + gap - bb_[0], wy), b, font=WF, fill=RED)
asc_box = d.textbbox((x0 - ba[0], wy), a, font=WF)
base = d.textbbox((x0 - ba[0], wy), 'nost', font=WF)[3]   # no descenders in either word except g
gbox = d.textbbox((x0 + wa + gap - bb_[0], wy), b, font=WF)
word_bottom = max(base, gbox[3])

LF = font('inter', 600, 36)
SF = font('inter', 500, 32)
by = word_bottom + 30
for (bx0, bx1, label, gloss, col) in (
        (x0, x0 + wa, 'nostos', 'homecoming', INK),
        (x0 + wa + gap, x0 + wa + gap + wb, 'algos', 'pain', RED)):
    d.line((bx0 + 4, by, bx1 - 4, by), fill=col, width=5)
    d.line((bx0 + 4, by - 18, bx0 + 4, by), fill=col, width=5)
    d.line((bx1 - 4, by - 18, bx1 - 4, by), fill=col, width=5)
    cx = (bx0 + bx1) / 2
    d.line((cx, by, cx, by + 18), fill=col, width=5)
    text(gloss, cx, by + 40, LF, col, 'c')
gloss_bottom = by + 40 + 36

note_bottom = gloss_bottom

# --- Footer -------------------------------------------------------------------
logo = Image.open('assets/hh-monogram-white-140.png').convert('RGBA')
LH = 44
logo = logo.resize((round(logo.width * LH / logo.height), LH), Image.LANCZOS)
tint = Image.new('RGBA', logo.size, DIM + (255,))
tint.putalpha(logo.getchannel('A'))
fy = H - M - LH
im.paste(tint, (W - M - logo.width, fy), tint)
FF = font('inter', 400, 30)
sb = d.textbbox((0, 0), 'Sources: Merriam-Webster, Encyclopedia.com', font=FF)
d.text((M - sb[0], fy + (LH - (sb[3] - sb[1])) / 2 - sb[1]), 'Sources: Merriam-Webster, Encyclopedia.com', font=FF, fill=DIM)

# --- Garment cutout -----------------------------------------------------------------
src = Image.open('photos/4618215622-4.jpg').convert('RGB')
arr = np.asarray(src).astype(int)
cand = Image.fromarray(np.where(arr.min(axis=2) > 236, 255, 0).astype(np.uint8), 'L').copy()
for pt in ((0, 0), (src.width - 1, 0), (0, src.height - 1), (src.width - 1, src.height - 1)):
    ImageDraw.floodfill(cand, pt, 128)
bg = np.asarray(cand) == 128
hard = Image.fromarray(np.where(bg, 0, 255).astype(np.uint8), 'L').copy()
mask = hard.filter(ImageFilter.MinFilter(5)).filter(ImageFilter.GaussianBlur(1.2))
bbox = hard.getbbox()
garment = src.crop(bbox)
gmask = mask.crop(bbox)
top_g = note_bottom + 44
avail_h = (fy - 40) - top_g
GH = avail_h
GW = round(garment.width * GH / garment.height)
if GW > W - 2 * M:
    GW = W - 2 * M
    GH = round(garment.height * GW / garment.width)
garment = garment.resize((GW, GH), Image.LANCZOS)
gmask = gmask.resize((GW, GH), Image.LANCZOS)
gx = (W - GW) // 2
gy = top_g + (avail_h - GH) // 2
im.paste(garment, (gx, gy), gmask)

print('head_bottom', head_bottom, 'word', wy, word_bottom, 'gloss_bottom', gloss_bottom, 'note_bottom', note_bottom,
      'garment', gx, gy, GW, GH, 'bottom', gy + GH, 'footer', fy)
out = os.environ.get('PIN_OUT', 'out.jpg')
im.save(out, 'JPEG', quality=82, optimize=True)
