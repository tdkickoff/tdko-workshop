import json, sys, pickle, random, re, unicodedata
sys.path.insert(0,'/tmp/claude-0/ttt')
from players import parse, CLUBS_LEAGUE
P=parse()
plan,days=pickle.load(open('plan_w1.pkl','rb')); days=[set(d) for d in days]
src=open('/tmp/claude-0/ttt/gen.py').read()
grid_src=src[src.index('# ---------- Tiki-Taka-Toe grids'):src.index('random.seed(5)')]
ident=lambda p:{'Ronaldo Nazário':'Ronaldo'}.get(p,p)
exec(grid_src)
old=json.load(open('/tmp/claude-0/ttt/puzzles.json'))['grids']
oldkeys=[(frozenset(map(tuple,g['r'])),frozenset(map(tuple,g['c']))) for g in old]
random.seed(1511)
grids=[]; attempts=0
while len(grids)<7 and attempts<300000:
    attempts+=1; d=len(grids)
    nat_mode = d in (2,5)
    rows=[('nat',x) for x in random.sample(ROWS_NAT,3)] if nat_mode else [('club',x) for x in random.sample(ROWS_CLUB,3)]
    cols=random.sample(COLS_FOR_NAT if nat_mode else COLS_FOR_CLUB,3)
    if sum(1 for c in cols if c[0]=='league')>1: continue
    if ('league','ITA') in cols and any(r[1] in CLUBS_LEAGUE['ITA'] for r in rows): continue
    key=frozenset(rows); ck=frozenset(cols)
    allg=[(frozenset(map(tuple,g['r'])),frozenset(map(tuple,g['c']))) for g in grids]+oldkeys
    if any(len(key&r)>=2 and len(ck&c)>=2 for r,c in allg): continue
    if any(len(key&r)>=2 for r,c in allg[:len(grids)][-3:]): continue
    cells=[answers(r,c) for r in rows for c in cols]
    if min(len(x) for x in cells)<3: continue
    ex=matching(cells,days[d])
    if not ex: continue
    grids.append({'r':[list(x) for x in rows],'c':[list(x) for x in cols],'rl':[label(x) for x in rows],'cl':[label(x) for x in cols],'ex':ex,'sizes':[len(x) for x in cells]})
print('grids',len(grids),'attempts',attempts)
for i,g in enumerate(grids): print(15+i,g['rl'],'x',g['cl'],g['sizes'],g['ex'])
json.dump(grids,open('tiki_w1.json','w'),ensure_ascii=False)
