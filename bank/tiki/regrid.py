import json,sys
sys.path.insert(0,'/home/claude/bank/tiki'); sys.path.insert(0,'/home/claude/bank/final')
from check_grids import P, fits
import clash
W=clash.W; T=W['tiki']
LAB={'hon':{'C':'Won the Champions League','W':'Won the World Cup','B':"Won the Ballon d'Or",'G':'Premier League Golden Boot'},'league':{'MLS':'Played in MLS','ITA':'Played in Serie A','SAU':'Played in the Saudi Pro League'}}
lab=lambda c: LAB[c[0]][c[1]] if c[0] in LAB else c[1]
CH={4:('r',2,('club','Real Madrid')),5:('c',2,('hon','W')),8:('c',2,('hon','W')),11:('r',1,('club','AC Milan')),18:('c',1,('hon','W')),
    22:('c',0,('hon','W')),23:('r',2,('club','Barcelona')),26:('c',1,('hon','W')),28:('r',2,('club','Chelsea')),
    19:[('r',1,('club','Chelsea')),('c',1,('hon','W'))],21:[('r',1,('club','Bayern Munich')),('c',2,('hon','C'))]}
for d,ch in CH.items():
    g=T[d-1]
    for side,i,c in (ch if isinstance(ch,list) else [ch]): g[side][i]=list(c)
RANK={p['name']:(1 if p.get('partial') else 0, k) for k,p in enumerate(P)}
for d in range(3,29):
    g=T[d-1]; g['rl']=[lab(c) for c in g['r']]; g['cl']=[lab(c) for c in g['c']]
    others=set()
    for k,s in clash.day_items(d-1):
        if k!='tiki': others|=s
    cells=[(r,c) for r in g['r'] for c in g['c']]
    C=[sorted([p['name'] for p in P if fits(p,r,c) and not any(clash.same(p['name'],o) for o in others)],key=lambda n:RANK[n])[:25] for r,c in cells]
    order=sorted(range(9),key=lambda k:len(C[k])); best=[None,None]
    def dfs(i,used,cost,asg):
        if best[0] is not None and cost>=best[0]: return
        if i==9: best[0]=cost; best[1]=dict(asg); return
        k=order[i]
        for n in C[k]:
            if n in used: continue
            asg[k]=n; dfs(i+1,used|{n},cost+RANK[n][0]*1000+RANK[n][1],asg)
    dfs(0,frozenset(),0,{})
    if best[1] is None: print('NO ASSIGNMENT',d,[len(x) for x in C]); ex=['?']*9
    else: ex=[best[1][k] for k in range(9)]
    g['ex']=ex
json.dump(W,open('/home/claude/bank/final/final28.json','w'),ensure_ascii=False,indent=1)
for d in range(3,29): print(d,T[d-1]['rl'],T[d-1]['cl'],T[d-1]['ex'])
