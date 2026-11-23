# Hex & Hollow pin: "Same band, new bedtime"
# Product: 4618209079 Elder Emo "Emotionally at the show, physically in bed by 9" crewneck.
# Skeleton: type-led field on top with a drawn two-lane show-night timeline, photo full bleed across the bottom
# with one hard horizontal edge. Palette sampled from photos/4618209079-1.jpg (print red, print cream, garment ink).
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 1000, 1500
M = 64

PRINT_RED = (139, 61, 60)        # sampled from the slogan's red line
FIELD = (104, 40, 38)            # print red, deepened: still clearly a red
CREAM = (232, 221, 190)          # sampled from the print's cream outline
DIM = (205, 160, 150)            # rose neutral between field and cream
INK = (22, 18, 18)               # garment black

def font(fam, w, s):
    return ImageFont.truetype(f'assets/fonts/{fam}-latin-{w}-normal.woff', s)

HEAD = font('archivo-black', 400, 104)
SUB = lambda s, w=400: font('inter', w, s)

im = Image.new('RGB', (W, H), FIELD)
d = ImageDraw.Draw(im)

# --- Photo: full bleed across the bottom, hard top edge ------------------------
PH_TOP = 860
src = Image.open('photos/4618209079-1.jpg').convert('RGB')
ph_h = H - PH_TOP
crop_h = round(src.width * ph_h / W)
cy = 168
photo = src.crop((0, cy, src.width, cy + crop_h)).resize((W, ph_h), Image.LANCZOS)
im.paste(photo, (0, PH_TOP))

# --- Headline -------------------------------------------------------------------
y = 70
for line in ('Same band,', 'new bedtime'):
    bb = d.textbbox((0, 0), line, font=HEAD)
    d.text((M - bb[0], y - bb[1]), line, font=HEAD, fill=CREAM)
    y += 118
head_bottom = y - 118 + (d.textbbox((0, 0), 'new bedtime', font=HEAD)[3] - d.textbbox((0, 0), 'new bedtime', font=HEAD)[1])

sf = SUB(32)
sub = 'A show night, at 19 and now'
bb = d.textbbox((0, 0), sub, font=sf)
sy = head_bottom + 34
d.text((M - bb[0], sy - bb[1]), sub, font=sf, fill=DIM)

# --- Timeline -------------------------------------------------------------------
def x(t):  # t in hours, 18 = 6 PM, 25 = 1 AM
    return M + (t - 18) * (W - 2 * M) / 7.0

lab = SUB(36, 600)
small = SUB(32, 500)
BAR = 30

def lane_label(text, ly):
    bb = d.textbbox((0, 0), text, font=lab)
    d.text((M - bb[0], ly - bb[1]), text, font=lab, fill=CREAM)

def marker_label(text, cx, ty, align, fnt=small, fill=CREAM):
    bb = d.textbbox((0, 0), text, font=fnt)
    w = bb[2] - bb[0]
    lx = cx - bb[0] if align == 'l' else (cx - w / 2 - bb[0] if align == 'c' else cx - w - bb[0])
    d.text((lx, ty - bb[1]), text, font=fnt, fill=fill)

top = sy + 90
# Lane 1: at 19. Doors at 7, headliner 10:30, and the bar runs off the edge.
lane_label('At 19', top)
b1 = top + 58
d.rectangle((x(19), b1, W, b1 + BAR), fill=CREAM)
for t in (19, 22.5):
    r = 20
    d.ellipse((x(t) - r, b1 + BAR / 2 - r, x(t) + r, b1 + BAR / 2 + r), fill=INK, outline=CREAM, width=6)
marker_label('Doors', x(19) - 20, b1 + BAR + 22, 'l')
marker_label('Headliner', x(22.5), b1 + BAR + 22, 'c')

# Lane 2: now. Earplugs in at 6:30, in bed at 9.
top2 = b1 + BAR + 92
lane_label('Now', top2)
b2 = top2 + 58
d.rectangle((x(18.5), b2, x(21), b2 + BAR), fill=CREAM)
for t in (18.5, 21):
    r = 20
    d.ellipse((x(t) - r, b2 + BAR / 2 - r, x(t) + r, b2 + BAR / 2 + r), fill=INK, outline=CREAM, width=6)
marker_label('Earplugs in', x(18.5) - 20, b2 + BAR + 22, 'l')
marker_label('In bed', x(21) + 34, b2 + BAR / 2 - 18, 'l', fnt=SUB(36, 600), fill=CREAM)

# Axis: hourly ticks, labels every two hours.
ay = b2 + BAR + 96
d.line((M, ay, W - M, ay), fill=DIM, width=3)
af = SUB(30, 500)
for t in range(18, 26):
    d.line((x(t), ay - 10, x(t), ay + 10), fill=DIM, width=3)
for t, s in ((18, '6 PM'), (20, '8 PM'), (22, '10 PM'), (24, '12 AM')):
    marker_label(s, x(t), ay + 22, 'l' if t == 18 else 'c', fnt=af, fill=DIM)

# --- Logo: top right, aligned to the headline's first line -----------------------
logo = Image.open('assets/hh-monogram-white-140.png').convert('RGBA')
LH = 44
logo = logo.resize((round(logo.width * LH / logo.height), LH), Image.LANCZOS)
tint = Image.new('RGBA', logo.size, DIM + (255,))
tint.putalpha(logo.getchannel('A'))
im.paste(tint, (W - M - logo.width, 76), tint)

print('head_bottom', head_bottom, 'sub', sy, 'lane1', top, 'lane2', top2, 'axis', ay, 'photo', PH_TOP)
out = os.environ.get('PIN_OUT', 'out.jpg')
im.save(out, 'JPEG', quality=82, optimize=True)
