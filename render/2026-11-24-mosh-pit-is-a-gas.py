# Hex & Hollow pin: "Your mosh pit is technically a gas"
# Product: 4611544912 Elder Emo "Still Ready for the Pit" mug.
# Skeleton a: photo full bleed across the top with one hard bottom edge; below it a Space Grotesk headline,
# then a drawn two-circle diagram (mosh pit as gas, circle pit as vortex) anchored to the foot. Logo top right of the
# field, on the headline's first line. Source named in the subline.
# Facts: Silverberg, Bierbaum, Sethna, Cohen (Cornell), "Collective Motion of Humans in Mosh and Circle Pits at
# Heavy Metal Concerts", Physical Review Letters 110, 228701 (2013): mosh pits are a disordered gas-like state
# whose speed distribution fits a 2D gas; circle pits are an ordered vortex-like state; about 95% of circle pits
# in their concert videos flowed counterclockwise (5% clockwise). Videos were filmed by fans and posted online.
# Palette sampled from photos/4611544912-1.jpg: pinecone brown (field), mug art red (accent), mug art white (cream).
import os, math
from PIL import Image, ImageDraw, ImageFont

W, H = 1000, 1500
M = 64

FIELD = (62, 36, 26)       # pinecone shadow (44,20,12), lifted so it reads as brown
CREAM = (236, 228, 216)    # mug art white, warmed
DIM = (184, 160, 146)      # linen and pinecone light, between field and cream
LINE = (122, 92, 78)       # circle outlines, a quiet step above the field
RED = (206, 64, 44)        # mug art red (160,47,33), lifted for the dark field

def font(fam, w, s):
    return ImageFont.truetype(f'assets/fonts/{fam}-latin-{w}-normal.woff', s)

im = Image.new('RGB', (W, H), FIELD)
d = ImageDraw.Draw(im)

# --- Photo: full bleed across the top, hard bottom edge --------------------------
PH_H = 690
src = Image.open('photos/4611544912-1.jpg').convert('RGB')
crop_h = round(src.width * PH_H / W)
cy = 140
im.paste(src.crop((0, cy, src.width, cy + crop_h)).resize((W, PH_H), Image.LANCZOS), (0, 0))

def text(x, y, s, f, fill, anchor='l'):
    bb = d.textbbox((0, 0), s, font=f)
    w = bb[2] - bb[0]
    xx = {'l': x, 'c': x - w / 2, 'r': x - w}[anchor] - bb[0]
    d.text((xx, y - bb[1]), s, font=f, fill=fill)
    return bb[3] - bb[1]

# --- Headline --------------------------------------------------------------------
HEAD = font('space-grotesk', 700, 88)
y = PH_H + 60
for i, line in enumerate(('Your mosh pit is', 'technically a gas')):
    text(M, y, line, HEAD, CREAM)
    y += 96
head_bottom = y - 96 + 64

SUB = font('inter', 400, 31)
sub_y = head_bottom + 28
text(M, sub_y, 'Cornell physicists studied metal show videos (2013)', SUB, DIM)

# --- Diagram: two circles --------------------------------------------------------
R = 150
CY = sub_y + 30 + 47 + R  # circle top sits 47 px under the subline
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
    d.ellipse((x - r, y - r, x + r, y + r), fill=CREAM)

for cx in (CX1, CX2):
    d.ellipse((cx - R, CY - R, cx + R, CY + R), outline=LINE, width=4)

# Mosh pit: scattered people, each heading a different way (gas-like, disordered).
# Positions from a seeded spacing search: every dot and arrow clears every other by 14 px or more.
S = 150 / 140
mosh = [(-72, 35, 270), (-55, -79, 75), (-20, 1, 30), (6, 93, 315), (40, -9, 45), (67, -70, 210),
        (104, 21, 255), (-102, -28, 90), (-57, 87, 210), (-1, -72, 225), (78, 69, 135)]
for ox, oy, deg in mosh:
    a = math.radians(deg)
    x, y0 = CX1 + ox * S, CY + oy * S
    arrow(x, y0, math.cos(a), math.sin(a), length=32, head=13)
    dot(x, y0)

# Circle pit: people on a ring, all running counterclockwise around an empty middle (vortex).
RR = 98
for k in range(8):
    th = math.radians(90 + k * 45)
    x, y0 = CX2 + RR * math.cos(th), CY - RR * math.sin(th)
    arrow(x, y0, -math.sin(th), -math.cos(th), length=32, head=13)
    dot(x, y0)

# Labels
LAB = font('inter', 600, 36)
DESC = font('inter', 400, 30)
ly = CY + R + 34
for cx, name, desc in ((CX1, 'Mosh pit', 'Moves like gas molecules'),
                       (CX2, 'Circle pit', '95% flow counterclockwise')):
    text(cx, ly, name, LAB, CREAM, 'c')
    text(cx, ly + 50 + 2, desc, DESC, DIM, 'c')
labels_bottom = ly + 52 + d.textbbox((0, 0), 'Moves like gas molecules', font=DESC)[3] - d.textbbox((0, 0), 'Moves like gas molecules', font=DESC)[1]

# --- Logo: top right of the field, on the headline's first line -----------------
logo = Image.open('assets/hh-monogram-white-140.png').convert('RGBA')
LH = 48
logo = logo.resize((round(logo.width * LH / logo.height), LH), Image.LANCZOS)
tint = Image.new('RGBA', logo.size, DIM + (255,))
tint.putalpha(logo.getchannel('A'))
im.paste(tint, (W - M - logo.width, PH_H + 60 + 8), tint)

print('head_bottom', head_bottom, 'sub', sub_y, 'circle top', CY - R, 'labels_bottom', labels_bottom, 'logo x', W - M - logo.width)
out = os.environ.get('PIN_OUT', 'out.jpg')
im.save(out, 'JPEG', quality=82, optimize=True)
