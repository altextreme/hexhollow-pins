"""Topical pin: what the carvings on old headstones mean. Photo-free labelled diagram.

Sources: South Carolina Dept. of Archives and History, "Symbolism" (skull = mortality, weeping willow =
mourning, lamb = baby or child); Chester County PA tombstone symbols list (hourglass = swiftness of time,
poppy = sleep); 99% Invisible cemetery symbols guide (poppies = eternal sleep).
"""
import os
from PIL import Image, ImageDraw, ImageFont
from lib.icons import icon

W, H = 1000, 1500
F = 'assets/fonts/'
FIELD = (33, 29, 37)        # dusk plum charcoal
STONE = (128, 126, 121)     # weathered granite
CARVE = (72, 68, 70)        # carved recess, darker stone
BONE = (232, 224, 210)
LICHEN = (172, 182, 124)    # lichen on old stone, the one accent
GREY = (166, 160, 158)

im = Image.new('RGBA', (W, H), FIELD + (255,))
d = ImageDraw.Draw(im)


def font(name, size):
    return ImageFont.truetype(F + name, size)


def centered(text, y, f, fill):
    w = d.textlength(text, font=f)
    d.text(((W - w) / 2, y), text, font=f, fill=fill)


# Headline, centered axis
hf = font('playfair-display-latin-900-normal.woff', 132)
centered('The dead', 70, hf, BONE)
centered('left notes', 214, hf, BONE)
sf = font('archivo-narrow-latin-500-normal.woff', 38)
centered('What the carvings on old headstones mean', 398, sf, GREY)

# Headstone: arched tablet on a plinth, ground line edge to edge
SX0, SX1 = 350, 650
R = (SX1 - SX0) // 2
TOP = 486
BASE = 1240
d.ellipse([SX0, TOP, SX1, TOP + 2 * R], fill=STONE)
d.rectangle([SX0, TOP + R, SX1, BASE], fill=STONE)
d.rectangle([SX0 - 30, BASE, SX1 + 30, BASE + 40], fill=STONE)
GROUND = BASE + 40
d.rectangle([0, GROUND, W, GROUND + 3], fill=LICHEN)

# Symbols carved into the stone, labels alternating sides
items = [
    ('gi:death-skull', 'Skull', 'mortality', 'L'),
    ('gi:hourglass', 'Hourglass', 'time moves fast', 'R'),
    ('gi:willow-tree', 'Weeping willow', 'mourning', 'L'),
    ('gi:sheep', 'Lamb', 'a child’s grave', 'R'),
    ('gi:poppy', 'Poppy', 'eternal sleep', 'L'),
]
IC = 122
nf = font('archivo-narrow-latin-700-normal.woff', 40)
mf = font('archivo-narrow-latin-500-normal.woff', 34)
y0, step = 612, 136
for k, (iid, name, meaning, side) in enumerate(items):
    cy = y0 + k * step
    ic = icon(iid, IC, CARVE)
    bb = ic.getbbox()
    gw, gh = bb[2] - bb[0], bb[3] - bb[1]
    im.alpha_composite(ic, (int(W / 2 - bb[0] - gw / 2), int(cy - bb[1] - gh / 2)))
    # leader: from just off the stone edge out toward the label, dot on the stone edge
    if side == 'L':
        x_edge, x_end = SX0, 300
        d.line([(x_end, cy), (x_edge, cy)], fill=LICHEN, width=3)
        d.ellipse([x_edge - 7, cy - 7, x_edge + 7, cy + 7], fill=LICHEN)
        nw = d.textlength(name, font=nf)
        mw = d.textlength(meaning, font=mf)
        d.text((x_end - 16 - nw, cy - 50), name, font=nf, fill=BONE)
        d.text((x_end - 16 - mw, cy + 2), meaning, font=mf, fill=GREY)
    else:
        x_edge, x_end = SX1, 700
        d.line([(x_edge, cy), (x_end, cy)], fill=LICHEN, width=3)
        d.ellipse([x_edge - 7, cy - 7, x_edge + 7, cy + 7], fill=LICHEN)
        d.text((x_end + 16, cy - 50), name, font=nf, fill=BONE)
        d.text((x_end + 16, cy + 2), meaning, font=mf, fill=GREY)

# Footer: sources and logo, centered at the foot
tf = font('inter-latin-500-normal.woff', 30)
centered('Sources: SC Archives and History, 99% Invisible', GROUND + 40, tf, GREY)
mono = Image.open('assets/hh-monogram-white-140.png').convert('RGBA')
mono = mono.resize((int(mono.width * 64 / mono.height), 64), Image.LANCZOS)
tint = Image.new('RGBA', mono.size, BONE + (255,))
tint.putalpha(mono.getchannel('A'))
wf = font('archivo-narrow-latin-700-normal.woff', 34)
word = 'Hex & Hollow'
ww = d.textlength(word, font=wf)
total = mono.width + 14 + ww
lx = int((W - total) / 2)
ly = H - 64 - mono.height
im.alpha_composite(tint, (lx, ly))
d.text((lx + mono.width + 14, ly + mono.height / 2), word, font=wf, fill=BONE, anchor='lm')

im.convert('RGB').save(os.environ['PIN_OUT'], 'JPEG', quality=82)
