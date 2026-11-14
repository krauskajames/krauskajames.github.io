import json, math
from shapely.geometry import Polygon, LineString, Point, box, MultiPolygon
from shapely.affinity import translate, scale, rotate
from shapely.ops import unary_union
from PIL import Image, ImageDraw, ImageFont
g=json.loads(json.load(open("/tmp/pb/subject_native.json"))["geom"])
P=Polygon(g["rings"][0]); x0,y0,x1,y1=P.bounds
P=translate(P,-x0,-y0); W,H=x1-x0,y1-y0
def ell(cx,cy,rx,ry): return scale(Point(cx,cy).buffer(1,resolution=64),rx,ry)
CX,CY=880,450
# streets
green=ell(CX,CY,165,105)
ring=ell(CX,CY,231,171).difference(green)
blvd=box(CX-45,CY+150,CX+45,H+10)                      # 90 ft boulevard ROW
median=box(CX-10,CY+190,CX+10,H-20).union(Point(CX,CY+190).buffer(10))
bw=LineString([(CX-225,CY-20),(600,CY-35),(380,CY-45),(150,CY-25),(60,CY-15)]).buffer(33,cap_style=2,join_style=1)
be=LineString([(CX+225,CY+15),(1250,CY+30),(1500,CY+40),(W+20,CY+35)]).buffer(33,cap_style=2,join_style=1)
alley_s=LineString([(160,250),(W+20,250)]).buffer(12,cap_style=2)
alley_n=LineString([(300,CY+130),(640,CY+130)]).buffer(12,cap_style=2)
streets=unary_union([ring,blvd,bw,be]).intersection(P)
alleys=unary_union([alley_s,alley_n]).intersection(P).difference(streets)
# pond + outlot
outlot=P.intersection(box(0,0,W,205)).difference(streets)
pond=Polygon([(380,55),(520,40),(700,60),(860,45),(1010,70),(1120,60),(1230,95),(1180,140),(1010,150),(860,130),(700,150),(540,135),(420,120)]).buffer(10,join_style=1)
trail=pond.buffer(28).exterior
plaza_path=LineString([(CX,CY-171),(CX,170)]).buffer(6)
# buildings
B=[]
B+= [Polygon([(CX-60,H-30),(CX-215,H-30),(CX-215,H-80),(CX-110,H-80),(CX-110,H-170),(CX-60,H-170)])]   # mixed-use L west
B+= [Polygon([(CX+60,H-30),(CX+215,H-30),(CX+215,H-80),(CX+110,H-80),(CX+110,H-170),(CX+60,H-170)])]  # mixed-use L east
B+= [box(70,H-150,250,H-60).intersection(P.buffer(-25))]                                               # retail pad
B+= [Polygon([(1180,H-35),(1600,H-35),(1600,H-95),(1240,H-95),(1240,H-260),(1180,H-260)]),            # apartments C east
     Polygon([(1300,CY+95),(1700,CY+95),(1700,CY+155),(1640,CY+155),(1640,H-150),(1700,H-150),(1700,H-95)]).buffer(0)]
B=[b for b in B if not b.is_empty]
apt2=Polygon([(1300,CY+90),(1700,CY+90),(1700,CY+150),(1360,CY+150),(1360,CY+260),(1300,CY+260)])
B[-1]=apt2
# townhome rows (rear-loaded): south side of Street B facing north, west side north rows facing B
rows=[]
def row(xa,xb,ya,yb,unit=26,gap=14,per=6):
    x=xa; out=[]
    while x+unit*per<=xb:
        out.append(box(x,ya,x+unit*per,yb)); x+=unit*per+gap
    return out
rows+=row(150,CX-240,268,CY-80,per=4)          # south-west of ring
rows+=row(CX+245,1720,272,CY-35)         # south-east
rows+=row(300,CX-250,CY+40,CY+110,per=4)  # north of Street B west (face B)
rows+=row(300,CX-250,CY+150,CY+220,per=4)  # back-to-back across the alley
rows=[r.intersection(P.buffer(-15)) for r in rows]
# parking lots
park=[box(CX-215,H-260,CX-115,H-180), box(CX+115,H-260,CX+215,H-180), box(60,H-230,300,H-160).intersection(P.buffer(-20)),
      box(1255,H-250,1620,H-110), box(1375,CY+165,1690,H-165)]
# lots (to show C1 commercial frontage etc.) skipped; draw
S=0.62; pad=50; top=95
im=Image.new('RGB',(int(W*S)+2*pad,int(H*S)+pad+top+110),(250,250,247)); d=ImageDraw.Draw(im)
F='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; R='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
f=ImageFont.truetype(F,14); fs=ImageFont.truetype(R,12); ft=ImageFont.truetype(F,18)
T=lambda x,y:(pad+x*S, top+(H-y)*S)
def poly(g,fill,out=None,w=1):
    for q in ([g] if g.geom_type=='Polygon' else [h for h in getattr(g,'geoms',[]) if h.geom_type=='Polygon']):
        if q.area<5: continue
        d.polygon([T(*c) for c in q.exterior.coords],fill=fill,outline=out,width=w)
        pass
