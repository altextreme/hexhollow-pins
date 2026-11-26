# Hex & Hollow topical pin: the Mari Lwyd, the horse skull that goes caroling in south Wales.
# Topical, photo-free, no link. A drawn Mari Lwyd (horse skull on a pole under a white sheet,
# ribbons, glass bottle eyes, snapping jaw) with labelled leaders, on a deep winter-night field.
# Palette for the topic: midnight indigo field, bone white for the skull and sheet, ribbon gold
# for the headline, one oxblood ribbon, bottle-glass green for the eyes only.
# Facts: Museum Wales, "Winter Folklore and Tradition: The Mari Lwyd" (horse's head decorated
# with coloured ribbons and rosettes and glass bottle eyes; lower jaw on a spring that shuts
# with a loud snap; a long white cloth hides the carrier; Christmas Day to Twelfth Night; south
# Wales; the pwnco rhyme contest at the closed door; a Mari inside was thought to bring good
# luck, so the Mari party would usually win, or be allowed to win). Wikipedia, Mari Lwyd
# (a horse's skull mounted on a pole, carried by a person hidden under a sheet).
import math
import os

from PIL import Image, ImageDraw, ImageFont

W, H, M = 1000, 1500, 64
S = 2
FIELD = (31, 34, 60)       # midnight indigo
FIELD_D = (24, 26, 47)     # orbit and mouth shadow
BONE = (234, 226, 208)     # skull
BONE_S = (196, 184, 162)   # skull shading lines
SHEET = (226, 222, 214)    # the white cloth, a touch cooler than the bone
SHEET_S = (184, 182, 186)  # cloth folds
GOLD = (224, 178, 92)      # headline, gold ribbon, leader dots
OXB = (150, 44, 56)        # oxblood ribbon
GLASS = (118, 176, 132)    # bottle-glass eye
TXT = (222, 218, 228)      # labels
DIM = (150, 150, 176)      # small text


def font(fam, wt, size):
    return ImageFont.truetype(f'assets/fonts/{fam}-latin-{wt}-normal.woff', size)


big = Image.new('RGB', (W * S, H * S), FIELD)
bd = ImageDraw.Draw(big)


def bez(p0, c1, c2, p1, n=28):
    out = []
    for i in range(n + 1):
        t = i / n
        u = 1 - t
        out.append((u**3 * p0[0] + 3 * u * u * t * c1[0] + 3 * u * t * t * c2[0] + t**3 * p1[0],
                    u**3 * p0[1] + 3 * u * u * t * c1[1] + 3 * u * t * t * c2[1] + t**3 * p1[1]))
    return out


def path(segs):
    pts = []
    for s in segs:
        pts += s if not pts else s[1:]
    return pts


# Skull local coords: nose tip at x=0, facing left, y down. Placed by OX, OY, scale K.
K = 0.92
OX, OY = 326, 516


def G(x, y):
    return (OX + x * K, OY + y * K)


def GS(pts):
    return [((OX + x * K) * S, (OY + y * K) * S) for x, y in pts]


def rot(pts, cx, cy, deg):
    a = math.radians(deg)
    ca, sa = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * ca - (y - cy) * sa, cy + (x - cx) * sa + (y - cy) * ca) for x, y in pts]


# ---------------------------------------------------------------------------- the sheet
# Hangs from the back of the skull to a wavy hem; drawn first so the skull sits on top.
sheet = path([
    bez((420, 30), (470, -20), (560, -10), (590, 60)),          # over the back of the head
    bez((590, 60), (610, 260), (640, 520), (660, 735)),         # back edge, falling
    bez((660, 735), (630, 760), (600, 712), (560, 742)),        # hem waves, right to left
    bez((560, 742), (520, 772), (490, 716), (450, 746)),
    bez((450, 746), (410, 776), (380, 718), (340, 748)),
    bez((340, 748), (310, 770), (285, 735), (262, 744)),
    bez((262, 744), (300, 560), (360, 330), (400, 170)),        # front edge, rising to the jaw
    bez((400, 170), (410, 120), (412, 70), (420, 30)),
])
bd.polygon(GS(sheet), fill=SHEET)
for f in [bez((470, 90), (480, 300), (500, 520), (505, 720)),
          bez((540, 80), (560, 300), (585, 520), (600, 715)),
          bez((420, 220), (410, 400), (380, 560), (360, 730))]:
    bd.line(GS(f), fill=SHEET_S, width=5 * S, joint='curve')

