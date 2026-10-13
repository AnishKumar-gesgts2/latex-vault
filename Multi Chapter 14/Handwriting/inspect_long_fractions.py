import sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
import natural_handwriting as h
from matplotlib import font_manager as fm
from matplotlib._mathtext import Parser
def group(s,i):
    assert s[i]=='{',s[i:]
    start=i+1;depth=1;i+=1
    while depth:
        if s[i]=='{':depth+=1
        elif s[i]=='}':depth-=1
        i+=1
    return s[start:i-1],i
def fractions(s):
    result=[];i=0
    while i<len(s):
        if s.startswith(r'\frac',i):
            a,j=group(s,i+5);b,end=group(s,j)
            result.append((i,end,a,b))
        i+=1
    return result
