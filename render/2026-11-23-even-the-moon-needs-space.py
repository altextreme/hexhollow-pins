"""Topical pin: the Moon drifts about 3.8 cm farther from Earth every year. Photo-free.

Source: NASA JPL, "Apollo 11 Experiment Continues to Return Valuable Data": the Moon is receding from Earth
at about 3.8 centimeters (1.5 inches) a year, measured by bouncing lasers off the retroreflector
Apollo 11 left on the Moon in July 1969.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1000, 1500
F = 'assets/fonts/'
FIELD = (46, 18, 24)        # deep oxblood night
MOON = (228, 218, 200)      # moon bone
MARE = (196, 184, 166)      # maria, a step darker than the bone
BONE = (238, 228, 210)      # headline
GOLD = (222, 182, 108)      # the one accent: the number, the mirror
DIM = (190, 160, 156)       # small text

im = Image.new('RGBA', (W, H), FIELD + (255,))
d = ImageDraw.Draw(im)


def font(name, size):
    return ImageFont.truetype(F + name, size)


M = 64

# Logo, top left
mono = Image.open('assets/hh-monogram-white-140.png').convert('RGBA')
mono = mono.resize((int(mono.width * 56 / mono.height), 56), Image.LANCZOS)
tint = Image.new('RGBA', mono.size, DIM + (255,))
tint.putalpha(mono.getchannel('A'))
im.alpha_composite(tint, (M, M))
wf = font('inter-latin-500-normal.woff', 30)
d.text((M + mono.width + 14, M + 28), 'Hex & Hollow', font=wf, fill=DIM, anchor='lm')

# The Moon, drawn flat: disc plus the main maria, clipped to the disc
CX, CY, R = 500, 440, 250
S = 4  # supersample
moon = Image.new('RGBA', (2 * R * S, 2 * R * S), (0, 0, 0, 0))
md = ImageDraw.Draw(moon)
md.ellipse((0, 0, 2 * R * S - 1, 2 * R * S - 1), fill=MOON + (255,))
maria = [  # (x, y, rx, ry) in units of R, x right, y down, near side as seen from the north
    (-0.26, -0.38, 0.28, 0.22),  # Imbrium
    (0.24, -0.42, 0.16, 0.14),   # Serenitatis
    (0.36, -0.02, 0.20, 0.17),   # Tranquillitatis
    (0.70, -0.30, 0.11, 0.10),   # Crisium
    (0.64, 0.24, 0.11, 0.14),    # Fecunditatis
    (-0.56, 0.02, 0.24, 0.40),   # Procellarum
    (-0.16, 0.36, 0.18, 0.12),   # Nubium
]
mask = Image.new('L', moon.size, 0)
ImageDraw.Draw(mask).ellipse((0, 0, 2 * R * S - 1, 2 * R * S - 1), fill=255)
layer = Image.new('RGBA', moon.size, (0, 0, 0, 0))
ld = ImageDraw.Draw(layer)
for x, y, rx, ry in maria:
    px, py = (1 + x) * R * S, (1 + y) * R * S
    ld.ellipse((px - rx * R * S, py - ry * R * S, px + rx * R * S, py + ry * R * S), fill=MARE + (255,))
layer.putalpha(Image.composite(layer.getchannel('A'), Image.new('L', moon.size, 0), mask))
moon.alpha_composite(layer)
moon = moon.resize((2 * R, 2 * R), Image.LANCZOS)
im.alpha_composite(moon, (CX - R, CY - R))

# Apollo 11 mirror (Tranquility Base, about 23.5 E, 0.7 N) with a leader to its label
ax, ay = int(CX + 0.40 * R), int(CY - 0.01 * R)
d.ellipse((ax - 9, ay - 9, ax + 9, ay + 9), fill=GOLD)
LX = CX + R + 34
d.line((ax + 9, ay, LX - 12, ay), fill=GOLD, width=3)
lf = font('inter-latin-500-normal.woff', 30)
d.text((LX, ay - 4), 'Apollo 11', font=lf, fill=GOLD, anchor='ls')
d.text((LX, ay + 34), 'mirror', font=lf, fill=GOLD, anchor='ls')

# Headline, flush left
hf = font('dm-serif-display-latin-400-normal.woff', 132)
HY = 800
d.text((M - 4, HY), 'Even the moon', font=hf, fill=BONE)
d.text((M - 4, HY + 128), 'needs space', font=hf, fill=BONE)

# Big number with its label centered on the figure height
nf = font('dm-serif-display-latin-400-normal.woff', 156)
NY = 1272  # baseline
num = '3.8 cm'
d.text((M - 4, NY), num, font=nf, fill=GOLD, anchor='ls')
nw = d.textlength(num, font=nf)
top = d.textbbox((M - 4, NY), '3', font=nf, anchor='ls')[1]
mid = (top + NY) / 2
sf = font('inter-latin-400-normal.woff', 36)
TX = M + nw + 36
d.text((TX, mid - 6), 'farther from Earth,', font=sf, fill=BONE, anchor='ls')
d.text((TX, mid + 40), 'every year', font=sf, fill=BONE, anchor='ls')

# Support line, anchored to the foot
bf = font('inter-latin-400-normal.woff', 32)
d.text((M, H - M - 46), 'NASA clocks it with lasers bounced off the', font=bf, fill=DIM, anchor='ls')
d.text((M, H - M), 'mirror Apollo 11 left on the moon in 1969', font=bf, fill=DIM, anchor='ls')

im.convert('RGB').save(os.environ['PIN_OUT'], 'JPEG', quality=82)
