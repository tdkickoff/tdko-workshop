"""ONE-OFF MIGRATION (19-22 Nov 2026): built tdko.db from the old puzzle files. Since 23 Nov the bank is the master: do not run this again
(it would wipe anything added to the bank since). Kept for the record. Override only with --rebuild-from-files."""
import json, sqlite3, os, re, datetime, sys
DB='/home/claude/db/tdko.db'
if os.path.exists(DB):
    if '--rebuild-from-files' not in sys.argv: sys.exit('tdko.db is the master copy now; refusing to rebuild it from the old files.')
    os.remove(DB)
con=sqlite3.connect(DB); con.execute('PRAGMA foreign_keys=ON'); con.executescript(open('/home/claude/db/schema.sql').read())
W=json.load(open('/home/claude/bank/final/final28.json'))
CS=json.load(open('/home/claude/bank/cleansweep/lists.json'))
CRJ=json.load(open('/home/claude/bank/cuprun/runs.json'))
sys.path.insert(0,'/home/claude/bank/cuprun'); from build_runs import ALL as CR_ALL, SCHED, NEXT
LAUNCH=datetime.date(2026,11,16)
cur=con.cursor()
REG_PATH='/home/claude/db/ids.json'
try: REG=json.load(open(REG_PATH))
except Exception: REG={}
def regid(table,key):
    t=REG.setdefault(table,{})
    if key not in t: t[key]=max(t.values(),default=0)+1
    return t[key]
def one(sql,*a): r=cur.execute(sql,a).fetchone(); return r[0] if r else None
def upsert(table,key,val,**extra):
    idc={'dim_nation':'nation_id','dim_club':'club_id','dim_player':'player_id','dim_competition':'competition_id','dim_season':'season_id','dim_source':'source_id'}[table]
    r=one(f'SELECT {idc} FROM {table} WHERE {key}=?',val)
    if r: 
        for k,v in extra.items():
            if v is not None: cur.execute(f'UPDATE {table} SET {k}=COALESCE({k},?) WHERE {idc}=?',(v,r))
        return r
    nid=regid(table,str(val)); cols=[idc,key]+list(extra); cur.execute(f'INSERT INTO {table}({",".join(cols)}) VALUES({",".join("?"*len(cols))})',[nid,val]+list(extra.values())); return nid
GAMES=[('fast-break','Fast Break',1,20,'question'),('whos-that-baller',"Who's That Baller",2,1,'player'),('clean-sweep','Clean Sweep',3,1,'list'),('cup-run','Cup Run',4,1,'run'),
 ('squad-goals','Squad Goals',5,1,'xi'),('link-up-play','Link Up Play',6,1,'chain'),('in-the-mixer','In The Mixer',7,1,'anagram'),('offside','Offside',8,1,'odd one out'),
 ('top-four','Top Four',9,1,'ranking'),('tiki-taka-toe','Tiki-Taka-Toe',10,1,'grid'),('shirt-swap','Shirt Swap',11,3,'word'),('ranked-highly','Ranked Highly',12,1,'chain of stats')]
