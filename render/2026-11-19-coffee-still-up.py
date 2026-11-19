# "Your 3 PM coffee is still up at midnight." (Awake and Unafraid skeleton coffee tee, listing 4588003563), Nov 19 2026.
# Format: infographic with a real chart (caffeine decay curve). Skeleton d: type-led, a huge headline across the
# top, the chart under it, the photo a tall crop bleeding off the right and bottom edges. Logo bottom left. No eyebrow.
# Palette sampled from photos/4588003563-1.jpg: field = the print's bone ink (#C5B6A3) lifted to pale bone;
# ink = the black tee's warm shadow; accent = the print's red moon (#A01E24), used on the curve and one figure.
# Facts: 8 oz brewed coffee is about 95 mg caffeine (USDA); typical adult half-life about 5 hours, varies widely.
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
W,H=1000,1500; M=64
FIELD=(231,222,208)
INK=(31,26,23)
RED=(160,30,36)
MUTE=(92,82,72)
GRID=(204,193,177)
DS='assets/fonts/dm-serif-display-latin-400-normal.woff'
IN='assets/fonts/inter-latin-%d-normal.woff'
f=lambda p,s: ImageFont.truetype(p,s)
im=Image.new('RGB',(W,H),FIELD); d=ImageDraw.Draw(im)

# photo: tall crop of the print, bleeding off right and bottom
PX,PY=560,540
src=Image.open('photos/4588003563-1.jpg').convert('RGB')
ch=1254; cw=int(ch*(W-PX)/(H-PY))
cx0=388; cy0=0
ph=src.crop((cx0,cy0,cx0+cw,cy0+ch)).resize((W-PX,H-PY),Image.LANCZOS)
im.paste(ph,(PX,PY))

# headline
hf=f(DS,120)
lines=['Your 3 PM coffee','is still up','at midnight.']
y=M-14
for ln in lines:
    d.text((M-4,y),ln,font=hf,fill=INK); y+=124
HB=y

# chart (left column)
CX0,CX1=M+44,PX-48
CY0,CY1=PY+100,PY+540
lab=f(IN%500,22); small=f(IN%400,22); tick=f(IN%500,20)
d.text((M,PY-6),'Caffeine left from one cup, in mg',font=f(IN%600,26),fill=INK)
# y grid at 0,25,50,75,100 mg
ymax=100
def yv(mg): return CY1-(CY1-CY0)*mg/ymax
for mg in (0,25,50,75,100):
    yy=yv(mg); d.line([(CX0,yy),(CX1,yy)],fill=GRID if mg else MUTE,width=2 if not mg else 1)
    t=str(mg); tw=d.textlength(t,font=tick); d.text((CX0-12-tw,yy-12),t,font=tick,fill=MUTE)
# x: hours 0..12 from 3 PM
def xv(h): return CX0+(CX1-CX0)*h/12
for h,t in ((0,'3 PM'),(3,'6'),(6,'9'),(9,'12 AM'),(12,'3')):
    xx=xv(h); d.line([(xx,CY1),(xx,CY1+8)],fill=MUTE,width=2)
    tw=d.textlength(t,font=tick)
    tx=min(max(xx-tw/2,CX0-10),CX1-tw+10)
    d.text((tx,CY1+14),t,font=tick,fill=MUTE)
# curve, rendered at 4x for smoothness
S=4
ov=Image.new('L',(W*S,H*S),0); od=ImageDraw.Draw(ov)
pts=[(xv(h)*S,yv(95*0.5**(h/5))*S) for h in np.linspace(0,12,200)]
od.line(pts,fill=255,width=5*S,joint='curve')
mx,my=xv(9),yv(95*0.5**(9/5))
r=10
od.ellipse([(mx-r)*S,(my-r)*S,(mx+r)*S,(my+r)*S],fill=255)
sx,sy=xv(0),yv(95)
od.ellipse([(sx-7)*S,(sy-7)*S,(sx+7)*S,(sy+7)*S],fill=255)
ov=ov.resize((W,H),Image.LANCZOS)
im.paste(Image.new('RGB',(W,H),RED),(0,0),ov); d=ImageDraw.Draw(im)
# midnight guide + callout
d.line([(mx,my+14),(mx,CY1)],fill=RED,width=2)
big=f(DS,64)
t1='27 mg'; t2='still in you at midnight'
w1=d.textlength(t1,font=big); w2=d.textlength(t2,font=small)
by=yv(86)
d.rectangle([CX1-max(w1,w2)-14,by+4,CX1+4,by+112],fill=FIELD)
d.text((CX1-w1,by),t1,font=big,fill=RED)
d.text((CX1-w2,by+76),t2,font=small,fill=INK)
d.text((sx+16,sy-14),'95 mg',font=lab,fill=INK)

# notes
ny=CY1+76
notes=['One 8 oz brewed coffee is about','95 mg. Half of it clears every','5 hours or so, on average.','Yours may run faster or slower.']
for ln in notes:
    d.text((M,ny),ln,font=small,fill=MUTE); ny+=34

# logo bottom left
mono=Image.open('assets/hh-monogram-white-140.png').convert('RGBA')
ms=56; mono=mono.resize((ms,int(mono.height*ms/mono.width)),Image.LANCZOS)
tint=Image.new('RGBA',mono.size,INK+(255,)); tint.putalpha(mono.split()[3])
LY=H-M-mono.height
im.paste(tint,(M,LY),tint)
d.text((M+ms+16,LY+mono.height/2-15),'Hex & Hollow',font=f(IN%600,26),fill=INK)

im.save(os.environ.get('PIN_OUT','pin.jpg'),'JPEG',quality=82,optimize=True)
