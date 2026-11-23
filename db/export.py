"""The bank is the master: builds each game's daily puzzle data from tdko.db.
Order = fact_schedule by date (No. 1 = Mon 16 Nov 2026). Returns {game_slug: {ARRAY_NAME: value}} exactly as the games read it.
Games that opened later (Clean Sweep, Cup Run from No. 8) are padded before their first day with their test puzzle (never shown: those pages were closed)."""
import sqlite3, json
DB='/home/claude/db/tdko.db'
NAMES={'fast-break':None,'whos-that-baller':'PLAYERS','in-the-mixer':'PUZZLES','link-up-play':'CHAINS','squad-goals':'XIS','shirt-swap':'ANSWERS',
       'tiki-taka-toe':'GRIDS','offside':'PUZZLES','top-four':'QUESTIONS','ranked-highly':'CHAINS','clean-sweep':'LISTS','cup-run':'RUNS'}
PAD={'clean-sweep':'cs:ballon-dor-since-2000','cup-run':'cup-run:esp-euro-2024'}
def export(db=DB):
    c=sqlite3.connect(db); c.row_factory=sqlite3.Row
    slug={r['game_id']:r['slug'] for r in c.execute('SELECT game_id, slug FROM dim_game')}
    pl=lambda qid: json.loads(c.execute('SELECT payload FROM fact_question WHERE question_id=?',(qid,)).fetchone()[0])
    rows=c.execute('''SELECT g.slug, d.day_no AS no, s.slot, s.question_id AS qid FROM fact_schedule s JOIN dim_date d USING(date_key)
                      JOIN dim_game g USING(game_id) ORDER BY g.slug, d.day_no, s.slot''').fetchall()
    drafts=c.execute("SELECT COUNT(*) FROM fact_schedule s JOIN fact_question q USING(question_id) WHERE q.status<>'approved'").fetchone()[0]
    assert drafts==0, f'{drafts} unapproved puzzle(s) on the calendar: approve them or take them off before building'
    by={}
    for r in rows: by.setdefault(r['slug'],{}).setdefault(r['no'],[]).append((r['slot'],r['qid']))
    out={}
    for g,days in by.items():
        nos=sorted(days); assert nos==list(range(nos[0],nos[-1]+1)), f'{g}: gap in schedule'
        if g=='fast-break':
            Q=[]; ix={}
            # only questions that are on a day go to the site (the unscheduled reserve stays private), numbered in bank order
            sched={q for n in nos for _,q in days[n]}
            order=sorted(((int(r['ext_id'].split(':')[1]),r['question_id']) for r in c.execute("SELECT question_id, ext_id FROM fact_question WHERE ext_id LIKE 'fast-break:%'") if r['question_id'] in sched))
            for i,(_,qid) in enumerate(order): ix[qid]=i; p=pl(qid); Q.append([p['q'],p['options'],p['d']])
            DAYS=[]
            for n in nos:
                o=[ix[q] for _,q in sorted(days[n])]
                DAYS.append({'e':[i for i in o if Q[i][2]=='e'],'m':[i for i in o if Q[i][2]=='m'],'h':[i for i in o if Q[i][2]=='h'],'o':o})
            out[g]={'Q':Q,'DAYS':DAYS}; continue
        if g=='shirt-swap':
            arr=[{str(pl(q)['len']):pl(q)['name'] for _,q in sorted(days[n])} for n in nos]
        else:
            arr=[pl(days[n][0][1]) for n in nos]
        if nos[0]>1:
            pad=pl(c.execute('SELECT question_id FROM fact_question WHERE ext_id=?',(PAD[g],)).fetchone()[0])
            arr=[pad]*(nos[0]-1)+arr
        if g=='cup-run':
            for a in arr: a.pop('lvl',None)
        out[g]={NAMES[g]:arr}
    return out
if __name__=='__main__':
    o=export(); print({g:{k:len(v) for k,v in d.items()} for g,d in o.items()})
