"""Bank checks, run before every go-live. All SQL against tdko.db.
1. Reuse: no question scheduled twice within 56 days (8 weeks) in the same game.
2. Clash: small-pool games must not share an answer on the same day (Who's That Baller, In The Mixer, Shirt Swap, Offside odd one out, Top Four).
3. Gaps: every game has a puzzle for every day up to its last scheduled day."""
import sqlite3, sys
import os
c=sqlite3.connect(os.environ.get('TDKO_DB','/home/claude/db/tdko.db')); bad=0
# days before a game went public were never shown, so they don't count as a use
FROM={'ranked-highly':'2026-11-19','clean-sweep':'2026-11-23','cup-run':'2026-11-23'}
c.execute('CREATE TEMP TABLE live_from(slug TEXT PRIMARY KEY, d TEXT)'); c.executemany('INSERT INTO live_from VALUES(?,?)',FROM.items())
print('1. Reuse within 8 weeks')
for r in c.execute('''SELECT g.name, q.answer, a.date, b.date FROM fact_schedule s1 JOIN fact_schedule s2 ON s1.question_id=s2.question_id AND s1.date_key<s2.date_key
    JOIN dim_date a ON a.date_key=s1.date_key JOIN dim_date b ON b.date_key=s2.date_key JOIN fact_question q ON q.question_id=s1.question_id JOIN dim_game g ON g.game_id=s1.game_id
    WHERE julianday(b.date)-julianday(a.date) < 56 AND a.date >= COALESCE((SELECT d FROM live_from WHERE slug=g.slug),'2026-11-16')'''): bad+=1; print('  ',r)
print('2. Same-day answer clash (small-pool games)')
for r in c.execute('''WITH x AS (SELECT s.date_key, g.slug, p.name FROM fact_schedule s JOIN dim_game g USING(game_id) JOIN bridge_question_player b ON b.question_id=s.question_id
      JOIN dim_player p USING(player_id) WHERE b.role IN ('answer','in_list') AND g.slug IN ('whos-that-baller','in-the-mixer','shirt-swap','offside','top-four'))
    SELECT d.date, x1.name, x1.slug, x2.slug FROM x x1 JOIN x x2 ON x1.date_key=x2.date_key AND x1.name=x2.name AND x1.slug<x2.slug JOIN dim_date d ON d.date_key=x1.date_key ORDER BY 1'''):
    bad+=1; print('  ',r)
print('3. Schedule gaps')
for g,lo,hi,n in c.execute('''SELECT g.name, MIN(d.day_no), MAX(d.day_no), COUNT(DISTINCT d.day_no) FROM fact_schedule s JOIN dim_date d USING(date_key) JOIN dim_game g USING(game_id) GROUP BY 1'''):
    if hi-lo+1!=n: bad+=1; print('  ',g,'missing days between',lo,hi)
    else: print(f'   {g}: No. {lo}-{hi} complete')
# Shirt Swap: every answer surname must be a valid guess (in the game's squad list), or players could never type it
def shirt_swap_words():
    import re, json, unicodedata, sqlite3, os
    s = open('/home/claude/shirt-swap.html').read()
    W = json.loads(re.search(r'WORDS\s*=\s*(\{.*?\})\s*[,;]', s, re.S).group(1))
    c = sqlite3.connect(os.environ.get('TDKO_DB', '/home/claude/db/tdko.db')); bad = []
    for (p,) in c.execute("SELECT payload FROM fact_question q JOIN dim_game g USING(game_id) WHERE g.slug='shirt-swap' AND q.status<>'retired'"):
        p = json.loads(p); w = unicodedata.normalize('NFD', p['name'].split()[-1]).encode('ascii', 'ignore').decode().upper().replace("'", '')
        if w not in W[str(p['len'])]: bad.append(p['name'])
    print('Shirt Swap answers missing from the guess list:', bad or 'none')
    return not bad
if not shirt_swap_words(): bad += 1
# drafts must never reach the live games: nothing on the calendar may be unapproved
def no_scheduled_drafts():
    import sqlite3, os
    c = sqlite3.connect(os.environ.get('TDKO_DB', '/home/claude/db/tdko.db'))
    n = c.execute("SELECT COUNT(*) FROM fact_schedule s JOIN fact_question q USING(question_id) WHERE q.status<>'approved'").fetchone()[0]
    print('Unapproved puzzles on the calendar:', n or 'none'); return n == 0
if not no_scheduled_drafts(): bad += 1
print('OK' if not bad else f'{bad} problem(s)'); sys.exit(1 if bad else 0)
