from pathlib import Path
import re
p=Path(r'C:/Users/notso/Documents/Latex Vault/Multi Chapter 14/Chapter_14_Solutions.tex')
s=p.read_text().replace(r'\tableofcontents',r'\clearpage\tableofcontents')
section=None
lines=[]
graphs={'14.1':{9,11,15,25,29,45,47,49,51},'14.4':{11}}
for line in s.splitlines():
    m=re.search(r'\\section\*\{(14\.[1-8]) ',line)
    if m:section=m.group(1)
    m=re.fullmatch(r'\\ex\{(\d+)\}',line)
    if m and int(m.group(1)) in graphs.get(section,set()):
        lines.append(r'\Needspace{25\baselineskip}' if section=='14.1' else r'\Needspace{40\baselineskip}')
    lines.append(line)
s='\n'.join(lines)+'\n'
s=s.replace('Each level is a vertical translate of the same decreasing square-root curve and begins at $(0,k)$.', 'Each level is a vertical translate of the same decreasing square-root curve and begins at $(0,k)$. The sketch uses $k=-2,-1,0,1,2$, ordered from bottom to top.')
s=s.replace('All approach the $x$ axis as $x\\to\\infty$.', 'All approach the $x$ axis as $x\\to\\infty$. The sketch uses $k=-2,-1,0,1,2$, ordered from bottom to top.')
s=s.replace('negative levels are empty.', 'negative levels are empty. The plotted circles correspond to $k=1,1.5,2$, from smallest to largest.')
s=s.replace('All nonzero contours have these same asymptotes.', 'All nonzero contours have these same asymptotes. Blue curves show $k=1,4$; red curves show $k=-1,-4$; dashed lines show $k=0$.')
p.write_text(s,encoding='utf-8')
print('Kept the contents together and kept single-graph exercises with their sketches.')
