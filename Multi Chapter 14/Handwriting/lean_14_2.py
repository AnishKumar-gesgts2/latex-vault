"""Rewrite section 14.2 in sampled ink; retain its original graph exactly."""
import json,math,random,re,copy
from pathlib import Path
from collections import Counter
import fitz,numpy as np
import fullsize_fractions as pen
import natural_handwriting as h
R=Path(__file__).parent
WORK=R/'build'
WORK.mkdir(exist_ok=True)
SOURCE=WORK/'right-lean-intermediate.pdf'
OUT=WORK/'rebuilt-homework.pdf'
old=fitz.open(SOURCE);doc=fitz.open(SOURCE);p=doc[3]
ds=old[3].get_drawings()
keep={7,*range(504,522)} # lesson frame and complete native graph, including labels
removed={i for i,d in enumerate(ds) if d['color']==(0.,0.,0.) and abs((d['width'] or 0)-1.59375)<1e-5 and i not in keep}
raw=p.read_contents();strokes=list(re.finditer(rb'\bS\b',raw))
black=[(j,d) for j,d in enumerate(ds) if d['type']=='s' and d['color']==(0.,0.,0.)]
assert len(strokes)==len(black)
for k,(j,d) in reversed(list(enumerate(black))):
    if j not in removed:continue
    previous=strokes[k-1].end() if k else 0
    moves=list(re.finditer(rb'(-?\d+(?:\.\d+)?)\s+(-?\d+(?:\.\d+)?)\s+m\b',raw[previous:strokes[k].start()]))
    assert moves
    start=previous+moves[0].start();end=strokes[k].end();raw=raw[:start]+raw[end:]
stack=[];leaves=[]
for m in re.finditer(rb'\bq\b|\bQ\b',raw):
    if m.group()==b'q':stack.append(m.start())
    else:
        a=stack.pop();block=raw[a:m.end()]
        if re.search(rb'1\.59380*\s+w',block) and len(re.findall(rb'\bq\b',block))==1:leaves.append((a,m.end()))
assert len(leaves)==2
for a,b in reversed(leaves):raw=raw[:a]+raw[b:]
xref=doc.get_new_xref();doc.update_object(xref,'<<>>');doc.update_stream(xref,raw);p.set_contents(xref)
baseline=lambda n:82.0+n*20.126
rng=random.Random(1412141011);changes=[];placements=[]

def character_transform(points,g):
    xs=[x for x,y in points];ys=[y for x,y in points];cx=(min(xs)+max(xs))/2;cy=(min(ys)+max(ys))/2
    is_text=g.get('text',False) and chr(g['code']).isalpha()
    multiplier=1.4 if is_text else 1.15
    factor=min(1.,g['size']/17)
    letter=chr(g['code']).isalnum() or g['code'] in [952,960,955]
    if letter:
        angle=math.radians(max(-3.2,min(3.2,rng.gauss(0,1.5)))*multiplier)
        dx=max(-.6,min(.6,rng.gauss(0,.29)))*factor*multiplier
        dy=max(-1.2,min(1.2,rng.gauss(0,.65)))*factor*multiplier
        amp=rng.uniform(.06,.19)*factor*multiplier
    else:
        angle=math.radians(max(-1.2,min(1.2,rng.gauss(0,.55)))*multiplier)
        dx=max(-.25,min(.25,rng.gauss(0,.11)))*factor*multiplier
        dy=max(-.45,min(.45,rng.gauss(0,.2)))*factor*multiplier
        amp=rng.uniform(.025,.065)*factor*multiplier
    angle*=1.15;dy*=.25
    phase=rng.uniform(0,2*math.pi);ca,sa=math.cos(angle),math.sin(angle)
    def transform(pt):
        x,y=pt[0]-cx,pt[1]-cy
        return (cx+ca*x-sa*y-.105*y+dx+amp*math.sin(y/4+phase),cy+sa*x+ca*y+dy+amp*.65*.25*math.sin(x/4+phase))
    changes.append({'code':g['code'],'category':'text' if is_text else 'math','multiplier':multiplier,'angle':math.degrees(angle),'dx':dx,'dy':dy,'warp':amp})
    return transform

