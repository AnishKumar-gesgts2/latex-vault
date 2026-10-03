from pathlib import Path
import subprocess, re, json

vault = Path(r'C:/Users/notso/Documents/Latex Vault')
source = subprocess.check_output(['git','-C',str(vault),'show','a376b49^:Multi Chapter 14/Chapter_14_Solutions.tex'],text=True,encoding='utf-8')
summaries = {}
def add(sec, items):
    for n, text in items.items(): summaries[(sec,str(n))] = text
add('14.1', {
9:r'Find and sketch the domain of $g(x,y)=\sqrt{x}+\sqrt{4-4x^2-y^2}$.',
11:r'Find and sketch the domain of $g(x,y)=(x-y)/(x+y)$.',
15:r'Find and sketch the domain of $f(x,y,z)=\sqrt{4-x^2}+\sqrt{9-y^2}+\sqrt{1-z^2}$.',
19:r'Use the wind-chill table for $W=f(T,v)$ to evaluate $f(-15,40)$, solve $f(-20,v)=-30$ and $f(T,20)=-49$, and interpret the slices $f(-5,v)$ and $f(T,50)$. Here $T$ is in degrees Celsius and $v$ in km/h.',
25:r'Sketch the surface $z=10-4x-5y$.',29:r'Sketch the surface $z=x^2+4y^2+1$.',
45:r'Draw several level curves of $f(x,y)=x^2-y^2$.',47:r'Draw several level curves of $f(x,y)=\sqrt{x}+y$.',49:r'Draw several level curves of $f(x,y)=ye^x$.',51:r'Draw several level curves of $f(x,y)=\sqrt[3]{x^2+y^2}$.',
61:r'Match $z=\sin(xy)$ to a surface A--F and a contour map I--VI in the textbook, explaining both choices.',
62:r'Match $z=e^x\cos y$ to a surface and a contour map, explaining both choices.',
63:r'Match $z=\sin(x-y)$ to a surface and a contour map, explaining both choices.',
64:r'Match $z=\sin x-\sin y$ to a surface and a contour map, explaining both choices.',
65:r'Match $z=(1-x^2)(1-y^2)$ to a surface and a contour map, explaining both choices.',
66:r'Match $z=(x-y)/(1+x^2+y^2)$ to a surface and a contour map, explaining both choices.',
67:r'Describe the level surfaces of $f(x,y,z)=2y-z+1$.',68:r'Describe the level surfaces of $g(x,y,z)=x+y^2-z^2$.',69:r'Describe the level surfaces of $g(x,y,z)=x^2+y^2-z^2$.',70:r'Describe the level surfaces of $f(x,y,z)=x^2+2y^2+3z^2$.'})
add('14.2', {
1:r'If $\lim_{(x,y)\to(3,1)}f(x,y)=6$, what can be said about $f(3,1)$? What changes if $f$ is continuous?',
5:r'Find $\lim_{(x,y)\to(3,2)}(x^2y^3-4y^2)$.',9:r'Find $\lim_{(x,y)\to(\pi,\pi/2)}y\sin(x-y)$.',
15:r'Show that $\lim_{(x,y)\to(0,0)}(x+y)^2/(x^2+y^2)$ does not exist.',19:r'Evaluate $\lim_{(x,y)\to(-1,-2)}(x^2y-xy^2+3)^3$.',
31:r'Use the Squeeze Theorem to find $\lim_{(x,y)\to(0,0)}xy\sin(1/(x^2+y^2))$.',
39:r'Graph $f(x,y)=e^{1/(x-y)}$ and explain where it is discontinuous.',41:r'Determine where $F(x,y)=xy/(1+e^{x-y})$ is continuous.'})
add('14.3', {
15:r'Find the first partial derivatives of $f(x,y)=ye^{xy}$.',17:r'Find the first partial derivatives of $g(x,y)=y(x+x^2y)^5$.',
19:r'Find the first partial derivatives of $f(x,y)=(ax+by)/(cx+dy)$, with $a,b,c,d$ constant.',
21:r'Find the first partial derivatives of $g(u,v)=(u^2v-v^3)^5$.',23:r'Find the first partial derivatives of $R(p,q)=\arctan(pq^2)$.',
25:r'Find the first partial derivatives of $F(x,y)=\int_y^x\cos(e^t)\,dt$.',27:r'Find the first partial derivatives of $f(x,y,z)=x^3yz^2+2yz$.',
29:r'Find the first partial derivatives of $w=\ln(x+2y+3z)$.',31:r'Find the first partial derivatives of $p=\sqrt{t^4+u^2\cos v}$.',
33:r'Find the first partial derivatives of $h(x,y,z,t)=x^2y\cos(z/t)$.',35:r'Find all first partial derivatives of $u=\sqrt{x_1^2+\cdots+x_n^2}$.',
37:r'For $R(s,t)=te^{s/t}$, find $R_t(0,1)$.',41:r'Use implicit differentiation to find $z_x,z_y$ when $x^2+2y^2+3z^2=1$.',
45:r'Find $z_x,z_y$ for (a) $z=f(x)+g(y)$ and (b) $z=f(x+y)$.',
47:r'Find all second partial derivatives of $f(x,y)=x^4y-2x^3y^2$.',49:r'Find all second partial derivatives of $z=y/(2x+3y)$.',
51:r'Find all second partial derivatives of $v=\sin(s^2-t^2)$.',53:r'Verify $u_{xy}=u_{yx}$ for $u=x^4y^3-y^4$.',
59:r'Find $f_{xyz}$ for $f(x,y,z)=e^{xyz^2}$.',61:r'Find $W_{uuv}$ for $W=\sqrt{u+v^2}$.',
65:r'Use the limit definition to find $f_x,f_y$ for $f(x,y)=xy^2-x^3y$.',67:r'Find $f_{xzy}$ for $f(x,y,z)=xy^2z^3+\arcsin(x\sqrt z)$, choosing an efficient derivative order.',
77:r'Check the wave equation $u_{tt}=a^2u_{xx}$ for (a) $\sin(kx)\sin(akt)$, (b) $t/(a^2t^2-x^2)$, (c) $(x-at)^6+(x+at)^6$, and (d) $\sin(x-at)+\ln(x+at)$.',
88:r'For blood-flow resistance $R=CL/r^4$, calculate $R_L,R_r$ and interpret them. Here $C>0$ is constant, $L$ is vessel length, and $r$ is radius.',
104:r'The manifest assigns Exercise 104; this PDF has no Exercise 104 in Section 14.3.'})
add('14.4', {
1:r'Find the tangent plane to $z=16-x^2-y^2$ at $(2,2,8)$.',3:r'Find the tangent plane to $z=2x^2+y^2-5y$ at $(1,2,-4)$.',5:r'Find the tangent plane to $z=e^{x-y}$ at $(2,2,1)$.',
11:r'Graph $z=x^2+xy+3y^2$ and its tangent plane at $(1,1,5)$, then zoom in to compare them.',15:r'Explain differentiability of $f(x,y)=x^3y^2$ at $(-2,1)$ and find its linearization there.',
25:r'Given $f(2,5)=6$, $f_x(2,5)=1$, and $f_y(2,5)=-1$, estimate $f(2.2,4.9)$ by linear approximation.',31:r'Find the differential of $m=p^5q^3$.'})
add('14.5', {
1:r'Find $dz/dt$ by both the chain rule and direct substitution for $z=x^2y+xy^2$, $x=3t$, $y=t^2$.',
3:r'Use the chain rule for $z=xy^3-x^3y$, $x=t^2+1$, $y=t^2-1$.',5:r'Use the chain rule for $z=\sin x\cos y$, $x=\sqrt t$, $y=1/t$.',
7:r'Use the chain rule for $w=xe^{y/z}$, $x=t^2$, $y=1-t$, $z=1+2t$.',9:r'Find $z_s,z_t$ by both methods for $z=x^2+y^2$, $x=2s+3t$, $y=s+t$.',
11:r'Find $z_s,z_t$ for $z=(x-y)^5$, $x=s^2t$, $y=st^2$.',13:r'Find $z_s,z_t$ for $z=\ln(3x+2y)$, $x=s\sin t$, $y=t\cos s$.',
15:r'Find $z_s,z_t$ for $z=(\sin\theta)/r$, $r=st$, $\theta=s^2+t^2$.',
17:r'Find $p\prime(2)$ for $p(t)=f(g(t),h(t))$ using $g(2)=4$, $g\prime(2)=-3$, $h(2)=5$, $h\prime(2)=6$, $f_x(4,5)=2$, and $f_y(4,5)=8$.',
19:r'For $g(u,v)=f(e^u+\sin v,e^u+\cos v)$, use the supplied table to find $g_u(0,0)$ and $g_v(0,0)$. The relevant row has $f_x(1,2)=2$, $f_y(1,2)=5$.',
21:r'Draw the dependency tree and write the chain rule for $u=f(x,y)$, with $x=x(r,s,t)$ and $y=y(r,s,t)$.',
23:r'Draw the dependency tree and write the chain rule for $T=F(p,q,r)$, where each of $p,q,r$ depends on $x,y,z$.',
25:r'Find $z_s,z_t,z_u$ at $(4,2,1)$ for $z=x^4+x^2y$, $x=s+2t-u$, $y=stu^2$.',
27:r'Find $w_r,w_\theta$ at $r=2$, $\theta=\pi/2$ for $w=xy+yz+zx$, $x=r\cos\theta$, $y=r\sin\theta$, $z=r\theta$.',
29:r'Find $N_u,N_v,N_w$ at $(2,3,4)$ for $N=(p+q)/(p+r)$, $p=u+vw$, $q=v+uw$, $r=w+uv$.',
31:r'Find $dy/dx$ implicitly from $y\cos x=x^2+y^2$.',33:r'Find $dy/dx$ implicitly from $\arctan(x^2y)=x+xy^2$.'})
add('14.6', {
5:r'Find the directional derivative of $f(x,y)=y\cos(xy)$ at $(0,1)$ in the direction $\theta=\pi/4$.',
7:r'Find the directional derivative of $f(x,y)=\arctan(xy)$ at $(2,-3)$ in the direction $\theta=3\pi/4$.',
9:r'Find $\nabla f$, its value at $P$, and $D_uf(P)$ for $f=x/y$, $P=(2,1)$, $u=\vv{3/5,4/5}$.',
11:r'Find $\nabla f$, its value at $P$, and $D_uf(P)$ for $f=x^2yz-xyz^3$, $P=(2,-1,1)$, $u=\vv{0,4/5,-3/5}$.',
15:r'Find the directional derivative of $g(s,t)=s\sqrt t$ at $(2,4)$ in the direction $v=\vv{2,-1}$.',
21:r'For $f=x^2y^2-y^3$, find the directional derivative at $P=(1,2)$ toward $Q=(-3,5)$.',
29:r'Find the maximum rate of change of $f=\sin(xy)$ at $(1,0)$ and its direction.',
41:r'Given $A=(1,3)$, $B=(3,3)$, $C=(1,7)$, $D=(6,15)$ and directional derivatives $3$ toward $B$ and $26$ toward $C$, find the derivative at $A$ toward $D$.',
43:r'Prove the gradient rules for $au+bv$, $uv$, $u/v$, and $u^n$, with $a,b$ constant.',
45:r'Calculate $D_u^2f(2,1)$ for $f=x^3+5x^2y+y^3$ and $u=\vv{3/5,4/5}$.',
51:r'Find the tangent plane and normal line to $x+y+z=e^{xyz}$ at $(0,0,1)$.',
57:r'Derive the tangent-plane equation to $x^2/a^2+y^2/b^2+z^2/c^2=1$ at $(x_0,y_0,z_0)$.',
61:r'Find any points on $x^2-y^2-z^2=1$ whose tangent plane is parallel to $z=x+y$.'})
add('14.7', {
5:r'Find and classify the critical points of $f=x^2+xy+y^2+y$.',9:r'Find and classify the critical points of $f=(x-y)(1-xy)$.',15:r'Find and classify the critical points of $f=x^4-2x^2+y^3-3y$.',
31:r'Find the critical points to three decimal places and classify them for $f=x^4+y^3-3x^2+y^2+x-2y+1$; determine whether the full graph has highest or lowest points.',
33:r'Find absolute extrema of $f=x^2+y^2-2x$ on the closed triangle with vertices $(2,0)$, $(0,2)$, $(0,-2)$.',
35:r'Find absolute extrema of $f=x^2+y^2+x^2y+4$ on $|x|\le1$, $|y|\le1$.',
37:r'Find absolute extrema of $f=x^2+2y^2-2x-4y+1$ on $0\le x\le2$, $0\le y\le3$.',
41:r'Show that $f=-(x^2-1)^2-(x^2y-x-1)^2$ has just two critical points, both local maxima, and no local minimum; graph it to explain this behavior.',
43:r'Find the shortest distance from $(2,0,-3)$ to the plane $x+y+z=1$.',45:r'Find the points on $z^2=x^2+y^2$ closest to $(4,2,0)$.',47:r'Find three positive numbers with sum $100$ and maximum product.'})
add('14.8', {
3:r'Use Lagrange multipliers to find extrema of $f=x^2-y^2$ subject to $x^2+y^2=1$.',
7:r'Use Lagrange multipliers to find extrema of $f=2x^2+6y^2$ subject to $x^4+3y^4=1$.',
17:r'Use Lagrange multipliers to give an alternative solution to Section 4.7, Exercise 3.',
19:r'Use Lagrange multipliers to give an alternative solution to Section 4.7, Exercise 7.',
21:r'Use Lagrange multipliers to give an alternative solution to Section 4.7, Exercise 25.',
23:r'For $f=x^2+y^2$ subject to $xy=1$, find the minimum by Lagrange multipliers and explain why there is no maximum.'})

