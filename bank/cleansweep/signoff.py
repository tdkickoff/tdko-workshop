"""Rebuilds the Clean Sweep sign-off sheet: the live schedule (No. 8-28) plus the proposed next week (No. 29-35)."""
import re,json,datetime,html
from pool import POOL,POOL2
f='/tmp/claude-0/-home-claude/dc39d1a6-6cbf-5f53-97ab-04ac97cd342b/scratchpad/signoff/clean-sweep-signoff.html'
s=open(f).read(); E=html.escape
LS=json.load(open('lists.json')); ALL={L['id']:L for L in POOL+POOL2}
NEXT=json.load(open('next_week.json'))
date=lambda n:(datetime.date(2026,11,16)+datetime.timedelta(n-1)).strftime('%a %-d %b')
clock=lambda L:f"{L['secs']//60}:00"
def row(n,L): d=ALL[L['id']]['diff']; return f'<tr><td class="no">{n}</td><td>{date(n)}</td><td><a href="#n{n}">{E(L["q"])}</a></td><td class="num">{len(L["names"])}</td><td class="num">{clock(L)}</td><td><span class="d {d}">{d}</span></td></tr>'
def card(n,L,tag=''):
    d=ALL[L['id']]['diff']
    names=''.join(f'<li><span class="lab">{E(x["l"])}</span><span class="nm">{E(x["n"])}</span>{"<span class=al>also: "+E(", ".join(x["a"]))+"</span>" if x.get("a") else ""}</li>' for x in L['names'])
    return f'''<section class="list" id="n{n}"><header><span class="eyebrow">{tag}No. {n} · {date(n)} · {len(L["names"])} names · {clock(L)} · {d}</span><h3>{E(L["q"])}</h3><p class="note">{E(L["note"])}</p></header>
<ol>{names}</ol><p class="src"><b>Source</b> {E(ALL[L["id"]]["src"])}</p></section>'''
rows=''.join(row(n,LS[n-1]) for n in range(8,29))
nrows=''.join(row(int(n),ALL[i]) for n,i in NEXT.items())
cards=''.join(card(n,LS[n-1]) for n in range(8,29))
ncards=''.join(card(int(n),ALL[i],'Proposed · ') for n,i in NEXT.items())
s=re.sub(r'<tbody>.*?</tbody>','<tbody>'+rows+'</tbody>',s,count=1,flags=re.S)
s=s[:s.index('<h2>The lists</h2>')]+'<h2>The lists</h2>\n '+cards+'''
 <h2>Next week: No. 29 to 35 (proposed)</h2>
 <p class="lede">Seven new lists for Mon 14 to Sun 20 Dec, with more easy and medium days. The clash check against that week's other games runs once those puzzles are built.</p>
 <div class="tbl"><table><thead><tr><th>No.</th><th>Date</th><th>List</th><th>Names</th><th>Clock</th><th>Level</th></tr></thead><tbody>'''+nrows+'</tbody></table></div>\n '+ncards+'\n</div>'
s=re.sub(r'<li>Exactly 10, 15 or 20 names[^<]*</li>','<li>Exactly 10, 15 or 20 names. Clock: 3 minutes for 10, 4 for 15, 5 for 20.</li>',s)
open(f,'w').write(s)
print('sign-off rebuilt')
