import random, itertools, json, sys
sys.path.insert(0,'.'); from pools import P
def ok(a,b,k):
    if a==b: return False
    g=abs(b-a)/a*100; lo,hi=(20,30) if k<=3 else (5,10.5)
    return lo<=g<=hi
def chains(pool, first_up, seed):
    names=list(pool); random.seed(seed); res=[]
    def rec(ch):
        if len(res)>=200: return
        k=len(ch)
        if k==6:
            dirs=[pool[ch[i]]>pool[ch[i-1]] for i in range(1,6)]
            if dirs[0]!=first_up: return
            if sum(dirs) in (0,5) or sum(dirs) in (1,4) and random.random()<0.5: return   # mix ups and downs
            res.append(list(ch)); return
        cand=[n for n in names if n not in ch and (k==0 or ok(pool[ch[-1]],pool[n],k))]
        random.shuffle(cand)
        for n in cand: rec(ch+[n])
    rec([]); return res
out={}
ids=list(P)
for i,pid in enumerate(ids):
    first_up = (i%2==0)
    for fu in (first_up, not first_up):
        r=chains(P[pid][2], fu, 7+i)
        if r: 
            # prefer chains that start with a well-known name: earlier in pool order = more famous-ish; pick max fame score
            pool=P[pid][2]; order={n:j for j,n in enumerate(pool)}
            r.sort(key=lambda c: sum(order[n] for n in c))
            out[pid]={'first_up':fu,'chain':[[n,pool[n]] for n in r[0]]}; break
    else: out[pid]=None
for pid,v in out.items():
    if not v: print(pid,'NONE'); continue
    ch=v['chain']; s=[]
    for k in range(1,6):
        a,b=ch[k-1][1],ch[k][1]; s.append(f"{'↑' if b>a else '↓'}{abs(b-a)/a*100:.1f}")
    print(pid.ljust(14), ' → '.join(f"{n} {x}" for n,x in ch)); print(' '*14,' '.join(s))
json.dump(out,open('gen.json','w'),ensure_ascii=False)
