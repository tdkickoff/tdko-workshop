import json,pickle,sys,re,random
sys.path.insert(0,'/home/claude/bank/sheet'); sys.path.insert(0,'/home/claude/bank/week2'); sys.path.insert(0,'/home/claude/bank/updown')
src=open('/home/claude/bank/sheet/rows.py').read()
head=src.split('# No. 1–14')[0].replace("import week1\nfrom fb_week1 import FB\n","").replace("plan,_=pickle.load(open('/home/claude/bank/plan_w1.pkl','rb'))\ntiki_w1=json.load(open('/home/claude/bank/tiki_w1.json'))\n","")
exec(head)
import week2
FB2=[tuple(x) for x in json.load(open('fb_all.json'))]
plan,_=pickle.load(open('plan_w2.pkl','rb')); tiki=json.load(open('tiki_w2.json'))
for d in range(7):
    n=22+d
    fb_rows(n,[FB2[i] for i in plan['fb'][d]])
    wtb_row(n,week2.WTB[plan['wtb'][d]]); mix_row(n,week2.MIXER[plan['mix'][d]]); link_row(n,week2.LINK[plan['link'][d]]); squad_row(n,week2.SQUAD[plan['squad'][d]])
    ss_row(n,plan['ss'][d]); tiki_row(n,tiki[d])
    oi,eight,odd=plan['off'][d]; off_row(n,week2.OFFSIDE[oi],eight,odd)
base=list(rows)
# ---- Top Four No.15-28 and Ranked Highly No.22-28, scheduled clash-free
from tf2 import Q2,RP
from pools import P
from ud import ok,gen_ex
from scipy.optimize import linear_sum_assignment
old=json.load(open('/home/claude/bank/sheet/rows_1_21.json'))
txt={n:' '.join(' '.join(map(str,r[3:6])) for r in old+base if r[0]==n) for n in range(15,29)}
def sur(n): return re.sub(r' \(.*\)|^Man City|^Liverpool \d|^Chelsea \d|^Arsenal \d','',n).split()[-1] if n.split()[-1][0].isalpha() else ''
def clash(names,n): return [x for x in names if len(x)>3 and re.search(r'\b'+re.escape(x.split()[-1])+r'\b',txt[n])]
NATIONS={'Spain','Germany','France','Denmark','Argentina','Uruguay','Brazil','Chile'}
names=lambda q:[a for a,b in q['items'] if not re.search(r'\d',a) and a not in NATIONS]
C=[[len(clash(names(q),n))*10 for n in range(15,29)] for q in Q2]
r,c=linear_sum_assignment(C); tforder=[None]*14
for qi,d in zip(r,c): tforder[d]=int(qi)
for d,qi in enumerate(tforder):
    n=15+d; q=Q2[qi]; print('TF',n,q['id'],clash(names(q),n)); txt[n]+=' '+' '.join(names(q))
# Ranked Highly: build a chain per theme per day avoiding that day's names, then assign
pools={k:(P[k] if v is None else P[v] if isinstance(v,str) else v) for k,v in RP.items()}
cur=json.load(open('/home/claude/bank/sheet/current.json'))
last_up=cur['rh'][6]['chain'][1][1]>cur['rh'][6]['chain'][0][1]
themes=list(pools); RC=[];CH={}
for ti,t in enumerate(themes):
    row=[]
    for d in range(7):
        n=22+d; up=(not last_up) if d%2==0 else last_up
        pool=pools[t][2]; excl={x for x in pool if clash([x],n)}
        ch=gen_ex(pool,up,excl,seed=7)
        CH[(t,d)]=ch; row.append((0 if ch else 99)+(5 if t.endswith(('-2','-3')) else 0))
    RC.append(row)
print(themes);[print(x) for x in RC]
r,c=linear_sum_assignment(RC); rhorder=[None]*7
for ti,d in zip(r,c): rhorder[d]=themes[ti]
RH=[]
for d,t in enumerate(rhorder):
    ch=CH[(t,d)]; th,unit,pool=pools[t]
    c=dict(id=t.replace('-2','-b').replace('-3','-c'),theme=th,unit=unit,chain=[[x,pool[x]] for x in ch]); RH.append(c)
    print('RH',22+d,t,[f'{x} {pool[x]}' for x in ch], 'clash',clash(ch,22+d))
for d,qi in enumerate(tforder): tf_row(15+d,Q2[qi])
for d,c in enumerate(RH): rh_row(22+d,c)
ORDER=['Fast Break',"Who's That Baller",'In The Mixer','Link Up Play','Squad Goals','Shirt Swap','Tiki-Taka-Toe','Offside','Top Four','Ranked Highly']
rows.sort(key=lambda r:(r[0],ORDER.index(r[2])))
json.dump(rows,open('rows_w2.json','w'),ensure_ascii=False)
json.dump(dict(tf=[Q2[i] for i in tforder],rh=RH),open('tf_rh_w2.json','w'),ensure_ascii=False)
from collections import Counter; print(len(rows),Counter(r[2] for r in rows))