# ---------------------------------------------------------------------------- ribbons
# Streamers tied behind the ear, falling over the front of the cloth.
rib = [(OXB, [(452, 2), (430, 120), (470, 220), (440, 330)]),
       (GOLD, [(462, 4), (468, 130), (500, 250), (486, 380)]),
       (OXB, [(474, 6), (510, 120), (540, 210), (536, 300)])]
for col, (a, b, c, d) in rib:
    bd.line(GS(bez(a, b, c, d)), fill=col, width=22 * S, joint='curve')

# ---------------------------------------------------------------------------- skull
upper = path([
    bez((0, 92), (10, 70), (60, 58), (140, 44)),                # nose tip up to the nasal bone
    bez((140, 44), (230, 28), (300, 16), (350, 2)),             # long nasal line
    bez((350, 2), (380, -8), (420, -30), (460, -26)),           # brow and poll
    bez((460, -26), (500, -22), (520, 8), (516, 44)),           # back of the skull
    bez((516, 44), (512, 80), (490, 100), (462, 110)),          # occiput down to the hinge
    bez((462, 110), (440, 132), (400, 150), (350, 154)),        # cheek to the tooth row
    bez((350, 154), (290, 158), (220, 152), (170, 146)),        # upper cheek teeth line
    bez((170, 146), (130, 138), (90, 128), (52, 130)),          # gap before the front teeth
    bez((52, 130), (30, 132), (6, 120), (0, 92)),               # incisors to the tip
])
HX, HY = 448, 118  # jaw hinge
JA = 10  # degrees the jaw hangs open
lower = path([
    bez((40, 150), (110, 150), (200, 160), (300, 168)),         # top edge, under the teeth
    bez((300, 168), (360, 170), (400, 160), (430, 132)),        # rising to the hinge
    bez((430, 132), (450, 120), (474, 120), (480, 140)),        # condyle
    bez((480, 140), (488, 190), (470, 236), (420, 244)),        # back of the jaw, the angle
    bez((420, 244), (360, 252), (300, 222), (220, 206)),        # jaw underside
    bez((220, 206), (150, 194), (80, 188), (40, 182)),
    bez((40, 182), (22, 178), (18, 156), (40, 150)),            # chin
])
lower = rot(lower, HX, HY, -JA)  # jaw dropped open
# mouth: the dark gap between the jaws, then teeth poking into it, then the bones on top
bot_edge = rot([(40, 150), (300, 168), (430, 132)], HX, HY, -JA)
bd.polygon(GS([(6, 110), (52, 130), (170, 146), (350, 154), (440, 130)] + bot_edge[::-1]), fill=FIELD_D)


