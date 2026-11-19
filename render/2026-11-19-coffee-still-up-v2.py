# "Your 3 PM coffee is still up at midnight." (Awake and Unafraid skeleton coffee tee, listing 4588003563), Nov 19 2026. v2 (after review: dark field, exact print red, crop below the chin, gutter = margin).
# Format: infographic with a real chart (caffeine decay curve). Skeleton d: type-led, a huge headline across the
# top, the chart under it, the photo a tall crop bleeding off the right and bottom edges, its left edge fading
# softly into the field. Logo bottom left. No eyebrow.
# Palette sampled from photos/4588003563-1.jpg: field = the wall's warm brown shadow, deepened to coffee;
# headline and promoted figure = the print's bone ink, lifted; curve and dots = the print's red (median #C12028);
# neutrals = the bone pulled down toward the wall.
# Facts: 8 oz brewed coffee is about 95 mg caffeine (USDA); typical adult half-life about 5 hours, varies widely.
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
W,H=1000,1500; M=64
FIELD=(40,30,25)
BONE=(226,214,196)
RED=(193,32,40)
MUTE=(168,156,142)
GRID=(78,64,55)
DS='assets/fonts/dm-serif-display-latin-400-normal.woff'
IN='assets/fonts/inter-latin-%d-normal.woff'
f=lambda p,s: ImageFont.truetype(p,s)
im=Image.new('RGB',(W,H),FIELD)

# photo: crop from the collar down, bleeding off right and bottom, left edge feathered into the field
PX,PY=520,580
PW,PH=W-PX,H-PY
src=Image.open('photos/4588003563-1.jpg').convert('RGB')
cy0=200; ch=1254-cy0; cw=int(ch*PW/PH); cx0=385
ph=src.crop((cx0,cy0,cx0+cw,cy0+ch)).resize((PW,PH),Image.LANCZOS)
pa=np.asarray(ph).astype(float)
xx=np.arange(PW)[None,:,None]; yy=np.arange(PH)[:,None,None]
fade=np.clip(xx/30,0,1)*np.clip(yy/56,0,1)
pa=pa*fade+np.array(FIELD,float)*(1-fade)
im.paste(Image.fromarray(pa.clip(0,255).astype('uint8')),(PX,PY))
d=ImageDraw.Draw(im)

# headline
hf=f(DS,120)
y=M-6
for ln in ['Your 3 PM coffee','is still up','at midnight.']:
    d.text((M-4,y),ln,font=hf,fill=BONE); y+=126

# chart (left column, gutter = margin)
CX0,CX1=M+40,PX-M
CY0,CY1=PY+92,PY+500
small=f(IN%400,22); tick=f(IN%500,20)
d.text((M,PY-6),'Caffeine left from one cup, in mg',font=f(IN%600,24),fill=BONE)
def yv(mg): return CY1-(CY1-CY0)*mg/100
for mg in (0,25,50,75,100):
    yy_=yv(mg); d.line([(CX0,yy_),(CX1,yy_)],fill=MUTE if mg==0 else GRID,width=2 if mg==0 else 1)
    t=str(mg); tw=d.textlength(t,font=tick); d.text((CX0-10-tw,yy_-12),t,font=tick,fill=MUTE)
def xv(h): return CX0+(CX1-CX0)*h/12
for h,t in ((0,'3 PM'),(6,'9 PM'),(9,''),(12,'3 AM')):
    xx_=xv(h); d.line([(xx_,CY1),(xx_,CY1+8)],fill=MUTE,width=2)
    if not t: continue
    tw=d.textlength(t,font=tick)
    tx=min(max(xx_-tw/2,CX0-8),CX1-tw)
    d.text((tx,CY1+14),t,font=tick,fill=MUTE)
# curve at 4x
S=4
ov=Image.new('L',(W*S,H*S),0); od=ImageDraw.Draw(ov)
pts=[(xv(h)*S,yv(95*0.5**(h/5))*S) for h in np.linspace(0,12,200)]
od.line(pts,fill=255,width=6*S,joint='curve')
mx,my=xv(9),yv(95*0.5**(9/5))
od.ellipse([(mx-11)*S,(my-11)*S,(mx+11)*S,(my+11)*S],fill=255)
sx,sy=xv(0),yv(95)
od.ellipse([(sx-8)*S,(sy-8)*S,(sx+8)*S,(sy+8)*S],fill=255)
ov=ov.resize((W,H),Image.LANCZOS)
im.paste(Image.new('RGB',(W,H),RED),(0,0),ov); d=ImageDraw.Draw(im)
d.line([(mx,my+15),(mx,CY1)],fill=RED,width=3)
# callout, knocked out of the grid
big=f(DS,64)
t1='27 mg'; t2='still in you at midnight'
w1=d.textlength(t1,font=big); w2=d.textlength(t2,font=small)
by=yv(88)
d.rectangle([CX1-max(w1,w2)-12,by+6,CX1+2,by+110],fill=FIELD)
d.text((CX1-w1,by),t1,font=big,fill=BONE)
d.text((CX1-w2,by+76),t2,font=small,fill=MUTE)
d.text((sx+18,sy-13),'95 mg',font=f(IN%500,22),fill=BONE)

# notes + kicker
ny=CY1+74
for ln in ['One 8 oz brewed coffee is about','95 mg. Half of it clears every','5 hours or so, on average.','Yours may run faster or slower.']:
    d.text((M,ny),ln,font=small,fill=MUTE); ny+=33
d.text((M,ny+14),'Awake, and apparently unafraid.',font=f(IN%500,22),fill=BONE)

# logo bottom left
mono=Image.open('assets/hh-monogram-white-140.png').convert('RGBA')
ms=54; mono=mono.resize((ms,int(mono.height*ms/mono.width)),Image.LANCZOS)
tint=Image.new('RGBA',mono.size,BONE+(255,)); tint.putalpha(mono.split()[3])
LY=H-M-mono.height
im.paste(tint,(M,LY),tint)
d.text((M+ms+14,LY+mono.height/2-15),'Hex & Hollow',font=f(IN%600,25),fill=BONE)

im.save(os.environ.get('PIN_OUT','pin.jpg'),'JPEG',quality=82,optimize=True)
