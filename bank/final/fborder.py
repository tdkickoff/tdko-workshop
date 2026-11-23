import json,re,random,itertools
W=json.load(open('final28.json')); Q=W['fb']['Q']
def cat(q):
    s=q.lower()
    if 'nicknamed' in s or 'nickname' in s: return 'nickname'
    if 'hosted' in s or 'host ' in s or 'co-host' in s: return 'host'
    if re.search(r'home games|plays at|stadium|ground|play its home',s): return 'ground'
    if re.search(r'in which city',s): return 'city'
    if re.search(r'\b(join|joined|sold|signed|sign|leave|left|move|moved|loan|transfer|buy|bought)\b',s): return 'transfer'
    if re.search(r'\bmanag|coach|\bboss\b',s): return 'manager'
    if re.search(r'^(which|what) (country|nation|national team)|^in which country|play for\?',s): return 'country'
    if re.search(r'golden (boot|ball|glove)|ballon|player of the year|award',s): return 'award'
    if re.search(r'\bfinal\b',s): return 'final'
    if re.search(r'world cup',s): return 'worldcup'
    return 'other'
from collections import Counter
print(Counter(cat(q[0]) for q in Q).most_common())
def ok_pair(a,b):
    ca,cb=cat(Q[a][0]),cat(Q[b][0])
    return (ca!=cb or ca=='other') and Q[a][1][0]!=Q[b][1][0]

random.seed(42)
def greedy(groups,prev=None):
    order=[]
    for g in groups:
        rem=g[:]
        while rem:
            last=order[-1] if order else prev
            c=[i for i in rem if last is None or ok_pair(last,i)]
            if not c: return None
            # prefer the most common category left, to avoid getting stuck
            cnt=Counter(cat(Q[i][0]) for i in rem); cnt['other']=0
            m=max(cnt[cat(Q[i][0])] for i in c); c=[i for i in c if cnt[cat(Q[i][0])]==m]
            i=random.choice(c); order.append(i); rem.remove(i)
    return order
fails=[]
for d,D in enumerate(W['fb']['DAYS']):
    o=None
    for t in range(5000):
        o=greedy([D['e'],D['m'],D['h']])
        if o: break
    if not o: fails.append(d+1)
    D['o']=o
print('fails',fails)
json.dump(W,open('final28.json','w'),ensure_ascii=False)
