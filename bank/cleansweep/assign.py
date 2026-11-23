import sys,json,itertools
sys.path.insert(0,'/home/claude/bank/final')
import clash as C
from pool import POOL
def norm(s): return C.n(s)
def day_people(d):
    s=set()
    for k,ps in C.day_items(d): s|={norm(p) for p in ps}
    return s
def keyset(n):
    f=norm(n); w=f.split(); return {f}|({w[-1]} if len(w)>1 and len(w[-1])>=4 else set())
DP={d:day_people(d) for d in range(28)}
def lsnames(L): return [x['n'] for x in L['names']]
def hits(L,d):
    out=[]
    for n in lsnames(L):
        f=norm(n)
        if f in DP[d] or (n=='Ronaldo' and 'ronaldo nazario' in DP[d]): out.append(n)
        else:
            # surname match against full names in the day (e.g. 'Kane' vs 'Harry Kane')
            last=f.split()[-1]
            if len(f.split())>1 and any(p.split()[-1]==last and p.split()[0]==f.split()[0] for p in DP[d]): out.append(n)
    return out
if __name__=='__main__':
    days=range(7,28)
    M={L['id']:{d+1:hits(L,d) for d in days} for L in POOL}
    for L in POOL:
        ok=[d for d in M[L['id']] if not M[L['id']][d]]
        print(f"{L['id']:28} {L['diff']:6} ok days: {ok}")
    json.dump(M,open('clashmatrix.json','w'),ensure_ascii=False,indent=0)
