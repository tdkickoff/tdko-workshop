import re, sys, itertools, random
from collections import Counter
words=set()
for line in open('/usr/share/hunspell/en_US.dic',encoding='utf-8',errors='ignore'):
    w=line.split('/')[0].strip()
    if re.fullmatch(r'[a-z]{3,8}',w): words.add(w)
common=[w for w in words]
def find(name, n=12, seed=0):
    target=Counter(re.sub(r'[^a-z]','',name.lower()))
    cand=[w for w in common if not (Counter(w)-target)]
    cand.sort(key=lambda w:-len(w))
    random.seed(seed); out=[]
    def rec(rem, parts, start):
        if len(out)>=n: return
        if not rem:
            out.append(' '.join(p.capitalize() for p in parts)); return
        if len(parts)>=3: return
        for i in range(start,len(cand)):
            w=cand[i]
            if not (Counter(w)-rem): rec(rem-Counter(w), parts+[w], i)
            if len(out)>=n: return
    rec(target,[],0)
    return out
for nm in sys.argv[1:]:
    print(nm, '->', find(nm, 15))
