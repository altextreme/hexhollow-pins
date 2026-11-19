# "How to goth up a Christmas tree" (Midnight Mistletoe gothic ornament, listing 4592243206), Nov 19 2026.
# No headline period (Anthony, Nov 18 2026: "headlines should [not] have periods on them unless it's multiple sentences").
# Format: how-to steps. Skeleton b: full-bleed photo filling the top two thirds, feathering softly into a
# sampled fog field that carries the headline and four short steps. Logo bottom right. No eyebrow.
# Palette sampled from photos/4592243206-1.jpg: field = the blurred gray room behind the tree (#B8B8B6 top,
# #97918A low) lifted to pale fog; headline = the ornament's berry red (median #632A2A); body = the black
# heart's charcoal (#26211C); step numbers = the gold hanging string (#B79251) deepened for contrast.
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
W,H=1000,1500; M=64
FIELD=(218,215,209)
BERRY=(99,42,42)
INK=(38,33,28)
GOLD=(128,94,40)
SOFT=(96,90,82)
IS='assets/fonts/instrument-serif-latin-400-normal.woff'
IN='assets/fonts/inter-latin-%d-normal.woff'
f=lambda p,s: ImageFont.truetype(p,s)

# photo: scale the 2048 square to 1229, centre the ornament horizontally, ornament centre near y=520
src=Image.open('photos/4592243206-1.jpg').convert('RGB')
S=1229; ph=src.resize((S,S),Image.LANCZOS)
cx=618; x0=cx-W//2; top=520-658
PB=top+S  # photo bottom on the pin
canvas=Image.new('RGB',(W,H),FIELD)
crop=ph.crop((x0,max(0,-top),x0+W,S))
canvas.paste(crop,(0,max(0,top)))
# soft tonal fade: photo feathers into the field over the last ~28% of its visible depth
F0=PB-300
arr=np.asarray(canvas).astype(float)
ys=np.arange(H)[:,None]
t=np.clip((ys-F0)/(PB-F0),0,1)
t=t*t*(3-2*t)  # smoothstep
arr=arr*(1-t[...,None])+np.array(FIELD)[None,None,:]*t[...,None]
im=Image.fromarray(arr.astype('uint8'))
d=ImageDraw.Draw(im)

def capb(font,s="H"):
    bb=d.textbbox((0,0),s,font=font); return bb[1],bb[3]-bb[1]
def text_top(xy,t,font,fill):
    x,y=xy; off,h=capb(font); d.text((x,y-off),t,font=font,fill=fill); return h

# headline
hd=f(IS,124)
y=905
for i,line in enumerate(["How to goth up","a Christmas tree"]):
    h=text_top((M,y),line,hd,BERRY)
    print('hl',line,d.textlength(line,font=hd))
    y+=h+(34 if i==0 else 66)

# steps, two columns of two
nf=f(IS,64); bf=f(IN%500,25); bd=f(IN%400,25)
steps=[("Warm white lights.","Skip the color changers."),
       ("Two colors, tops.","Black and one deep red."),
       ("Thorns over tinsel.","Bare twigs, dried eucalyptus."),
       ("One moon somewhere.","Every dark tree needs one.")]
CW=(W-2*M-48)//2
for i,(a,b) in enumerate(steps):
    col=i%2; row=i//2
    x=M+col*(CW+48); yy=y+row*104
    nh=text_top((x,yy),str(i+1),nf,GOLD)
    tx=x+52
    text_top((tx,yy+2),a,bf,INK)
    text_top((tx,yy+2+capb(bf)[1]+14),b,bd,SOFT)
    print(a, tx+d.textlength(b,font=bd)-x, CW)
end=y+104+capb(bf)[1]*2+16
print('steps end',end,'photo bottom',PB,'fade start',F0)

# logo, bottom right on the right margin (v2: moved off the centered foot the toxic-frog pin uses)
logo=Image.open('assets/hh-monogram-white-140.png').convert('RGBA')
lh=34; lw=round(logo.width*lh/logo.height); logo=logo.resize((lw,lh),Image.LANCZOS)
logo=Image.merge('RGBA',(*[Image.new('L',logo.size,c) for c in INK],logo.split()[3]))
nm=f(IN%500,21); name="Hex & Hollow"; nw=d.textlength(name,font=nm)
tot=lw+12+nw; lx=round(W-M-tot); ly=H-60-lh
im.paste(logo,(lx,ly),logo)
bb=d.textbbox((0,0),name,font=nm)
d.text((lx+lw+12,ly+(lh-(bb[3]-bb[1]))//2-bb[1]),name,font=nm,fill=INK)
print('logo top',ly)
im.save(os.environ.get('PIN_OUT','/tmp/pin.jpg'),quality=80,optimize=True,progressive=True)
