"""Batch 3: 'Which country has X played for?' from the sourced Tiki-Taka-Toe player list, plus missing Ballon d'Or years.
Fame filter (only well-known names): appears in 2+ of our puzzles, or Ballon d'Or / Premier League Golden Boot winner, or World Cup winner who also appears in our puzzles.
Era: a player whose honours are all before 1990 is never Easy (owner's rule)."""
import json, re, random, sqlite3, collections, unicodedata
random.seed(31)
T='/home/claude/bank/tiki/'
P={p['name']:p for p in json.load(open(T+'players.json'))}
def norm(s): return re.sub(r'\s+',' ',re.sub(r'[^a-z ]','',unicodedata.normalize('NFD',s.lower()).encode('ascii','ignore').decode().replace('-',' '))).strip()
yrs=collections.defaultdict(set); src=collections.defaultdict(set)
SRC={'ucl':'https://en.wikipedia.org/wiki/List_of_European_Cup_and_UEFA_Champions_League_winning_players','wc':'https://www.rsssf.org/miscellaneous/wcwinners.html',
     'aw':'https://www.topendsports.com/sport/soccer/list-player-of-year-ballondor.htm','gb':'https://en.wikipedia.org/wiki/Premier_League_Golden_Boot'}
for l in open(T+'ucl_raw1.txt'):
    if l.startswith('#') or not l.strip(): continue
    n,nat,rest=l.rstrip('\n').split('|'); src[norm(n)].add('ucl')
    for y in re.findall(r'(19\d\d|20\d\d)',rest): yrs[norm(n)].add(int(y))
for l in open(T+'ucl_raw2.txt'):
    if l.startswith('#') or not l.strip(): continue
    cy,names=l.rstrip('\n').split('|'); y=int(cy.rsplit(' ',1)[1])
    for n in names.split(';'): yrs[norm(n)].add(y); src[norm(n)].add('ucl')
for l in open(T+'wc_raw.txt'):
    if l.startswith('#') or not l.strip(): continue
    y,nat,rest=l.rstrip('\n').split('|')
    for e in rest.split(';'): n=e.rsplit(':',1)[0]; yrs[norm(n)].add(int(y)); src[norm(n)].add('wc')
BD={}
for l in open(T+'awards_raw.txt'):
    if l.startswith('#') or not l.strip(): continue
    h,n,nat,club,y=l.rstrip('\n').split('|')
    for yy in re.findall(r'\d{4}',y): yrs[norm(n)].add(int(yy))
    src[norm(n)].add('aw' if h=='B' else 'gb')
    if h=='B':
        for yy in re.findall(r'\d{4}',y): BD[int(yy)]=(n,nat,club)
c=sqlite3.connect('/home/claude/db/tdko.db')
FB=[json.loads(p) for (p,) in c.execute("select payload from fact_question where game_id=1")]
asked_nat={n for q in FB for n in P if re.search(r'which (country|national team)',q['q'].lower()) and n.lower() in q['q'].lower()}
app=collections.Counter(n for (n,) in c.execute('select p.name from bridge_question_player b join dim_player p using(player_id)'))
REG={'Europe-W':['England','Scotland','Wales','Northern Ireland','Republic of Ireland','France','Belgium','Netherlands','Germany','Switzerland','Austria','Denmark','Sweden','Norway'],
 'Europe-S':['Spain','Portugal','Italy','Greece','Croatia','Serbia','Turkey'],'Europe-E':['Czech Republic','Poland','Ukraine','Russia','Soviet Union','Hungary','Romania','Bulgaria','Slovakia','Czechoslovakia','Yugoslavia'],
 'SAm':['Brazil','Argentina','Uruguay','Chile','Colombia','Paraguay','Peru','Ecuador'],'Africa':['Nigeria','Ghana','Ivory Coast','Cameroon','Senegal','Egypt','Morocco','Algeria','Mali','Gabon','Liberia'],
 'Other':['USA','Mexico','Costa Rica','Japan','South Korea','Australia','Trinidad and Tobago','Jamaica']}
reg={n:r for r,ns in REG.items() for n in ns}
out=[]
for name,p in P.items():
    if len(p['nat'])!=1 or name in asked_nat: continue
    nat=p['nat'][0]; k=norm(name); y=yrs.get(k,set())
    if nat not in reg: continue
    pre= bool(y) and max(y)<1990
    fame=app[name]+(2 if p['B'] else 0)+(1 if p['G'] else 0)+(1 if p['W'] and app[name] else 0)
    if fame<2: continue
    big=app[name]>=3 or p['B'] or p['G'] or (p['W'] and app[name]>=2)
    d='m' if pre else 'e'
    if pre and fame<3: d='h'
    same=[x for x in REG[reg[nat]] if x!=nat]; random.shuffle(same)
    if len(same)<3: same+= [x for x in REG['Europe-W'] if x!=nat and x not in same]
    s=sorted(src[k])[0] if src[k] else 'ucl'
    out.append(dict(comp='Nationality',kind='other',year=None,q=f"Which country has {name} played for?",a=nat,wrong=same[:3],d=d,src=SRC[s],
                    note=f"Honours {min(y)}–{max(y)}" if y else ''))
# Ballon d'Or years missing from the bank (1990 onwards)
have={(r['comp'],r['kind'],r['year']) for r in json.load(open('/home/claude/bank/fbgap/classified.json')) if r['comp'] and r['year']}
winners=[BD[y][0] for y in sorted(BD)]
for y in sorted(BD):
    if y<1990 or ("Ballon d'Or",'winner',y) in have: continue
    n,nat,club=BD[y]; near=[BD[x][0] for x in sorted(BD,key=lambda x:abs(x-y)) if BD[x][0]!=n]; near=list(dict.fromkeys(near))[:5]; random.shuffle(near)
    out.append(dict(comp="Ballon d'Or",kind='winner',year=y,q=f"Who won the {y} Ballon d'Or?",a=n,wrong=near[:3],d='e' if y>=2005 else 'm',src=SRC['aw'],note=f"{n} ({nat}, {club})"))
json.dump(out,open('/home/claude/bank/fbgap/batch3.json','w'),ensure_ascii=False,indent=1)
print(len(out),collections.Counter(q['d'] for q in out),collections.Counter(q['comp'] for q in out))
