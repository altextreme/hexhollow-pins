# v3: creative director round 2 fixes. The twelve names now hang on a drawn year: two timelines (Jan to Jun,
# Jul to Dec), each a spine with a gold full-moon dot per month. Icons redrawn as one family of solid
# silhouettes in the names' ivory; gold only on the small moon dots (the mug's pinprick stars). Ground warmed
# toward the mug's warm black. Headline broken by phrase. Names in the text sans.
# "Twelve moons, twelve excuses to stay up late" (Emotionally Nocturnal opossum mug, listing 4592258658), Nov 20 2026.
# Manual photo-free icon pin (Anthony asked for an infographic tied to a product with no product photography,
# built from the icon bank). One game-icons icon per moon's namesake.
# Names as listed by The Old Farmer's Almanac (almanac.com/full-moon-names); September is its Corn Moon,
# also called the Harvest Moon.
# Palette sampled from the mug's print in photos/4592258658-1.jpg: ground = the print's warm black, kept
# clearly wine-brown; headline = the opossum's dusty rose nose and ears; icons and names = the night-blooming
# flowers' ivory; labels = the mauve buds, dimmed; moon dots = the gold stars. No headline period.
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from lib.icons import icon

W, H, M = 1000, 1500, 72
FIELD = (52, 37, 41)     # the print's warm black ground, kept a wine-brown
ROSE = (205, 150, 157)   # opossum nose and ears (#B68D87), dusty, lifted for the ground
IVORY = (238, 228, 210)  # night-blooming flower petals
MAUVE = (178, 154, 160)  # mauve buds, dimmed toward the ground
GOLD = (222, 186, 118)   # print stars (#A1896A), lifted; moon dots only
SPINE = (104, 80, 88)    # ground lifted, for the year line

F = 'assets/fonts/'
def f(name, w, s): return ImageFont.truetype(f'{F}{name}-latin-{w}-normal.woff', s)
YS, IN = 'young-serif', 'inter'

im = Image.new('RGBA', (W, H), FIELD + (255,))
d = ImageDraw.Draw(im)

def ink(s, font):
    b = d.textbbox((0, 0), s, font=font); return b

def text_top(xy, s, font, fill, tracking=0):
    """Draw s with its ink top at xy[1]."""
    x, y = xy
    top = ink(s, font)[1]
    if not tracking:
        d.text((x, y - top), s, font=font, fill=fill); return
    for ch in s:
        d.text((x, y - top), ch, font=font, fill=fill)
        x += d.textlength(ch, font=font) + tracking

def width(s, font, tracking=0):
    return d.textlength(s, font=font) + tracking * max(len(s) - 1, 0)

# Kicker: ties the pin to the mug at the label tier.
kf = f(IN, 500, 30)
text_top((M, 72), 'FOR THE EMOTIONALLY NOCTURNAL', kf, MAUVE, tracking=3)

# Headline: three phrase lines.
HS = 100
hf = f(YS, 400, HS)
capT = ink('T', hf); asc = capT[3] - capT[1]
y = 132
for ln in ['Twelve moons,', 'twelve excuses', 'to stay up late']:
    assert width(ln, hf) <= W - 2 * M
    text_top((M, y), ln, hf, ROSE)
    y += round(HS * 1.02)
base = y - round(HS * 1.02) + asc
print('headline last baseline', base)

# Deck: says what the grid is.
df = f(IN, 400, 30)
dy = base + 22 + 34
text_top((M, dy), 'Each full moon’s traditional name, by month', df, MAUVE)
deck_bottom = dy + (ink('Eh', df)[3] - ink('Eh', df)[1])
print('deck bottom', deck_bottom)

def glyph(iid, box, color, dilate=0):
    """Icon cropped to its ink, scaled so its larger side is box px; dilate fills out a line-drawn glyph."""
    big = icon(iid, 480, color)
    a = big.split()[3]
    if dilate:
        a = a.filter(ImageFilter.MaxFilter(dilate))
    big = Image.merge('RGBA', (*[Image.new('L', big.size, c) for c in color], a))
    big = big.crop(a.getbbox())
    k = box / max(big.size)
    return big.resize((round(big.width * k), round(big.height * k)), Image.LANCZOS)

