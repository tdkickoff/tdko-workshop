import json,re,sys,random
sys.path.insert(0,'/home/claude/bank/updown')
from pools import P
src=open('/home/claude/bank/topfour/schedule.py').read().split("C=[[")[0]
_ns={}; exec(src,_ns); days=_ns['days']
tf=json.load(open('/home/claude/bank/topfour/daily.json'))
fam=lambda s: {'pl-goals':'plg','cult-pl-goals':'plg','eng-caps':'engc','eng-caps-2':'engc','eng-goals':'engg','pl-apps':'pla','arsenal-goals':'ars','mufc-apps':'mu','chelsea-goals':'che','liverpool-goals':'lfc','lfc-apps':'lfc'}.get(s,s)
def dtext(d): return days[d]+' '+' '.join(x for x,y in tf[d]['items'])
def hits(names,d): t=dtext(d); return [n for n in names if re.search(r'\b'+re.escape(re.sub(r' \(.*\)','',n).split()[-1])+r'\b',t)]
def ok(a,b,k):
    if a==b: return False
    g=abs(b-a)/a*100; lo,hi=(20,30) if k<=3 else (5,10.5); return lo<=g<=hi
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
    rec([]); order={n:j for j,n in enumerate(pool)}; res.sort(key=lambda c: sum(order[n] for n in c)); return res[0] if res else None
