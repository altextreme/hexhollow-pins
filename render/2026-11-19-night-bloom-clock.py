# "When the night garden opens" (Emotionally Nocturnal opossum mug, listing 4592258658), Nov 19 2026.
# Format: infographic, a timeline chart of when four night-blooming flowers are open, late afternoon to dawn.
# Skeleton c: photo as a full-width band through the middle, headline above, chart below. Both band edges
# feather softly into the field (top over the dark room, bottom over the pale tablecloth); the mug stays unfaded.
# Palette sampled from photos/4592258658-1.jpg: field = the dark rust-brown room behind the mug (#3A2B25,
# #381A14) kept warm; headline + one accent = the copper string lights and candle glow (#C2814D, 80th pct
# #DD995D); bars = the cereus-like cream flower on the mug (#BFAE9F) lifted; labels = warm neutrals from the room.
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
W,H=1000,1500; M=64
FIELD=(52,32,27)
COPPER=(221,153,93)
CREAM=(232,218,202)
MUTED=(176,152,140)
RULE=(92,66,58)
CG='assets/fonts/cormorant-garamond-latin-%d-normal.woff'
MR='assets/fonts/manrope-latin-%d-normal.woff'
f=lambda p,w,s: ImageFont.truetype(p%w,s)

# photo band: source 1200 wide, y 120..1020, scaled 0.8333 to 1000x750, placed at y=250
BT,BH=250,750
src=Image.open('photos/4592258658-1.jpg').convert('RGB')
band=src.crop((0,120,1200,120+900)).resize((W,BH),Image.LANCZOS)
canvas=np.full((H,W,3),FIELD,dtype=float)
b=np.asarray(band).astype(float)
ys=np.arange(BH)[:,None]
def ss(t): t=np.clip(t,0,1); return t*t*(3-2*t)
TOPF=64; BOTF0=622  # top fade 0..64 over the dark room, bottom fade 622..750 over the cloth; mug spans ~70..612
alpha=ss(ys/TOPF)*(1-ss((ys-BOTF0)/(BH-BOTF0)))
canvas[BT:BT+BH]=b*alpha[...,None]+np.array(FIELD)[None,None,:]*(1-alpha[...,None])
im=Image.fromarray(canvas.astype('uint8'))
d=ImageDraw.Draw(im)

def capb(font,s="H"):
    bb=d.textbbox((0,0),s,font=font); return bb[1],bb[3]-bb[1]
def text_top(xy,t,font,fill,track=0,anchor_right=False):
    x,y=xy; off,h=capb(font)
    if track:
        if anchor_right: x-=sum(d.textlength(c,font=font)+track for c in t)-track
        for c in t: d.text((x,y-off),c,font=font,fill=fill); x+=d.textlength(c,font=font)+track
    else:
        if anchor_right: x-=d.textlength(t,font=font)
        d.text((x,y-off),t,font=font,fill=fill)
    return h

# headline
hd=f(CG,700,104)
y=64
for i,line in enumerate(["When the night","garden opens."]):
    h=text_top((M,y),line,hd,COPPER); print('hl',d.textlength(line,font=hd)); y+=h+(30 if i==0 else 0)
print('headline end',y,'band top',BT)

# chart
X0,X1=300,W-M
ticks=["AFTERNOON","DUSK","AFTER DARK","MIDNIGHT","DAWN"]
tx=[X0+i*(X1-X0)/4 for i in range(5)]
AY=1036
ax=f(MR,600,15)
for i,(t,x) in enumerate(zip(ticks,tx)):
    w=sum(d.textlength(c,font=ax)+2 for c in t)-2
    xx= x if i==0 else (x-w if i==4 else x-w/2)
    text_top((xx,AY),t,ax,MUTED,track=2)
nm=f(MR,600,25); sb=f(MR,400,18)
rows=[("Four o’clock","opens ~4 PM",0,4,None),
      ("Evening primrose","opens in minutes",1,4,None),
      ("Moonflower","one night per bloom",1,4,None),
      ("Night cereus","peaks at midnight",2,4,3)]
RY=AY+40; RH=64
# faint tick guides through the rows, drawn under the bars
for x in tx:
    for yy in range(AY+30,RY+4*RH,8): d.point((round(x),yy),fill=RULE)
for name,sub,a,bnd,peak in rows:
    d.line([M,RY,X1,RY],fill=RULE,width=1)
    cy=RY+RH//2
    text_top((M,cy-capb(nm)[1]-5),name,nm,CREAM)
    text_top((M,cy+7),sub,sb,MUTED)
    xa,xb=tx[a],tx[bnd]
    bh=14
    d.rounded_rectangle([xa,cy-bh//2,xb,cy+bh//2],radius=bh//2,fill=CREAM)
    d.ellipse([xa-9,cy-9,xa+9,cy+9],fill=CREAM)
    if peak is not None:
        px=tx[peak]; d.ellipse([px-13,cy-13,px+13,cy+13],fill=COPPER)
    RY+=RH
d.line([M,RY,X1,RY],fill=RULE,width=1)
print('chart end',RY)

# logo bottom left, note bottom right
logo=Image.open('assets/hh-monogram-white-140.png').convert('RGBA')
lh=32; lw=round(logo.width*lh/logo.height); logo=logo.resize((lw,lh),Image.LANCZOS)
logo=Image.merge('RGBA',(*[Image.new('L',logo.size,c) for c in CREAM],logo.split()[3]))
ly=H-56-lh; im.paste(logo,(M,ly),logo)
lf=f(MR,600,20); bb=d.textbbox((0,0),"Hex & Hollow",font=lf)
d.text((M+lw+12,ly+(lh-(bb[3]-bb[1]))//2-bb[1]),"Hex & Hollow",font=lf,fill=CREAM)
note=f(MR,400,17); nt="Bars show when each bloom is open"
bb2=d.textbbox((0,0),nt,font=note)
d.text((X1-d.textlength(nt,font=note),ly+(lh-(bb2[3]-bb2[1]))//2-bb2[1]),nt,font=note,fill=MUTED)
print('logo top',ly)
im.save(os.environ.get('PIN_OUT','/tmp/pin.jpg'),quality=80,optimize=True,progressive=True)
