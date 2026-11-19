# "Still here, by the numbers" (opossum mug), Nov 19 2026. v2.
# No headline period (Anthony, Nov 18 2026: "headlines should [not] have periods on them unless it's multiple sentences").
# The v1 render script was never committed, so this patches the v1 pin: the period after "numbers" (x 820 to 837,
# y 787 to 836 at 1000 px) is covered with the flat field color it sits on (#2E1A11). Nothing else changes.
import os
from PIL import Image, ImageDraw
im=Image.open('pins/2026-11-19-opossum-by-the-numbers.jpg').convert('RGB')
d=ImageDraw.Draw(im)
d.rectangle([814,778,846,846],fill=(46,26,17))
im.save(os.environ.get('PIN_OUT','/tmp/pin.jpg'),quality=90,optimize=True,progressive=True)
