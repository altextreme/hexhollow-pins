# "Raven or crow?" (Skull and Raven tee, listing 4587520183), Nov 19 2026.
# Comparison / this-or-that table. Product photo on top, a two-column field ID below.
# Palette sampled from photos/4587520183-1.jpg: field = the print's red ink (#9C2026) deepened to oxblood,
# headline = the same red ink lifted for the dark field, neutrals = the print's bone ink (#C9B5A2).
import os
from PIL import Image, ImageDraw, ImageFont
W,H=1000,1500; M=64
FIELD=(46,13,16)      # red ink #9C2026, deepened, still clearly oxblood
RED=(218,64,66)       # red ink, lifted for the dark field (headline only)
BONE=(231,218,203)    # bone ink #C9B5A2, lifted
MUTED=(184,160,150)   # bone toward the field
RULE=(104,40,42)      # red ink, half-lit hairline
PF='assets/fonts/playfair-display-latin-%d-normal.woff'
IN='assets/fonts/inter-latin-%d-normal.woff'
f=lambda p,w,s: ImageFont.truetype(p%w,s)
im=Image.new('RGB',(W,H),FIELD); d=ImageDraw.Draw(im)
# photo: full bleed, under half the page, print centered
PH=600
src=Image.open('photos/4587520183-1.jpg').convert('RGB')
cw=1254; ch=round(cw*PH/W); cy0=350
im.paste(src.crop((0,cy0,cw,cy0+ch)).resize((W,PH),Image.LANCZOS),(0,0))
def capb(font):
    bb=d.textbbox((0,0),"H",font=font); return bb[1],bb[3]-bb[1]
def text_top(xy,t,font,fill,track=0):
    x,y=xy; off,h=capb(font)
    if track:
        for c in t: d.text((x,y-off),c,font=font,fill=fill); x+=d.textlength(c,font=font)+track
    else: d.text((x,y-off),t,font=font,fill=fill)
    return h
def wrap(t,font,w):
    out=[];cur=''
    for wd in t.split():
        tr=(cur+' '+wd).strip()
        if d.textlength(tr,font=font)<=w: cur=tr
        else: out.append(cur);cur=wd
    out.append(cur);return out
y=PH+50
lab=f(IN,600,20)
y+=text_top((M,y),"A FIELD GUIDE FOR THE NIGHT SHIFT",lab,MUTED,track=4)+30
hd=f(PF,900,144)
for i,line in enumerate(["Raven","or crow?"]):
    y+=text_top((M,y),line,hd,RED)+(38 if i==0 else 48)
# table: row label column + two columns
LW=176; G=28; CW=(W-2*M-LW-G*2)//2
X1=M+LW+G; X2=X1+CW+G
colh=f(PF,700,40)
text_top((X1,y),"Raven",colh,BONE); h=text_top((X2,y),"Crow",colh,BONE)
y+=h+24
rl=f(IN,600,18); body=f(IN,400,25)
rows=[("SIZE","Hawk-sized, heavy bill","Smaller, slimmer bill"),
      ("TAIL IN FLIGHT","Wedge-shaped, pointed","Fan-shaped, rounded"),
      ("CALL","A deep, rolling croak","The classic caw"),
      ("THROAT","Shaggy, bearded feathers","Smooth and sleek")]
for lbl,a,b in rows:
    d.line([M,y,W-M,y],fill=RULE,width=2)
    ty=y+24
    text_top((M,ty+4),lbl,rl,MUTED,track=2)
    ends=[]
    for x,t in ((X1,a),(X2,b)):
        yy=ty
        for ln in wrap(t,body,CW):
            text_top((x,yy),ln,body,BONE); yy+=36
        ends.append(yy)
    y=max(ends)+14
print('table end',y)
# footer
logo=Image.open('assets/hh-monogram-white-140.png').convert('RGBA')
lh=60; lw=round(logo.width*lh/logo.height); logo=logo.resize((lw,lh),Image.LANCZOS)
logo=Image.merge('RGBA',(*[Image.new('L',logo.size,c) for c in BONE],logo.split()[3]))
ly=H-54-lh; im.paste(logo,(M,ly),logo)
nm=f(IN,600,27); bb=d.textbbox((0,0),"Hex & Hollow",font=nm)
d.text((M+lw+16,ly+(lh-(bb[3]-bb[1]))//2-bb[1]),"Hex & Hollow",font=nm,fill=BONE)
print('footer top',ly)
im.save(os.environ.get('PIN_OUT','/tmp/pin.jpg'),quality=80,optimize=True,progressive=True)
