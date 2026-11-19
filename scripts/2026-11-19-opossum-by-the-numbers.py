# Reference: "Still here, by the numbers" (opossum mug, listing 4604532797), Nov 19 2026.
# Big-number infographic. Run from the repo root: python3 scripts/2026-11-19-opossum-by-the-numbers.py
# Palette sampled from photos/4604532797-2.jpg: field = pinecone shadow deepened, headline = the orange,
# rules = cinnamon stick, neutrals = candle wax. Copy the approach, not the layout.
from PIL import Image, ImageDraw, ImageFont
W,H=1000,1500; M=64
FIELD=(47,26,18)      # pinecone shadow, deepened (h19)
ORANGE=(224,157,80)   # the orange, sampled #E09D50
CREAM=(226,212,196)   # candle wax, lifted
MUTED=(170,148,130)   # candle wax toward the field
RULE=(152,101,65)     # cinnamon stick, sampled #986541
FR='assets/fonts/fraunces-latin-%d-normal.woff'
IN='assets/fonts/inter-latin-%d-normal.woff'
f=lambda p,w,s: ImageFont.truetype(p%w,s)
im=Image.new('RGB',(W,H),FIELD); d=ImageDraw.Draw(im)
PH=570
ph=Image.open('photos/4604532797-2.jpg').convert('RGB')
s=W/ph.width; ph=ph.resize((W,round(ph.height*s)),Image.LANCZOS)
y0=130; im.paste(ph.crop((0,y0,W,y0+PH)),(0,0))
def text_top(xy,t,font,fill,track=0):
    x,y=xy; bb=d.textbbox((0,0),"H",font=font)
    if track:
        for ch in t: d.text((x,y-bb[1]),ch,font=font,fill=fill); x+=d.textlength(ch,font=font)+track
    else: d.text((x,y-bb[1]),t,font=font,fill=fill)
    return bb[3]-bb[1]
# label
lab=f(IN,600,22)
y=PH+48
ch=text_top((M,y),"FIELD NOTES ON THE OPOSSUM",lab,MUTED,track=4)
y+=ch+26
# headline
hd=f(FR,600,100)
for line in ["Still here,","by the numbers."]:
    capH=text_top((M,y),line,hd,ORANGE); y+=capH+34
print('headline end',y)
# grid
y+=8
colw=(W-2*M-48)//2
num=f(FR,600,92); body=f(IN,400,28)
stats=[("50","teeth. The most of any land mammal in North America."),
       ("4 hrs","How long playing dead can last. It’s involuntary. Same."),
       ("94°F","Runs cool, about 94 to 97°F. Rabies rarely takes hold."),
       ("1","The only marsupial north of Mexico. The odd one out.")]
def wrap(t,font,w):
    out=[];cur=''
    for wd in t.split():
        tr=(cur+' '+wd).strip()
        if d.textlength(tr,font=font)<=w: cur=tr
        else: out.append(cur);cur=wd
    out.append(cur);return out
rowh=0
for i,(n,t) in enumerate(stats):
    cx=M+(i%2)*(colw+48); cy=y+(i//2)*0
    if i==2: y=rowbottom+30
    cy=y
    d.line([cx,cy,cx+colw,cy],fill=RULE,width=2)
    nh=text_top((cx,cy+30),n,num,CREAM)
    ty=cy+30+nh+22
    for ln in wrap(t,body,colw-10):
        text_top((cx,ty),ln,body,MUTED); ty+=39
    if i%2==0: rb=ty
    else: rowbottom=max(rb,ty)
print('grid end',rowbottom)
# footer
logo=Image.open('assets/hh-monogram-white-140.png').convert('RGBA')
lh=64; lw=round(logo.width*lh/logo.height); logo=logo.resize((lw,lh),Image.LANCZOS)
logo=Image.merge('RGBA',(*[Image.new('L',logo.size,c) for c in CREAM],logo.split()[3]))
ly=H-56-lh; im.paste(logo,(M,ly),logo)
nm=f(IN,600,28); bb=d.textbbox((0,0),"Hex & Hollow",font=nm)
d.text((M+lw+16,ly+(lh-(bb[3]-bb[1]))//2-bb[1]),"Hex & Hollow",font=nm,fill=CREAM)
print('footer top',ly)
im.save('/tmp/pin.jpg',quality=82,optimize=True,progressive=True)
im.resize((180,270),Image.LANCZOS).save('/tmp/pin-thumb.png')  # check feed-size legibility
