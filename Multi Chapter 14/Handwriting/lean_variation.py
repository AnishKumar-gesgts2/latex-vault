"""Subtle per-character pen imperfections without reflowing existing work."""
import json, math, random, re, sys
from collections import Counter
from pathlib import Path
import fitz, numpy as np
from PIL import Image, ImageDraw
R=Path(__file__).parent
SOURCE=R/'assets/layout-base.pdf'
WORK=R/'build'
WORK.mkdir(exist_ok=True)
OUT=WORK/'right-lean-intermediate.pdf'
records=json.loads((R/'assets/numerals-placements.json').read_text())
base=json.loads((R/'assets/pen-paths.json').read_text())
variants=json.loads((R/'assets/variable-variants.json').read_text())
numerals=json.loads((R/'assets/numeral-variants.json').read_text())
text={120:[[(70,549),(510,74)],[(70,74),(510,549)]],108:[[(120,839),(120,59)]],116:[[(210,710),(210,60)],[(70,480),(340,480)]]}
old=fitz.open(SOURCE);doc=fitz.open(SOURCE)
rng=random.Random(1410110712)
previous=json.loads((R/'assets/adjusted-glyphs.json').read_text())
previous_lookup={(e['row'],*e['segment_range']):e for e in previous}
variation_counts=Counter()
number=rb'[-+]?(?:\d*\.\d+|\d+\.?\d*)'
op_re=re.compile(rb'(?:'+number+rb'\s+){2}[ml]\b|(?:'+number+rb'\s+){6}c\b|\bh\b')

def key(g,r):return (g['code'],round(g['size']*r['scale'],8),g.get('variant'),g.get('numeral_variant'),g.get('text',False))
def pattern(k):
    code,size,var,nvar,is_text=k
    if nvar is not None:paths=numerals[str(code)][nvar]
    elif var is not None:paths=variants[str(code)][var]
    elif is_text and code in text:paths=text[code]
    else:paths=base[str(code)]
    out=[]
    for path in paths:
        ps=[fitz.Point(x*size/1000,-y*size/1000) for x,y in path]
        if len(ps)==1:out.append(('l',ps[0],ps[0]+fitz.Point(.01,0)))
        else:out.extend(('l',a,b) for a,b in zip(ps,ps[1:]))
    return out
def matches(items,patt):
    for start in range(len(items)-len(patt)+1):
        if items[start][0]!='l':continue
        offset=items[start][1]-patt[0][1]
        if abs(items[start][2]-patt[0][2]-offset)>.002:continue
        def equal(a,b):
            # MuPDF can reverse a microscopic closed pen dot's winding.
            tolerance=.045 if abs(b[2]-b[1])<.03 else .002
            return a[0]=='l' and abs(a[1]-b[1]-offset)<tolerance and abs(a[2]-b[2]-offset)<tolerance
        if all(equal(a,b) for a,b in zip(items[start:start+len(patt)],patt)):
            yield start,start+len(patt),offset

