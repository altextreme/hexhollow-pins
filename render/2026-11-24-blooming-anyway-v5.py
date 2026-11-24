# Hex & Hollow pin: the Hildesheim rose, bombed in 1945 and blooming anyway.
# Product: Still Growing skull and roses hoodie (listing 4611545302). Photo-free cross-section diagram.
# Palette sampled from the listing mockup (photos/4611545302-1.jpg): hoodie charcoal, skull bone,
# rose red (lifted for contrast on the dark field), leaf taupe.
import math
import os
import random

from PIL import Image, ImageDraw, ImageFont

W, H, M = 1000, 1500, 64
SKY = (46, 47, 50)        # hoodie charcoal, a touch deeper
SOIL = (30, 29, 31)       # under the ground line
STONE = (70, 69, 72)      # apse wall
MORTAR = (58, 57, 60)
RUBBLE = (92, 87, 84)
RUBBLE2 = (74, 70, 68)
BONE = (226, 208, 186)    # skull print
DIM = (188, 178, 166)
RED = (184, 48, 52)       # rose print, lifted
STEM = (156, 141, 125)    # leaf print
ROOT = (176, 146, 112)


def font(fam, wt, size):
    return ImageFont.truetype(f'assets/fonts/{fam}-latin-{wt}-normal.woff', size)


im = Image.new('RGB', (W, H), SKY)
d = ImageDraw.Draw(im)
random.seed(1945)

GROUND = 1010
d.rectangle((0, GROUND, W, H), fill=SOIL)


def text(s, x, y, f, col, anchor='l'):
    b = d.textbbox((0, 0), s, font=f)
    if anchor == 'r':
        x = x - (b[2] - b[0])
    d.text((x - b[0], y - b[1]), s, font=f, fill=col)
    return b[3] - b[1]


# --- Headline ----------------------------------------------------------------------------
HF = font('pirata-one', 400, 136)
y = M + 6
h1 = text('Bombed in 1945.', M, y, HF, BONE)
y += 150
text('Blooming anyway.', M, y, HF, RED)
y += 150 + 14
SF = font('inter', 500, 34)
text('The rose on Hildesheim Cathedral, Germany', M, y, SF, DIM)

