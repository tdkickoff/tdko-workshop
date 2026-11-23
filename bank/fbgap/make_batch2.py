import json, random, collections
from batch2_data import *
# country of each club (from the stadium list) and same-country options, so wrong answers are believable
CTRY={'Manchester United':'ENG','Barcelona':'ESP','Atlético Madrid':'ESP','Benfica':'POR','Marseille':'FRA','Ajax':'NED','Napoli':'ITA','Porto':'POR','Sheffield Wednesday':'ENG',
 'Millwall':'ENG','Portsmouth':'ENG','Queens Park Rangers':'ENG','Charlton Athletic':'ENG',"Birmingham City":'ENG','Bristol City':'ENG','Preston North End':'ENG','Wrexham':'ENG',
 'Everton':'ENG','Athletic Bilbao':'ESP','Sporting CP':'POR','Real Betis':'ESP','Sevilla':'ESP','Feyenoord':'NED','Werder Bremen':'GER','Fiorentina':'ITA','Lille':'FRA',
 'Bayer Leverkusen':'GER','RB Leipzig':'GER','Lazio':'ITA','PSV':'NED','Schalke 04':'GER','Beşiktaş':'TUR','Hertha BSC':'GER','Espanyol':'ESP','Real Sociedad':'ESP','Celta':'ESP',
 'Young Boys':'SUI','AEK':'GRE','Olympiacos':'GRE'}
POOL_BY={'ESP':['Valencia','Villarreal','Real Madrid'],'POR':['Braga','Vitória SC','Boavista'],'FRA':['Lyon','Monaco','Nice'],'NED':['PSV','Twente','AZ'],'ITA':['Roma','Lazio','Juventus'],
 'GER':['Borussia Dortmund','Eintracht Frankfurt','VfB Stuttgart']}
CITIES_BY={'ITA':['Rome','Florence','Milan','Turin','Naples','Genoa'],'POR':['Lisbon','Porto','Braga','Guimarães'],'ESP':['Seville','Barcelona','Madrid','Valencia','San Sebastián','Vigo','Bilbao','Málaga'],
 'NED':['Rotterdam','Eindhoven','Amsterdam','Enschede'],'GER':['Gelsenkirchen','Berlin','Dortmund','Cologne','Hamburg'],'TUR':['Istanbul','Ankara','Izmir','Trabzon'],
 'SUI':['Bern','Basel','Geneva','Zurich'],'GRE':['Athens','Piraeus','Thessaloniki','Patras']}
random.seed(30)
have={(r['comp'],r['kind'],r['year']) for r in json.load(open('/home/claude/bank/fbgap/classified.json')) if r['comp'] and r['year']}
import sqlite3; exist=[json.loads(p)['q'].lower() for (p,) in sqlite3.connect('/home/claude/db/tdko.db').execute("select payload from fact_question where game_id=1")]
existA={json.loads(p)['options'][0] for (p,) in sqlite3.connect('/home/claude/db/tdko.db').execute("select payload from fact_question where game_id=1")}
out=[]
def add(comp,kind,year,q,a,wrong,d,src,note=''):
    if year and (comp,kind,year) in have: return
    if any(q.lower()[:-1] in e for e in exist): return
    wrong=[w for w in dict.fromkeys(wrong) if w!=a][:3]; assert len(wrong)==3,(q,wrong)
    out.append(dict(comp=comp,kind=kind,year=year,q=q,a=a,wrong=wrong,d=d,src=SRC[src],note=note))
def near(vals,i,exclude):
    o=sorted(range(len(vals)),key=lambda j:abs(j-i)); r=[]
    for j in o:
        for v in vals[j]:
            if v not in exclude and v not in r: r.append(v)
    return r[:5]
