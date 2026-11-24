# Hex & Hollow topical pin: bats fly with their hands (Chiroptera means "hand wing").
# Topical, photo-free, no link. A drawn bat, wings spread, with the hand bones showing
# light through a dark membrane. Palette for the topic: pale bone-paper field like a
# naturalist plate, dusk aubergine ink, one dusk rust accent for the finger numbers.
# Facts: National Park Service, How Bats Fly (Chiroptera means hand wing; the wing is a
# modified hand with skin between long finger bones; the only mammals capable of true
# flight). Animal Diversity Web, bat wings (the thumb sits on the leading edge with a
# claw used for climbing, handling food and fighting; digits 2 to 5 support the wing).
import os

from PIL import Image, ImageDraw, ImageFont

W, H, M = 1000, 1500, 64
S = 2  # supersample for smooth curves
FIELD = (236, 230, 219)   # bone paper
INK = (52, 35, 56)        # dusk aubergine: membrane and headline
BONE = (232, 222, 206)    # bones, lighter than the membrane
DIM = (104, 88, 104)      # small text, aubergine gray
RUST = (176, 70, 42)      # dusk rust accent, finger numbers only


def font(fam, wt, size):
    return ImageFont.truetype(f'assets/fonts/{fam}-latin-{wt}-normal.woff', size)


# ---------------------------------------------------------------------------- the bat
big = Image.new('RGB', (W * S, H * S), FIELD)
bd = ImageDraw.Draw(big)
CX = 500


K, OY = 0.88, 34  # scale the drawing about the center line


def T(x, y):
    return (CX + (x - CX) * K, OY + y * K)


def P(x, y):
    x, y = T(x, y)
    return (x * S, y * S)


def qbez(p0, c, p1, n=24):
    pts = []
    for i in range(n + 1):
        t = i / n
        x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * c[0] + t * t * p1[0]
        y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * c[1] + t * t * p1[1]
        pts.append((x, y))
    return pts


# Left wing joints (the right wing mirrors them). y grows downward.
SHOULDER = (462, 372)
ELBOW = (352, 430)
WRIST = (214, 250)
THUMB = [(214, 250), (196, 214), (204, 192)]           # short, hooked claw at the tip
D2 = [(214, 250), (150, 218), (104, 206)]
D3 = [(214, 250), (140, 252), (84, 300), (58, 360)]     # wingtip
D4 = [(214, 250), (168, 340), (130, 440), (112, 520)]
D5 = [(214, 250), (250, 360), (282, 470), (300, 548)]
ANKLE = (440, 600)
HIP = (474, 520)


def scallop(a, b, depth):
    # concave trailing edge between two finger tips, pulled toward the wrist
    mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
    cx = mx + (WRIST[0] - mx) * depth
    cy = my + (WRIST[1] - my) * depth
    return qbez(a, (cx, cy), b)[1:]


def wing_outline():
    pts = [SHOULDER, (300, 296), WRIST, D2[-1]]
    pts += qbez(D2[-1], (60, 250), D3[-1])[1:]              # leading edge to the tip
    pts += scallop(D3[-1], D4[-1], 0.34)
    pts += scallop(D4[-1], D5[-1], 0.30)
    pts += scallop(D5[-1], ANKLE, 0.24)
    pts += [HIP]
    return pts


def mirror(pts):
    return [(2 * CX - x, y) for x, y in pts]


def poly(pts, fill):
    bd.polygon([P(x, y) for x, y in pts], fill=fill)


left = wing_outline()
poly(left, INK)
poly(mirror(left), INK)

# body, head, ears, legs
bd.ellipse((P(452, 350) + P(548, 560)), fill=INK)
bd.ellipse((P(462, 292) + P(538, 368)), fill=INK)
for side in (1, -1):
    ear = [(CX + side * 12, 300), (CX + side * 34, 246), (CX + side * 38, 316)]
    poly(ear, INK)
    leg = [HIP, ANKLE, (ANKLE[0] - 6, ANKLE[1] + 22), (ANKLE[0] + 14, ANKLE[1] + 6), (500, 548)]
    poly(leg if side == 1 else mirror(leg), INK)


