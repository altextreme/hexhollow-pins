# Hex & Hollow topical pin: Dante's Hell has a frozen basement.
# Topical, photo-free, no link. A drawn funnel: Hell as nine stepped circles narrowing downward,
# each a deeper red, until the ninth, Cocytus, which is ice.
# Palette for the topic: oxblood night field, bone headline, reds deepening by circle,
# one ice blue accent for the ninth circle and the word that names it.
# Facts: Dante Alighieri, Inferno (early 1300s). Nine circles: Limbo, Lust, Gluttony, Greed,
# Wrath, Heresy, Violence, Fraud, Treachery (traitors). Treachery is the deepest circle.
# Canto 32 to 34: the ninth circle is Cocytus, a frozen lake; in Canto 34 the wind from
# Satan's six beating wings is what keeps Cocytus frozen.
import os

from PIL import Image, ImageDraw, ImageFont

W, H, M = 1000, 1500, 64
S = 2
FIELD = (29, 12, 13)        # oxblood night
BONE = (240, 230, 214)      # headline, tier names
DIM = (176, 150, 140)       # small text
ICE = (196, 226, 236)       # ninth circle, accent
ICE_TXT = (22, 40, 50)
REDS = [(170, 62, 44), (160, 56, 42), (149, 50, 40), (138, 45, 38), (127, 40, 36),
        (116, 36, 34), (105, 32, 32), (94, 28, 30)]
CIRCLES = ['Limbo', 'Lust', 'Gluttony', 'Greed', 'Wrath', 'Heresy', 'Violence', 'Fraud', 'Treachery']


def font(fam, wt, size):
    return ImageFont.truetype(f'assets/fonts/{fam}-latin-{wt}-normal.woff', size * S)


def P(x, y):
    return (round(x * S), round(y * S))


big = Image.new('RGB', (W * S, H * S), FIELD)
d = ImageDraw.Draw(big)


def centered(text, f, y, fill):
    w = d.textlength(text, font=f) / S
    d.text(P((W - w) / 2, y), text, font=f, fill=fill)


# ------------------------------------------------------------------ headline
HF = font('pirata-one', 400, 150)
centered('Hell has a', HF, 58, BONE)
centered('frozen basement', HF, 200, ICE)

SF = font('inter', 400, 32)
centered('Dante’s Inferno sorts sinners into nine circles.', SF, 392, DIM)
centered('The worst don’t burn. They freeze.', SF, 436, DIM)

# ------------------------------------------------------------------ funnel
TOP, TH, GAP = 530, 70, 8
WTOP, WBOT = 1000, 300
TOTAL = 9 * TH + 8 * GAP
NF = font('inter', 600, 32)
LF = font('inter', 500, 32)


def width_at(y):
    t = (y - TOP) / TOTAL
    return WTOP + (WBOT - WTOP) * t


for i, name in enumerate(CIRCLES):
    y0 = TOP + i * (TH + GAP)
    y1 = y0 + TH
    w0, w1 = width_at(y0), width_at(y1)
    col = ICE if i == 8 else REDS[i]
    d.polygon([P((W - w0) / 2, y0), P((W + w0) / 2, y0), P((W + w1) / 2, y1), P((W - w1) / 2, y1)],
              fill=col)
    num = str(i + 1)
    nw = d.textlength(num, font=NF) / S
    lw = d.textlength(name, font=LF) / S
    gap = 18
    x = (W - (nw + gap + lw)) / 2
    ty = y0 + (TH - 32) / 2 - 6
    tc = ICE_TXT if i == 8 else BONE
    nc = ICE_TXT if i == 8 else ICE
    d.text(P(x, ty), num, font=NF, fill=nc)
    d.text(P(x + nw + gap, ty), name, font=LF, fill=tc)

# ------------------------------------------------------------------ note under the ice
FUNNEL_END = TOP + TOTAL
NF2 = font('inter', 500, 32)
centered('Circle 9 is a frozen lake.', NF2, FUNNEL_END + 44, ICE)
centered('Satan’s own beating wings keep it frozen.', NF2, FUNNEL_END + 88, BONE)

# ------------------------------------------------------------------ footer
im = big.resize((W, H), Image.LANCZOS)
dd = ImageDraw.Draw(im)
FF = ImageFont.truetype('assets/fonts/inter-latin-400-normal.woff', 30)
FY = 1418
dd.text((M, FY), 'Source: Dante, Inferno, Cantos 32 to 34', font=FF, fill=DIM)
logo = Image.open('assets/hh-monogram-white-140.png').convert('RGBA')
LH = 40
logo = logo.resize((round(logo.width * LH / logo.height), LH), Image.LANCZOS)
tint = Image.new('RGBA', logo.size, DIM + (255,))
tint.putalpha(logo.getchannel('A'))
im.paste(tint, (W - M - logo.width, FY - 2), tint)

im.save(os.environ.get('PIN_OUT', 'out.jpg'), quality=82, optimize=True)