# Premier League champions
for i,(y,ch,ru) in enumerate(PL):
    y=int(y); s=f"{y-1}–{str(y)[2:]}"; pool=near([p[1:] for p in PL],i,{ch,ru}); random.shuffle(pool)
    add('Premier League','winner',y,f"Who won the Premier League in {s}?",ch,[ru]+pool[:2],'e' if y>=2005 else 'm','pl',f"{ch} champions, {ru} second")
    if y>=2010: add('Premier League','runner-up',y,f"Who finished second in the Premier League in {s}?",ru,[ch]+pool[:2],'m','pl',f"{ch} champions, {ru} second")
# Golden Boot
for i,(y,p,club,g) in enumerate(GB):
    y=int(y); s=f"{y-1}–{str(y)[2:]}"; pool=near([[x[1]] for x in GB],i,{p}); pool=[x for x in pool if x!=p]; random.shuffle(pool)
    add('PL Golden Boot','scorer',y,f"Who won the Premier League Golden Boot in {s}?",p,pool[:3],'e' if y>=2005 else 'm','gb',f"{p} ({club}), {g} goals")
# World Cup and Euros
for comp,rows,src,label in [('World Cup',WC,'wc','World Cup'),('Euros',EU,'eu','Euro')]:
    for i,(y,w,ru,host) in enumerate(rows):
        y=int(y); pre=y<1990; title=f"the {y} World Cup" if comp=='World Cup' else f"Euro {y}" if y>=1996 else f"the {y} European Championship"
        pool=near([r[1:3] for r in rows],i,{w,ru}); random.shuffle(pool)
        add(comp,'winner',y,f"Which country won {title}?",w,[ru]+pool[:2],'m' if pre else 'e',src,f"{w} beat {ru} in the final")
        add(comp,'runner-up',y,f"Who did {w} beat in the {y} {label} final?",ru,pool[:3],'h' if pre else 'm',src,f"{w} beat {ru} in the final")
        if host and ' and ' not in host and ',' not in host:
            hosts=[r[3] for r in rows if r[3] and r[3]!=host and ' and ' not in r[3] and ',' not in r[3]]; hosts=list(dict.fromkeys(hosts)); random.shuffle(hosts)
            add(comp,'venue',y,f"Which country hosted {title}?",host,hosts[:3],'m' if pre else 'e',src,f"Hosted by {host}")
# stadiums
for i,(st,club,d,src) in enumerate(STAD):
    if club in existA and any(st.lower().replace('the ','') in e for e in exist): continue
    others=[c for _,c,_,_ in STAD if c!=club and CTRY[c]==CTRY[club]]; random.shuffle(others)
    if len(others)<3: others+= [c for c in POOL_BY[CTRY[club]] if c not in others and c!=club]
    add('Stadium','other',None,f"Which club plays its home games at {st}?",club,others[:3],d,src)
for nick,club,d in CLUBNICK:
    others=[c for _,c,_ in CLUBNICK if c!=club]; random.shuffle(others)
    add('Nickname','other',None,f"Which club is nicknamed '{nick}'?",club,others[:3],d,'nick')
for nick,c,d,src in NATNICK:
    others=[x for _,x,_,s2 in NATNICK if x!=c and s2==src]; random.shuffle(others)
    others+=[x for x in {'uefa_n':['Northern Ireland','Scotland','Wales','Croatia'],'con_n':['Peru','Ecuador','Chile','Bolivia'],'caf_n':['Ghana','Nigeria','Mali']}[src] if x not in others and x!=c]
    add('Nickname','other',None,f"Which national team is nicknamed '{nick}'?",c,others[:3],d,src)
cities=[c for _,c,_ in CITY]
for club,city,d in CITY:
    others=[x for x in CITIES_BY[CTRY[club]] if x!=city]; random.shuffle(others)
    add('City','other',None,f"In which city are {club} based?",city,others[:3],d,'eust')
json.dump(out,open('/home/claude/bank/fbgap/batch2.json','w'),ensure_ascii=False,indent=1)
print(len(out)); print(collections.Counter(q['d'] for q in out)); print(collections.Counter(q['comp'] for q in out))
