import json,re,unicodedata
W=json.load(open('final28.json'))
def n(s): return re.sub(r'\s+',' ',re.sub(r"[^a-z ]",' ',unicodedata.normalize('NFD',s.lower()).encode('ascii','ignore').decode())).strip()
STOP={'villa','charlton','james','young','silva','costa','city','united','neville','ronaldo','carlos','kane','cole','owen','pepe','marcos','deco','king','johnson','thomas','james','hall','burn','gordon','murphy','evans','diop','barry','smith','jones','wright','robson','hughes','ferdinand','schmeichel','martinez','toure','koeman','pires','silva','muller','fernandes','alonso','torres','garcia','rodriguez','sanchez','suarez','dante','kanu'}
def people(k,x):
    if k=='wtb': return [x['name']]
    if k=='mix': return [x['name']]
    if k=='link': return [x['start']['p'][0]]+[l['p'][0] for l in x['links']]
    if k=='squad': return [p[0] for r in x['rows'] for p in r]
    if k=='ss': return list(x.values())
    if k=='tiki': return x['ex']
    if k=='off': return x['eight']+[x['odd']]
    if k=='tf': return [a for a,b in x['items'] if not re.search(r'\d',a) and a not in NATIONS]
    if k=='rh': return [a for a,b in x['chain']]
NATIONS={'Spain','Germany','France','Denmark','Argentina','Uruguay','Brazil','Chile','England','Italy'}
roster=set(json.load(open('/tmp/claude-0/chk/roster.json'))['roster'])
for k in W:
    if k=='fb': continue
    for x in W[k]: roster|=set(people(k,x))
def keys(p):
    f=n(p); w=f.split(); ks={f}
    if len(w)>1 and len(w[-1])>=5 and w[-1] not in STOP: ks.add(w[-1])
    return ks
RK={p:keys(p) for p in roster if p}
def mentions(text):
    t=' '+n(text)+' '
    return {p for p,ks in RK.items() if any(' '+k+' ' in t for k in ks)}
def fbtext(i): q=W['fb']['Q'][i]; return q[0]+' '+' '.join(q[1])
def day_items(d, skip_fb=False):
    items=[]
    for k in W:
        if k=='fb': continue
        if k=='rh' and d<7: continue
        x=W[k][d]; items.append((k,set(people(k,x))))
    if not skip_fb:
        D=W['fb']['DAYS'][d]
        for i in D['e']+D['m']+D['h']: items.append(('fb%d'%i, mentions(fbtext(i))))
    return items
def same(a,b):
    a=a.replace('Ronaldo Nazário','R9'); b=b.replace('Ronaldo Nazário','R9')
    return a==b
def clashes(d):
    it=day_items(d); out=[]
    for i in range(len(it)):
        for j in range(i+1,len(it)):
            ki,si=it[i]; kj,sj=it[j]
            if ki.startswith('fb') and kj.startswith('fb'): continue
            c=si&sj
            if c: out.append((ki,kj,sorted(c)))
    return out
if __name__=='__main__':
    tot=0
    for d in range(28):
        c=clashes(d); tot+=len(c)
        for x in c: print('No.',d+1,x)
    print('total',tot)
