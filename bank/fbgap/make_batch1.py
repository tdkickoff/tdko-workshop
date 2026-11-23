"""Batch 1: FA Cup, League Cup, Champions League, Europa League finals 1990-2026. Four question shapes per final; skips any the bank already has."""
import json, random, re
from finals import DATA, MGR, SRC
random.seed(29)
have={(r['comp'],r['kind'],r['year']) for r in json.load(open('/home/claude/bank/fbgap/classified.json')) if r['comp'] and r['year']}
SKIP_VENUE={('Champions League',2000),('Champions League',2006),('Champions League',2022),('Europa League',2017),('Europa League',2018)}  # stadium outside the city usually named
def cname(comp,y):
    if comp=='Champions League': return 'European Cup' if y<=1992 else 'Champions League'
    if comp=='Europa League': return 'UEFA Cup' if y<=2009 else 'Europa League'
    return comp
def grade(comp,kind,y):
    if kind=='venue': return 'h'                                   # rule: naming a final's stadium or city = Hard
    base={'FA Cup':(2005,1990),'Champions League':(2005,1990),'League Cup':(2015,1995),'Europa League':(2015,2005)}[comp]   # (Easy from, Medium from)
    g='e' if y>=base[0] else 'm' if y>=base[1] else 'h'
    if kind in('runner-up','manager'): g={'e':'m','m':'h','h':'h'}[g]   # one step harder than naming the winner
    return g
def near(rows,y,key,exclude,k=3):
    pool=[]
    for d in sorted(rows,key=lambda r:abs(r['year']-y)):
        for v in ([d['win'],d['ru']] if key=='club' else [d[key]]):
            if v and v not in exclude and v not in pool: pool.append(v)
    return pool[:6]
out=[]
for comp,rows in DATA.items():
    for r in rows:
        y=r['year']; c=cname(comp,y); w,ru=r['win'],r['ru']
        def add(kind,q,a,opts,note):
            if (comp,kind,y) in have: return
            opts=[o for o in opts if o!=a][:3]; assert len(opts)==3, (q,opts)
            out.append({'comp':comp,'kind':kind,'year':y,'q':q,'a':a,'wrong':opts,'d':grade(comp,kind,y),'src':SRC[comp],'note':note})
        pool=near(rows,y,'club',{w,ru}); random.shuffle(pool)
        add('winner',f"Who won the {y} {c} final?",w,[ru]+pool[:2],f"{w} {r['score']} {ru}")
        pool=near(rows,y,'club',{w,ru}); random.shuffle(pool)
        add('runner-up',f"Who did {w} beat in the {y} {c} final?",ru,pool[:3],f"{w} {r['score']} {ru}")
        if comp in MGR:
            mg=MGR[comp][y]; others=[MGR[comp][x] for x in sorted(MGR[comp],key=lambda x:abs(x-y)) if MGR[comp][x]!=mg]
            others=list(dict.fromkeys(others))[:5]; random.shuffle(others)
            add('manager',f"Who managed {w} to the {y} FA Cup?",mg,others[:3],f"{w} manager: {mg}")
        v=r['venue']
        if comp in('Champions League','Europa League') and v and (comp,y) not in SKIP_VENUE:
            cities=[d['venue'] for d in sorted(rows,key=lambda d:abs(d['year']-y)) if d['venue'] and d['venue']!=v]
            cities=list(dict.fromkeys(cities))[:5]; random.shuffle(cities)
            add('venue',f"In which city was the {y} {c} final played?",v,cities[:3],f"{w} {r['score']} {ru}, in {v}")
        if comp in('FA Cup','League Cup') and v=='Millennium Stadium':
            add('venue',f"Where was the {y} {c} final played?",'Millennium Stadium',['Wembley Stadium','Old Trafford','Villa Park'],'Played in Cardiff while Wembley was rebuilt (2001-2006/07)')
json.dump(out,open('/home/claude/bank/fbgap/batch1.json','w'),ensure_ascii=False,indent=1)
import collections
print(len(out),'questions'); print(collections.Counter((q['comp'],q['kind']) for q in out)); print(collections.Counter(q['d'] for q in out))
