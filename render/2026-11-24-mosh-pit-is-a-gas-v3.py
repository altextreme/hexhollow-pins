# Hex & Hollow pin: "Your mosh pit is technically a gas" (v3, goth palette rebuild of v2)
# Product: 4611544912 Elder Emo "Still Ready for the Pit" mug.
# Why v3: Anthony, Nov 24: "I want it to look a little bit more emo and or goth right now. The dominant collar is
# brown and that doesn't seem to be on brand for what the product is". v2 sampled its field from the pinecones in
# the cozy autumn mockup (photos/4611544912-1.jpg), so the backdrop, not the product, set the palette.
# v3 keeps the headline, facts and two-circle diagram, and changes the photo and the palette:
# - Photo: photos/4611544912-2.jpg (both sides of the mug: the safety-pin heart "Emotionally ready. Physically: nope."
#   and Elder Emo), a cool gray desk scene with no brown props in the crop. Full bleed across the top, hard edge.
# - Palette sampled from the mug itself: black-cherry field (the heart's red taken nearly to black), bone type from
#   the mug art white, arrows in the heart art's brighter red tone (207,40,45), drawn big enough to read at feed size.
# - Display face: Anton (gig flyer) instead of Space Grotesk, sentence case.
# Skeleton a. Facts: Silverberg, Bierbaum, Sethna, Cohen (Cornell), "Collective Motion of Humans in Mosh and Circle
# Pits at Heavy Metal Concerts", Physical Review Letters 110, 228701 (2013): mosh pits are a disordered gas-like
# state; circle pits an ordered vortex-like state; about 95% of circle pits in their videos flowed counterclockwise.
import os, math
from PIL import Image, ImageDraw, ImageFont

W, H = 1000, 1500
M = 64

FIELD = (28, 10, 15)       # black cherry: the mug's heart red (186,32,34) taken nearly to black, tilted off brown
BONE = (232, 226, 220)     # mug art white
DIM = (168, 150, 152)      # secondary text, dimmed toward the floor (6.8:1 on the field)
LINE = (126, 87, 99)       # circle outlines, about 3:1 on the field
RED = (207, 40, 45)        # the heart art's red, its brighter (75th percentile) tone (3.6:1 on the field)

def font(fam, w, s):
    return ImageFont.truetype(f'assets/fonts/{fam}-latin-{w}-normal.woff', s)

im = Image.new('RGB', (W, H), FIELD)
d = ImageDraw.Draw(im)

# --- Photo: full bleed across the top, hard bottom edge --------------------------
PH_H = 660
src = Image.open('photos/4611544912-2.jpg').convert('RGB')
CW, CX, CY = 1020, 120, 462   # edge sits ~55 px below the binder clips; left handle lands on the 64 px text margin
im.paste(src.crop((CX, CY, CX + CW, CY + round(CW * PH_H / W))).resize((W, PH_H), Image.LANCZOS), (0, 0))

def text(x, y, s, f, fill, anchor='l'):
    bb = d.textbbox((0, 0), s, font=f)
    w = bb[2] - bb[0]
    xx = {'l': x, 'c': x - w / 2, 'r': x - w}[anchor] - bb[0]
    d.text((xx, y - bb[1]), s, font=f, fill=fill)
    return bb[3] - bb[1]

# --- Headline --------------------------------------------------------------------
HEAD = font('anton', 400, 112)
LEAD = 118
top = PH_H + 56
y = top
for line in ('Your mosh pit is', 'technically a gas'):
    text(M, y, line, HEAD, BONE)
    y += LEAD
last = d.textbbox((0, 0), 'technically a gas', font=HEAD)
head_bottom = top + LEAD + (last[3] - last[1])

SUB = font('inter', 400, 31)
sub_y = head_bottom + 26
sub_h = text(M, sub_y, 'Cornell physicists studied metal show videos (2013)', SUB, DIM)

# --- Diagram: two circles --------------------------------------------------------
R = 140
CYC = sub_y + sub_h + 44 + R
CX1, CX2 = 266, 734

def arrow(x0, y0, dx, dy, length=46, width=5, head=14):
    x1, y1 = x0 + dx * length, y0 + dy * length
    d.line((x0, y0, x1, y1), fill=RED, width=width)
    ang = math.atan2(dy, dx)
    p1 = (x1 + math.cos(ang) * head, y1 + math.sin(ang) * head)
    p2 = (x1 + math.cos(ang + 2.4) * head, y1 + math.sin(ang + 2.4) * head)
    p3 = (x1 + math.cos(ang - 2.4) * head, y1 + math.sin(ang - 2.4) * head)
    d.polygon((p1, p2, p3), fill=RED)

def dot(x, y, r=12):
    d.ellipse((x - r, y - r, x + r, y + r), fill=BONE)

for cx in (CX1, CX2):
    d.ellipse((cx - R, CYC - R, cx + R, CYC + R), outline=LINE, width=5)

# Mosh pit: scattered people, each heading a different way (gas-like, disordered). Same spacing-searched positions
# as v2, scaled to the smaller circle.
S = R / 140
mosh = [(-72, 35, 270), (-55, -79, 75), (-20, 1, 30), (6, 93, 315), (40, -9, 45), (67, -70, 210),
        (104, 21, 255), (-102, -28, 90), (-57, 87, 210), (-1, -72, 225), (78, 69, 135)]
for ox, oy, deg in mosh:
    a = math.radians(deg)
    x, y0 = CX1 + ox * S, CYC + oy * S
    arrow(x, y0, math.cos(a), math.sin(a), length=38, width=6, head=17)
    dot(x, y0)

# Circle pit: people on a ring, all running counterclockwise around an empty middle (vortex).
RR = 92
for k in range(8):
    th = math.radians(90 + k * 45)
    x, y0 = CX2 + RR * math.cos(th), CYC - RR * math.sin(th)
    arrow(x, y0, -math.sin(th), -math.cos(th), length=38, width=6, head=17)
    dot(x, y0)

# Labels
LAB = font('inter', 600, 36)
DESC = font('inter', 400, 30)
ly = CYC + R + 30
for cx, name, desc in ((CX1, 'Mosh pit', 'Moves like gas molecules'),
                       (CX2, 'Circle pit', '95% flow counterclockwise')):
    text(cx, ly, name, LAB, BONE, 'c')
    dh = text(cx, ly + 50, desc, DESC, DIM, 'c')
labels_bottom = ly + 50 + dh

# --- Logo: top right of the field, on the headline's first line -----------------
logo = Image.open('assets/hh-monogram-white-140.png').convert('RGBA')
LH = 52
logo = logo.resize((round(logo.width * LH / logo.height), LH), Image.LANCZOS)
tint = Image.new('RGBA', logo.size, DIM + (255,))
tint.putalpha(logo.getchannel('A'))
first = d.textbbox((0, 0), 'Your mosh pit is', font=HEAD)
im.paste(tint, (W - M - logo.width, top + 8), tint)

print('headline right', M + first[2] - first[0], 'logo x', W - M - logo.width, 'head_bottom', head_bottom,
      'sub', sub_y, 'circle top', CYC - R, 'labels_bottom', labels_bottom, 'foot', H - labels_bottom)
out = os.environ.get('PIN_OUT', 'out.jpg')
im.save(out, 'JPEG', quality=82, optimize=True)