for i,g in enumerate(GAMES,1): cur.execute('INSERT INTO dim_game VALUES(?,?,?,?,?,?)',(i,)+g)
G={g[0]:i for i,g in enumerate(GAMES,1)}
for i,(c,l) in enumerate([('E','Easy'),('M','Medium'),('H','Hard')],1): cur.execute('INSERT INTO dim_difficulty VALUES(?,?,?)',(i,c,l))
D={'E':1,'M':2,'H':3,'e':1,'m':2,'h':3}
QT=['multiple_choice','guess_player','name_them_all','guess_winner','name_the_xi','chain','anagram','odd_one_out','rank','grid','word','higher_lower']
for i,c in enumerate(QT,1): cur.execute('INSERT INTO dim_question_type VALUES(?,?,?)',(i,c,c.replace('_',' ').capitalize()))
QTID={c:i for i,c in enumerate(QT,1)}
GQT={'fast-break':'multiple_choice','whos-that-baller':'guess_player','clean-sweep':'name_them_all','cup-run':'guess_winner','squad-goals':'name_the_xi','link-up-play':'chain','in-the-mixer':'anagram','offside':'odd_one_out','top-four':'rank','tiki-taka-toe':'grid','shirt-swap':'word','ranked-highly':'higher_lower'}
CODES={'ENG':'England','ESP':'Spain','FRA':'France','GER':'Germany','ITA':'Italy','NED':'Netherlands','POR':'Portugal','BRA':'Brazil','ARG':'Argentina','CZE':'Czech Republic','AUS':'Australia','NOR':'Norway','IRL':'Republic of Ireland','FIN':'Finland','POL':'Poland','MLI':'Mali','URU':'Uruguay','BEL':'Belgium','CRO':'Croatia','SCO':'Scotland','WAL':'Wales','DEN':'Denmark','SWE':'Sweden','CMR':'Cameroon','CIV':'Ivory Coast','NGA':'Nigeria','SEN':'Senegal','GHA':'Ghana','EGY':'Egypt','ALG':'Algeria','MAR':'Morocco','USA':'United States','KOR':'South Korea','JPN':'Japan','SUI':'Switzerland','AUT':'Austria','SRB':'Serbia','TUR':'Turkey','RUS':'Russia','UKR':'Ukraine','GRE':'Greece','CHI':'Chile','COL':'Colombia','MEX':'Mexico','NIR':'Northern Ireland','ISL':'Iceland','SVK':'Slovakia','SVN':'Slovenia','BIH':'Bosnia and Herzegovina','GAB':'Gabon','TOG':'Togo','JAM':'Jamaica','CAN':'Canada','PAR':'Paraguay','ECU':'Ecuador','PER':'Peru','HUN':'Hungary','ROU':'Romania','BUL':'Bulgaria','GEO':'Georgia','ALB':'Albania'}
def nation(n,code=None):
    if not n: return None
    return upsert('dim_nation','name',n,fifa_code=code)
def player(n,pos=None,nat=None,aliases=None):
    return upsert('dim_player','name',n,position=pos,nation_id=nation(nat) if nat else None,aliases=json.dumps(aliases) if aliases else None)
def club(n,code=None,c=None): return upsert('dim_club','name',n,code3=code,colour1=c[0] if c else None,colour2=c[1] if c else None)
def comp(n,kind,scope): return upsert('dim_competition','name',n,kind=kind,scope=scope)
def season(label):
    y=int(str(label)[:4]); return upsert('dim_season','label',str(label),start_year=y,decade=f'{y//10*10}s')
def source(t,url=None): return upsert('dim_source','title',t,url=url) if t else None
def q(ext,game,prompt,answer,payload,diff=None,comp_id=None,season_id=None,src=None,narr=None):
    r=one('SELECT question_id FROM fact_question WHERE ext_id=?',ext)
    if r: return r,False
    nid=regid('fact_question',ext)
    cur.execute('INSERT INTO fact_question(question_id,ext_id,game_id,qtype_id,difficulty_id,competition_id,season_id,source_id,prompt,answer,narrative,payload) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)',
      (nid,ext,G[game],QTID[GQT[game]],D.get(diff) if diff else None,comp_id,season_id,src,prompt,answer,narr,json.dumps(payload,ensure_ascii=False))); return nid,True
def ans(qid,seq,text,ok,pid=None,cid=None,nid=None): cur.execute('INSERT OR IGNORE INTO fact_answer VALUES(?,?,?,?,?,?,?)',(qid,seq,text,ok,pid,cid,nid))
def bp(qid,pid,role): cur.execute('INSERT OR IGNORE INTO bridge_question_player VALUES(?,?,?)',(qid,pid,role))
def bc(qid,cid,role): cur.execute('INSERT OR IGNORE INTO bridge_question_club VALUES(?,?,?)',(qid,cid,role))
def bn(qid,nid,role): cur.execute('INSERT OR IGNORE INTO bridge_question_nation VALUES(?,?,?)',(qid,nid,role))
def day(no):
    d=LAUNCH+datetime.timedelta(days=no-1); k=int(d.strftime('%Y%m%d'))
    cur.execute('INSERT OR IGNORE INTO dim_date VALUES(?,?,?,?,NULL)',(k,d.isoformat(),no,d.strftime('%A'))); return k
