# Hex & Hollow pin: Peak goth hours, by city. Topical pin (no product, no shop link).
# Photo-free drawn chart. Each column is one full day (24 hours) on Dec 21, 2026, the winter solstice:
# ink from the top for the hours of night (sunset to sunrise), candle gold at the foot for daylight.
# Night hours, rounded: Tromso 24 (polar night, the sun stays below the horizon), Reykjavik 20, Anchorage 18.5,
# London 16, Chicago 15, Quito 12. Computed with the NOAA sunrise equation and checked against timeanddate.com
# (Reykjavik Dec 21, 2026: daylight 4 h 7 m). Luxury register: Bodoni Moda headline on a deep midnight field.
# Layout: type-led headline top, full-width column chart as the hero, logo bottom left, source bottom right.
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1000, 1500
M = 64
F = 'assets/fonts/'


def font(name, size):
    return ImageFont.truetype(F + name, size)


FIELD = (27, 32, 66)      # midnight indigo
NIGHT = (11, 13, 32)      # ink of the night columns
GOLD = (214, 166, 74)     # candle gold: daylight
MOON = (238, 228, 200)    # moon ivory: headline, numbers
MUTED = (160, 163, 196)   # lavender gray: labels and metadata

img = Image.new('RGB', (W, H), FIELD)
d = ImageDraw.Draw(img)

# ---------- headline ----------
hf = font('bodoni-moda-latin-700-normal.woff', 118)
lines = ['Peak goth', 'hours, by city']
y = 92
asc = hf.getbbox('Th')[1]
lead = 124
for i, t in enumerate(lines):
    d.text((M, y + i * lead - asc), t, font=hf, fill=MOON)
    assert M + d.textlength(t, font=hf) <= W - M, t
head_bottom = y + lead + hf.getbbox('hours, by city')[3] - asc

sf = font('inter-latin-400-normal.woff', 34)
sub = 'Hours of darkness on the solstice, Dec 21, 2026'
sy = head_bottom + 40
sb = sf.getbbox(sub)
d.text((M, sy - sb[1]), sub, font=sf, fill=MUTED)
sub_bottom = sy + sb[3] - sb[1]

# ---------- legend ----------
lf = font('inter-latin-400-normal.woff', 30)
ly = sub_bottom + 30
sw = 28
x = M
for col, txt in ((NIGHT, 'night'), (GOLD, 'daylight')):
    d.rectangle([x, ly, x + sw, ly + sw], fill=col)
    if col == NIGHT:
        d.rectangle([x, ly, x + sw, ly + sw], outline=MUTED, width=1)
    tb = lf.getbbox(txt)
    d.text((x + sw + 12, ly + (sw - (tb[3] - tb[1])) / 2 - tb[1]), txt, font=lf, fill=MUTED)
    x += sw + 12 + d.textlength(txt, font=lf) + 40
legend_bottom = ly + sw

# ---------- chart ----------
data = [('Tromsø', 24, '24'), ('Reykjavík', 20, '20'), ('Anchorage', 18.5, '18½'),
        ('London', 16, '16'), ('Chicago', 15, '15'), ('Quito', 12, '12')]
n = len(data)
cw = 116
gap = (W - 2 * M - n * cw) / (n - 1)
top = legend_bottom + 74
ch = 720
unit = ch / 24
bottom = top + ch
nf = font('bodoni-moda-latin-700-normal.woff', 52)
cf = font('archivo-narrow-latin-500-normal.woff', 32)
for i, (city, hrs, lab) in enumerate(data):
    x0 = round(M + i * (cw + gap))
    x1 = x0 + cw
    split = round(top + hrs * unit)
    d.rectangle([x0, top, x1, split], fill=NIGHT)
    if split < bottom:
        d.rectangle([x0, split, x1, bottom], fill=GOLD)
    nb = nf.getbbox(lab)
    nw = nb[2] - nb[0]
    d.text((x0 + (cw - nw) / 2 - nb[0], top + 28 - nb[1]), lab, font=nf, fill=MOON)
    cb = cf.getbbox(city)
    cwid = cb[2] - cb[0]
    assert cwid <= cw + gap - 12, (city, cwid)
    d.text((x0 + (cw - cwid) / 2 - cb[0], bottom + 26 - cb[1]), city, font=cf, fill=MOON)
    if hrs == 24:
        # the one storytelling point: the sun never rises, said inside the all-night column
        for k, note in enumerate(('no', 'sunrise')):
            nb2 = cf.getbbox(note)
            d.text((x0 + (cw - (nb2[2] - nb2[0])) / 2 - nb2[0], bottom - 28 - 2 * 40 + k * 40 + 8 - nb2[1]), note,
                   font=cf, fill=GOLD)
labels_bottom = bottom + 26 + cf.getbbox('Reykjavík')[3] - cf.getbbox('Reykjavík')[1]

# ---------- footer ----------
logo = Image.open('assets/hh-monogram-white-140.png').convert('RGBA')
lh = 54
logo = logo.resize((round(logo.width * lh / logo.height), lh), Image.LANCZOS)
tint = Image.new('RGBA', logo.size, MUTED + (255,))
tint.putalpha(logo.getchannel('A'))
fy = H - M - lh
img.paste(tint, (M, fy), tint)
wf = font('inter-latin-500-normal.woff', 30)
word = 'Hex & Hollow'
wb = wf.getbbox(word)
d.text((M + logo.width + 14, fy + (lh - (wb[3] - wb[1])) / 2 - wb[1]), word, font=wf, fill=MUTED)
src = 'Sun times: timeanddate.com'
sb2 = lf.getbbox(src)
d.text((W - M - d.textlength(src, font=lf), fy + (lh - (sb2[3] - sb2[1])) / 2 - sb2[1]), src, font=lf, fill=MUTED)

print('head', head_bottom, 'sub', sub_bottom, 'legend', legend_bottom, 'chart', top, bottom, 'labels', labels_bottom,
      'footer', fy, 'pause', fy - labels_bottom, 'gap', round(gap, 1))
img.save(os.environ.get('PIN_OUT', 'out.jpg'), 'JPEG', quality=84, optimize=True)
