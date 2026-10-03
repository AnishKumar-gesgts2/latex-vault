from pathlib import Path
import re,json
root=Path(r'C:/Users/notso/Documents/Latex Vault')
p=root/'Multi Chapter 14/Chapter_14_Solutions.tex'
s=p.read_text(encoding='utf-8')
new=r'''\ex{89}
\textbf{Question.} A bird's power requirement during flapping flight is modeled by
\[P(v,x,m)=Av^3+\frac{B(mg/x)^2}{v},\]
where $A,B$ are positive constants for the species, $g$ is gravitational acceleration, $v>0$ is speed, $m>0$ is mass, and $0<x\le1$ is the fraction of flight time spent flapping. Find $P_v,P_x,P_m$ and interpret them.

\textbf{Worked solution.}
First rewrite the second term so the powers of each variable are explicit:
\[P=Av^3+Bg^2m^2x^{-2}v^{-1}.\]
Hold the other two variables fixed in each derivative. The power rule gives
\begin{align*}
P_v&=3Av^2-Bg^2m^2x^{-2}v^{-2}
     =\ans{3Av^2-\frac{Bm^2g^2}{x^2v^2}},\\
P_x&=Bg^2m^2v^{-1}(-2x^{-3})
     =\ans{-\frac{2Bm^2g^2}{vx^3}},\\
P_m&=Bg^2x^{-2}v^{-1}(2m)
     =\ans{\frac{2Bmg^2}{vx^2}}.
\end{align*}
Here $P_v$ measures the change in required power per change in speed, at fixed mass and flapping fraction. Its sign depends on $v$: the $Av^3$ contribution increases with speed, while the inverse-speed contribution decreases. In fact, $P_v=0$ at
\[v=\left(\frac{Bm^2g^2}{3Ax^2}\right)^{1/4};\]
below this speed $P_v<0$, and above it $P_v>0$.
Since $P_x<0$, increasing the flapping fraction decreases the modeled power needed during flapping, with $v,m$ fixed. Since $P_m>0$, a heavier bird needs more modeled power, with $v,x$ fixed. For a small change in a single variable, the power change is approximately the corresponding partial derivative times that change.

\ex{97}
\textbf{Question.} Assuming the third-order partial derivatives are continuous, use Clairaut's Theorem to prove $f_{xyy}=f_{yxy}=f_{yyx}$.

\textbf{Worked solution.}
The subscript order means $f_{xyy}=\partial_y(\partial_y(\partial_x f))$. Clairaut's Theorem permits interchanging two successive differentiation variables when the relevant mixed partials are continuous.

First, $f_{xy}=f_{yx}$. Differentiate this equality with respect to $y$:
\[\partial_y f_{xy}=\partial_y f_{yx}
\quad\Longrightarrow\quad f_{xyy}=f_{yxy}.\]
Next apply Clairaut's Theorem to the function $h=f_y$. Its mixed second derivatives are
\[h_{xy}=f_{yxy},\qquad h_{yx}=f_{yyx}.\]
They are continuous by the stated assumption, so $h_{xy}=h_{yx}$. Combining the two equalities gives
\[\ans{f_{xyy}=f_{yxy}=f_{yyx}}.\]
All three expressions differentiate once in $x$ and twice in $y$; continuity is what allows the order to be changed.

\ex{99}
\textbf{Question.} For $f(x,y)=x(x^2+y^2)^{-3/2}e^{\sin(x^2y)}$, find $f_x(1,0)$ using the partial-derivative definition rather than expanding the general derivative.

\textbf{Worked solution.}
When finding the $x$ partial at $(1,0)$, keep $y=0$. The exponential becomes $e^{\sin0}=1$, and near $x=1$ we have $x>0$, so
\[f(x,0)=x(x^2)^{-3/2}=\frac{x}{x^3}=\frac1{x^2},
\qquad f(1,0)=1.\]
Thus the required limit is a one-variable difference quotient:
\begin{align*}
f_x(1,0)
&=\lim_{h\to0}\frac{f(1+h,0)-f(1,0)}{h}\\
&=\lim_{h\to0}\frac{(1+h)^{-2}-1}{h}\\
&=\lim_{h\to0}\frac{1-(1+h)^2}{h(1+h)^2}
=\lim_{h\to0}\frac{-2-h}{(1+h)^2}
=\ans{-2}.
\end{align*}
The simplification $x(x^2)^{-3/2}=x^{-2}$ is used only near the positive point $x=1$.

\ex{101}
\textbf{Question.} Let
\[f(x,y)=\begin{cases}
\dfrac{x^3y-xy^3}{x^2+y^2},&(x,y)\ne(0,0),\\[0.4em]
0,&(x,y)=(0,0).
\end{cases}\]
(a) Graph $f$. (b) Find $f_x,f_y$ away from the origin. (c) Find them at the origin by their definitions. (d) Show that $f_{xy}(0,0)=-1$ and $f_{yx}(0,0)=1$. (e) Explain why this does not contradict Clairaut's Theorem, using graphs of the mixed partials.

\textbf{Worked solution.}
\textbf{(a) Surface and behavior at the origin.} Write $x=r\cos\theta$, $y=r\sin\theta$. Then, for $r>0$,
\[f=\frac{xy(x^2-y^2)}{x^2+y^2}
=r^2\cos\theta\sin\theta(\cos^2\theta-\sin^2\theta)
=\frac{r^2}{4}\sin(4\theta).\]
Thus the sign alternates in the eight sectors separated by $x=0$, $y=0$, and $y=\pm x$. Also $|f|\le r^2/4\to0$, so the assigned value $f(0,0)=0$ makes the surface continuous at the origin.
\begin{center}\begin{tikzpicture}\begin{axis}[domain=-1.5:1.5,y domain=-1.5:1.5,title={Surface $z=f(x,y)$}]
\addplot3[surf,shader=interp,samples=26,samples y=26,opacity=.8]{(x^3*y-x*y^3)/(x^2+y^2)};
\addplot3[only marks,mark=*,black] coordinates {(0,0,0)};
\end{axis}\end{tikzpicture}\end{center}
The even number of grid samples avoids division by zero in the surface plot; the black point separately marks the defined value at the origin.

\textbf{(b) First partials away from the origin.} Put $N=x^3y-xy^3$ and $S=x^2+y^2>0$. Then
\[N_x=3x^2y-y^3,\quad N_y=x^3-3xy^2,\quad S_x=2x,\quad S_y=2y.\]
Apply the quotient rule and collect like terms:
\begin{align*}
f_x&=\frac{(3x^2y-y^3)S-2xN}{S^2}
=\ans{\frac{x^4y+4x^2y^3-y^5}{(x^2+y^2)^2}},\\
f_y&=\frac{(x^3-3xy^2)S-2yN}{S^2}
=\ans{\frac{x^5-4x^3y^2-xy^4}{(x^2+y^2)^2}}.
\end{align*}

\textbf{(c) First partials at the origin.} On either coordinate axis the numerator of $f$ is zero. Therefore $f(h,0)=f(0,h)=0$, and
\[f_x(0,0)=\lim_{h\to0}\frac{f(h,0)-f(0,0)}h=\ans{0},\]
\[f_y(0,0)=\lim_{h\to0}\frac{f(0,h)-f(0,0)}h=\ans{0}.\]

\textbf{(d) Mixed partials at the origin.} To find $f_{xy}$, differentiate $f_x$ in $y$. From part (b), for $h\ne0$,
\[f_x(0,h)=\frac{-h^5}{h^4}=-h.\]
Together with $f_x(0,0)=0$, this gives
\[f_{xy}(0,0)=\lim_{h\to0}\frac{f_x(0,h)-f_x(0,0)}h
=\lim_{h\to0}\frac{-h}{h}=\ans{-1}.\]
For the other order, part (b) gives $f_y(h,0)=h^5/h^4=h$. Hence
\[f_{yx}(0,0)=\lim_{h\to0}\frac{f_y(h,0)-f_y(0,0)}h
=\lim_{h\to0}\frac{h}{h}=\ans{1}.\]

\textbf{(e) Continuity is the missing hypothesis.} Away from the origin, $f$ is a quotient with a nonzero denominator and is smooth, so its mixed partials agree. For example, differentiating the numerator of $f_x$ in $y$ gives $x^4+12x^2y^2-5y^4$, and the quotient rule gives
\begin{align*}
f_{xy}&=\frac{(x^4+12x^2y^2-5y^4)S-4y(x^4y+4x^2y^3-y^5)}{S^3}\\
&=\frac{x^6+9x^4y^2-9x^2y^4-y^6}{(x^2+y^2)^3}
=f_{yx},\qquad (x,y)\ne(0,0).
\end{align*}
Along the $x$ axis this common expression is $1$; along the $y$ axis it is $-1$. It has no limit at the origin. Consequently neither mixed partial is continuous there, and Clairaut's continuity hypothesis is not satisfied. Their unequal values at $(0,0)$ do not contradict the theorem.

The two graphs below have the same surface off the origin but different assigned center values. In polar coordinates their common off-origin height is
\[\cos(2\theta)\bigl(1+2\sin^2(2\theta)\bigr),\]
which depends on angle, not on radius. The directional height differences persist as the radius shrinks. A small hole leaves the origin visible; the red point is its actual assigned value.
\begin{center}\begin{tikzpicture}\begin{axis}[domain=0:360,y domain=.06:1.5,title={$f_{xy}$: center value $-1$},zmin=-2,zmax=2]
\addplot3[surf,shader=interp,samples=65,samples y=18,opacity=.7] ({y*cos(x)},{y*sin(x)},{cos(2*x)*(1+2*sin(2*x)^2)});
\addplot3[only marks,mark=*,mark size=2pt,red] coordinates {(0,0,-1)};
\end{axis}\end{tikzpicture}\end{center}
\begin{center}\begin{tikzpicture}\begin{axis}[domain=0:360,y domain=.06:1.5,title={$f_{yx}$: center value $1$},zmin=-2,zmax=2]
\addplot3[surf,shader=interp,samples=65,samples y=18,opacity=.7] ({y*cos(x)},{y*sin(x)},{cos(2*x)*(1+2*sin(2*x)^2)});
\addplot3[only marks,mark=*,mark size=2pt,red] coordinates {(0,0,1)};
\end{axis}\end{tikzpicture}\end{center}
'''
s=re.sub(r'\\ex\{88\}.*?(?=\\clearpage\\section\*\{14\.4)',lambda m:new,s,flags=re.S)
old='At your request, four inaccessible assigned entries are skipped: 14.3 \\#104 (this section ends at \\#101) and 14.8 \\#17, \\#19, \\#21 (they refer to Section 4.7 \\#3, \\#7, \\#25 outside this volume). This file contains the other 103 assigned exercises; add the skipped items after receiving the updated assignment.'
replacement='This file follows the updated assignment manifest and contains 106 worked exercises. As previously requested, three inaccessible entries remain skipped: 14.8 \\#17, \\#19, \\#21, which refer to Section 4.7 \\#3, \\#7, \\#25 outside this volume. Section 14.3 now includes \\#89, \\#97, \\#99, and \\#101; \\#88 and \\#104 are no longer assigned.'
assert old in s
s=s.replace(old,replacement)
manifest=json.loads((root/'assignment_manifest.json').read_text())['sections']
expected=set()
for section,spec in manifest.items():
    if not section.startswith('14.'):continue
    for part in spec.split(','):
        nums=list(map(int,re.findall(r'\d+',part)))
        values=range(nums[0],nums[1]+1) if len(nums)==2 else nums
        expected.update((section,n) for n in values if 'odd' not in part or n%2)
actual=[]; section=None
for line in s.splitlines():
    m=re.search(r'\\section\*\{(14\.[1-8]) ',line)
    if m:section=m.group(1)
    m=re.fullmatch(r'\\ex\{(\d+)\}',line)
    if m:actual.append((section,int(m.group(1))))
skipped={('14.8',17),('14.8',19),('14.8',21)}
assert set(actual)==expected-skipped
assert len(actual)==len(set(actual))==106
p.write_text(s,encoding='utf-8')
print('Verified 106 unique solved exercises against manifest; only the three previously skipped 14.8 cross-references remain.')