def sched(no,game,slot,qid): cur.execute('INSERT OR REPLACE INTO fact_schedule VALUES(?,?,?,?)',(day(no),G[game],slot,qid))
def compname(s):
    s=re.sub(r'\s+final$','',s,flags=re.I).strip()
    m={'Champions League':('Champions League','cup','club'),'European Cup':('Champions League','cup','club'),'UEFA Cup':('Europa League','cup','club'),'Europa League':('Europa League','cup','club'),
       'Conference League':('Conference League','cup','club'),'FA Cup':('FA Cup','cup','club'),'League Cup':('League Cup','cup','club'),'World Cup':('World Cup','international','international'),
       'Euros':('Euros','international','international'),'European Championship':('Euros','international','international'),'Copa América':('Copa América','international','international'),
       'AFCON':('AFCON','international','international'),'Asian Cup':('Asian Cup','international','international')}
    for k,v in m.items():
        if k.lower() in s.lower(): return comp(*v)
    return comp(s,'cup','club')
# ---- Fast Break
FBQ=W['fb']['Q']
for i,(text,opts,d) in enumerate(FBQ):
    qid,_=q(f'fast-break:{i}','fast-break',text,opts[0],{'q':text,'options':opts,'d':d},diff=d)
    for j,o in enumerate(opts): ans(qid,j,o,1 if j==0 else 0)
for n,dd in enumerate(W['fb']['DAYS'],1):
    for s,ix in enumerate(dd['o'],1): sched(n,'fast-break',s,one('SELECT question_id FROM fact_question WHERE ext_id=?',f'fast-break:{ix}'))
# ---- Who's That Baller
for n,p in enumerate(W['wtb'],1):
    qid,new=q(f'wtb:{p["name"]}','whos-that-baller','Guess the player from his career file',p['name'],p,narr=p.get('blurb'))
    pid=player(p['name'],p.get('position'),p.get('nationality'),p.get('aliases'))
    ans(qid,0,p['name'],1,pid=pid); [ans(qid,k+1,a,1,pid=pid) for k,a in enumerate(p.get('aliases',[]))]
    bp(qid,pid,'answer'); bn(qid,nation(p.get('nationality')),'answer')
    for c in p.get('clubs',[]): bc(qid,club(c[0]),'clue')
    sched(n,'whos-that-baller',1,qid)
# ---- In The Mixer
for n,p in enumerate(W['mix'],1):
    qid,_=q(f'mix:{p["name"]}','in-the-mixer',f'Unscramble: {p["phrase"]}',p['name'],p,narr=p.get('blurb'))
    pid=player(p['name'],aliases=p.get('aliases')); ans(qid,0,p['name'],1,pid=pid); bp(qid,pid,'answer'); sched(n,'in-the-mixer',1,qid)
# ---- Link Up Play
for n,c in enumerate(W['link'],1):
    names=[c['start']['p'][0]]+[l['p'][0] for l in c['links']]
    qid,_=q(f'link:{n}:{names[0]}','link-up-play',f'Link up from {names[0]}',' → '.join(names[1:]),c,diff=c.get('d'))
    for k,l in enumerate([c['start']]+c['links']):
        p=l['p']; pid=player(p[0],p[1],p[2],p[3]); bp(qid,pid,'start' if k==0 else 'answer')
        if k: ans(qid,k,p[0],1,pid=pid)
    for cl in c['start'].get('clubs','').split(', '):
        if cl: bc(qid,club(cl),'clue')
    sched(n,'link-up-play',1,qid)
# ---- Squad Goals
for n,x in enumerate(W['squad'],1):
    cid=compname(x['comp']); sid=season(x['year'])
    qid,_=q(f'squad:{x["id"]}','squad-goals',f'Name the {x["team"]} XI: {x["comp"]} {x["year"]}',x['team'],x,comp_id=cid,season_id=sid)
    if x['type']=='club': bc(qid,club(x['team']),'answer')
    else: bn(qid,nation(x['team']),'answer')
    k=0
    for row in x['rows']:
        for p in row:
            pid=player(p[0],p[1],CODES.get(p[2])); bp(qid,pid,'answer'); ans(qid,k,p[0],1,pid=pid); k+=1
    sched(n,'squad-goals',1,qid)
# ---- Shirt Swap (3 a day)
for n,d in enumerate(W['ss'],1):
    for L,name in d.items():
        qid,_=q(f'ss:{name}','shirt-swap',f'{L}-letter surname on the back of the shirt',name,{'len':int(L),'name':name},diff={'5':'E','6':'M','7':'H'}[L])
        pid=player(name); bp(qid,pid,'answer'); ans(qid,0,name,1,pid=pid); sched(n,'shirt-swap',int(L),qid)
