# "Toxic is learned." (Toxic Energy punk frog mug, listing 4611527807), Nov 19 2026.
# Format: single fact, one statement. Skeleton b: full-bleed photo, headline over a sampled-color scrim,
# minimal supporting text, logo centered at the foot.
# Palette sampled from photos/4611527807-1.jpg: scrim = the room's dark walnut shadows (#2C190D, #280F07);
# headline = the frog's green ink (median #7F981B) lifted to lime for the dark ground;
# neutrals = the candle's warm wax light (#F59228) pulled toward cream.
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
W,H=1000,1500; M=64
LIME=(184,214,72)
CREAM=(244,232,212)
DIM=(214,196,172)
SHADOW=np.array([38,21,11],dtype=float)
AB='assets/fonts/archivo-black-latin-%d-normal.woff'
IN='assets/fonts/inter-latin-%d-normal.woff'
f=lambda p,w,s: ImageFont.truetype(p%w,s)

src=Image.open('photos/4611527807-1.jpg').convert('RGB')
cw=836; cx0=320
im=src.crop((cx0,0,cx0+cw,1254)).resize((W,H),Image.LANCZOS)
# tonal scrims in the room's own shadow color: top for the headline, foot for the note
a=np.asarray(im).astype(float)
yy=np.arange(H)[:,None]
top=np.clip(1-(yy-250)/260,0,1)*0.86           # solid to y=250, gone by y=510
bot=np.clip((yy-1050)/220,0,1)*0.90            # starts y=1050, full by y=1270
alpha=np.maximum(top,bot)[...,None]
a=a*(1-alpha)+SHADOW*alpha
im=Image.fromarray(a.clip(0,255).astype('uint8')); d=ImageDraw.Draw(im)

def capb(font,s="H"):
    bb=d.textbbox((0,0),s,font=font); return bb[1],bb[3]-bb[1]
def text_top(xy,t,font,fill):
    x,y=xy; off,h=capb(font); d.text((x,y-off),t,font=font,fill=fill); return h

# headline
hd=f(AB,400,150)
y=88
for i,line in enumerate(["Toxic is","learned."]):
    y+=text_top((M,y),line,hd,LIME)+(40 if i==0 else 0)
print('headline bottom',y,[d.textlength(l,font=hd) for l in ["Toxic is","learned."]])

# supporting note at the foot
bd=f(IN,400,29); bb=f(IN,600,29)
lines=[("Poison dart frogs aren’t born toxic.",bb,CREAM),
       ("They build it from the ants and mites they eat.",bd,DIM),
       ("Raised on fruit flies, they’re not toxic at all. Relatable.",bd,DIM)]
y=1214
for t,fn,c in lines:
    text_top((M,y),t,fn,c); print(t, M+d.textlength(t,font=fn)); y+=44
print('note bottom',y)

# logo centered at the foot
logo=Image.open('assets/hh-monogram-white-140.png').convert('RGBA')
lh=40; lw=round(logo.width*lh/logo.height); logo=logo.resize((lw,lh),Image.LANCZOS)
logo=Image.merge('RGBA',(*[Image.new('L',logo.size,c) for c in CREAM],logo.split()[3]))
nm=f(IN,600,22); tw=d.textlength("Hex & Hollow",font=nm)
total=lw+12+tw; lx=round((W-total)/2); ly=H-56-lh
im.paste(logo,(lx,ly),logo)
b2=d.textbbox((0,0),"Hex & Hollow",font=nm)
d.text((lx+lw+12,ly+(lh-(b2[3]-b2[1]))//2-b2[1]),"Hex & Hollow",font=nm,fill=CREAM)
print('logo top',ly)
im.save(os.environ.get('PIN_OUT','/tmp/pin.jpg'),quality=80,optimize=True,progressive=True)