choices=[];misses=[];row_count=0;assigned=set()
for pnum in range(len(old)):
    if pnum==3:continue
    raw=old[pnum].read_contents();stack=[];leaves=[]
    for m in re.finditer(rb'\bq\b|\bQ\b',raw):
        if m.group()==b'q':stack.append(m.start())
        else:
            start=stack.pop();block=raw[start:m.end()]
            if re.search(rb'1\.59380*\s+w',block) and len(re.findall(rb'\bq\b',block))==1:leaves.append((start,m.end()))
    leaves.sort()
    draws=[(j,d) for j,d in enumerate(old[pnum].get_drawings()) if abs((d['width'] or 0)-1.5938)<.00001]
    assert len(leaves)==len(draws),(pnum+1,len(leaves),len(draws))
    lookup={}
    for rid,r in enumerate(records):
        if r['page']!=pnum+1 or r['tag'].startswith('question-mark-'):continue
        rect=fitz.Rect(r['rect'])
        def score(v):
            d=v[1]['rect'];return abs(d.x0-rect.x0-.55)+abs(d.x1-rect.x1+.55)+abs(d.y0-rect.y0-.55)
        j,d=min((v for v in draws if v[1]['color']==(0.,0.,0.)),key=score)
        assert score((j,d))<9,(rid,r['math'],score((j,d)))
        assert j not in lookup,(rid,lookup[j][0])
        lookup[j]=(rid,r)
    for (start,end),(j,d) in reversed(list(zip(leaves,draws))):
        if j not in lookup:continue
        rid,r=lookup[j]
        stack=[];translation=0.
        for token in re.finditer(rb'\bq\b|\bQ\b|1 0 0 1 0 (-?[0-9.]+) cm',raw[:start]):
            if token.group()==b'q':stack.append(translation)
            elif token.group()==b'Q':translation=stack.pop()
            else:translation+=float(token[1])
        leaf=raw[start:end];commands=[];current=None;pending_move=None;subpath_start=None
        def pagepoint(x,y):return fitz.Point(x,792-y-translation)
        for token in op_re.finditer(leaf):
            fields=token.group().split();op=fields[-1];values=list(map(float,fields[:-1]))
            if op==b'm':current=pagepoint(*values);pending_move=token.start();subpath_start=current
            elif op==b'l':
                point=pagepoint(*values)
                commands.append({'item':('l',current,point),'start':token.start(),'end':token.end(),'move':pending_move})
                current=point;pending_move=None
            elif op==b'h':
                commands.append({'item':('l',current,subpath_start),'start':token.start(),'end':token.end(),'move':pending_move})
                current=subpath_start;pending_move=None
            else:
                points=[pagepoint(*values[k:k+2]) for k in range(0,6,2)]
                commands.append({'item':('c',current,*points),'start':token.start(),'end':token.end(),'move':pending_move})
                current=points[-1];pending_move=None
        items=[c['item'] for c in commands];found=[];used=set()
        keys=Counter(key(g,r) for g in r['glyphs'] if str(g['code']) in base and g['code'] not in [8730,8594])
        for k,count in sorted(keys.items(),key=lambda kv:-len(pattern(kv[0]))):
            patt=pattern(k)
            occurrences=[(a,b,o) for a,b,o in matches(items,patt) if not any(i in used for i in range(a,b)) and commands[a]['move'] is not None]
            if len(occurrences)!=count:
                misses.append({'page':pnum+1,'row':rid,'char':chr(k[0]),'key':k,'found':len(occurrences),'expected':count})
            for a,b,offset in occurrences[:count]:
                used.update(range(a,b));found.append((a,b,k))
        edits=[]
        for a,b,k in sorted(found):
            points=[p for it in items[a:b] for p in it[1:]]
            box=fitz.Rect(min(p.x for p in points),min(p.y for p in points),max(p.x for p in points),max(p.y for p in points))
            cx=(box.x0+box.x1)/2;cy=(box.y0+box.y1)/2
            factor=min(1.,k[1]/17)
            category='text' if k[4] and chr(k[0]).isalpha() else 'math'
            multiplier=1.4 if category=='text' else 1.15
            if (rid,a,b) in previous_lookup:
                prior=previous_lookup[(rid,a,b)]
                angle=math.radians(prior['angle']*1.15)
                dx=prior['dx'];dy=prior['dy']*.25
                amp=prior['warp'];phase=prior['phase']
            else:
                # Small operator irregularities keep paired strokes together.
                angle=math.radians(max(-1.2,min(1.2,rng.gauss(0,.55)))*multiplier)
                dx=max(-.25,min(.25,rng.gauss(0,.11)))*factor*multiplier
                dy=max(-.45,min(.45,rng.gauss(0,.20)))*factor*multiplier
                amp=rng.uniform(.025,.065)*factor*multiplier;phase=rng.uniform(0,2*math.pi)
            variation_counts[category]+=1
            ca,sa=math.cos(angle),math.sin(angle)
            def transform(p):
                x=p.x-cx;y=p.y-cy
                # A smooth common warp keeps the parts of each letter connected.
                xx=cx+ca*x-sa*y-.105*y+dx+amp*math.sin(y/4+phase)
                yy=cy+sa*x+ca*y+dy+amp*.65*.25*math.sin(x/4+phase)
                return fitz.Point(xx,yy)
            replacement=[];newpoints=[]
            for ci in range(a,b):
                cmd=commands[ci];aa,bb=map(transform,cmd['item'][1:]);newpoints.extend([aa,bb])
                if cmd['move'] is not None:replacement.append(f'{aa.x:.8f} {792-aa.y-translation:.8f} m')
                replacement.append(f'{bb.x:.8f} {792-bb.y-translation:.8f} l')
            edits.append((commands[a]['move'],commands[b-1]['end'],'\n'.join(replacement).encode()))
            points+=newpoints
            maskbox=fitz.Rect(min(p.x for p in points)-2,min(p.y for p in points)-2,max(p.x for p in points)+2,max(p.y for p in points)+2)
            choices.append({'page':pnum+1,'row':rid,'char':chr(k[0]),'rect':list(maskbox),'angle':math.degrees(angle),'dx':dx,'dy':dy,'warp':amp,'center':[cx,cy],'phase':phase,'key':k,'segment_range':[a,b],'category':category,'multiplier':multiplier,'vertical_factor':.25,'tilt_variation_factor':1.15,'right_shear':.105})
        if edits:row_count+=1
        for a,b,newglyph in sorted(edits,reverse=True):leaf=leaf[:a]+newglyph+leaf[b:]
        raw=raw[:start]+leaf+raw[end:]
    xref=doc.get_new_xref();doc.update_object(xref,'<<>>');doc.update_stream(xref,raw);doc[pnum].set_contents(xref)
    print('Page',pnum+1,'processed',flush=True)