def tooth(x0, y0, x1, y1, ang=0):
    pts = rot([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], HX, HY, -ang) if ang else \
        [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    bd.polygon(GS(pts), fill=BONE)


for x in range(184, 344, 24):       # upper cheek teeth hang into the gap
    tooth(x, 130, x + 19, 166)
for x in range(6, 50, 14):          # upper incisors
    tooth(x, 110, x + 11, 142)
for x in range(198, 330, 24):       # lower cheek teeth rise from the jaw
    tooth(x, 150, x + 19, 178, JA)
for x in range(36, 80, 14):         # lower incisors
    tooth(x, 136, x + 11, 168, JA)
bd.polygon(GS(lower), fill=BONE)
bd.polygon(GS(upper), fill=BONE)

# nasal notch, facial crest, eye ridge
bd.polygon(GS(path([bez((34, 96), (70, 82), (130, 76), (176, 70)),
                    bez((176, 70), (130, 88), (80, 98), (34, 96))])), fill=FIELD_D)
bd.line(GS(bez((360, 120), (320, 112), (270, 108), (220, 112))), fill=BONE_S, width=5 * S)
bd.line(GS(bez((470, 20), (490, 40), (496, 70), (480, 96))), fill=BONE_S, width=4 * S)

# rosette at the knot, pinned behind the ear
cx, cy = G(474, -12)
for i in range(10):
    a = math.radians(i * 36)
    px, py = cx + math.cos(a) * 22, cy + math.sin(a) * 22
    bd.ellipse([(px - 13) * S, (py - 13) * S, (px + 13) * S, (py + 13) * S], fill=GOLD)
bd.ellipse([(cx - 14) * S, (cy - 14) * S, (cx + 14) * S, (cy + 14) * S], fill=OXB)

# orbit and the glass bottle eye
EX, EY, ER = 392, 52, 40
ex, ey = G(EX, EY)
bd.ellipse([(ex - ER) * S, (ey - ER * 0.9) * S, (ex + ER) * S, (ey + ER * 0.9) * S], fill=FIELD_D)
gr = 26
bd.ellipse([(ex - gr) * S, (ey - gr) * S, (ex + gr) * S, (ey + gr) * S], fill=GLASS)
bd.ellipse([(ex - gr + 9) * S, (ey - gr + 8) * S, (ex - gr + 21) * S, (ey - gr + 20) * S],
           fill=(214, 236, 214))

im = big.resize((W, H), Image.LANCZOS)
d = ImageDraw.Draw(im)


def text(s, x, y, f, col):
    d.text((x, y), s, font=f, fill=col)


# ---------------------------------------------------------------------------- type
HF = font('gloock', 400, 92)
y = 84
for line in ['Wales goes caroling', 'with a horse skull']:
    text(line, M - 4, y, HF, GOLD)
    y += 102
SF = font('inter', 400, 34)
text('The Mari Lwyd, Christmas to Twelfth Night', M, y + 26, SF, DIM)

LF = font('inter', 500, 32)


def dot(x, y, r=7):
    d.ellipse([x - r, y - r, x + r, y + r], fill=GOLD)


def leader(pts):
    d.line(pts, fill=GOLD, width=3)
    dot(*pts[-1])


# eye: text above the skull, elbow down to the orbit
exg, eyg = G(EX, EY)
text('Glass bottle eyes', M, 418, LF, TXT)
leader([(M + 290, 438), (exg, 438), (exg, eyg - ER * 0.9 + 4)])

# jaw: text under the open front of the jaw
jx, jy = G(*rot([(70, 186)], HX, HY, -JA)[0])
text('A spring jaw', M, 744, LF, TXT)
text('that snaps shut', M, 784, LF, TXT)
leader([(M + 206, 764), (jx, 764), (jx, jy + 6)])

# ribbons
rx, ry = G(440, 330)
text('Ribbons and', M, 890, LF, TXT)
text('rosettes', M, 930, LF, TXT)
leader([(M + 200, 912), (rx - 14, 912), (rx - 14, ry - 4)])

# sheet
sx, sy = G(300, 580)
text('A white sheet', M, 1040, LF, TXT)
text('hides the carrier', M, 1080, LF, TXT)
leader([(M + 262, 1062), (sx + 18, 1062)])

# the rule of the door
BF = font('inter', 400, 34)
y = 1282
for line in ['At each door, her party trades rhymes with the house',
             'and usually wins: a Mari inside meant good luck.']:
    text(line, M, y, BF, TXT)
    y += 46

# ---------------------------------------------------------------------------- footer
FY = H - M - 34
text('Source: Museum Wales', M, FY + 2, font('inter', 400, 30), DIM)
logo = Image.open('assets/hh-monogram-white-140.png').convert('RGBA')
LH = 40
logo = logo.resize((round(logo.width * LH / logo.height), LH), Image.LANCZOS)
tint = Image.new('RGBA', logo.size, DIM + (255,))
tint.putalpha(logo.getchannel('A'))
im.paste(tint, (W - M - logo.width, FY - 4), tint)

im.save(os.environ.get('PIN_OUT', 'out.jpg'), quality=82, optimize=True)
