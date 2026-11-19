# "Your 3 PM coffee is still up at midnight." (Awake and Unafraid skeleton coffee tee, listing 4588003563), Nov 19 2026. v3.
# Redo after Anthony's note: no faded, floating photo in a corner. Image first: the photo bleeds full width across the
# top with a clean hard edge (43% of the height); headline, chart and notes sit below on the coffee field.
# Palette as v2, sampled from photos/4588003563-1.jpg: coffee field from the wall shadow, bone from the print ink,
# red = the print's red (#C12028). Facts: 8 oz brewed coffee ~95 mg (USDA); adult caffeine half-life ~5 h, varies widely.
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
W,H=1000,1500; M=64
FIELD=(40,30,25); BONE=(226,214,196); RED=(193,32,40); MUTE=(168,156,142); GRID=(78,64,55)
DS='assets/fonts/dm-serif-display-latin-400-normal.woff'
IN='assets/fonts/inter-latin-%d-normal.woff'
f=lambda p,s: ImageFont.truetype(p,s)
im=Image.new('RGB',(W,H),FIELD)

# photo: full bleed across the top, hard edge, from the necklace to the bottom of the print
PH=640
src=Image.open('photos/4588003563-1.jpg').convert('RGB')
sw=src.width; sh=int(sw*PH/W)
sy0=250
im.paste(src.crop((0,sy0,sw,sy0+sh)).resize((W,PH),Image.LANCZOS),(0,0))
d=ImageDraw.Draw(im)

# headline
hf=f(DS,94)
y=PH+46
for ln in ['Your 3 PM coffee is','still up at midnight.']:
    d.text((M-3,y),ln,font=hf,fill=BONE); y+=100

# chart, full measure
small=f(IN%400,24); tick=f(IN%500,22)
CAP=y+62
d.text((M,CAP),'Caffeine left from one cup, in mg',font=f(IN%600,26),fill=BONE)
CX0,CX1=M+44,W-M
CY0,CY1=CAP+76,CAP+350
def yv(mg): return CY1-(CY1-CY0)*mg/100
def xv(h): return CX0+(CX1-CX0)*h/12
for mg in (0,50,100):
    yy=yv(mg); d.line([(CX0,yy),(CX1,yy)],fill=MUTE if mg==0 else GRID,width=2 if mg==0 else 1)
    t=str(mg); tw=d.textlength(t,font=tick); d.text((CX0-12-tw,yy-13),t,font=tick,fill=MUTE)
for h,t in ((0,'3 PM'),(6,'9 PM'),(9,'12 AM'),(12,'3 AM')):
    xx=xv(h); d.line([(xx,CY1),(xx,CY1+8)],fill=MUTE,width=2)
    tw=d.textlength(t,font=tick); tx=min(max(xx-tw/2,CX0-6),CX1-tw)
    d.text((tx,CY1+14),t,font=tick,fill=RED if h==9 else MUTE)
S=4
ov=Image.new('L',(W*S,H*S),0); od=ImageDraw.Draw(ov)
pts=[(xv(h)*S,yv(95*0.5**(h/5))*S) for h in np.linspace(0,12,240)]
od.line(pts,fill=255,width=6*S,joint='curve')
mx,my=xv(9),yv(95*0.5**(9/5)); sx,sy=xv(0),yv(95)
od.ellipse([(mx-12)*S,(my-12)*S,(mx+12)*S,(my+12)*S],fill=255)
od.ellipse([(sx-9)*S,(sy-9)*S,(sx+9)*S,(sy+9)*S],fill=255)
ov=ov.resize((W,H),Image.LANCZOS)
im.paste(Image.new('RGB',(W,H),RED),(0,0),ov); d=ImageDraw.Draw(im)
d.line([(mx,my+16),(mx,CY1)],fill=RED,width=3)
d.text((sx+20,sy-14),'95 mg',font=f(IN%600,24),fill=BONE)
# callout, top right of the plot where the curve has fallen away
big=f(DS,76); t1='27 mg'; t2='still in you at midnight'
w1=d.textlength(t1,font=big); w2=d.textlength(t2,font=small)
d.text((CX1-w1,CY0-30),t1,font=big,fill=BONE)
d.text((CX1-w2,CY0+56),t2,font=small,fill=MUTE)

# notes left, logo right, sharing the bottom edge
ny=H-M-62
d.text((M,ny),'One 8 oz brewed coffee is about 95 mg.',font=small,fill=MUTE)
d.text((M,ny+34),'Half clears every 5 hours or so. Yours may vary.',font=small,fill=MUTE)
mono=Image.open('assets/hh-monogram-white-140.png').convert('RGBA')
ms=46; mono=mono.resize((ms,int(mono.height*ms/mono.width)),Image.LANCZOS)
tint=Image.new('RGBA',mono.size,BONE+(255,)); tint.putalpha(mono.split()[3])
lf=f(IN%600,22); lt='Hex & Hollow'; lw=d.textlength(lt,font=lf)
LX=W-M-lw-ms-12; LY=H-M-mono.height+4
im.paste(tint,(int(LX),LY),tint)
d.text((LX+ms+12,LY+mono.height/2-14),lt,font=lf,fill=BONE)
im.save(os.environ.get('PIN_OUT','pin.jpg'),'JPEG',quality=86,optimize=True)
