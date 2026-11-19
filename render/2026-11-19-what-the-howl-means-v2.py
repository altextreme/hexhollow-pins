# "What the howl really means" (howling wolf moon tee, listing 4588762149), Nov 19 2026.
# No headline period (Anthony, Nov 18 2026: "headlines should [not] have periods on them unless it's multiple sentences").
# Comparison: myth vs truth, three rows. Photo leads.
# Palette sampled from photos/4588762149-1.jpg: field = the candlelit wall behind her (#743F23) deepened,
# headline = the apple in the print (#88242A) lifted, accent = the candle flame (#F7A871),
# neutrals = the moon in the print, lifted.
import os
from PIL import Image, ImageDraw, ImageFont
W,H=1000,1500; M=64
FIELD=(50,30,21)      # candle glow on the wall, deepened, still a warm umber
APPLE=(222,78,80)     # print apple #88242A, lifted for the dark field
FLAME=(240,170,118)   # candle flame #F7A871
MOON=(232,224,212)    # moon, lifted
MUTED=(168,146,130)   # moon toward the field
RULE=(96,64,48)       # candle glow, lifted for a hairline
PF='assets/fonts/playfair-display-latin-%d-normal.woff'
IN='assets/fonts/inter-latin-%d-normal.woff'
f=lambda p,w,s: ImageFont.truetype(p%w,s)
im=Image.new('RGB',(W,H),FIELD); d=ImageDraw.Draw(im)
PH=640
src=Image.open('photos/4588762149-1.jpg').convert('RGB')
cw=src.width; ch=round(cw*PH/W); cy0=250
im.paste(src.crop((0,cy0,cw,cy0+ch)).resize((W,PH),Image.LANCZOS),(0,0))
def text_top(xy,t,font,fill,track=0):
    x,y=xy; bb=d.textbbox((0,0),"H",font=font)
    if track:
        for c in t: d.text((x,y-bb[1]),c,font=font,fill=fill); x+=d.textlength(c,font=font)+track
    else: d.text((x,y-bb[1]),t,font=font,fill=fill)
    return bb[3]-bb[1]
def wrap(t,font,w):
    out=[];cur=''
    for wd in t.split():
        tr=(cur+' '+wd).strip()
        if d.textlength(tr,font=font)<=w: cur=tr
        else: out.append(cur);cur=wd
    out.append(cur);return out
y=PH+50
lab=f(IN,600,21)
y+=text_top((M,y),"FIELD NOTES  /  THE HOWL",lab,MUTED,track=4)+28
hd=f(PF,700,92)
for line in ["What the howl","really means"]:
    y+=text_top((M,y),line,hd,APPLE)+34
y+=14
# columns
LX=M; LW=300; RX=M+LW+40; RW=W-M-RX
sm=f(IN,600,19)
text_top((LX,y),"THE MYTH",sm,MUTED,track=3)
text_top((RX,y),"THE TRUTH",sm,FLAME,track=3)
y+=d.textbbox((0,0),"H",font=sm)[3]-d.textbbox((0,0),"H",font=sm)[1]+20
rows=[(["They howl at","the moon."],"There’s no evidence the moon is why. Pointing up helps the sound carry."),
      (["It’s a lonely,","mournful cry."],"Mostly it’s a check-in: where’s the pack, and whose land is this."),
      (["The pack howls","one note."],"Each wolf takes its own pitch, so a few can sound like many.")]
my=f(IN,400,25); tr=f(IN,500,27)
for m,t in rows:
    d.line([M,y,W-M,y],fill=RULE,width=2)
    ty=y+24
    ly=ty
    for ln in m: text_top((LX,ly),ln,my,MUTED); ly+=36
    ry=ty
    for ln in wrap(t,tr,RW): text_top((RX,ry),ln,tr,MOON); ry+=38
    y=max(ly,ry)+14
print('rows end',y)
logo=Image.open('assets/hh-monogram-white-140.png').convert('RGBA')
lh=60; lw=round(logo.width*lh/logo.height); logo=logo.resize((lw,lh),Image.LANCZOS)
logo=Image.merge('RGBA',(*[Image.new('L',logo.size,c) for c in MOON],logo.split()[3]))
ly=H-54-lh; im.paste(logo,(M,ly),logo)
nm=f(IN,600,27); bb=d.textbbox((0,0),"Hex & Hollow",font=nm)
d.text((M+lw+16,ly+(lh-(bb[3]-bb[1]))//2-bb[1]),"Hex & Hollow",font=nm,fill=MOON)
print('footer top',ly)
im.save(os.environ.get('PIN_OUT','/tmp/pin.jpg'),quality=80,optimize=True,progressive=True)
