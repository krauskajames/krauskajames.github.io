import json
from shapely.geometry import Polygon, LineString, box
from shapely.affinity import translate
from PIL import Image, ImageDraw, ImageFont
g=json.loads(json.load(open("/tmp/pb/subject_native.json"))["geom"])
p=Polygon(g["rings"][0]); x0,y0,x1,y1=p.bounds
p=translate(p,-x0,-y0); W,H=x1-x0,y1-y0
A=LineString([(800,H+5),(800,430)]).buffer(33,cap_style=2)
B=LineString([(60,430),(W+5,430)]).buffer(33,cap_style=2)
streets=A.union(B).intersection(p)
pond=p.intersection(box(0,0,W,170)).difference(streets)
comm=p.intersection(box(0,H-330,520,H)).difference(streets)
rest=p.difference(streets).difference(pond).difference(comm)
S=0.6; pad=60
im=Image.new('RGB',(int(W*S)+2*pad,int(H*S)+2*pad+70),'white'); d=ImageDraw.Draw(im)
B_='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; f=ImageFont.truetype(B_,15); fs=ImageFont.truetype(B_,13); ft=ImageFont.truetype(B_,18)
T=lambda x,y:(pad+x*S, pad+(H-y)*S+40)
def poly(g,fill,out,w=2):
    for q in ([g] if g.geom_type=='Polygon' else list(g.geoms)):
        if q.area>10: d.polygon([T(*c) for c in q.exterior.coords],fill=fill,outline=out,width=w)
d.text((pad,8),"Concept only (made up): Playbird Rd PUD, about 31 acres. Lots are yours to lay out.",font=ft,fill='black')
poly(rest,(238,242,226),(60,60,60)); poly(comm,(244,214,180),(60,60,60)); poly(pond,(205,226,240),(60,60,60)); poly(streets,(225,225,225),(90,90,90))
d.line([T(0,H+20),T(W,H+20)],fill=(120,120,120),width=8); d.text(T(W/2-80,H+75),"PLAYBIRD RD",font=f,fill='black')
def lab(x,y,t,font=f,c='black'): d.text(T(x,y),t,font=font,fill=c)
lab(60,H-120,"C1 commercial"); lab(60,H-150,"~3 ac on Playbird Rd",fs)
lab(812,H-60,"Street A",fs); lab(812,H-85,"66 ft ROW",fs); lab(420,470,"Street B (66 ft ROW)",fs)
lab(560,330,"Townhome lots (block 2)"); lab(1050,700,"Apartment lots (block 1),"); lab(1050,672,"next to the R-4 apartments",fs)
lab(545,700,"Townhomes",fs); lab(545,676,"(block 3)",fs)
lab(500,110,"Outlot 1: stormwater pond + trail along the woods")
lab(130,470,"<- stub west",fs,(180,60,40)); lab(1600,470,"stub east ->",fs,(180,60,40))
d.rectangle((pad,im.size[1]-55,im.size[0]-pad,im.size[1]-8),outline='black')
d.text((pad+10,im.size[1]-48),"Stubs keep future connections open (west toward N 40th St, east toward the apartments).\nYou choose lot counts and sizes; the made-up PUD sets them, within Town, County and City review rules.",font=fs,fill='black')
im.save('/home/claude/out/ch3_concept_sketch.png')