def render(page,r,a):
    paths=copy.deepcopy(a['paths']);glyphs=a['glyphs'];cursor=0;groups=[]
    for g in glyphs:
        code=g['code']
        if code==8730:n=1
        elif 'variant' in g:n=len(h.VARIANTS[str(code)][g['variant']])
        elif g.get('text') and code in h.TEXT:n=len(h.TEXT[code])
        else:n=len(h.ATLAS[str(code)])
        group=paths[cursor:cursor+n];assert len(group)==n;cursor+=n;groups.append((g,group))
    # Short relationship arrows and their neighboring gaps match later lessons.
    for g,group in groups:
        if g['code']!=8594:continue
        ps=[pt for path in group for pt in path['points']];left=min(x for x,y in ps);right=max(x for x,y in ps);cy=(min(y for x,y in ps)+max(y for x,y in ps))/2
        other=[pt for path in paths if not any(path is q for q in group) for pt in path['points']]
        before=[x for x,y in other if x<left-.01];after=[x for x,y in other if x>right+.01]
        trim=max(0,left-max(before))*.2 if before else 0
        endtrim=max(0,min(after)-right)*.2 if after else 0
        removed=(right-left)*.48+trim+endtrim
        limit=g['size']<r['size']*.99 and '\\lim' in r['math']
        arrow_index=next(i for i,(otherg,othergroup) in enumerate(groups) if otherg is g)
        for gi,(otherg,othergroup) in enumerate(groups):
            if otherg is g:
                for path in othergroup:path['points']=[(left-trim+(x-left)*.52,cy+(y-cy)*.52) for x,y in path['points']]
                continue
            ps=[pt for path in othergroup for pt in path['points']]
            # Move whole characters, never individual strokes across a cutoff.
            # A limit's arrow only compacts the condition underneath its word.
            if (limit and gi>arrow_index) or (not limit and min(x for x,y in ps)>right+.01):
                for path in othergroup:path['points']=[(x-removed,y) for x,y in path['points']]
            elif limit and otherg['code'] in [108,105,109] and abs(otherg['y']-g['y'])>7 and otherg['x']<right+15:
                for path in othergroup:path['points']=[(x-removed/2,y) for x,y in path['points']]
        for path in paths[cursor:]:
            if min(x for x,y in path['points'])>right+.01:
                path['points']=[(x-removed,y) for x,y in path['points']]
    shape=page.new_shape();allpoints=[]
    def pagepoint(pt):return (r['rect'][0]+pt[0]-a['x0'],r['baseline']-(pt[1]-a['base']))
    for g,group in groups:
        points=[pagepoint(pt) for path in group for pt in path['points']]
        # Transform each whole character together so its strokes stay connected.
        transform=character_transform(points,g)
        for path in group:
            ps=[transform(pagepoint(pt)) for pt in path['points']];allpoints+=ps
            if path.get('root'):h.rounded_root(shape,ps)
            elif len(ps)==1:shape.draw_line(fitz.Point(*ps[0]),fitz.Point(ps[0][0]+.01,ps[0][1]))
            else:shape.draw_polyline([fitz.Point(*pt) for pt in ps])
    for path in paths[cursor:]:
        ps=[pagepoint(pt) for pt in path['points']];allpoints+=ps
        shape.draw_polyline([fitz.Point(*pt) for pt in ps])
    shape.finish(color=(0,0,0),width=1.5938,lineCap=1,lineJoin=1,closePath=False);shape.commit()
    r['rect']=[min(x for x,y in allpoints)-.8,min(y for x,y in allpoints)-.8,max(x for x,y in allpoints)+.8,max(y for x,y in allpoints)+.8]
    return r
h.render_record=render

def write(s,x,line,tag,size=17):
    rr=pen.write(p,s,x,baseline(line),size,maxw=610-x,tag='14.2-rewrite-'+tag);placements.append(rr);return rr