# ---- Tiki-Taka-Toe
for n,t in enumerate(W['tiki'],1):
    qid,_=q(f'tiki:{n}','tiki-taka-toe','Fill the grid: '+' / '.join(t['rl'])+' × '+' / '.join(t['cl']),'; '.join(t.get('ex',[])),t)
    for kind,v in t['r']+t['c']:
        if kind=='club': bc(qid,club(v),'category')
        elif kind=='nat': bn(qid,nation(v),'category')
    for k,p in enumerate(t.get('ex',[])): pid=player(p); bp(qid,pid,'example'); ans(qid,k,p,1,pid=pid)
    sched(n,'tiki-taka-toe',1,qid)
# ---- Offside
for n,o in enumerate(W['off'],1):
    link = f'{o["a"]} / {o["b"]}' if 'a' in o else o.get('x') or o.get('head','')
    qid,_=q(f'off:{n}','offside',f'Who is offside? Link: {link}',o['odd'],o,narr=o.get('note'))
    if o['kind']=='club' and 'a' in o: bc(qid,club(o['a']),'category'); bc(qid,club(o['b']),'category')
    pid=player(o['odd']); bp(qid,pid,'answer'); ans(qid,0,o['odd'],1,pid=pid)
    for k,p in enumerate(o['eight'],1): pp=player(p); bp(qid,pp,'option'); ans(qid,k,p,0,pid=pp)
    sched(n,'offside',1,qid)
# ---- Top Four
for n,t in enumerate(W['tf'],1):
    qid,_=q(f'tf:{t["id"]}','top-four',t['q'],' > '.join(i[0] for i in t['items']),t)
    for k,(p,v) in enumerate(t['items']): pid=player(p); bp(qid,pid,'in_list'); ans(qid,k,f'{p} ({v})',1,pid=pid)
    sched(n,'top-four',1,qid)
# ---- Ranked Highly
for n,r in enumerate(W['rh'],1):
    qid,_=q(f'rh:{r["id"]}','ranked-highly',f'Higher or lower: {r["theme"]}',', '.join(f'{p} {v}' for p,v in r['chain']),r)
    for k,(p,v) in enumerate(r['chain']): pid=player(p); bp(qid,pid,'in_list'); ans(qid,k,f'{p}: {v} {r["unit"]}',1,pid=pid)
    sched(n,'ranked-highly',1,qid)
# ---- Clean Sweep (No. 8 on; days 1-7 were the test list)
sys.path.insert(0,'/home/claude/bank/cleansweep')
for n,L in enumerate(CS,1):
    qid,_=q(f'cs:{L["id"]}','clean-sweep',L['q'],', '.join(x['n'] for x in L['names']),L,narr=L.get('note'))
    for k,x in enumerate(L['names']): pid=player(x['n'],aliases=x.get('a')); bp(qid,pid,'in_list'); ans(qid,k,x['n'],1,pid=pid)
    if n>=8: sched(n,'clean-sweep',1,qid)
# ---- Cup Run
def team(t,role,qid):
    if 'c' in t: cid=club(t['n'],t['code'],t['c']); bc(qid,cid,role); return None,cid,None
    nid=nation(t['n'],t['code']); bn(qid,nid,role); return None,None,nid
for k,r in CR_ALL.items():
    cid=compname(r['comp']); sid=season(r['year'])
    qid,_=q(f'cup-run:{k}','cup-run','Every team they beat on the way. Who won it?',r['answer']['n'],r,diff=r.get('lvl'),comp_id=cid,season_id=sid,src=source(r['src']))
    _,c,nn=team(r['answer'],'answer',qid); ans(qid,0,r['answer']['n'],1,cid=c,nid=nn)
    for j,a in enumerate(r['answer'].get('a',[]),1): ans(qid,j,a,1,cid=c,nid=nn)
    for rd in r['rounds']:
        for m in rd['m']: team(m['t'],'opponent',qid)
for i,k in enumerate(SCHED+NEXT): sched(8+i,'cup-run',1,one('SELECT question_id FROM fact_question WHERE ext_id=?',f'cup-run:{k}'))
con.commit()
json.dump(REG,open(REG_PATH,'w'),ensure_ascii=False)
for t in ['fact_question','fact_answer','fact_schedule','dim_player','dim_club','dim_nation','dim_competition','dim_season','bridge_question_player','bridge_question_club','bridge_question_nation']:
    print(t, one(f'SELECT COUNT(*) FROM {t}'))
