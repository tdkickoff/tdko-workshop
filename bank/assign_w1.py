import json, re, unicodedata, itertools, random, sys, pickle
exec(open('week1.py').read()); exec(open('fb_week1.py').read())
def n(s): return re.sub(r'\s+',' ',re.sub(r"[^a-z ]",' ',unicodedata.normalize('NFD',s.lower()).encode('ascii','ignore').decode())).strip()
STOP={'villa','charlton','james','young','silva','costa','city','united','neville','ronaldo','carlos','kane','cole','owen','pepe','marcos','deco'}
# roster of people
roster=set(json.load(open('/tmp/claude-0/chk/roster.json'))['roster'])
for p in WTB+MIXER: roster.add(p['name'])
for c in LINK: roster.add(c['start'][0]); roster|={l[0][0] for l in c['links']}
for x in SQUAD: roster|={p[0] for r in x['rows'] for p in r}
for z in OFFSIDE: roster|=set(z['eight'])|set(z['odds'])
for L in SHIRT.values(): roster|=set(L)
roster|={'Ian Callaghan','Arsène Wenger','José Mourinho','Pep Guardiola','Jürgen Klopp','Claudio Ranieri','Mauricio Pochettino','Kenny Dalglish','Franz Beckenbauer','Patrick Kluivert','René Higuita','Gareth Southgate','Mohamed Salah','Raheem Sterling','Philippe Coutinho','Carlos Tevez','Petr Čech','Rio Ferdinand','Ashley Cole','Jamie Vardy','Ruud Gullit','Frank Rijkaard','Marco van Basten','Ole Gunnar Solskjær','George Weah'}
def keys(p):
    f=n(p); w=f.split(); ks={f}
    if len(w)>1 and len(w[-1])>=5 and w[-1] not in STOP: ks.add(w[-1])
    if len(w)>2: ks.add(' '.join(w[-2:]))
    return ks
RK={p:keys(p) for p in roster}
alias={'Ronaldo Nazário':'Ronaldo'}
ident=lambda p: alias.get(p,p)
def mentions(text):
    t=' '+n(text)+' '
    return {ident(p) for p,ks in RK.items() if any(' '+k+' ' in t for k in ks)}
# fixed item name sets
items={
 'wtb':[{ident(p['name'])}|mentions(p['blurb']) for p in WTB],
 'mix':[{ident(p['name'])}|mentions(p['blurb']+' '+' '.join(p['hints'])) for p in MIXER],
 'link':[{c['start'][0]}|{l[0][0] for l in c['links']} for c in LINK],
 'squad':[{ident(p[0]) for r in x['rows'] for p in r} for x in SQUAD],
}
for k in items:
    for s in items[k]:
        if s & {'Ronaldo','Cristiano Ronaldo'}: s|={'Ronaldo','Cristiano Ronaldo'}
best=None
random.seed(1)
def try_assign():
    days=[set() for _ in range(7)]; plan={}
    for g in ['squad','link','wtb','mix']:
        perms=list(itertools.permutations(range(7)))
        random.shuffle(perms)
        for perm in perms[:20000]:
            if all(not (items[g][perm[d]] & days[d]) for d in range(7)):
                plan[g]=perm
                for d in range(7): days[d]|=items[g][perm[d]]
                break
        else: return None
    # offside: pick puzzle per day + 8 + odd avoiding names
    for perm in itertools.permutations(range(7)):
        ok=True; choice=[]
        for d in range(7):
            z=OFFSIDE[perm[d]]
            e=[x for x in z['eight'] if ident(x) not in days[d]]
            o=[x for x in z['odds'] if ident(x) not in days[d]]
            if len(e)<8 or not o: ok=False; break
            choice.append((perm[d],e[:8],o[0]))
        if ok: break
    else: return None
    for d,(i,e,o) in enumerate(choice): days[d]|=set(e)|{o}
    plan['off']=choice
    # shirt swap: per day pick one name per length not in day
    ss=[]; used=set()
    for d in range(7):
        pick={}
        for L in (5,6,7):
            c=[x for x in SHIRT[L] if x not in used and ident(x) not in days[d] and not ({'Ronaldo','Cristiano Ronaldo'}&{x} and days[d]&{'Ronaldo','Cristiano Ronaldo'})]
            if not c: return None
            pick[L]=c[0]; used.add(c[0]); days[d].add(ident(c[0]))
            if c[0]=='Ronaldo': days[d]|={'Cristiano Ronaldo'}
        ss.append(pick)
    plan['ss']=ss
    # fast break: 10 e, 9 m, 1 h per day
    fbm=[mentions(q+' '+' '.join(o)) for q,o,t in FB]
    for x in fbm:
        if x & {'Ronaldo','Cristiano Ronaldo'}: x|={'Ronaldo','Cristiano Ronaldo'}
    pools={t:[i for i,(q,o,tt) in enumerate(FB) if tt==t] for t in 'emh'}
    need={'e':10,'m':9,'h':1}
    fbdays=[[] for _ in range(7)]
    for t in 'hme':
        idx=pools[t][:]; random.shuffle(idx)
        # place most-constrained first
        idx.sort(key=lambda i:-len(fbm[i]))
        for i in idx:
            cands=[d for d in range(7) if sum(1 for j in fbdays[d] if FB[j][2]==t)<need[t] and not (fbm[i]&days[d])]
            if not cands: return None
            d=min(cands,key=lambda d:sum(1 for j in fbdays[d] if FB[j][2]==t))
            fbdays[d].append(i); days[d]|=fbm[i]
    plan['fb']=fbdays
    return plan, days
for attempt in range(300):
    r=try_assign()
    if r: break
print('found' if r else 'FAILED', attempt)
plan,days=r
pickle.dump((plan,[sorted(d) for d in days]),open('plan_w1.pkl','wb'))
for d in range(7):
    print('No.',15+d, '| WTB',WTB[plan['wtb'][d]]['name'],'| MIX',MIXER[plan['mix'][d]]['name'],'| LINK',LINK[plan['link'][d]]['start'][0],'| XI',SQUAD[plan['squad'][d]]['id'],'| OFF',OFFSIDE[plan['off'][d][0]]['id'],plan['off'][d][2],'| SS',list(plan['ss'][d].values()))