# --- Apse wall (above ground, right side) ------------------------------------------------
WX0, WX1, WTOP = 504, 936, 452
AR = (WX1 - WX0) // 2  # arch radius
d.rectangle((WX0, WTOP + AR, WX1, GROUND), fill=STONE)
d.pieslice((WX0, WTOP, WX1, WTOP + 2 * AR), 180, 360, fill=STONE)
# mortar courses
for yy in range(WTOP + AR + 30, GROUND, 52):
    d.line((WX0, yy, WX1, yy), fill=MORTAR, width=3)
    off = 0 if (yy // 52) % 2 else 40
    for xx in range(WX0 + off, WX1, 80):
        d.line((xx, yy, xx, min(yy + 52, GROUND)), fill=MORTAR, width=3)

# --- Rubble band just under the ground line ---------------------------------------------
RB0, RB1 = GROUND + 8, GROUND + 96


def chunk(cx, cy, r, col):
    n = random.randint(5, 7)
    pts = []
    for i in range(n):
        a = 2 * math.pi * i / n + random.uniform(-0.3, 0.3)
        rr = r * random.uniform(0.7, 1.0)
        pts.append((cx + rr * math.cos(a), cy + rr * 0.75 * math.sin(a)))
    d.polygon(pts, fill=col)


for _ in range(56):
    cx = random.uniform(560, W - M - 20)
    cy = random.uniform(RB0 + 14, RB1 - 10)
    chunk(cx, cy, random.uniform(14, 28), random.choice((RUBBLE, RUBBLE2)))
# one deliberate stone at the heap's left end, where the March 1945 leader lands
STONE_PT = (486, 1058)
chunk(STONE_PT[0], STONE_PT[1], 28, RUBBLE)

# --- Root under the rubble ---------------------------------------------------------------
RX, RY = 700, 1176
d.ellipse((RX - 34, RY - 22, RX + 34, RY + 22), fill=ROOT)
for ang, ln in ((200, 120), (230, 90), (250, 70), (290, 70), (315, 100), (340, 130), (160, 80), (20, 90)):
    a = math.radians(ang)
    x1 = RX + ln * math.cos(a)
    y1 = RY - ln * 0.45 * math.sin(a) + 30
    d.line((RX, RY, x1, y1), fill=ROOT, width=9)
    d.line((x1, y1, x1 + 24 * math.cos(a + 0.5), y1 + 18), fill=ROOT, width=5)

# --- Shoots: up from the root, through the rubble, up the wall ----------------------------
def stem(x0, y0, pts, w=6):
    path = [(x0, y0)] + pts
    d.line(path, fill=STEM, width=w, joint='curve')
    return path


BR = 22                    # bloom radius
TIP_CLEAR = BR + 24         # a bare stem tip stops this far from any bloom centre

tops = []
for i in range(25):
    t = i / 24
    tx = 572 + 296 * t + random.uniform(-14, 14)
    arch = 1 - (2 * t - 1) ** 2
    ty = 690 - 170 * arch + random.uniform(0, 200) * (i % 3 == 1) + random.uniform(0, 40)
    tops.append((tx, ty))

placed = []
for (x, y) in tops:
    if y > GROUND - 120:
        continue
    if all((x - px) ** 2 + (y - py) ** 2 >= 60 ** 2 for px, py in placed):
        placed.append((x, y))


def near_bloom(x, y):
    return min(math.hypot(x - px, y - py) for px, py in placed)


def full_path(i, tx, ty):
    sx = RX - 36 + 3 * i
    pts = [(sx, RY - 18)]
    steps = 60
    for k in range(1, steps + 1):
        u = k / steps
        mx = sx + (tx - sx) * (u ** 0.8) + 10 * math.sin(u * 5 + i)
        my = RY - 20 + (ty - (RY - 20)) * u
        pts.append((mx, my))
    return pts


def seg_dist(px, py, a, b):
    (x1, y1), (x2, y2) = a, b
    dx, dy = x2 - x1, y2 - y1
    ln = dx * dx + dy * dy
    t = 0 if ln == 0 else max(0, min(1, ((px - x1) * dx + (py - y1) * dy) / ln))
    return math.hypot(px - x1 - t * dx, py - y1 - t * dy)


full = [full_path(i, tx, ty) for i, (tx, ty) in enumerate(tops)]

# A flowering stem may pass another bloom only clearly behind it (edge 6+ px inside)
# or clearly clear of it (15+ px). Drop any bloom that a flowering stem grazes.
changed = True
while changed:
    changed = False
    for b in list(placed):
        for i, top in enumerate(tops):
            if top == b or top not in placed:
                continue
            dm = min(seg_dist(b[0], b[1], full[i][k], full[i][k + 1]) for k in range(len(full[i]) - 1))
            gap = dm - 2 - BR  # stem half width 2
            if -6 < gap < 15:
                placed.remove(b)
                changed = True
                break
        if changed:
            break

paths = []
for i, (tx, ty) in enumerate(tops):
    pts = full[i]
    if (tx, ty) not in placed:
        # a bare stem: cut it where it first comes within TIP_CLEAR of a bloom
        for k, (x, y) in enumerate(pts):
            if near_bloom(x, y) < TIP_CLEAR:
                pts = pts[:max(k, 2)]
                break
    d.line(pts, fill=STEM, width=4, joint='curve')
    paths.append(pts)

for p in paths:
    for (x, y) in p[10:-3:7]:
        if y < GROUND - 20 and near_bloom(x, y) > BR + 24:
            d.line((x, y, x + 9, y - 7), fill=STEM, width=3)

# blooms: each sits on the tip of its own stem; a petal cup plus a spiral heart
DARK = (124, 26, 32)


def bloom(x, y, r):
    for a in (90, 210, 330):
        ox = r * 0.32 * math.cos(math.radians(a))
        oy = r * 0.32 * math.sin(math.radians(a))
        d.ellipse((x + ox - r * 0.78, y + oy - r * 0.78, x + ox + r * 0.78, y + oy + r * 0.78), fill=RED)
    pts = []
    for k in range(40):
        th = k * 0.32
        rr = r * 0.62 * (1 - k / 44)
        pts.append((x + rr * math.cos(th) + 2, y + rr * math.sin(th)))
    d.line(pts, fill=DARK, width=4, joint='curve')


for (x, y) in placed:
    bloom(x, y, BR)
# the Today leader lands on the highest bloom in the left half of the bush
left = [b for b in placed if b[0] < 700]
TODAY = min(left, key=lambda b: b[1])

# --- Labels with leaders -------------------------------------------------------------------
LB = font('inter', 600, 34)
LR = font('inter', 400, 32)


def label(y, head, body, tx, ty, hc=BONE):
    text(head, M, y, LB, hc)
    text(body, M, y + 46, LR, DIM)
    lx = M + max(d.textlength(head, font=LB), d.textlength(body, font=LR)) + 20
    d.line((lx, ty, tx, ty), fill=DIM, width=2)
    d.ellipse((tx - 9, ty - 9, tx + 9, ty + 9), fill=DIM, outline=SOIL, width=3)


label(round(TODAY[1]) - 20, 'Today', 'about 10 m up the apse', round(TODAY[0]), round(TODAY[1]))
label(900, '8 weeks later', '25 new shoots', 470, 942)  # ends in open air, short of the wall
label(1036, 'March 1945', 'the cathedral is bombed', STONE_PT[0], STONE_PT[1])
label(1140, 'Under the debris', 'one root survives', RX, RY)  # centred on the root bulb

NF = font('inter', 500, 34)
text('Believed to be the oldest living rose on Earth', M, 1300, NF, BONE)

# --- Footer --------------------------------------------------------------------------------
logo = Image.open('assets/hh-monogram-white-140.png').convert('RGBA')
LH = 44
logo = logo.resize((round(logo.width * LH / logo.height), LH), Image.LANCZOS)
tint = Image.new('RGBA', logo.size, DIM + (255,))
tint.putalpha(logo.getchannel('A'))
fy = H - M - LH
im.paste(tint, (W - M - logo.width, fy), tint)
FF = font('inter', 400, 32)
s = 'Sources: Hildesheim Cathedral, Wikipedia'
sb = d.textbbox((0, 0), s, font=FF)
d.text((M - sb[0], fy + (LH - (sb[3] - sb[1])) / 2 - sb[1]), s, font=FF, fill=DIM)

im.save(os.environ.get('PIN_OUT', 'out.jpg'), quality=82, optimize=True)