poly(P,(228,236,212),(70,70,70),2)
poly(outlot,(214,232,200))
for x in range(140,1750,55):
    for y in (215,):
        pass
poly(pond,(160,200,226),(110,150,185),2)
d.line([T(*c) for c in trail.coords],fill=(176,140,90),width=3)
poly(plaza_path,(176,140,90))
poly(ring,(255,255,255),(150,150,150),1); poly(green,(170,206,140),(110,150,90),2); poly(blvd.intersection(P),(255,255,255),(150,150,150),1); poly(bw.intersection(P),(255,255,255),(150,150,150),1); poly(be.intersection(P),(255,255,255),(150,150,150),1)
poly(median,(150,190,120))
poly(alleys,(236,236,236),(190,190,190))
for pk in park:
    pk=pk.intersection(P)
    poly(pk,(214,214,214),(170,170,170))
    xa,ya,xb,yb=pk.bounds
    x=xa+9
    while x<xb-5: d.line([T(x,ya+18),T(x,ya+5)],fill=(255,255,255),width=1); d.line([T(x,yb-5),T(x,yb-18)],fill=(255,255,255),width=1); x+=9
for b in B: poly(b,(120,120,124),(70,70,70))
for r in rows:
    poly(r,(150,120,108),(90,70,60))
    xa,ya,xb,yb=r.bounds; x=xa+26
    while x<xb-2: d.line([T(x,ya),T(x,yb)],fill=(90,70,60),width=1); x+=26
# trees
import random; random.seed(4)
for t in list(green.exterior.coords)[::5]: d.ellipse([T(t[0]-7,t[1]+7),T(t[0]+7,t[1]-7)],fill=(90,140,80))
for y in range(CY+200,int(H)-10,40): 
    for x in (CX-30,CX+30): d.ellipse([T(x-6,y+6),T(x+6,y-6)],fill=(90,140,80))
d.ellipse([T(CX-28,CY+20),T(CX+28,CY-20)],fill=(235,225,200),outline=(150,130,100))
# Playbird Rd
d.rectangle([T(0,H+46),T(W,H+8)],fill=(255,255,255),outline=(150,150,150))
def lab(x,y,t,font=f,c=(20,20,20),anchor='mm'): d.text(T(x,y),t,font=font,fill=c,anchor=anchor)
lab(W/2+350,H+27,"PLAYBIRD RD"); lab(CX,CY+60,"The Commons",fs); lab(CX,CY,"pavilion",fs)
lab(CX-150,H-55,"mixed use",fs,(255,255,255)); lab(CX+150,H-55,"mixed use",fs,(255,255,255))
lab(160,H-105,"retail",fs,(255,255,255)); lab(1420,H-65,"apartments",fs,(255,255,255)); lab(1500,CY+120,"apartments",fs,(255,255,255))
lab(CX+110,H-215,"Boulevard",fs); lab(470,CY-60,"Street B",fs); lab(1450,CY+5,"Street B",fs); lab(CX+205,CY-150,"Commons Loop",fs)
lab(800,100,"Outlot: pond + trail loop",f); lab(470,CY+240,"townhomes, alley between rows",fs); lab(1260,330,"townhomes (rear alley)",fs)
lab(40,CY-60,"stub W",fs,(180,60,40),'lm'); lab(W-10,CY-5,"stub E",fs,(180,60,40),'rm')
d.text((pad,10),"Concept 2 (made up): a walkable PUD center, after the North Town pattern next door",font=ft,fill=(20,20,20))
d.text((pad,34),"Boulevard entry · loop street around a green · mixed use on Playbird Rd · rear-loaded townhomes · pond and trail",font=fs,fill=(60,60,60))
# scale bar + north
by=im.size[1]-70; bx=pad
for i in range(4): d.rectangle([bx+i*100*S,by,bx+(i+1)*100*S,by+8],fill=(20,20,20) if i%2==0 else (255,255,255),outline=(20,20,20))
[d.text((bx+i*100*S-3,by+12),str(i*100)+(" ft" if i==4 else ""),font=fs,fill=(20,20,20)) for i in range(5)]
nx=bx+330; d.polygon([(nx,by-12),(nx-9,by+14),(nx,by+8),(nx+9,by+14)],fill=(20,20,20)); d.text((nx-5,by-30),"N",font=f,fill=(20,20,20))
d.text((pad+400,by-8),"Real parcel outline (31.2 ac, county data). Streets, buildings and lots are invented.\nStreet widths: boulevard 90 ft ROW, local streets 66 ft ROW, alleys 24 ft.",font=fs,fill=(60,60,60))
im.save('/home/claude/out/ch3_concept2.png'); print(im.size)
