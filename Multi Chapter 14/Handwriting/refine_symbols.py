"""Refine added radicals, limit arrows, and text-only x/l/t centerlines."""
import json, math, re, hashlib
from pathlib import Path
from collections import Counter
import fitz, numpy as np
import matplotlib as mpl
from matplotlib import font_manager as fm
from matplotlib.mathtext import MathTextParser
from fontTools.ttLib import TTFont
from fontTools.pens.ttGlyphPen import TTGlyphPen
from shapely.geometry import LineString
from handwritten_layout import layout, norm, write, typed, ATLAS, PARSER

R=Path(__file__).parent
PEN=1.5938
TEXT={
 120:[[(70,549),(510,74)],[(70,74),(510,549)]],
 108:[[(120,839),(120,59)]],
 116:[[(210,710),(210,60)],[(70,480),(340,480)]],
}
ADVANCES={120:600,108:300,116:395}
font=TTFont(R/'assets/AnishPen.ttf')
for code,paths in TEXT.items():
    pen=TTGlyphPen(None)
    for path in paths:
        polygon=LineString(path).buffer(28,cap_style=1,join_style=1)
        for ring in [polygon.exterior,*polygon.interiors]:
            pts=list(ring.coords);pen.moveTo(pts[0])
            for point in pts[1:]:pen.lineTo(point)
            pen.closePath()
    name=font.getBestCmap()[code]
    font['glyf'][name]=pen.glyph()
    font['hmtx'][name]=(ADVANCES[code],42)
for entry in font['name'].names:
    if entry.nameID in [1,4,6]:
        value='AnishText' if entry.nameID==6 else 'Anish Text'
        entry.string=value.encode(entry.getEncoding())
font.save(R/'assets/AnishText.ttf')
fm.fontManager.addfont(R/'assets/AnishText.ttf')
REFINED_PARSER=MathTextParser('path')

def refined_layout(s,size):
    with mpl.rc_context({'mathtext.rm':'Anish Text','mathtext.sf':'Anish Text','mathtext.tt':'Anish Text'}):
        parsed=REFINED_PARSER.parse('$'+norm(s)+'$',dpi=72,prop=fm.FontProperties(family='Anish Pen',size=size))
    old=layout(s,size)
    assert [int(g[2]) for g in parsed.glyphs]==[g['code'] for g in old['glyphs']]
    roots=[];used=set();paths=[];glyphs=[];text_counts=Counter();arrows=0
    for ft,sz,code,gx,gy in parsed.glyphs:
        code=int(code)
        assert ft.family_name in ['Anish Pen','Anish Text'],ft.family_name
        glyphs.append({'code':code,'size':float(sz),'x':float(gx),'y':float(gy),'text':ft.family_name=='Anish Text'})
        if code==8730:
            choices=[(abs((rx-gx)-sz*.40),j,(rx,ry,rw,rh)) for j,(rx,ry,rw,rh) in enumerate(parsed.rects) if j not in used and rx>gx and rx-gx<sz*.7]
            assert choices
            _,j,(rx,ry,rw,rh)=min(choices);used.add(j)
            roof=ry+rh/2;h=sz*.90
            # Begin with the descending stroke; omit the short left lead-in.
            points=[(gx+.13*h,roof-.62*h),(gx+.24*h,roof-.94*h),(rx+.12,roof),(rx+rw,roof)]
            paths.append({'points':points,'root':True});roots.append(points)
            continue
        is_text=code in TEXT and ft.family_name=='Anish Text'
        atlas=TEXT[code] if is_text else ATLAS[str(code)]
        if is_text:text_counts[chr(code)]+=1
        is_limit_arrow=code==8594 and '\\lim' in s and sz<size*.99
        if is_limit_arrow:arrows+=1
        for index,path in enumerate(atlas):
            adjusted=[]
            for px,py in path:
                if is_limit_arrow:
                    # Shorten only the shaft. Translate the unchanged arrowhead
                    # by half the reduction to preserve the glyph's center.
                    delta=(1434-123)*.22
                    if index==len(atlas)-1 and px<1434:px=1434+(px-1434)*.78
                    px-=delta/2
                adjusted.append((gx+px*sz/1000,gy+py*sz/1000))
            paths.append({'points':adjusted,'root':False})
    for j,(rx,ry,rw,rh) in enumerate(parsed.rects):
        if j not in used:paths.append({'points':[(rx,ry+rh/2),(rx+rw,ry+rh/2)],'root':False})
    xs=[x for p in paths for x,y in p['points']];ys=[y for p in paths for x,y in p['points']]
    baseline=Counter(round(g['y'],2) for g in glyphs if abs(g['size']-size)<.01 and g['code'] not in [8730,40,41,91,93,124]).most_common(1)
    base=baseline[0][0] if baseline else 0
    return {'paths':paths,'x0':min(xs)-.55,'x1':max(xs)+.55,'y0':min(ys)-.55,'y1':max(ys)+.55,'base':base,'roots':roots,'glyphs':glyphs,'text_counts':text_counts,'arrows':arrows}

def rounded_root(shape,points):
    current=points[0]
    for a,b,c in zip(points,points[1:],points[2:]):
        incoming=np.array(b)-np.array(a);outgoing=np.array(c)-np.array(b)
        l1,l2=np.linalg.norm(incoming),np.linalg.norm(outgoing)
        u,v=incoming/l1,outgoing/l2
        theta=math.acos(float(np.clip(np.dot(u,v),-1,1)))
        distance=min(.28*math.tan(theta/2),.22*min(l1,l2))
        radius=distance/math.tan(theta/2)
        start=np.array(b)-distance*u;end=np.array(b)+distance*v
        k=4/3*math.tan(theta/4)*radius
        shape.draw_line(fitz.Point(*current),fitz.Point(*start))
        shape.draw_bezier(fitz.Point(*start),fitz.Point(*(start+k*u)),fitz.Point(*(end-k*v)),fitz.Point(*end))
        current=end
    shape.draw_line(fitz.Point(*current),fitz.Point(*points[-1]))

def render_record(page,r,refined):
    x=r['rect'][0];b=r['baseline'];sc=r['scale']
    shape=page.new_shape()
    for path in refined['paths']:
        points=[(x+(px-refined['x0'])*sc,b-(py-refined['base'])*sc) for px,py in path['points']]
        if path['root']:rounded_root(shape,points)
        elif len(points)==1:shape.draw_line(fitz.Point(*points[0]),fitz.Point(points[0][0]+.01,points[0][1]))
        else:shape.draw_polyline([fitz.Point(*p) for p in points])
    shape.finish(color=(0,0,0),width=PEN,lineCap=1,lineJoin=1,closePath=False);shape.commit()
    updated=dict(r)
    updated['rect']=[x,b-(refined['y1']-refined['base'])*sc,x+(refined['x1']-refined['x0'])*sc,b+(refined['base']-refined['y0'])*sc]
    updated['text_letter_counts']=dict(refined['text_counts']);updated['limit_arrows']=refined['arrows']
    updated['root_centerlines']=[[[x+(px-refined['x0'])*sc,b-(py-refined['base'])*sc] for px,py in points] for points in refined['roots']]
    return updated
