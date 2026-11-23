"""Batch 4: famous transfers from 2016 on (Wikipedia list of most expensive transfers, 23 Nov 2026; every 2026 move also checked against news reports)."""
import json, random, sqlite3, collections
random.seed(32)
SRC='https://en.wikipedia.org/wiki/List_of_most_expensive_association_football_transfers'
T=[l.split('|') for l in """Neymar|Barcelona|Paris Saint-Germain|2017|e
Kylian Mbappé|Monaco|Paris Saint-Germain|2017|e
Enzo Fernández|Chelsea|Manchester City|2026|e
Alexander Isak|Newcastle United|Liverpool|2025|e
Morgan Rogers|Aston Villa|Chelsea|2026|e
Elliot Anderson|Nottingham Forest|Manchester City|2026|e
João Félix|Benfica|Atlético Madrid|2019|e
Bradley Barcola|Paris Saint-Germain|Liverpool|2026|e
Enzo Fernández|Benfica|Chelsea|2023|e
Antoine Griezmann|Atlético Madrid|Barcelona|2019|e
Philippe Coutinho|Liverpool|Barcelona|2018|e
Jack Grealish|Aston Villa|Manchester City|2021|e
Florian Wirtz|Bayer Leverkusen|Liverpool|2025|e
Declan Rice|West Ham United|Arsenal|2023|e
Moisés Caicedo|Brighton & Hove Albion|Chelsea|2023|e
Romelu Lukaku|Inter Milan|Chelsea|2021|m
Sandro Tonali|Newcastle United|Tottenham Hotspur|2026|e
Ousmane Dembélé|Borussia Dortmund|Barcelona|2017|e
Paul Pogba|Juventus|Manchester United|2016|e
Jude Bellingham|Borussia Dortmund|Real Madrid|2023|e
Eden Hazard|Chelsea|Real Madrid|2019|e
Cristiano Ronaldo|Real Madrid|Juventus|2018|e
Harry Kane|Tottenham Hotspur|Bayern Munich|2023|e
Antony|Ajax|Manchester United|2022|e
Neymar|Paris Saint-Germain|Al-Hilal|2023|e
Joško Gvardiol|RB Leipzig|Manchester City|2023|e
Gonzalo Higuaín|Napoli|Juventus|2016|m
Bruno Guimarães|Newcastle United|Arsenal|2026|e
Harry Maguire|Leicester City|Manchester United|2019|e
Jadon Sancho|Borussia Dortmund|Manchester United|2021|e
Romelu Lukaku|Everton|Manchester United|2017|e
Virgil van Dijk|Southampton|Liverpool|2018|e
Wesley Fofana|Leicester City|Chelsea|2022|m
Romelu Lukaku|Manchester United|Inter Milan|2019|m
Nicolas Pépé|Lille|Arsenal|2019|m
Kepa Arrizabalaga|Athletic Bilbao|Chelsea|2018|m
Hugo Ekitike|Eintracht Frankfurt|Liverpool|2025|m
Aurélien Tchouaméni|Monaco|Real Madrid|2022|m
Lucas Hernandez|Atlético Madrid|Bayern Munich|2019|m
Jhon Durán|Aston Villa|Al-Nassr|2025|m
Benjamin Šeško|RB Leipzig|Manchester United|2025|e""".split('\n')]
CHECK={('Enzo Fernández',2026):'https://www.aljazeera.com/sports/2026/9/1/fernandez-transfers-to-man-city-from-chelsea-in-joint-british-record-fee',
 ('Morgan Rogers',2026):'https://www.chelseafc.com/en/news/article/morgan-rogers-signs-for-chelsea',('Elliot Anderson',2026):'https://www.mancity.com/news/mens/elliot-anderson-signs-for-man-city-63920416',
 ('Bradley Barcola',2026):'https://www.liverpoolfc.com/news/liverpool-sign-bradley-barcola-paris-saint-germain',('Bruno Guimarães',2026):'https://www.espn.com/soccer/story/_/id/49511174/arsenal-sign-bruno-guimaraes-newcastle',
 ('Sandro Tonali',2026):'https://www.newcastleunited.com/en/news/sandro-tonali-leaves-newcastle-united-for-tottenham-hotspur'}
BIG=['Manchester City','Manchester United','Liverpool','Chelsea','Arsenal','Tottenham Hotspur','Real Madrid','Barcelona','Atlético Madrid','Bayern Munich','Paris Saint-Germain','Juventus','Inter Milan','Newcastle United']
c=sqlite3.connect('/home/claude/db/tdko.db'); FB=' || '.join(json.loads(p)['q'] for (p,) in c.execute("select payload from fact_question where game_id=1"))
out=[]
for p,fr,to,y,d in T:
    y=int(y)
    if f"{p}" in FB and str(y) in FB and (fr in FB or to in FB):   # rough: skip if the bank already asks about this move
        if any(seg for seg in FB.split(' || ') if p in seg and str(y) in seg): continue
    note=f"{p}: {fr} to {to}, {y}"+(f" (also checked: {CHECK[(p,y)]})" if (p,y) in CHECK else '')
    w=[x for x in BIG if x not in (to,fr)]; random.shuffle(w)
    out.append(dict(comp='Transfers',kind='other',year=y,q=f"Which club did {p} join from {fr} in {y}?",a=to,wrong=w[:3],d=d,src=SRC,note=note))
    w=[x for x in BIG if x not in (to,fr)]; random.shuffle(w)
    out.append(dict(comp='Transfers',kind='other',year=y,q=f"Which club sold {p} to {to} in {y}?",a=fr,wrong=w[:3],d='m' if d=='e' else 'h',src=SRC,note=note))
json.dump(out,open('/home/claude/bank/fbgap/batch4.json','w'),ensure_ascii=False,indent=1)
print(len(out),collections.Counter(q['d'] for q in out))
