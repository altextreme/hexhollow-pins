# "Speak fluent tape deck" (We Got Older, The Playlist Didn't cassette sweatshirt, listing 4611527435), Nov 19 2026.
# Format: glossary. Skeleton c: headline band on top, the photo as a hard-edged full-bleed band through the middle
# (a tape-window crop of the print and the iced coffee), glossary below. Logo top right. No eyebrow.
# Palette sampled from photos/4611527435-1.jpg: field = the iced latte (median #C8986A) taken down to a deep
# coffee brown; headline = the latte itself; terms = the cream wall (#ECE4DE); definitions = the wall dimmed.
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
W,H=1000,1500; M=64
LATTE=(200,152,105)
FIELD=(66,42,24)
CREAM=(236,228,222)
DIM=(196,182,170)
BC='assets/fonts/barlow-condensed-latin-800-normal.woff'
MONO='assets/fonts/ibm-plex-mono-latin-600-normal.woff'
IN='assets/fonts/inter-latin-%d-normal.woff'
f=lambda p,s: ImageFont.truetype(p,s)

im=Image.new('RGB',(W,H),FIELD)
d=ImageDraw.Draw(im)
def capb(font,s="H"):
    bb=d.textbbox((0,0),s,font=font); return bb[1],bb[3]-bb[1]
def text_top(xy,t,font,fill):
    x,y=xy; off,h=capb(font); d.text((x,y-off),t,font=font,fill=fill); return h

# headline, two lines, set huge
hd=f(BC,186)
y=150
for i,line in enumerate(["Speak fluent","tape deck."]):
    h=text_top((M,y),line,hd,LATTE)
    print('hl',line,d.textlength(line,font=hd))
    y+=h+(30 if i==0 else 0)
HL_END=y

# photo band: full bleed, hard edges like a cassette window
src=Image.open('photos/4611527435-1.jpg').convert('RGB')
S=1000; ph=src.resize((S,S),Image.LANCZOS)
BT=HL_END+70; BH=560
crop_top=150
im.paste(ph.crop((0,crop_top,W,crop_top+BH)),(0,BT))
BB=BT+BH
print('band',BT,BB)

# glossary, two columns
tf=f(MONO,26); df=f(IN%400,25)
terms=[("C90","90 minutes of tape,","45 a side. A whole mood."),
       ("Leader","The clear strip at each end.","It holds no sound. Wind past it."),
       ("Auto-reverse","Decks that flipped","to side B on their own."),
       ("The pencil fix","Rewinding a tape by hand","to save the batteries.")]
CW=(W-2*M-56)//2
gy=BB+72
for i,(t,a,b) in enumerate(terms):
    col=i%2; row=i//2
    x=M+col*(CW+56); yy=gy+row*150
    th=text_top((x,yy),t,tf,CREAM)
    l1=yy+th+22
    dh=text_top((x,l1),a,df,DIM)
    text_top((x,l1+dh+14),b,df,DIM)
    print(t, d.textlength(a,font=df), d.textlength(b,font=df), CW)
print('gloss end',gy+150+capb(tf)[1]+22+capb(df)[1]*2+14)

# logo, top right
logo=Image.open('assets/hh-monogram-white-140.png').convert('RGBA')
lh=34; lw=round(logo.width*lh/logo.height); logo=logo.resize((lw,lh),Image.LANCZOS)
logo=Image.merge('RGBA',(*[Image.new('L',logo.size,c) for c in CREAM],logo.split()[3]))
nm=f(IN%500,21); name="Hex & Hollow"; nw=d.textlength(name,font=nm)
tot=lw+12+nw; lx=round(W-M-tot); ly=58
im.paste(logo,(lx,ly),logo)
bb=d.textbbox((0,0),name,font=nm)
d.text((lx+lw+12,ly+(lh-(bb[3]-bb[1]))//2-bb[1]),name,font=nm,fill=CREAM)
im.save(os.environ.get('PIN_OUT','/tmp/pin.jpg'),quality=80,optimize=True,progressive=True)