write('14.2',99,1,'heading',19)
write('1.',74,3,'1-number')
write(r'\lim_{(x,y)\to(3,1)}f(x,y)=6',98,3,'1-math')
write(r'\mathrm{is\ about\ values\ around}\ (3,1).',266,3,'1-text-a')
write(r'\mathrm{If}\ f\ \mathrm{is\ continuous\ then}\ f(3,1)\ \mathrm{would\ equal}\ 6',250,4,'1-text-b')
write('5.',74,6,'5-number')
write(r'\lim_{(x,y)\to(3,2)}(x^2y^3-4y^2)=72-16=56',98,6,'5')
write('9.',74,8,'9-number')
write(r'\lim_{(x,y)\to(\pi,\frac{\pi}{2})}y\sin(x-y)=\frac{\pi}{2}\sin(\pi-\frac{\pi}{2})=\frac{\pi}{2}',98,8,'9')
write('15.',70,10,'15-number')
write(r'\lim_{(x,y)\to(0,0)}\frac{(x+y)^2}{x^2+y^2}',98,10,'15-intro')
write(r'\lim_{(x,y)\to(0,0)}(x,x)=\frac{4x^2}{2x^2}=2',255,10,'15-a')
write(r'\mathrm{limit\ DNE}',490,10,'15-answer')
write(r'\lim_{(x,y)\to(0,0)}(x,0)=\frac{x^2}{x^2}=1',255,12,'15-b')
write('19.',70,14,'19-number')
write(r'\lim_{(x,y)\to(-1,-2)}(x^2y-xy^2+3)^3=(-2+4+3)^3=(5)^3=125',98,14,'19')
write('31.',70,16,'31-number')
write(r'\lim_{(x,y)\to(0,0)}xy\sin(\frac{1}{x^2+y^2})',98,16,'31-intro')
write(r'|xy\sin(\frac{1}{x^2+y^2})|\le|xy|\le\frac{x^2+y^2}{2}\to0\quad\mathrm{squeeze}',98,18,'31-work')
write('39.',70,20,'39-number')
rr=write(r'f(x,y)=e^{\frac{1}{x-y}}',98,20,'39-function')
rr=write(r'\{(x,y)',230,20,'39-domain-left')
# The membership sign is sampled from the user's two original connected strokes.
xx=rr['rect'][2]+7;yy=baseline(20)-2;points=[];sourcebox=ds[447]['rect']|ds[448]['rect'];segments=[]
for j in [447,448]:
    for item in ds[j]['items']:
        ps=[]
        if item[0]=='l':ps=list(item[1:])
        elif item[0]=='c':
            a,b,c,e=item[1:]
            for i in range(17):
                t=i/16;ps.append(a*((1-t)**3)+b*(3*(1-t)**2*t)+c*(3*(1-t)*t*t)+e*(t**3))
        else:raise ValueError(item[0])
        coords=[(xx+pt.x-sourcebox.x0,yy-sourcebox.height+pt.y-sourcebox.y0) for pt in ps];segments.append(coords);points+=coords
trans=character_transform(points,{'code':8712,'size':17,'text':False});shape=p.new_shape()
for seg in segments:shape.draw_polyline([fitz.Point(*trans(pt)) for pt in seg])
shape.finish(color=(0,0,0),width=1.5938,lineCap=1,lineJoin=1,closePath=False);shape.commit()
write(r'x\ne y\}',xx+sourcebox.width+8,20,'39-domain-right')
write(r'\mathrm{it\ goes\ to\ infinity\ as}\ x-y\to0^+,\ \mathrm{and}\ 0\ \mathrm{as}\ x-y\to0^-',98,22,'39-behavior')
write('41.',70,31,'41-number')
write(r'F(x,y)=\frac{xy}{1+e^{x-y}}\quad\mathrm{continuous\ everywhere}',98,31,'41-function')
write(r'1+e^{x-y}>0',98,33,'41-work')
doc.save(OUT,garbage=4,deflate=True)
final=fitz.open(OUT);assert len(final)==31
for i in range(31):
    if i!=3:assert old[i].get_pixmap(matrix=fitz.Matrix(1.5,1.5)).samples==final[i].get_pixmap(matrix=fitz.Matrix(1.5,1.5)).samples,('Other page changed',i+1)
graph=fitz.Rect(82,534,187,664)
assert old[3].get_pixmap(matrix=fitz.Matrix(3,3),clip=graph).samples==final[3].get_pixmap(matrix=fitz.Matrix(3,3),clip=graph).samples,'Graph altered'
for d in final[3].get_drawings():
    if d['color']==(0.,0.,0.) and abs((d['width'] or 0)-1.59375)>.00001:assert abs(d['width']-1.5938)<1e-5
final[3].get_pixmap(matrix=fitz.Matrix(2,2),alpha=False).save(WORK/'lean-14-2.png')
(WORK/'lean-14-2-placements.json').write_text(json.dumps(placements,indent=2))
(WORK/'lean-14-2-variation.json').write_text(json.dumps(changes,indent=2))
(WORK/'lean-14-2-audit.json').write_text(json.dumps({'pages':31,'questions':[1,5,9,15,19,31,39,41],'math_multiplier':1.15,'text_multiplier':1.4,'graph_pixels_unchanged':True,'all_other_pages_unchanged':True,'sampled_membership_symbol':True,'characters_varied':len(changes)},indent=2))
print('Rewritten',len(placements),'fragments;',len(changes),'varied sampled characters;',OUT)