# Retain the mathematical derivations as a starting point, after comparing them
# directly with the PDF. Remove old substitutions for unavailable cross-references.
source = source[:source.index(r'\section*{Prompt needed to finish this chapter}')] + '\\end{document}\n'
for n, ref in [(17,3),(19,7),(21,25)]:
    pat = r'(\\ex\{'+str(n)+r'\}\n)(.*?)(?=\\ex\{|\\end\{document\})'
    start = source.index(r'\section*{14.8')
    tail = re.sub(pat, lambda m: m.group(1) + rf'\textbf{{Source needed.}} The PDF explicitly refers to Section 4.7, Exercise {ref}. Section 4.7 is not included in this multivariable volume, which begins with Chapter 12. The optimization problem and its constraint must be obtained from the other book before a worked solution can be verified. No different exercise has been substituted.'+'\n', source[start:], flags=re.S)
    source = source[:start]+tail
source = source.replace(r'\clearpage\section*{14.4', r'''\ex{104}
\textbf{Source needed.} Section 14.3 ends at Exercise 101 on printed page 973 (PDF page 336). Exercise 104 is assigned in the manifest but is absent from this edition. Compare the other book and supply the exact prompt before solving it.
\clearpage\section*{14.4''')
source = source.replace(r'\noindent Source: Stewart, Clegg, and Watson, ninth edition. This chapter follows the assignment screenshot. Question 103 of Section 14.3 has been removed as requested; Question 104 still requires its original prompt.', r'''\noindent\fbox{\parbox{0.94\linewidth}{\textbf{Reminder to myself:} I need to verify that the first three assigned questions (14.1 \#9, \#11, and \#15) match between this PDF and the other book I am supposed to use. This comparison is still pending.}}
\medskip

\noindent\textbf{Source and scope.} Stewart, Clegg, and Watson, \emph{Calculus}, ninth edition, multivariable volume. Only Chapter 14 exercises in \texttt{assignment\_manifest.json} are included. Each entry gives a short description followed by the method, intermediate steps, and conclusion. Four assigned entries need an additional source: 14.3 \#104 and 14.8 \#17, \#19, \#21. Their missing prompts are explained at their assigned locations.
\medskip

\noindent\textbf{Reading the notation.} A subscript such as $f_x$ means a partial derivative; hold the other variables fixed. A boxed expression marks a result. A decimal approximation is indicated by $\approx$; exact fractions and radicals are kept when possible.
\medskip

\noindent\textbf{Textbook navigation (printed pages / PDF pages).}
\begin{center}\begin{tabular}{lll}\toprule Section & Printed exercise pages & PDF pages\\\midrule
14.1 & 946--950 & 309--313\\
14.2 & 960 & 323\\
14.3 & 970--973 & 333--336\\
14.4 & 981--982 & 344--345\\
14.5 & 991--992 & 354--355\\
14.6 & 1005--1007 & 368--370\\
14.7 & 1017--1018 & 380--381\\
14.8 & 1026--1027 & 389--390\\\bottomrule\end{tabular}\end{center}''')
source = '% Reminder: Verify that the first three assigned questions (14.1 #9, #11, #15) match the PDF and the other required book.\n'+source
source = source.replace(r'\author{}\date{}',r'\author{Anish Kumar}\date{}')
source = source.replace(r'\usepackage[colorlinks=true,linkcolor=blue]{hyperref}',r'''\usepackage{needspace}
\usepackage[colorlinks=true,linkcolor=blue]{hyperref}
\setlength{\parindent}{0pt}
\setlength{\parskip}{0.4em}
\setlength{\emergencystretch}{2em}''')
source = source.replace(r'\newcommand{\ex}[1]{\subsection*{#1.}}',r'\newcommand{\ex}[1]{\Needspace{8\baselineskip}\subsection*{Exercise #1}}')
source = source.replace(r'\ans{u_r=f_xx_r+f_yy_r}',r'\ans{u_r=f_x\,x_r+f_y\,y_r}').replace(r'\ans{u_s=f_xx_s+f_yy_s}',r'\ans{u_s=f_x\,x_s+f_y\,y_s}').replace(r'\ans{u_t=f_xx_t+f_yy_t}',r'\ans{u_t=f_x\,x_t+f_y\,y_t}')
source = source.replace('Here $f_xx_r$ means the product $f_x\\,x_r$, not a second derivative.', 'Each term is a product of derivatives along one path through the dependency tree.')
source = source.replace('The values fall as $v$ rises:', 'The values are nonincreasing as $v$ rises:')
source = source.replace('The values rise with $T$:', 'The values rise with $T$:')
# The plotted color scale must agree with the description of the tangent-plane plot.
source = source.replace(r'\addplot3[surf,opacity=.65,samples=19]',r'\addplot3[surf,opacity=.65,samples=19,colormap={blue}{color=(blue) color=(blue)}]')
# A plotted range can hide an important ridge; include a close window at each peak.
peak_graphs = r'''
The following two closer views retain both peaks without clipping the narrow ridge.
\surf{domain=-1.25:-.75,y domain=-.75:.75,zmin=-2,zmax=.1}{x}{y}{-(x^2-1)^2-(x^2*y-x-1)^2}
\surf{domain=.75:1.25,y domain=1.25:2.75,zmin=-2,zmax=.1}{x}{y}{-(x^2-1)^2-(x^2*y-x-1)^2}
'''
source=source.replace(r'\ex{43}'+'\nOn $x+y+z=1$',peak_graphs+r'\ex{43}'+'\nOn $x+y+z=1$')

