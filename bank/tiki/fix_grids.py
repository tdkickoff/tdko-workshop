import json, itertools, sys
sys.path.insert(0,'.')
from check_grids import P, T, fits
CLUBS=['Barcelona','Real Madrid','Bayern Munich','Juventus','AC Milan','Inter','Chelsea','Arsenal','Liverpool','Manchester United','Manchester City','Tottenham','Paris Saint-Germain']
NATS=['England','France','Brazil','Argentina','Germany','Netherlands','Spain','Italy']
POOL=[('club',c) for c in CLUBS]+[('hon',h) for h in 'CWBG']+[('nat',n) for n in NATS]+[('league',l) for l in ('MLS','ITA')]
def counts(rows,cols): return [sum(1 for p in P if fits(p,r,c)) for r in rows for c in cols]
def opts(g, mn=3):
    rows=[tuple(x) for x in g['r']]; cols=[tuple(x) for x in g['c']]; res=[]
    for side in ('r','c'):
        cur=rows if side=='r' else cols
        for i in range(3):
            for cand in POOL:
                if cand in rows or cand in cols: continue
                if cand[0]!=cur[i][0]: continue   # same kind keeps the grid's style
                new=cur[:]; new[i]=cand
                cs=counts(new,cols) if side=='r' else counts(rows,new)
                if min(cs)>=mn: res.append((min(cs),side,i,cur[i],cand,cs))
    return sorted(res,key=lambda x:-x[0])
if __name__=='__main__':
    for d in map(int,sys.argv[1:]):
        g=T[d-1]; o=opts(g)
        print(d,[x[1] for x in g['r']],[x[1] for x in g['c']])
        for x in o[:8]: print('   ',x)
