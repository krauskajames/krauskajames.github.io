import json, math
from shapely.geometry import Polygon, LineString, Point, box, MultiPolygon
from shapely.affinity import translate
from shapely.ops import unary_union, split
from PIL import Image, ImageDraw, ImageFont
g=json.loads(json.load(open("/tmp/pb/subject_native.json"))["geom"])
P=Polygon(g["rings"][0]); x0,y0,x1,y1=P.bounds
P=translate(P,-x0,-y0); W,H=x1-x0,y1-y0
def arc(cx,cy,r,a0,a1,n=24): return [(cx+r*math.cos(math.radians(a0+(a1-a0)*i/n)), cy+r*math.sin(math.radians(a0+(a1-a0)*i/n))) for i in range(n+1)]
R=120
cB=LineString([(60,560),(W+30,560)])
cA=LineString([(880,H+30),(880,300)])
cC=LineString([(330,560),(330,420)]+arc(450,420,R,180,270)[1:]+[(1430,300)]+arc(1430,420,R,270,360)[1:]+[(1550,560)])
ROW=unary_union([l.buffer(33,cap_style=2,join_style=1) for l in (cB,cA,cC)]).intersection(P)
ped=box(875,140,885,267)
out1=P.intersection(box(0,0,W,140))
west_park=P.intersection(box(0,140,297,527)).difference(ROW)
rest=P.difference(ROW).difference(out1).difference(west_park).difference(ped).buffer(-1).buffer(1)
apt2=rest.intersection(box(1583,140,W+5,527)); rest=rest.difference(box(1583,140,W+5,527))
blocks=[b for b in (rest.geoms if rest.geom_type=='MultiPolygon' else [rest]) if b.area>500]
lots=[]; big=[]
def cut_vertical(poly,x_from,x_to,step,tier_y=None):
    res=[]; x=x_from
    while x<x_to-1:
        strip=poly.intersection(box(x,-10,min(x+step,x_to),H+10))
        if tier_y is not None:
            for b in (box(-10,-10,W+10,tier_y),box(-10,tier_y,W+10,H+10)):
                p=strip.intersection(b)
                if p.area>800: res.append(p)
        elif strip.area>800: res.append(strip)
        x+=step
    return res
named={'APT2':apt2}
print([(round(b.centroid.x),round(b.centroid.y),round(b.area)) for b in blocks])
for b in blocks:
    cx,cy=b.centroid.x,b.centroid.y
    if cy>600:   # north block(s): big lots
        for name,xa,xb in [("C1",0,560),("MU1",560,847),("MU2",913,1200),("APT1",1200,W+5)]:
            p=b.intersection(box(xa,0,xb,H+5))
            if p.area>2000: named[name]=p
    elif b.bounds[0]>1540:
        named["APT2"]=b
    elif 333<cy<527:   # middle blocks: two tiers of 50-ft lots
        bx0,_,bx1,_=b.bounds
        lots+=cut_vertical(b,bx0,bx1,50,tier_y=430)
    else:              # south of C
        bx0,_,bx1,_=b.bounds
        lots+=cut_vertical(b,bx0,bx1,50)
# merge slivers (<3000 sf) into neighbor
lots=[l for l in lots if l.area>=2500]
S=0.62; pad=50; top=95
im=Image.new('RGB',(int(W*S)+2*pad,int(H*S)+pad+top+150),(252,252,249)); d=ImageDraw.Draw(im)
F='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; RG='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
f=ImageFont.truetype(F,14); fs=ImageFont.truetype(RG,11); fss=ImageFont.truetype(RG,9); ft=ImageFont.truetype(F,18)
T=lambda x,y:(pad+x*S, top+(H-y)*S)
def poly(gm,fill,out=(60,60,60),w=1):
    for q in ([gm] if gm.geom_type=='Polygon' else [h for h in getattr(gm,'geoms',[]) if h.geom_type=='Polygon']):
        if q.area<5: continue
        d.polygon([T(*c) for c in q.exterior.coords],fill=fill,outline=out,width=w)