sec = None
seen = []
out=[]
for line in source.splitlines():
    m=re.search(r'\\section\*\{(14\.[1-8]) ',line)
    if m: sec=m.group(1)
    out.append(line)
    m=re.fullmatch(r'\\ex\{(\d+)\}',line)
    if m:
        key=(sec,m.group(1)); seen.append(key)
        out.append(r'\textbf{Question.} '+summaries[key])
        out.append('')
        out.append(r'\textbf{Worked solution.}' if key not in [('14.3','104'),('14.8','17'),('14.8','19'),('14.8','21')] else r'\textbf{Status.}')
assert len(seen)==len(set(seen))
manifest=json.loads((vault/'assignment_manifest.json').read_text())['sections']
expected=[]
for s,spec in manifest.items():
    if not s.startswith('14.'):continue
    for part in spec.split(','):
        nums=list(map(int,re.findall(r'\d+',part)))
        values=range(nums[0],nums[1]+1) if len(nums)==2 else nums
        expected += [(s,str(n)) for n in values if 'odd' not in part or n%2]
assert set(expected)==set(seen), (set(expected)-set(seen),set(seen)-set(expected))
dest=vault/'Multi Chapter 14'/'Chapter_14_Solutions.tex'
dest.parent.mkdir(exist_ok=True)
dest.write_text('\n'.join(out)+'\n',encoding='utf-8')
print(f'Wrote {dest}; {len(seen)} assigned entries, {len(seen)-4} worked solutions and 4 source-needed entries.')