MOONS = [
    ('JAN', 'Wolf', 'gi:wolf-howl', 0), ('FEB', 'Snow', 'gi:snowing', 0), ('MAR', 'Worm', 'gi:earth-worm', 25),
    ('APR', 'Pink', 'gi:flowers', 0), ('MAY', 'Flower', 'gi:shut-rose', 0), ('JUN', 'Strawberry', 'gi:strawberry', 0),
    ('JUL', 'Buck', 'gi:deer', 0), ('AUG', 'Sturgeon', 'gi:double-fish', 0), ('SEP', 'Corn', 'gi:corn', 0),
    ('OCT', 'Hunter’s', 'gi:archer', 0), ('NOV', 'Beaver', 'gi:beaver', 0), ('DEC', 'Cold', 'gi:thermometer-cold', 0),
]

# Two timelines: columns of 400 px with a 56 px gutter, six rows each.
TOP = deck_bottom + 62
FOOT = H - 64 - 60          # footer band top
BOT = FOOT - 64             # last row bottom
ICON = 100
PITCH = (BOT - TOP - ICON) / 5
COLW = (W - 2 * M - 56) // 2
mf = f(IN, 500, 30)
nf = f(IN, 600, 38)
mcap = ink('JAN', mf); mcap = mcap[3] - mcap[1]
ncap = ink('Wolf', nf); ncap = ncap[3] - ncap[1]
for c in range(2):
    x0 = M + c * (COLW + 56)
    sx = x0 + 13                      # spine x
    cy0 = TOP + ICON / 2
    cy1 = TOP + 5 * PITCH + ICON / 2
    d.line([sx, cy0, sx, cy1], fill=SPINE, width=3)
    for r in range(6):
        mon, name, iid, dil = MOONS[c * 6 + r]
        ry = round(TOP + r * PITCH)
        cy = ry + ICON / 2
        d.ellipse([sx - 13, cy - 13, sx + 13, cy + 13], fill=GOLD)
        g = glyph(iid, ICON, IVORY, dil)
        gx = x0 + 52
        im.alpha_composite(g, (gx + (ICON - g.width) // 2, round(cy - g.height / 2)))
        tx = gx + ICON + 26
        stack = mcap + 12 + ncap
        ty = round(cy - stack / 2)
        text_top((tx, ty), mon, mf, MAUVE, tracking=3)
        assert tx + width(name, nf) <= x0 + COLW, name
        text_top((tx, ty + mcap + 12), name, nf, IVORY)
print('pitch', PITCH, 'rows end', TOP + 5 * PITCH + ICON, 'footer top', FOOT)

# Footer: logo bottom left, source bottom right.
logo = Image.open('assets/hh-monogram-white-140.png').convert('RGBA')
lh = 60; lw = round(logo.width * lh / logo.height)
logo = logo.resize((lw, lh), Image.LANCZOS)
logo = Image.merge('RGBA', (*[Image.new('L', logo.size, v) for v in IVORY], logo.split()[3]))
im.alpha_composite(logo, (M, FOOT))
wf = f(IN, 600, 30)
bb = ink('Hex & Hollow', wf)
d.text((M + lw + 16, FOOT + (lh - (bb[3] - bb[1])) // 2 - bb[1]), 'Hex & Hollow', font=wf, fill=IVORY)
sf = f(IN, 400, 30)
src = 'Names: The Old Farmer’s Almanac'
sb = ink(src, sf)
d.text((W - M - (sb[2] - sb[0]) - sb[0], FOOT + (lh - (sb[3] - sb[1])) // 2 - sb[1]), src, font=sf, fill=MAUVE)

im.convert('RGB').save(os.environ.get('PIN_OUT', '/tmp/pin.jpg'), quality=82, optimize=True, progressive=True)
