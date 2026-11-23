"""Build the Tiki-Taka-Toe player database with honours tied to clubs.
Inputs: existing curated PLAYERS (tiki-taka-toe.html source), ucl_raw1.txt (per player), ucl_raw2.txt (per final), wc_raw.txt, awards_raw.txt, extra_nat.json.
Output: players.json  [{name, nat:[..], clubs:[..], partial, C:[clubs], W:[clubs], B:[clubs], G:[clubs]}]"""
import re, json, unicodedata, sys, os
D=os.path.dirname(os.path.abspath(__file__))
SRC='/home/claude/tiki-taka-toe.html'
def norm(s): return re.sub(r'\s+',' ',re.sub(r'[^a-z ]','',unicodedata.normalize('NFD',s.lower()).encode('ascii','ignore').decode().replace('-',' '))).strip()
CLUB={'Internazionale':'Inter','Milan':'AC Milan','Bayern München':'Bayern Munich','Paris SG':'Paris Saint-Germain','FC Barcelona':'Barcelona'}
NAT={'West Germany':'Germany','Ireland':'Republic of Ireland','Czechia':'Czech Republic'}
ALIAS={'Theo Hernández':'Theo Hernandez','Emerson Palmieri':'Emerson','Mariano Díaz':'Mariano',
 'Jesús Fernández':'Jesús','Borja Fernández':'Borja','Juan Carlos Rodríguez':'Juan Carlos','Nuno Espírito Santo':'Nuno Espírito Santo'}
OLD=json.load(open(D+'/curated_old.json'))   # the original hand-curated ~200 players (full club histories)
P={}; ORDER=[]
def get(name, nat=None):
    name=ALIAS.get(name,name); k=norm(name)
    if k not in P:
        P[k]={'name':name,'nat':[],'clubs':[],'partial':True,'C':[],'W':[],'B':[],'G':[],'old':{}}; ORDER.append(k)
    p=P[k]
    for n in (nat or []):
        n=NAT.get(n,n)
        if n and n!='?' and n not in p['nat']: p['nat'].append(n)
    return p
def add(lst,x):
    if x and x not in lst: lst.append(x)
for o in OLD:
    p=get(o['name'],[o['nat']]); p['clubs']=list(o['clubs']); p['partial']=False; p['old']={h:o[h] for h in 'CBWG'}
# UCL per player
for line in open(D+'/ucl_raw1.txt'):
    if line.startswith('#') or not line.strip(): continue
    name,nat,rest=line.rstrip('\n').split('|')
    p=get(name,nat.split(';'))
    for part in rest.split(';'):
        m=re.match(r'(.+?) ([\d,]+)$',part.strip()); club=CLUB.get(m.group(1),m.group(1))
        add(p['C'],club); add(p['clubs'],club)
EXN=json.load(open(D+'/extra_nat.json')) if os.path.exists(D+'/extra_nat.json') else {}
for line in open(D+'/ucl_raw2.txt'):
    if line.startswith('#') or not line.strip(): continue
    cy,names=line.rstrip('\n').split('|'); club=cy.rsplit(' ',1)[0]
    for n in names.split(';'):
        p=get(n,EXN.get(n,EXN.get(ALIAS.get(n,n),[]))); add(p['C'],club); add(p['clubs'],club)
for line in open(D+'/wc_raw.txt'):
    if line.startswith('#') or not line.strip(): continue
    yr,nat,rest=line.rstrip('\n').split('|')
    for e in rest.split(';'):
        n,c=e.rsplit(':',1); p=get(n,[nat]); add(p['W'],c if c!='-' else '(other)')
        if c!='-': add(p['clubs'],c)
for line in open(D+'/awards_raw.txt'):
    if line.startswith('#') or not line.strip(): continue
    h,n,nat,club,yrs=line.rstrip('\n').split('|'); p=get(n,nat.split(';')); add(p[h],club); add(p['clubs'],club)
# full careers checked one by one (careers.json): replace partial club lists
CAR=json.load(open(D+'/careers.json')) if os.path.exists(D+'/careers.json') else {}
for n,v in CAR.items():
    if n.startswith('_'): continue
    k=norm(ALIAS.get(n,n))
    if k not in P: warn.append(f'careers.json: {n} not in the pool'); continue
    p=P[k]
    for h in 'CWBG':
        for c in p[h]:
            if c!='(other)' and c not in v['clubs']: warn.append(f"careers.json: {n} won {h} at {c}, not in his career list")
    p['clubs']=list(v['clubs']); p['partial']=False
out=[]; warn=[]
for k in ORDER:
    p=P[k]
    for h in 'CBWG':
        if p['old'].get(h) and not p[h]: warn.append(f"{p['name']}: old data said {h} but no source entry")
    if not p['nat']: warn.append(f"{p['name']}: no nationality")
    q={x:p[x] for x in ('name','nat','clubs','C','W','B','G')}
    if p['partial']: q['partial']=1
    out.append(q)
json.dump(out,open(D+'/players.json','w'),ensure_ascii=False)
print(len(out),'players'); print('\n'.join(warn))
