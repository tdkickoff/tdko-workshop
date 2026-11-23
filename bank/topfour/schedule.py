import re,json,sys
sys.path.insert(0,'/home/claude/bank/topfour'); from questions import Q
from scipy.optimize import linear_sum_assignment
src={f:open('/home/claude/'+f+'.html').read() for f in ['one-touch','whos-that-baller','scramble-head','pass-and-connect','who-playedle','shirt-swap','tiki-taka-toe','offside']}
def arr(f,name):
    s=src[f]; i=s.index('const '+name+' = ')+len('const '+name+' = '); depth=0
    for j in range(i,len(s)):
        if s[j] in '[{': depth+=1
        elif s[j] in ']}':
            depth-=1
            if depth==0: return s[i:j+1]
def split_top(a):
    out=[];depth=0;start=1;q=None
    for j,c in enumerate(a):
        if q:
            if c==q and a[j-1]!='\\': q=None
            continue
        if c in '"\'`': q=c; continue
        if c in '[{': depth+=1
        elif c in ']}': depth-=1
        if c==',' and depth==1: out.append(a[start:j]); start=j+1
    out.append(a[start:-1]); return [x for x in out if x.strip()]
per={f:split_top(arr(f,n)) for f,n in [('whos-that-baller','PLAYERS'),('scramble-head','PUZZLES'),('pass-and-connect','CHAINS'),('who-playedle','XIS'),('shirt-swap','ANSWERS'),('tiki-taka-toe','GRIDS'),('offside','PUZZLES')]}
Qfb=json.loads(re.search(r'const Q = (\[.*?\]);\n',src['one-touch']).group(1)); D=json.loads(arr('one-touch','DAYS'))
days=[' '.join(per[f][d] for f in per)+' '+' '.join(Qfb[i][0]+' '+' '.join(Qfb[i][1]) for k in 'emh' for i in D[d][k]) for d in range(14)]
def clash(q,d): return [n for n,v in q['items'] if re.search(r'\b'+re.escape(n.split()[-1])+r'\b',days[d])]
C=[[len(clash(q,d)) for d in range(14)] for q in Q]
r,c=linear_sum_assignment(C)
order=[None]*14
for qi,d in zip(r,c): order[d]=int(qi)
tot=0
for d,qi in enumerate(order):
    cl=clash(Q[qi],d); tot+=len(cl); print(d+1,Q[qi]['id'],cl)
print('total',tot)
json.dump(order,open('/home/claude/bank/topfour/order.json','w'))