def bone_line(pts, w):
    for side in (False, True):
        q = mirror(pts) if side else pts
        bd.line([P(x, y) for x, y in q], fill=BONE, width=w * S, joint='curve')
        for x, y in q:
            r = w * 0.85
            bd.ellipse((P(x - r, y - r) + P(x + r, y + r)), fill=BONE)


bone_line([SHOULDER, ELBOW], 12)       # humerus
bone_line([ELBOW, WRIST], 10)          # forearm
for finger in (D2, D3, D4, D5):
    bone_line(finger, 7)

# thumb: a dark, skin-covered nub on the leading edge with a hooked claw
for side in (False, True):
    th = mirror(THUMB) if side else THUMB
    bd.line([P(x, y) for x, y in th], fill=INK, width=round(14 * K * S), joint='curve')
    tip = th[-1]
    dx = -1 if side else 1
    claw = qbez(tip, (tip[0] + dx * 14, tip[1] - 8), (tip[0] + dx * 22, tip[1] + 8), 10)
    bd.line([P(x, y) for x, y in claw], fill=INK, width=round(6 * K * S), joint='curve')

im = big.resize((W, H), Image.LANCZOS)
d = ImageDraw.Draw(im)


def text(s, x, y, f, col, anchor='l'):
    b = d.textbbox((0, 0), s, font=f)
    if anchor == 'r':
        x = x - (b[2] - b[0])
    elif anchor == 'c':
        x = x - (b[2] - b[0]) / 2
    d.text((x - b[0], y - b[1]), s, font=f, fill=col)
    return b[2] - b[0], b[3] - b[1]


# ---------------------------------------------------------------- labels on the drawing
NF = font('fraunces', 900, 46)
LF = font('inter', 500, 32)
# finger numbers sit just past each tip on the right wing
tips = {'2': D2[-1], '3': D3[-1], '4': D4[-1], '5': D5[-1]}
offs = {'2': (-8, -62), '3': (14, -10), '4': (14, 10), '5': (-12, 26)}
for k, (x, y) in tips.items():
    mx, my = T(2 * CX - x, y)
    ox, oy = offs[k]
    text(k, mx + ox, my + oy, NF, RUST)
# the thumb's number, on the same wing, up and left of its claw
tx, ty = T(2 * CX - THUMB[-1][0], THUMB[-1][1])
text('1', tx - 60, ty - 58, NF, RUST)

# ------------------------------------------------------------------------- type block
HF = font('fraunces', 900, 128)
y = 726
text('Bats fly with', M, y, HF, INK)
y += 140
text('their hands', M, y, HF, INK)
y += 140 + 40
SF = font('inter', 400, 36)
text('Chiroptera, the bat order, is Greek for “hand wing”', M, y, SF, DIM)

y += 100
KF = font('fraunces', 900, 44)
KT = font('inter', 400, 34)
rows = [('1', 'A free thumb with a claw, for climbing'),
        ('2 to 5', 'Four long fingers stretch the skin into a wing')]
for n, s in rows:
    text(n, M, y - 4, KF, RUST)
    text(s, M + 150, y, KT, INK)
    y += 66

# --------------------------------------------------------------------------- footer
FY = H - M - 34
text('Sources: National Park Service, Animal Diversity Web', M, FY + 2, font('inter', 400, 30), DIM)
logo = Image.open('assets/hh-monogram-white-140.png').convert('RGBA')
LH = 40
logo = logo.resize((round(logo.width * LH / logo.height), LH), Image.LANCZOS)
tint = Image.new('RGBA', logo.size, DIM + (255,))
tint.putalpha(logo.getchannel('A'))
im.paste(tint, (W - M - logo.width, FY - 4), tint)

im.save(os.environ.get('PIN_OUT', 'out.jpg'), quality=82, optimize=True)
