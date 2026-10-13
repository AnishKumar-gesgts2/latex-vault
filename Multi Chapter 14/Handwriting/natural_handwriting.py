"""Established pen renderer with authentic alternate variable centerlines."""
from pathlib import Path
import json,random
from handwritten_layout import layout as original_layout
R=Path(__file__).parent
source=(R/'refine_symbols.py').read_text(encoding='utf-8')
start=source.index("font=TTFont(R/'assets/AnishPen.ttf')")
end=source.index("REFINED_PARSER=MathTextParser('path')")
source=source[:start]+"fm.fontManager.addfont(R/'assets/AnishText.ttf')\n"+source[end:]
source=source.replace('old=layout(s,size)','old=original_layout(s,size)')
source=source.replace("'points':[(rx,ry+rh/2),(rx+rw,ry+rh/2)],'root':False", "'points':[(rx,ry+rh/2),(rx+rw,ry+rh/2)],'root':False,'fraction':True")
source=source.replace("atlas=TEXT[code] if is_text else ATLAS[str(code)]",'''atlas=TEXT[code] if is_text else ATLAS[str(code)]
        if VARY and (ft.family_name=='Anish Pen' or 48<=code<=57) and str(code) in VARIANTS:
            candidates=[j for j in range(3) if j!=LAST.get(code)]
            chosen=RNG.choice(candidates);LAST[code]=chosen
            atlas=VARIANTS[str(code)][chosen]
            glyphs[-1]['variant']=chosen
''')
exec(compile(source,str(R/'natural_handwriting_core.py'),'exec'))
VARIANTS=json.loads((R/'assets/variable-variants.json').read_text())
if (R/'assets/numeral-variants.json').exists():
    VARIANTS.update(json.loads((R/'assets/numeral-variants.json').read_text()))
RNG=random.Random(1406140831);LAST={};VARY=False;BASE_CACHE={}
INK=PEN

def layout(s,size=17):
    global VARY
    key=(s,size)
    if key not in BASE_CACHE:
        VARY=False;BASE_CACHE[key]=refined_layout(s,size)
    return BASE_CACHE[key]

def dimensions(s,size=17,maxw=499):
    a=layout(s,size)
    # Allow for centerline placement differences within the identical source
    # glyph frames. Keep every body glyph at its full writing size.
    width=a['x1']-a['x0']+1.6
    if width>maxw+.001:raise ValueError(('Wrap this row',round(width,2),s))
    return a,1.,a['y1']-a['base']+.8,a['base']-a['y0']+.8

def write(p,s,x,baseline,size=17,maxw=499,tag=''):
    global VARY
    base,sc,asc,desc=dimensions(s,size,maxw)
    VARY=True
    try:a=refined_layout(s,size)
    finally:VARY=False
    natural_x0=a['x0'];a['x0']=base['x0'];a['base']=base['base']
    record={'page':p.number+1,'rect':[x,baseline-asc,x+base['x1']-base['x0'],baseline+desc],'math':s,'normalized':norm(s),'baseline':baseline,'size':size,'scale':1.,'tag':tag,'root_count':len(a['roots']),'glyphs':a['glyphs'],'origin_x':x}
    record=render_record(p,record,a)
    record['rect'][0]=x+natural_x0-base['x0']
    record['variant_count']=sum('variant' in g for g in a['glyphs'])
    record['fraction_bars']=[[[x+(px-a['x0']),baseline-(py-a['base'])] for px,py in path['points']] for path in a['paths'] if path.get('fraction')]
    return record
