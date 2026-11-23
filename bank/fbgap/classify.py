"""Sorts every Fast Break question in the bank into competition x question type x year, to find the gaps since 1990."""
import json, re, sqlite3, collections
c=sqlite3.connect('/home/claude/db/tdko.db')
Q=[(e,json.loads(p)) for e,p in c.execute("SELECT ext_id,payload FROM fact_question WHERE ext_id LIKE 'fast-break:%'")]
COMP=[('Champions League',r"champions league|european cup"),('Europa League',r"europa league|uefa cup"),("Cup Winners' Cup",r"cup winners"),
 ('Conference League',r"conference league"),('FA Cup',r"fa cup"),('League Cup',r"league cup|carabao|carling|capital one"),
 ("Women's World Cup",r"women's world cup"),("Women's Euros",r"women's euro"),('World Cup',r"world cup"),('Euros',r"\beuros?\b|european championship"),
 ('Copa América',r"copa am"),('AFCON',r"afcon|africa cup of nations"),('Asian Cup',r"asian cup"),('Premier League',r"premier league|title|league champions|first division"),
 ("Ballon d'Or",r"ballon"),('PL Golden Boot',r"golden boot"),('PFA',r"pfa"),('Community Shield',r"community shield"),('Club World Cup',r"club world cup"),('Super Cup',r"super cup")]
def year(t):
    m=re.search(r"\b(19[5-9]\d|20[0-2]\d)(?:[–-](\d{2}))?\b",t) or re.search(r"\bEuro (\d{2})\b",t)
    if not m: return None
    y=m.group(1); y=int(y) if len(y)==4 else (1900+int(y) if int(y)>50 else 2000+int(y))
    return y+1 if m.group(0).count('–') or m.group(0).count('-') else y   # season 2007–08 -> 2008
def kind(t):
    tl=t.lower()
    if re.search(r"\b(who|which \w+) did .* beat|beat whom|against whom|lose to|lost (the|to)|runners?-up|who did .* face",tl): return 'runner-up'
    if re.search(r"which city|in which city|what city|stadium|where was|which ground|venue|hosted",tl): return 'venue'
    if re.search(r"manag|coach",tl): return 'manager'
    if re.search(r"scored|scorer|golden boot|top scorer|goals",tl): return 'scorer'
    if re.search(r"captain",tl): return 'captain'
    if re.search(r"\bwon\b|\bwin\b|winners?|champions|lift|beat|clinch",tl): return 'winner'
    return 'other'
rows=[]
for e,p in Q:
    t=p['q']; comp=next((n for n,rx in COMP if re.search(rx,t.lower())),None)
    rows.append({'ext':e,'q':t,'a':p['options'][0],'d':p['d'],'comp':comp,'kind':kind(t),'year':year(t)})
json.dump(rows,open('/home/claude/bank/fbgap/classified.json','w'),ensure_ascii=False,indent=0)
cnt=collections.Counter((r['comp'],r['kind']) for r in rows if r['comp'])
print('no competition:',sum(1 for r in rows if not r['comp']))
for (cm,k),n in sorted(cnt.items(),key=lambda x:(-x[1])): print(f'{n:4}  {cm:20} {k}')
