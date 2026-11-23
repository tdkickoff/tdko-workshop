"""Builds the review rows: one per puzzle (Fast Break: one per question)."""
import json,pickle,sys,datetime
sys.path.insert(0,'/home/claude/bank')
import week1
from fb_week1 import FB
cur=json.load(open('/home/claude/bank/sheet/current.json'))
plan,_=pickle.load(open('/home/claude/bank/plan_w1.pkl','rb'))
tiki_w1=json.load(open('/home/claude/bank/tiki_w1.json'))
LEV={'e':'Easy','m':'Medium','h':'Hard'}
TYP={'club':'Club','intl':'Country','swap':'Transfer swap','boss':'Manager','family':'Family','youth':'Boyhood club'}
def date(n): d=datetime.date(2026,11,16)+datetime.timedelta(days=n-1); return d.strftime('%a %-d %b')
rows=[]
def add(n,game,q,a,det): rows.append([n,date(n),game,q,a,det])

def fb_rows(n,qs):  # qs: list of (question, options, level)
    for i,(q,o,l) in enumerate(qs,1): add(n,'Fast Break',f'Q{i}. {q}',o[0],f'Wrong options: {", ".join(o[1:])} · {LEV[l]}')
def wtb_row(n,p):
    clubs='; '.join(f'{c} {a} apps/{g} goals' for c,a,g in p['clubs'])
    add(n,"Who's That Baller",f"Mystery player ({p['position']})",p['name'],
        f"{p['nationality']} · youth: {p['youth']} · first 3 clubs: {clubs} · {p['caps']} caps/{p['capGoals']} goals · career league {p['apps']} apps/{p['goals']} goals · honour: {p['honour'][0]} ({p['honour'][1]}) · award: {p['award'][0]} ({p['award'][1]})")
def mix_row(n,p):
    add(n,'In The Mixer',f"Anagram: {p['phrase']}",p['name'],f"Hints: {' | '.join(p['hints'])} · Reveal: {p['blurb']}")
def link_row(n,c):
    if isinstance(c['start'],dict):   # live format
        st=c['start']['p'][0]; clubs=c['start']['clubs']; links=[(l['p'][0],l['t'],l['x']) for l in c['links']]
    else:
        st=c['start'][0]; clubs=c['clubs']; links=[(l[0][0],l[1],l[2]) for l in c['links']]
    add(n,'Link Up Play',f"Start: {st} ({clubs})",' → '.join([st]+[x[0] for x in links]),' | '.join(f"{p}: {TYP.get(t,t)}, {x}" for p,t,x in links))
def squad_row(n,x):
    names=[p for r in x['rows'] for p in r]
    add(n,'Squad Goals',f"{x['team']} · {x['comp']} {x['year']}",', '.join(p[0] for p in names),f"Captain: {x['cap']} · positions: "+', '.join(f'{p[0]} ({p[1]}, {p[2]})' for p in names))
def ss_row(n,a):
    def sur(full): return full.split()[-1].upper()
    a={str(k):v for k,v in a.items()}
    add(n,'Shirt Swap','Three shirts: 5, 6 and 7 letters',' / '.join(sur(a[k]) for k in '567'),' / '.join(a[k] for k in '567'))
def tiki_row(n,g):
    ex=g['ex']; cells=[f"{g['rl'][r]} × {g['cl'][c]}: {ex[r*3+c]}" for r in range(3) for c in range(3)]
    add(n,'Tiki-Taka-Toe',f"Rows: {', '.join(g['rl'])} · Columns: {', '.join(g['cl'])}",'Any player who fits each square',' | '.join(cells))
def off_row(n,P,eight=None,odd=None):
    eight=eight or P['eight']; odd=odd or P['odd']
    k=P['kind']
    if k=='club': link=f"Played for {P['a']}"; rev=f"{odd} played for {P['b']} and never for {P['a']}."
    elif k=='nation': link=f"Played for {P['a']}"; rev=f"{odd} played for {P['b']}." + (' '+P['note'] if P.get('note') else '')
    elif k=='text': link=P['head']; rev=P['body_odd'].replace('{odd}',odd)
    else: link=P['x'][0].upper()+P['x'][1:]; rev=f"{odd} {P['nx']}."
    add(n,'Offside',f"Link: {link} · Line-up: {', '.join(eight)}, {odd}",odd,f"Reveal: {rev}")
def tf_row(n,q):
    add(n,'Top Four',f"{q['q']} ({q['top']} at the top)",' > '.join(i[0] for i in q['items']),', '.join(f'{a}: {b}' for a,b in q['items'])+(f" · {q['note']}" if q.get('note') else ''))
def rh_row(n,c):
    ch=c['chain']; calls=' '.join(('↑' if ch[k][1]>ch[k-1][1] else '↓') for k in range(1,6))
    add(n,'Ranked Highly',f"{c['theme']} · start: {ch[0][0]}",calls+'  ('+' → '.join(p[0] for p in ch[1:])+')',
        ' → '.join(f'{p[0]} {p[1]:,}' for p in ch)+f" ({c['unit']})")

# No. 1–14: what's in the games now
Q=cur['fb']['Q']; D=cur['fb']['DAYS']
for d in range(14):
    n=d+1
    fb_rows(n,[Q[i] for k in 'emh' for i in D[d][k]])
    wtb_row(n,cur['wtb'][d]); mix_row(n,cur['mix'][d]); link_row(n,cur['link'][d]); squad_row(n,cur['squad'][d])
    ss_row(n,cur['ss'][d]); tiki_row(n,cur['tiki'][d]); off_row(n,cur['off'][d]); tf_row(n,cur['tf'][d])
    if n>=8: rh_row(n,cur['rh'][d])
# No. 15–21: week 1 of the bank (Top Four and Ranked Highly come later)
for d in range(7):
    n=15+d
    fb_rows(n,[FB[i] for i in plan['fb'][d]])
    wtb_row(n,week1.WTB[plan['wtb'][d]]); mix_row(n,week1.MIXER[plan['mix'][d]]); link_row(n,week1.LINK[plan['link'][d]]); squad_row(n,week1.SQUAD[plan['squad'][d]])
    ss_row(n,plan['ss'][d]); tiki_row(n,tiki_w1[d])
    oi,eight,odd=plan['off'][d]; off_row(n,week1.OFFSIDE[oi],eight,odd)
    rh_row(n,cur['rh'][d])     # Ranked Highly opens on No. 8, so No. 15–21 can use chains 1–7, which the public never saw
ORDER=['Fast Break',"Who's That Baller",'In The Mixer','Link Up Play','Squad Goals','Shirt Swap','Tiki-Taka-Toe','Offside','Top Four','Ranked Highly']
rows.sort(key=lambda r:(r[0],ORDER.index(r[2])))
json.dump(rows,open('/home/claude/bank/sheet/rows_1_21.json','w'),ensure_ascii=False)
from collections import Counter
print(len(rows)); print(Counter(r[2] for r in rows))
for r in rows[:2]+[x for x in rows if x[2]!='Fast Break'][:10]: print(r)
