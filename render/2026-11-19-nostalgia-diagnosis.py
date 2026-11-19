# "Nostalgia used to be a diagnosis" (Running on Nostalgia skeleton Christmas sweatshirt, listing 4618215622), Nov 19 2026.
# Skeleton: vertical side split. The photo fills the whole left side, top to bottom, out to the pin's left edge, and
# meets the field in one straight hard vertical edge. The right column carries a drawn vertical timeline, years spaced
# to scale (1688, 1861, 2012). No eyebrow, no rows of text, no headline period. Logo foot of the text column.
# Palette sampled from photos/4618215622-1.jpg: field = the print's cardigan red (172,11,23) taken deeper;
# cream = the print's ink (237,222,210). Facts: Johannes Hofer, Basel medical dissertation, 1688, coined
# "nostalgia" as a disease of homesickness; Union army recorded 5,213 + 334 nostalgia cases (Medical and Surgical
# History of the War of the Rebellion); Zhou, Wildschut, Sedikides et al. 2012 (Emotion): recalling nostalgic
# memories made a cold room feel warmer.
import os
from PIL import Image, ImageDraw, ImageFont
W,H=1000,1500
FIELD=(124,14,24); CREAM=(237,222,210); SOFT=(226,182,176)
AN='assets/fonts/archivo-narrow-latin-700-normal.woff'
IN='assets/fonts/inter-latin-%d-normal.woff'
f=lambda p,s: ImageFont.truetype(p,s)
im=Image.new('RGB',(W,H),FIELD)

# photo: full height, left side, hard vertical edge. Cut decisively through the mug, not beside it.
PW=578
src=Image.open('photos/4618215622-1.jpg').convert('RGB')
sw=round(src.height*PW/H); SX=330
im.paste(src.crop((SX,0,SX+sw,src.height)).resize((PW,H),Image.LANCZOS),(0,0))
d=ImageDraw.Draw(im)

CL=PW+56; CR=W-52
# headline
hs=100; hf=f(AN,hs)
lines=['Nostalgia','used to be','a diagnosis']
while max(d.textlength(l,font=hf) for l in lines)>CR-CL: hs-=2; hf=f(AN,hs)
y=60
for l in lines:
    d.text((CL-2,y),l,font=hf,fill=CREAM); y+=int(hs*1.0)
HEND=y

# timeline, years to scale
yf=f(AN,74); bf=f('assets/fonts/archivo-narrow-latin-500-normal.woff',40)
T0,T1=HEND+120,1130
def ty(yr): return T0+(T1-T0)*(yr-1688)/(2012-1688)
AX=CL+10
d.line([(AX,ty(1688)),(AX,ty(2012))],fill=CREAM,width=4)
items=[(1688,'1688',['Named a disease','of homesickness']),
       (1861,'1861',['Union doctors log','5,000+ cases']),
       (2012,'2012',['It makes a cold','room feel warmer'])]
TX=AX+40
for yr,lab,body in items:
    yy=ty(yr)
    r=13 if yr!=2012 else 17
    if yr==2012:
        d.ellipse([AX-r,yy-r,AX+r,yy+r],fill=FIELD,outline=CREAM,width=5)
    else:
        d.ellipse([AX-r,yy-r,AX+r,yy+r],fill=CREAM)
    # year optically centered on the dot
    bb=d.textbbox((0,0),lab,font=yf)
    d.text((TX,yy-(bb[1]+bb[3])/2),lab,font=yf,fill=CREAM)
    by=yy+(bb[3]-bb[1])/2+20
    for ln in body:
        d.text((TX,by),ln,font=bf,fill=SOFT); by+=48

# logo, foot of the text column, flush with the column's left edge
mono=Image.open('assets/hh-monogram-white-140.png').convert('RGBA')
ms=50; mono=mono.resize((ms,int(mono.height*ms/mono.width)),Image.LANCZOS)
tint=Image.new('RGBA',mono.size,CREAM+(255,)); tint.putalpha(mono.split()[3])
lf=f(IN%600,30)
LY=H-60-mono.height
im.paste(tint,(CL,LY),tint)
lb=d.textbbox((0,0),'Hex & Hollow',font=lf)
d.text((CL+ms+14,LY+mono.height/2-(lb[1]+lb[3])/2),'Hex & Hollow',font=lf,fill=CREAM)
im.save(os.environ.get('PIN_OUT','pin.jpg'),quality=84,optimize=True)
