# "Black cat luck, by place" (Black Cat witchy tumbler, listing 4587517884), Nov 19 2026.
# No headline period (Anthony, Nov 18 2026: "headlines should [not] have periods on them unless it's multiple sentences").
# Format: world-tour glossary list. Skeleton e: text on top, full-bleed photo across the bottom.
# Palette sampled from photos/4587517884-2.jpg: field = the print's deep green moon disc and the blurred
# foliage (#505A3C) deepened to forest; headline = the print's gold ink (median #B18E58, 80th pct #E4BA7C);
# neutrals = the pale, sunlit forest floor (#C1B997) lifted to bone.
import os
from PIL import Image, ImageDraw, ImageFont
W,H=1000,1500; M=64
FIELD=(27,42,30)
GOLD=(228,186,124)
BONE=(236,231,212)
MUTED=(170,177,150)
RULE=(62,82,62)
BD='assets/fonts/bodoni-moda-latin-%d-normal.woff'
MR='assets/fonts/manrope-latin-%d-normal.woff'
AN='assets/fonts/archivo-narrow-latin-%d-normal.woff'
f=lambda p,w,s: ImageFont.truetype(p%w,s)
im=Image.new('RGB',(W,H),FIELD); d=ImageDraw.Draw(im)

# photo: full bleed across the bottom, under half the page
PH=668; PY=H-PH
src=Image.open('photos/4587517884-2.jpg').convert('RGB')
cw=1640; ch=round(cw*PH/W); cx0=1000-cw//2; cy0=360
im.paste(src.crop((cx0,cy0,cx0+cw,cy0+ch)).resize((W,PH),Image.LANCZOS),(0,PY))

def capb(font):
    bb=d.textbbox((0,0),"H",font=font); return bb[1],bb[3]-bb[1]
def text_top(xy,t,font,fill,track=0):
    x,y=xy; off,h=capb(font)
    if track:
        for c in t: d.text((x,y-off),c,font=font,fill=fill); x+=d.textlength(c,font=font)+track
    else: d.text((x,y-off),t,font=font,fill=fill)
    return h

# logo, top left
logo=Image.open('assets/hh-monogram-white-140.png').convert('RGBA')
lh=46; lw=round(logo.width*lh/logo.height); logo=logo.resize((lw,lh),Image.LANCZOS)
logo=Image.merge('RGBA',(*[Image.new('L',logo.size,c) for c in BONE],logo.split()[3]))
ly=60; im.paste(logo,(M,ly),logo)
nm=f(MR,600,24); bb=d.textbbox((0,0),"Hex & Hollow",font=nm)
d.text((M+lw+14,ly+(lh-(bb[3]-bb[1]))//2-bb[1]),"Hex & Hollow",font=nm,fill=BONE)

# headline
y=ly+lh+66
hd=f(BD,700,116)
for i,line in enumerate(["Black cat luck,","by place"]):
    y+=text_top((M,y),line,hd,GOLD)+(32 if i==0 else 50)
print('headline end',y, d.textlength("Black cat luck,",font=hd))

# rows
LW=228
pl=f(AN,700,19); vb=f(MR,600,25); bd=f(MR,400,25)
rows=[("JAPAN","Lucky.","Said to bring good fortune, and suitors."),
      ("SCOTLAND","Lucky.","One on your doorstep means prosperity."),
      ("FISHING TOWNS","Lucky.","Fishermen’s wives kept one for a safe return."),
      ("THE MIDLANDS","Lucky.","A wedding gift that brings the bride good luck."),
      ("MUCH OF THE WEST","Unlucky,","if one crosses your path. Blame witch lore.")]
RH=72
for p,v,t in rows:
    d.line([M,y,W-M,y],fill=RULE,width=2)
    ty=y+(RH-capb(bd)[1])//2
    text_top((M,ty+ (capb(bd)[1]-capb(pl)[1])//2),p,pl,MUTED,track=2.5)
    x=M+LW; text_top((x,ty),v,vb,BONE); x+=d.textlength(v+' ',font=vb)
    text_top((x,ty),t,bd,(206,206,184))
    print(p, x+d.textlength(t,font=bd))
    y+=RH
d.line([M,y,W-M,y],fill=RULE,width=2)
print('rows end',y,'photo top',PY)
im.save(os.environ.get('PIN_OUT','/tmp/pin.jpg'),quality=80,optimize=True,progressive=True)