(WORK/'lean-matches.json').write_text(json.dumps({'changes':len(choices),'rows':row_count,'misses':misses},indent=2))
assert not misses,('Unmatched sampled glyphs',misses[:5])
assert len(choices)>5000
doc.save(OUT,garbage=4,deflate=True)
final=fitz.open(OUT);assert len(final)==len(old)==31
for i in range(len(old)):
    a=old[i].get_pixmap(matrix=fitz.Matrix(2,2),alpha=False);b=final[i].get_pixmap(matrix=fitz.Matrix(2,2),alpha=False)
    aa=np.frombuffer(a.samples,np.uint8).reshape(a.height,a.width,3);bb=np.frombuffer(b.samples,np.uint8).reshape(b.height,b.width,3)
    diff=np.any(aa!=bb,axis=2)
    for e in choices:
        if e['page']!=i+1:continue
        x0,y0,x1,y1=e['rect'];diff[max(0,int(y0*2)):int(y1*2)+1,max(0,int(x0*2)):int(x1*2)+1]=False
    assert not diff.any(),('Changed unrelated pixels',i+1)
    # All line widths, structural symbols, and native drawings stay untouched.
    da=old[i].get_drawings();db=final[i].get_drawings()
    assert len(da)==len(db)
    for a,b in zip(da,db):
        assert a['width']==b['width'] and a['color']==b['color']
        if abs((a['width'] or 0)-1.5938)>.00001 or a['color']!=(0.,0.,0.):assert a==b,('Native drawing changed',i+1)
    final[i].get_pixmap(matrix=fitz.Matrix(1.5,1.5),alpha=False).save(WORK/f'lean-page-{i+1:02}.png')
for s in json.loads((R/'assets/condensed-graph-spaces.json').read_text()):
    rect=fitz.Rect(s['rect']);p=s['page']-1
    assert old[p].get_pixmap(matrix=fitz.Matrix(2,2),clip=rect).samples==final[p].get_pixmap(matrix=fitz.Matrix(2,2),clip=rect).samples
for batch in range(math.ceil(len(final)/6)):
    board=Image.new('RGB',(1500,1400),'#eee');pen=ImageDraw.Draw(board)
    for slot,i in enumerate(range(batch*6,min((batch+1)*6,len(final)))):
        pix=final[i].get_pixmap(matrix=fitz.Matrix(.78,.78),alpha=False);im=Image.frombytes('RGB',[pix.width,pix.height],pix.samples)
        x=slot%3*500;y=slot//3*700;pen.text((x+8,y+6),f'Page {i+1}',fill='black');board.paste(im,(x+8,y+28))
    board.save(WORK/f'lean-board-{batch+1}.png')
audit={'pages':31,'characters_varied':len(choices),'rows_varied':row_count,'pen_width_unchanged':True,'math_content_unchanged':True,'unrelated_pixels_unchanged':True,'native_drawings_unchanged':True,'graph_spaces_unchanged':True,'math_variation_multiplier':1.15,'text_variation_multiplier':1.4,'vertical_variation_factor':.25,'tilt_variation_factor':1.15,'right_shear':.105,'variation_counts':dict(variation_counts)}
(WORK/'lean-audit.json').write_text(json.dumps(audit,indent=2))
(WORK/'lean-glyphs.json').write_text(json.dumps(choices,indent=2))
print(json.dumps(audit,indent=2))
