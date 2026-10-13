import json,re,math,io
from collections import Counter
from pathlib import Path
import fitz,numpy as np
import matplotlib as mpl
from matplotlib import font_manager as fm
from matplotlib.mathtext import MathTextParser,math_to_image
R=Path(__file__).parent
fm.fontManager.addfont(R/'assets/AnishPen.ttf')
mpl.rcParams.update({'font.family':'Anish Pen','mathtext.fontset':'custom','mathtext.rm':'Anish Pen','mathtext.it':'Anish Pen','mathtext.bf':'Anish Pen','mathtext.sf':'Anish Pen','mathtext.tt':'Anish Pen','mathtext.cal':'Anish Pen','mathtext.fallback':None,'savefig.transparent':True})
ATLAS=json.loads((R/'assets/pen-paths.json').read_text())
PARSER=MathTextParser('path')
INK=1.10
CACHE={}
def norm(s):
    s=re.sub(r'\\sqrt\s*([a-zA-Z0-9])',lambda m:r'\sqrt{'+m[1]+'}',s)
    s=re.sub(r'\\frac([a-zA-Z0-9])',lambda m:r'\frac{'+m[1]+'}',s)
    s=re.sub(r'(\\frac\{[^{}]+\})([a-zA-Z0-9])',lambda m:m[1]+'{'+m[2]+'}',s)
    s=re.sub(r'\\le(?![a-zA-Z])',r'\\leq',s);s=re.sub(r'\\ge(?![a-zA-Z])',r'\\geq',s)
    s=s.replace(r'\Rightarrow',r'\to').replace(r'\cdots','...').replace(r'\ldots','...').replace(r'\#','')
    return s.replace(r'\in[5,7]',r',\quad5\leq f\leq7')
def layout(s,size=17):
    key=(norm(s),size)
    if key in CACHE:return CACHE[key]
    parsed=PARSER.parse('$'+key[0]+'$',dpi=72,prop=fm.FontProperties(family='Anish Pen',size=size))
    roots=[];used=set();paths=[];glyph_meta=[]
    for ft,sz,code,gx,gy in parsed.glyphs:
        if ft.family_name!='Anish Pen':raise ValueError(('Unexpected font',ft.family_name,code,s))
        if code==8730:
            # The rule emitted by the typesetter gives the exact roof position.
            choices=[(abs((rx-gx)-sz*.40),j,(rx,ry,rw,rh)) for j,(rx,ry,rw,rh) in enumerate(parsed.rects) if j not in used and rx>gx and rx-gx<sz*.7]
            if not choices:raise ValueError(('No radical roof',s,gx))
            _,j,(rx,ry,rw,rh)=min(choices);used.add(j)
            roof=ry+rh/2;h=sz*.90
            hook=[(gx+.04*h,roof-.67*h),(gx+.13*h,roof-.62*h),(gx+.24*h,roof-.94*h),(rx+.12,roof),(rx+rw,roof)]
            paths.append(hook);roots.append({'root':[float(gx),float(gy)],'roof':[float(rx),float(roof),float(rx+rw)],'joined':True})
            glyph_meta.append({'code':int(code),'size':float(sz),'x':float(gx),'y':float(gy)})
            continue
        if str(code) not in ATLAS:raise ValueError(('Missing pen glyph',code,s))
        for path in ATLAS[str(code)]:paths.append([(gx+px*sz/1000,gy+py*sz/1000) for px,py in path])
        glyph_meta.append({'code':int(code),'size':float(sz),'x':float(gx),'y':float(gy)})
    for j,(rx,ry,rw,rh) in enumerate(parsed.rects):
        if j not in used:paths.append([(rx,ry+rh/2),(rx+rw,ry+rh/2)])
    xs=[x for path in paths for x,y in path];ys=[y for path in paths for x,y in path]
    # Base-level glyphs identify the equation baseline independently of fractions
    # and superscripts. This is anchored to the same notebook ruling every time.
    baseline=Counter(round(g['y'],2) for g in glyph_meta if abs(g['size']-size)<.01 and g['code'] not in [8730,40,41,91,93,124]).most_common(1)
    baseline=baseline[0][0] if baseline else 0
    result={'paths':paths,'glyphs':glyph_meta,'roots':roots,'x0':min(xs)-INK/2,'x1':max(xs)+INK/2,'y0':min(ys)-INK/2,'y1':max(ys)+INK/2,'base':baseline,'math':key[0]}
    CACHE[key]=result;return result
def dimensions(s,size=17,maxw=499):
    a=layout(s,size);scale=min(1,maxw/(a['x1']-a['x0']))
    return a,scale,(a['y1']-a['base'])*scale,(a['base']-a['y0'])*scale
def write(p,s,x,baseline,size=17,maxw=499,tag=''):
    a,sc,asc,desc=dimensions(s,size,maxw)
    if sc<.8:raise ValueError(('Too small',sc,s))
    shape=p.new_shape()
    for path in a['paths']:
        coords=[fitz.Point(x+(px-a['x0'])*sc,baseline-(py-a['base'])*sc) for px,py in path]
        if len(coords)==1:shape.draw_line(coords[0],coords[0]+fitz.Point(.01,0))
        else:shape.draw_polyline(coords)
    shape.finish(color=(0,0,0),width=INK,lineCap=1,lineJoin=1,closePath=False);shape.commit()
    return {'page':p.number+1,'rect':[x,baseline-asc,x+(a['x1']-a['x0'])*sc,baseline+desc],'math':s,'normalized':a['math'],'baseline':baseline,'size':size*sc,'scale':sc,'tag':tag,'root_count':len(a['roots']),'glyphs':a['glyphs']}
def typed(s,size=17):
    # Independent conventional typography for side-by-side formula inspection.
    with mpl.rc_context({'font.family':'DejaVu Sans','mathtext.fontset':'dejavusans','savefig.transparent':True}):
        b=io.BytesIO();math_to_image('$'+norm(s)+'$',b,prop=fm.FontProperties(family='DejaVu Sans',size=size),format='pdf')
    return fitz.open(stream=b.getvalue(),filetype='pdf')
if __name__=='__main__':
    doc=fitz.open();p=doc.new_page(width=612,height=792)
    for n,s in enumerate(['abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ',r'0123456789\quad x^2y_1^3\quad x^{12}y^{2/3}',r'35.\quad u=\sqrt{x_1^2+...+x_n^2}',r'u_{x_i}=\frac{x_i}{\sqrt{x_1^2+...+x_n^2}}',r'\lim_{h\to0}\frac{|h|}{h}\quad\mathrm{DNE}',r'\nabla f(2,-3)=(-3/37,2/37),\quad u=(-1/\sqrt2,1/\sqrt2)',r'\frac{\cos\sqrt t\cos(1/t)}{2\sqrt t}+\frac{\sin\sqrt t\sin(1/t)}{t^2}']):
        write(p,s,85,110+n*75)
    p.get_pixmap(matrix=fitz.Matrix(1.6,1.6)).save(R/'uniform-sample.png')
