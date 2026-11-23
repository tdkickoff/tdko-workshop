import json,re,sys,random
sys.path.insert(0,'.')
exec(open('sched.py').read().split("def pack")[0].replace("print(","(lambda *a,**k:None)("))
from gen import ok
dj=json.load(open('daily.json'))
def gen_ex(pool, first_up, excl, seed=1):
    names=[n for n in pool if n not in excl]; random.seed(seed); res=[]
    def rec(ch):
        if len(res)>=300: return
        k=len(ch)
        if k==6:
            dirs=[pool[ch[i]]>pool[ch[i-1]] for i in range(1,6)]
            if dirs[0]!=first_up or sum(dirs) in (0,5): return
            res.append(list(ch)); return
        cand=[n for n in names if n not in ch and (k==0 or ok(pool[ch[-1]],pool[n],k))]; random.shuffle(cand)
        for n in cand: rec(ch+[n])
    rec([]); 
    order={n:j for j,n in enumerate(pool)}; res.sort(key=lambda c: sum(order[n] for n in c)); return res[0] if res else None
for d,q in enumerate(dj):
    cl=clash(q['id'],d)
    if not cl: continue
    pool=P[q['id']][2]; fu=q['chain'][1][1]>q['chain'][0][1]
    excl=[n for n in pool if re.search(r'\b'+re.escape(re.sub(r' \(.*\)','',n).split()[-1])+r'\b',days[d]+' '+' '.join(n for n,v in tf[d]['items']))]
    new=gen_ex(pool,fu,set(excl)) or gen_ex(pool,not fu,set(excl))
    print(d+1,q['id'],'clash',cl,'->',new)
    if new: q['chain']=[[n,pool[n]] for n in new]
json.dump(dj,open('daily.json','w'),ensure_ascii=False)
# report
for d,q in enumerate(dj):
    ch=q['chain']; s=' '.join(f"{'↑' if ch[k][1]>ch[k-1][1] else '↓'}{abs(ch[k][1]-ch[k-1][1])/ch[k-1][1]*100:.0f}" for k in range(1,6))
    print(d+1,q['id'].ljust(14),s,'| clash:',clash(q['id'],d) if False else [n for n,v in ch if re.search(r'\b'+re.escape(re.sub(r' \(.*\)','',n).split()[-1])+r'\b',days[d]+' '+' '.join(x for x,y in tf[d]['items']))])
