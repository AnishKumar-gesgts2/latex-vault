"""Use the full writing size for long fractions, reserving vertical room."""
import natural_handwriting as h
from natural_handwriting import *
from inspect_long_fractions import fractions
import matplotlib._mathtext as mt
STEP=20.126
THRESHOLD=75
_genfrac=mt.Parser._genfrac
DISPLAY_METRICS=[]
ACTIVE_GEOMETRY=None

def notebook_genfrac(self,ldelim,rdelim,rule,style,num,den):
    if style!=self._MathStyle.DISPLAYSTYLE:
        return _genfrac(self,ldelim,rdelim,rule,style,num,den)
    state=self.get_state();thickness=state.get_current_underline_thickness()
    cnum=mt.HCentered([num]);cden=mt.HCentered([den])
    width=max(num.width,den.width)
    cnum.hpack(width,'exactly');cden.hpack(width,'exactly')
    # Aim at adjacent notebook baselines. Reserve only the extra space required
    # for superscripts, descenders and the unchanged physical pen width.
    upper,lower=ACTIVE_GEOMETRY or (cnum.depth,cden.height)
    separation=max(STEP,upper+lower+h.PEN+2.0)
    gap=(separation-upper-lower-thickness)/2
    topgap=gap+upper-cnum.depth;bottomgap=gap+lower-cden.height
    vlist=mt.Vlist([cnum,mt.Vbox(0,topgap),mt.Hrule(state,rule),mt.Vbox(0,bottomgap),cden])
    metrics=state.fontset.get_metrics(state.font,mpl.rcParams['mathtext.default'],'=',state.fontsize,state.dpi)
    vlist.shift_amount=separation/2-(metrics.ymax+metrics.ymin)/2
    DISPLAY_METRICS.append({'width':width,'baseline_gap':separation,'size':state.fontsize,'upper':cnum.depth,'lower':cden.height})
    result=[mt.Hlist([vlist,mt.Hbox(thickness*2)])]
    if ldelim or rdelim:return self._auto_sized_delimiter(ldelim or '.',result,rdelim or '.')
    return result
mt.Parser._genfrac=notebook_genfrac

PROMOTIONS={}
def promote(s,size=17):
    normalized=h.norm(s)
    selected=[];all_fractions=fractions(normalized)
    for start,end,a,b in all_fractions:
        widths=[h.layout(t,size)['x1']-h.layout(t,size)['x0'] for t in [a,b]]
        if max(widths)>=THRESHOLD:selected.append(start)
    # Keep peer fractions in the same expression consistent in writing size.
    if selected:
        selected=sorted(set(selected)|{start for start,end,a,b in all_fractions if not any(i<start<j for i,j,_,_ in all_fractions)})
    for start in reversed(selected):normalized=normalized[:start]+r'\dfrac'+normalized[start+5:]
    PROMOTIONS[s]=len(selected)
    return normalized

_layout=h.refined_layout
def full_layout(s,size):
    global ACTIVE_GEOMETRY
    expression=promote(s,size)
    if PROMOTIONS[s]:
        varying=h.VARY;h.VARY=False;begin=len(DISPLAY_METRICS)
        h.REFINED_PARSER._parse_cached.cache_clear()
        _layout(expression,size)
        measured=DISPLAY_METRICS[begin:]
        ACTIVE_GEOMETRY=(max(v['upper'] for v in measured),max(v['lower'] for v in measured))
        h.REFINED_PARSER._parse_cached.cache_clear();h.VARY=varying
        try:result=_layout(expression,size)
        finally:ACTIVE_GEOMETRY=None
    else:result=_layout(expression,size)
    if PROMOTIONS[s]:
        # Anchor the upper of the two full-size fraction rows to the notebook.
        bars=[p for p in result['paths'] if p.get('fraction') and p['points'][1][0]-p['points'][0][0]>=THRESHOLD-2]
        if bars:
            bar=max(bars,key=lambda p:p['points'][1][0]-p['points'][0][0]);left,right=bar['points'][0][0],bar['points'][1][0];y=bar['points'][0][1]
            candidates=[g for g in result['glyphs'] if abs(g['size']-size)<.01 and left-1<=g['x']<=right+1 and g['y']>y and g['code'] not in [8730,40,41,91,93,124]]
            if candidates:result['base']=Counter(round(g['y'],3) for g in candidates).most_common(1)[0][0]
    return result
h.refined_layout=full_layout
h.BASE_CACHE.clear()

def write(p,s,x,baseline,size=17,maxw=499,tag=''):
    result=h.write(p,s,x,baseline,size,maxw,tag)
    result['fullsize_fraction_count']=PROMOTIONS.get(s,0)
    result['display_math']=promote(s,size)
    return result