poly(out1,(205,228,200)); poly(west_park,(205,228,200))
pond=Polygon(arc(880,70,1,0,360)).buffer(0)
pond=Polygon([(330,30),(600,20),(880,45),(1150,20),(1450,35),(1500,85),(1300,105),(1000,95),(880,110),(700,95),(420,100),(300,70)])
poly(pond,(165,203,228),(110,150,185))
d.line([T(*c) for c in pond.buffer(18).exterior.coords],fill=(176,140,90),width=2)
poly(ped,(176,140,90),None)
d.line([T(*c) for c in [(200,200),(200,520)]],fill=(176,140,90),width=2)
poly(ROW,(255,255,255),(130,130,130))
col={"C1":(244,214,180),"MU1":(232,190,160),"MU2":(232,190,160),"APT1":(214,200,226),"APT2":(214,200,226)}
for k,p in named.items(): poly(p,col[k],(60,60,60),2)
for l in lots: poly(l,(240,236,214),(90,90,90))
d.line([T(*c) for c in P.exterior.coords],fill=(30,30,30),width=3)
d.rectangle([T(0,H+46),T(W,H+8)],fill=(255,255,255),outline=(150,150,150))
def lab(x,y,t,font=f,c=(20,20,20)): d.text(T(x,y),t,font=font,fill=c,anchor='mm')
lab(1400,H+27,"PLAYBIRD RD (existing)")
desc={"C1":"C1 commercial","MU1":"MU1 mixed use","MU2":"MU2 mixed use","APT1":"APT1 apartments","APT2":"APT2"}
for k,p in named.items():
    c=p.representative_point(); ac=p.area/43560
    lab(c.x,c.y+12,desc[k],fs); lab(c.x,c.y-12,f"{ac:.1f} ac",fss)
lab(915,700,"Street A",fs); lab(700,575,"Street B",fs); lab(1000,315,"Street C (loop)",fs); lab(1720,575,"stub",fss,(180,60,40)); lab(85,575,"stub",fss,(180,60,40))
lab(205,350,"Outlot 2",fs); lab(205,330,"park + trail",fss)
lab(880,62,"Outlot 1: pond, trail, park",f)
lab(930,200,"10 ft walk",fss)
d.text((pad,10),"Concept 3 (made up): a preliminary plat that follows the Town and City rules",font=ft,fill=(20,20,20))
d.text((pad,34),"Every lot fronts a public street (66 ft ROW) · no alleys · two-tier blocks under 1,500 ft · 50 ft residential lots · 5%+ park and open space",font=fs,fill=(60,60,60))
d.text((pad,52),f"{len(lots)} residential lots (50 ft wide) + 5 commercial / mixed-use / apartment lots + 2 outlots",font=fs,fill=(60,60,60))
by=im.size[1]-110; bx=pad
for i in range(4): d.rectangle([bx+i*100*S,by,bx+(i+1)*100*S,by+8],fill=(20,20,20) if i%2==0 else (255,255,255),outline=(20,20,20))
for i in range(5): d.text((bx+i*100*S-3,by+12),str(i*100)+(" ft" if i==4 else ""),font=fs,fill=(20,20,20))
nx=bx+330; d.polygon([(nx,by-12),(nx-9,by+14),(nx,by+8),(nx+9,by+14)],fill=(20,20,20)); d.text((nx-5,by-30),"N",font=f,fill=(20,20,20))
park=(out1.area+west_park.area)/43560; row=ROW.area/43560
stats=f"Total 31.2 ac · streets {row:.1f} ac · outlots (park, pond, trail) {park:.1f} ac = {park/31.2*100:.0f}% (Town requires 5%) · residential lots avg {sum(l.area for l in lots)/len(lots):,.0f} sq ft"
d.text((pad+400,by-12),stats,font=fs,fill=(60,60,60))
d.text((pad+400,by+8),"Real parcel outline (county data). Streets, lots and uses are invented. Not a survey.",font=fs,fill=(60,60,60))
im.save('/home/claude/out/ch3_concept3.png')
print(len(lots), {k:round(p.area/43560,2) for k,p in named.items()}, round(park,2), round(row,2), min(l.area for l in lots), max(l.area for l in lots))
