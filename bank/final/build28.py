import json,pickle,sys,re,copy
sys.path.insert(0,'/home/claude/bank'); sys.path.insert(0,'/home/claude/bank/week2'); sys.path.insert(0,'/home/claude/bank/final')
import week1, week2
from fb_week1 import FB as FB1
from changes import *
cur=json.load(open('/home/claude/bank/sheet/current.json'))
p1,_=pickle.load(open('/home/claude/bank/plan_w1.pkl','rb')); p2,_=pickle.load(open('/home/claude/bank/week2/plan_w2.pkl','rb'))
t1=json.load(open('/home/claude/bank/tiki_w1.json')); t2=json.load(open('/home/claude/bank/week2/tiki_w2.json'))
FB2=json.load(open('/home/claude/bank/week2/fb_all.json'))
tfrh=json.load(open('/home/claude/bank/week2/tf_rh_w2.json'))
W={'wtb':[],'mix':[],'link':[],'squad':[],'ss':[],'tiki':[],'off':[],'tf':[],'rh':[]}
def link_live(c): return {'d':c['d'],'start':{'p':c['start'],'clubs':c['clubs']},'links':[{'p':l[0],'t':l[1],'x':l[2]} for l in c['links']]}
def wtb_live(p): return {k:v for k,v in p.items() if k!='check'}
def off_live(P,eight,odd):
    o={k:v for k,v in P.items() if k not in ('id','eight','odds')}; o['eight']=list(eight); o['odd']=odd; return o
def tik(g): return {k:g[k] for k in ('r','c','rl','cl','ex')}
def tf_live(q):
    def f(v):
        if q.get('fmt'): return q['fmt'].format(v)
        u=q['unit']; 
        if v==1 and u.endswith('s'): u=u[:-1]
        return f"{v:,} {u}".strip()
    o={k:q[k] for k in ('id','q','top','bottom')}; o['items']=[[a,f(b)] for a,b in q['items']]
    if q.get('note'): o['note']=q['note']
    return o
# days 1-14
for k in W:
    if k in ('tf','rh'): continue
    W[k]+=copy.deepcopy(cur[k])
W['tf']+=copy.deepcopy(cur['tf'])
# days 15-21
for d in range(7):
    W['wtb'].append(wtb_live(week1.WTB[p1['wtb'][d]])); W['mix'].append(week1.MIXER[p1['mix'][d]]); W['link'].append(link_live(week1.LINK[p1['link'][d]]))
    W['squad'].append(week1.SQUAD[p1['squad'][d]]); W['ss'].append({str(k):v for k,v in p1['ss'][d].items()}); W['tiki'].append(tik(t1[d]))
    oi,e,o=p1['off'][d]; W['off'].append(off_live(week1.OFFSIDE[oi],e,o))
for d in range(7):
    W['wtb'].append(wtb_live(week2.WTB[p2['wtb'][d]])); W['mix'].append(week2.MIXER[p2['mix'][d]]); W['link'].append(link_live(week2.LINK[p2['link'][d]]))
    W['squad'].append(week2.SQUAD[p2['squad'][d]]); W['ss'].append({str(k):v for k,v in p2['ss'][d].items()}); W['tiki'].append(tik(t2[d]))
    oi,e,o=p2['off'][d]; W['off'].append(off_live(week2.OFFSIDE[oi],e,o))
W['tf']+=[tf_live(q) for q in tfrh['tf']]
# Ranked Highly: index = day-1. Days 1-7 never shown (opens day 8); days 8-14 = cur[7..13], 15-21 = cur[0..6], 22-28 new
W['rh']=copy.deepcopy(cur['rh'][0:7])+copy.deepcopy(cur['rh'][7:14])+copy.deepcopy(cur['rh'][0:7])+tfrh['rh']
# ---- sign-off changes
for n,(odd,b) in OFF_ODD.items():
    P=W['off'][n-1]; P['odd']=odd
    if b: P['b']=b
for n,x in SQUAD.items(): W['squad'][n-1]=x
for n,p in WTB.items(): W['wtb'][n-1]=p
W['link'][24]=LINK25
# Top Four: always most/biggest at the top
for q in W['tf']:
    if q['top'] in ('Fewest','Smallest'):
        q['items']=q['items'][::-1]; q['top'],q['bottom']={'Fewest':('Most','Fewest'),'Smallest':('Biggest','Smallest')}[q['top']]
# Fast Break: one Q list, DAYS as index groups
Q=[list(x) for x in cur['fb']['Q']]; DAYS=copy.deepcopy(cur['fb']['DAYS'])
o1=len(Q); Q+=[list(x) for x in FB1]
for d in range(7):
    idx=[o1+i for i in p1['fb'][d]]; DAYS.append({t:[i for i in idx if Q[i][2]==t] for t in 'emh'})
o2=len(Q); Q+=[list(x) for x in FB2]
for d in range(7):
    idx=[o2+i for i in p2['fb'][d]]; DAYS.append({t:[i for i in idx if Q[i][2]==t] for t in 'emh'})
W['fb']={'Q':Q,'DAYS':DAYS}
for k,v in W.items(): print(k, len(v) if isinstance(v,list) else (len(v['Q']),len(v['DAYS'])))
json.dump(W,open('final28.json','w'),ensure_ascii=False)
