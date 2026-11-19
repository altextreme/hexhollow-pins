# "Nostalgia was a diagnosis" (Running on Nostalgia skeleton Christmas sweatshirt, listing 4618215622), Nov 19 2026. v2.
# Skeleton: vertical side split. The photo fills the whole left side, top to bottom, out to the pin's left edge, and
# meets the field in one straight hard vertical edge on the golden line (x 618). The cocoa mug is cut through
# its middle at the pin's outer edge, about half shown, and the shirt slogan keeps 60 px or more from the split.
# The right column: headline, then a drawn vertical timeline with stops spaced to scale (1688, 1860s, 2012), logo foot.
# No eyebrow, no rows of text, no headline period.
# Palette sampled from photos/4618215622-1.jpg: field = black cherry from the cardigan's shadow tones;
# cream = the print's ink (237,222,210); captions a dimmer warm cream.
# Facts: Johannes Hofer, Basel medical dissertation, 1688, coined "nostalgia" for a disease of homesickness. Union army
# doctors recorded 5,213 + 334 nostalgia cases over the Civil War (Medical and Surgical History of the War of the
# Rebellion). Zhou, Wildschut, Sedikides et al. 2012 (Emotion): people who recalled a nostalgic memory judged a cold
# room warmer.
import os
from PIL import Image, ImageDraw, ImageFont
W,H=1000,1500
FIELD=(62,12,20); CREAM=(237,222,210); DIM=(204,176,168)
F='assets/fonts/'
f=lambda p,s: ImageFont.truetype(F+p,s)
im=Image.new('RGB',(W,H),FIELD)

PW=618
src=Image.open('photos/4618215622-1.jpg').convert('RGB')
sw=round(src.height*PW/H); SX=320
im.paste(src.crop((SX,0,SX+sw,src.height)).resize((PW,H),Image.LANCZOS),(0,0))
d=ImageDraw.Draw(im)

CL=PW+46; CR=W-40
# headline: Archivo Narrow 700, as large as the column allows
lines=['Nostalgia','was a','diagnosis']
hs=120; hf=f('archivo-narrow-latin-700-normal.woff',hs)
while max(d.textlength(l,font=hf) for l in lines)>CR-CL: hs-=1; hf=f('archivo-narrow-latin-700-normal.woff',hs)
y=56
for l in lines:
    d.text((CL-3,y),l,font=hf,fill=CREAM); y+=int(hs*0.98)
HEND=y+int(hs*0.22)

# timeline, stops spaced to scale
yf=f('ibm-plex-mono-latin-600-normal.woff',34); bf=f('inter-latin-400-normal.woff',30)
T0=HEND+110; T1=T0+700
def ty(yr): return T0+(T1-T0)*(yr-1688)/(2012-1688)
AX=CL+7
d.line([(AX,ty(1688)),(AX,ty(2012))],fill=CREAM,width=3)
items=[(1688,'1688',['Hofer names it','a disease of','homesickness']),
       (1863,'1860s',['Union doctors log','5,000+ cases']),
       (2012,'2012',['Recalling it','made a cold room','feel warmer'])]
TX=AX+26
for yr,lab,body in items:
    yy=ty(yr); r=9
    d.ellipse([AX-r,yy-r,AX+r,yy+r],fill=CREAM)
    bb=d.textbbox((0,0),lab,font=yf)
    d.text((TX,yy-(bb[1]+bb[3])/2),lab,font=yf,fill=CREAM)
    by=yy+(bb[3]-bb[1])/2+16
    for ln in body:
        assert d.textlength(ln,font=bf)<=CR-TX, ln
        d.text((TX,by),ln,font=bf,fill=DIM); by+=40

# logo, foot of the text column, on the column's left edge
mono=Image.open('assets/hh-monogram-white-140.png').convert('RGBA')
ms=46; mono=mono.resize((ms,int(mono.height*ms/mono.width)),Image.LANCZOS)
tint=Image.new('RGBA',mono.size,CREAM+(255,)); tint.putalpha(mono.split()[3])
lf=f('inter-latin-600-normal.woff',30)
LY=H-60-mono.height
im.paste(tint,(CL,LY),tint)
lb=d.textbbox((0,0),'Hex & Hollow',font=lf)
d.text((CL+ms+14,LY+mono.height/2-(lb[1]+lb[3])/2),'Hex & Hollow',font=lf,fill=CREAM)
print('hs',hs,'HEND',HEND,'T1',T1)
im.save(os.environ.get('PIN_OUT','pin.jpg'),quality=84,optimize=True)
