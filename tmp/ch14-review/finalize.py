from pathlib import Path
import re
p=Path(r'C:/Users/notso/Documents/Latex Vault/Multi Chapter 14/Chapter_14_Solutions.tex')
s=p.read_text()
s=s.replace('Four assigned entries need an additional source: 14.3 \\#104 and 14.8 \\#17, \\#19, \\#21. Their missing prompts are explained at their assigned locations.', 'At your request, four inaccessible assigned entries are skipped: 14.3 \\#104 (this section ends at \\#101) and 14.8 \\#17, \\#19, \\#21 (they refer to Section 4.7 \\#3, \\#7, \\#25 outside this volume). This file contains the other 103 assigned exercises; add the skipped items after receiving the updated assignment.')
s=re.sub(r'\\ex\{104\}.*?(?=\\clearpage)', '', s, flags=re.S)
start=s.index(r'\section*{14.8')
tail=re.sub(r'\\ex\{(?:17|19|21)\}.*?(?=\\ex\{|\\end\{document\})','',s[start:],flags=re.S)
p.write_text(s[:start]+tail,encoding='utf-8')
print('Saved 103 solved entries; four inaccessible entries skipped.')
