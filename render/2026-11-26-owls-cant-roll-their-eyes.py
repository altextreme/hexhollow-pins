# Hex & Hollow topical pin: owls can't roll their eyes, so they turn their heads up to 270 degrees.
# Topical, photo-free, no link. A drawn dial: a flat owl face at the center, two amber arcs
# sweeping 270 degrees clockwise and counterclockwise from facing forward. Below the headline,
# a neck-bone comparison: 7 cervical vertebrae for a person, 14 for an owl.
# Palette for the topic: night pine field, bone headline, tawny and wheat for the owl,
# amber accent on the arcs, eyes and the owl's 14 bones only.
# Facts: Johns Hopkins University, Jan 31 2013 (via ScienceDaily): owls can rotate their heads
# by as much as 270 degrees in either direction; 14 cervical vertebrae in the owl's neck.
# National Geographic (2013): owls have fixed eye sockets, so their eyeballs can't rotate.
# Humans have 7 cervical vertebrae (standard anatomy).
import math
import os

from PIL import Image, ImageDraw, ImageFont

W, H, M = 1000, 1500, 64
S = 2
FIELD = (27, 43, 38)       # night pine
FIELD_D = (20, 33, 29)     # pupils, beak shadow
BONE = (234, 228, 210)     # headline
TXT = (206, 210, 196)      # body
DIM = (150, 164, 152)      # small text, human bones
AMBER = (232, 168, 70)     # arcs, eyes, owl bones
TAWNY = (138, 100, 66)     # owl head
WHEAT = (204, 172, 124)    # facial disc
BEAK = (74, 56, 42)


def font(fam, wt, size):
    return ImageFont.truetype(f'assets/fonts/{fam}-latin-{wt}-normal.woff', size * S)


big = Image.new('RGB', (W * S, H * S), FIELD)
d = ImageDraw.Draw(big)


def P(x, y):
    return (round(x * S), round(y * S))


def circ(cx, cy, r, fill):
    d.ellipse([P(cx - r, cy - r), P(cx + r, cy + r)], fill=fill)


# ------------------------------------------------------------------ dial
CX, CY = 500, 368
R1, R2 = 262, 218   # outer arc clockwise, inner arc counterclockwise
AW = 10


def arc_pts(r, a0, a1, n=240):
    # angles in degrees, 0 = facing forward (up), positive = clockwise
    pts = []
    for i in range(n + 1):
        a = math.radians(a0 + (a1 - a0) * i / n)
        pts.append((CX + r * math.sin(a), CY - r * math.cos(a)))
    return pts


def head(r, sign):
    # arrowhead whose tip sits exactly at 270 degrees on radius r
    L, Wd = 40, 21
    a_tip = sign * 270
    a_base = sign * (270 - math.degrees(L / r))
    def at(a, rr):
        t = math.radians(a)
        return (CX + rr * math.sin(t), CY - rr * math.cos(t))
    d.polygon([P(*at(a_tip, r)), P(*at(a_base, r + Wd)), P(*at(a_base, r - Wd))], fill=AMBER)
    return a_base


for r, sign in ((R1, 1), (R2, -1)):
    a_base = head(r, sign)
    pts = arc_pts(r, 0, a_base + sign * 1)
    d.line([P(*p) for p in pts], fill=AMBER, width=AW * S, joint='curve')
    circ(*pts[0], AW / 2, AMBER)

# start marker: a short bone tick across both arcs at facing forward
d.line([P(CX, CY - R1 - 22), P(CX, CY - R2 + 22)], fill=BONE, width=4 * S)

# owl face
d.polygon([P(CX - 118, CY - 60), P(CX - 92, CY - 152), P(CX - 40, CY - 96)], fill=TAWNY)   # tufts
d.polygon([P(CX + 118, CY - 60), P(CX + 92, CY - 152), P(CX + 40, CY - 96)], fill=TAWNY)
d.ellipse([P(CX - 132, CY - 112), P(CX + 132, CY + 138)], fill=TAWNY)
circ(CX - 56, CY + 2, 70, WHEAT)
circ(CX + 56, CY + 2, 70, WHEAT)
for ex in (CX - 56, CX + 56):
    circ(ex, CY - 2, 40, AMBER)
    circ(ex, CY - 2, 21, FIELD_D)
d.polygon([P(CX - 14, CY + 46), P(CX + 14, CY + 46), P(CX, CY + 84)], fill=BEAK)

# 270 degree labels at the arrow tips
LF = font('dm-serif-display', 400, 58)
d.text(P(M, CY), '270°', font=LF, fill=AMBER, anchor='lm')
d.text(P(W - M, CY), '270°', font=LF, fill=AMBER, anchor='rm')

# ------------------------------------------------------------------ type
HF = font('dm-serif-display', 400, 112)
y = 694
for line in ['Owls can’t roll', 'their eyes']:
    d.text(P(M - 4, y), line, font=HF, fill=BONE)
    y += 116
BF = font('dm-sans', 400, 36)
y = 974
for line in ['Their eyes are fixed in place, so the whole head', 'turns instead, up to 270° either way.']:
    d.text(P(M, y), line, font=BF, fill=TXT)
    y += 50

# ------------------------------------------------------------------ neck bones
SF = font('dm-sans', 500, 32)
BW, BH, GAP = 38, 46, 8
rows = [('Your neck: 7 vertebrae', 7, DIM), ('An owl’s neck: 14', 14, AMBER)]
y = 1104
for label, n, col in rows:
    d.text(P(M, y), label, font=SF, fill=col if col == AMBER else TXT)
    by = y + 48
    for i in range(n):
        x = M + i * (BW + GAP)
        d.rounded_rectangle([P(x, by), P(x + BW, by + BH)], radius=10 * S, fill=col)
    y += 122

# ------------------------------------------------------------------ footer
FY = H - M - 32
FF = font('dm-sans', 400, 30)
d.text(P(W - M, FY), 'Sources: Johns Hopkins, National Geographic', font=FF, fill=DIM, anchor='ra')

im = big.resize((W, H), Image.LANCZOS)
logo = Image.open('assets/hh-monogram-white-140.png').convert('RGBA')
LH = 40
logo = logo.resize((round(logo.width * LH / logo.height), LH), Image.LANCZOS)
tint = Image.new('RGBA', logo.size, DIM + (255,))
tint.putalpha(logo.getchannel('A'))
im.paste(tint, (M, FY - 4), tint)

im.save(os.environ.get('PIN_OUT', 'out.jpg'), quality=82, optimize=True)
