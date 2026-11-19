# "How to read a moth" (red moth sweatshirt, listing 4588636322), Nov 19 2026.
# No headline period (Anthony, Nov 18 2026: "headlines should [not] have periods on them unless it's multiple sentences").
# Labelled diagram / field guide. Keyed markers on the print, four entries below.
# Palette sampled from photos/4588636322-1.jpg: field = the print's red ink (#68282B) deepened,
# headline = the iced coffee (#C79763), neutrals = the plaster wall (#EDE4DF).
import os
from PIL import Image, ImageDraw, ImageFont
W,H=1000,1500; M=64
FIELD=(56,19,23)      # print ink #68282B, deepened, still clearly wine
COFFEE=(206,160,108)  # iced coffee #C79763, lifted a touch for the dark field
CREAM=(237,228,223)   # plaster wall, sampled
MUTED=(186,160,156)   # wall toward the field
RULE=(122,62,62)      # print ink, lifted for a visible hairline on the field
GA='assets/fonts/eb-garamond-latin-%d-normal.woff'
IN='assets/fonts/inter-latin-%d-normal.woff'
f=lambda p,w,s: ImageFont.truetype(p%w,s)
im=Image.new('RGB',(W,H),FIELD); d=ImageDraw.Draw(im)
# photo: full bleed, under half the page
PH=672
src=Image.open('photos/4588636322-1.jpg').convert('RGB')
cw=1430; ch=round(cw*PH/W); cx0=980-cw//2; cy0=300
s=W/cw
im.paste(src.crop((cx0,cy0,cx0+cw,cy0+ch)).resize((W,PH),Image.LANCZOS),(0,0))
P=lambda sx,sy:(round((sx-cx0)*s),round((sy-cy0)*s))
def text_top(xy,t,font,fill,track=0,anchor_cap=True):
    x,y=xy; bb=d.textbbox((0,0),"H",font=font)
    if track:
        for c in t: d.text((x,y-bb[1]),c,font=font,fill=fill); x+=d.textlength(c,font=font)+track
    else: d.text((x,y-bb[1]),t,font=font,fill=fill)
    return bb[3]-bb[1]
# keyed markers on the print (source coords of each part, then where the marker sits)
mk=f(IN,600,24); R=19
marks=[(1,(882,580),(760,480)),    # left antenna -> marker up-left
       (2,(965,700),(770,640)),     # head -> marker left
       (3,(995,775),(1200,850)),    # thorax -> marker lower-right on the wing
       (4,(1250,640),(1340,560))]   # forewing scales -> marker up-right
for n,part,at in marks:
    px,py=P(*part); mx,my=P(*at)
    d.line([px,py,mx,my],fill=CREAM,width=2)
    d.ellipse([px-4,py-4,px+4,py+4],fill=CREAM)
    d.ellipse([mx-R,my-R,mx+R,my+R],fill=CREAM)
    t=str(n); bb=d.textbbox((0,0),t,font=mk)
    d.text((mx-(bb[0]+bb[2])/2,my-(bb[1]+bb[3])/2),t,font=mk,fill=FIELD)
# label
y=PH+52
lab=f(IN,600,21)
ch_=text_top((M,y),"FIELD NOTES  /  ENTOMOLOGY",lab,MUTED,track=4); y+=ch_+30
# headline
hd=f(GA,600,118)
for line in ["How to read","a moth"]:
    capH=text_top((M,y),line,hd,COFFEE); y+=capH+36
y+=6
# entries, 2x2
colw=(W-2*M-48)//2
num=f(IN,600,22); tt=f(IN,600,29); body=f(IN,400,25)
items=[("Feathery antennae","Many males use them to smell a mate’s pheromones from far off."),
       ("No mouth, for some","Luna and other giant silk moths can’t eat as adults."),
       ("Furry thorax","Many moths shiver to warm up before they can fly."),
       ("Scaled wings","Lepidoptera means “scale wing.” That dust is scales.")]
def wrap(t,font,w):
    out=[];cur=''
    for wd in t.split():
        tr=(cur+' '+wd).strip()
        if d.textlength(tr,font=font)<=w: cur=tr
        else: out.append(cur);cur=wd
    out.append(cur);return out
rowtop=y
for i,(t,b) in enumerate(items):
    cx=M+(i%2)*(colw+48)
    if i==2: rowtop=rowbottom+34
    cy=rowtop
    d.line([cx,cy,cx+colw,cy],fill=RULE,width=2)
    nh=text_top((cx,cy+24),f"{i+1}",num,COFFEE)
    th=text_top((cx+34,cy+24),t,tt,CREAM)
    ty=cy+24+th+18
    for ln in wrap(b,body,colw-6):
        text_top((cx,ty),ln,body,MUTED); ty+=36
    if i%2==0: rb=ty
    else: rowbottom=max(rb,ty)
print('grid end',rowbottom)
# footer
logo=Image.open('assets/hh-monogram-white-140.png').convert('RGBA')
lh=60; lw=round(logo.width*lh/logo.height); logo=logo.resize((lw,lh),Image.LANCZOS)
logo=Image.merge('RGBA',(*[Image.new('L',logo.size,c) for c in CREAM],logo.split()[3]))
ly=H-54-lh; im.paste(logo,(M,ly),logo)
nm=f(IN,600,27); bb=d.textbbox((0,0),"Hex & Hollow",font=nm)
d.text((M+lw+16,ly+(lh-(bb[3]-bb[1]))//2-bb[1]),"Hex & Hollow",font=nm,fill=CREAM)
print('footer top',ly)
im.save(os.environ.get('PIN_OUT','/tmp/pin.jpg'),quality=78,optimize=True,progressive=True)
