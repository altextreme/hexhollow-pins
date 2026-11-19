# Reference: "The Carpool Setlist" (sweatshirt, listing 4620217027), Nov 19 2026.
# List format. Run from the repo root after fetching the listing photo into photos/.
# Palette: espresso field from the leather shadows, red from the print, amber from the autumn leaves.
# Copy the approach, not the layout.
PHOTO='photos/4620217027-1.jpg'
from PIL import Image, ImageDraw, ImageFont
W,H=1000,1500; M=64
BG=(33,22,16)        # espresso, from the leather shadows
RED=(214,40,48)      # print red, lifted for contrast on dark
CREAM=(239,230,214)  # print cream
MUTED=(176,155,136)
AMBER=(226,152,84)   # autumn leaves
RULE=(66,48,38)
im=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(im)
PH=660
ph=Image.open(PHOTO).convert('RGB')
s=W/ph.width; ph=ph.resize((W,round(ph.height*s)),Image.LANCZOS)
y0=round(140*s); im.paste(ph.crop((0,y0,W,y0+PH)),(0,0))
I='assets/fonts/'
def f(p,sz): return ImageFont.truetype(p,sz)
ANTON='assets/fonts/anton-latin-400-normal.woff'
lab=f(I+'inter-latin-600-normal.woff',24); head=f(ANTON,98); item=f(I+'inter-latin-500-normal.woff',36); art=f(I+'inter-latin-400-normal.woff',28); num=f(I+'inter-latin-600-normal.woff',36); nm=f(I+'inter-latin-600-normal.woff',30)
y=PH+50
x=M
for ch in "THE CARPOOL SETLIST":
    d.text((x,y),ch,font=lab,fill=AMBER); x+=d.textlength(ch,font=lab)+5
y+=46
for line in ["STILL SCREAMING THESE","AT SCHOOL DROP-OFF"]:
    bb=d.textbbox((0,0),line,font=head)
    d.text((M,y-bb[1]),line,font=head,fill=RED); y+=bb[3]-bb[1]+14
print('headline width', d.textlength("STILL SCREAMING THESE",font=head))
y+=24
songs=[("The Middle","Jimmy Eat World"),("Misery Business","Paramore"),("Sugar, We’re Goin Down","Fall Out Boy"),("Welcome to the Black Parade","MCR"),("I Write Sins Not Tragedies","Panic!"),("Ocean Avenue","Yellowcard")]
rowh=58
for i,(t,a) in enumerate(songs):
    d.line([M,y,W-M,y],fill=RULE,width=2)
    bb=d.textbbox((0,0),"Hg",font=item); ty=y+(rowh-(bb[3]-bb[1]))//2-bb[1]
    d.text((M,ty),str(i+1),font=num,fill=AMBER)
    d.text((M+52,ty),t,font=item,fill=CREAM)
    ab=d.textbbox((0,0),"Hg",font=art)
    d.text((W-M-d.textlength(a,font=art),y+(rowh-(ab[3]-ab[1]))//2-ab[1]),a,font=art,fill=MUTED)
    y+=rowh
d.line([M,y,W-M,y],fill=RULE,width=2)
print('list end',y)
logo=Image.open('assets/hh-monogram-white-140.png').convert('RGBA')
lh=70; lw=round(logo.width*lh/logo.height); logo=logo.resize((lw,lh),Image.LANCZOS)
# tint logo cream
r,g,b,a=logo.split(); logo=Image.merge('RGBA',(*[Image.new('L',logo.size,c) for c in CREAM],a))
ly=H-56-lh
print('logo top',ly)
im.paste(logo,(M,ly),logo)
bb=d.textbbox((0,0),"Hex & Hollow",font=nm)
d.text((M+lw+18,ly+(lh-(bb[3]-bb[1]))//2-bb[1]),"Hex & Hollow",font=nm,fill=CREAM)
import os
im.save(os.environ.get('PIN_OUT','/tmp/pin.jpg'),quality=82,optimize=True)
im.resize((180,270),Image.LANCZOS).save('/tmp/pin-thumb.png')
