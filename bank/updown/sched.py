import json,re,sys
from scipy.optimize import linear_sum_assignment
sys.path.insert(0,'/home/claude/bank/topfour')
exec(open('/home/claude/bank/topfour/schedule.py').read().split("C=[[")[0])   # gives days[] text for the 8 older games
g=json.load(open('gen.json'))
g['eng-caps-2']={'chain':[["Steven Gerrard",114],["Gary Neville",85],["Alan Shearer",63],["John Barnes",79],["Kenny Sansom",86],["John Terry",78]]}
from pools import P
theme={k:P[k][0] for k in P}; theme['eng-caps-2']="England caps"; unit={k:P[k][1] for k in P}; unit['eng-caps-2']='caps'
ids=[k for k in g if k!='sco-caps']
tf=json.load(open('/home/claude/bank/topfour/daily.json'))   # Top Four by day index
fam=lambda s: {'pl-goals':'plg','cult-pl-goals':'plg','eng-caps':'engc','eng-caps-2':'engc','eng-goals':'engg','pl-apps':'pla','arsenal-goals':'ars','mufc-apps':'mu','chelsea-goals':'che','liverpool-goals':'lfc','lfc-apps':'lfc'}.get(s,s)
def clash(cid,d):
    t=days[d]+' '+' '.join(n for n,v in tf[d]['items'])
    return [n for n,v in g[cid]['chain'] if re.search(r'\b'+re.escape(re.sub(r' \(.*\)','',n).split()[-1])+r'\b',t)]
Cm=[[len(clash(c,d))+(10 if fam(c)==fam(tf[d]['id']) else 0) for d in range(14)] for c in ids]
r,c=linear_sum_assignment(Cm); order=[None]*14
for ci,d in zip(r,c): order[d]=ids[ci]
tot=0
for d,cid in enumerate(order):
    cl=clash(cid,d); tot+=len(cl); print(d+1,cid.ljust(14),'TopFour:',tf[d]['id'].ljust(16),cl)
print('total',tot)
def pack(cid): return {'id':cid,'theme':theme[cid],'unit':unit[cid],'chain':g[cid]['chain']}
json.dump([pack(c) for c in order],open('daily.json','w'),ensure_ascii=False)
json.dump(pack('sco-caps'),open('test.json','w'),ensure_ascii=False)
