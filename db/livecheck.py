"""Live-stat re-checks. Puzzles flagged live=1 hold a number that can still change (an active player's goals, caps...).
   python3 livecheck.py                 list flagged puzzles on the calendar for tomorrow
   python3 livecheck.py --date 2026-12-20 / --all
   python3 livecheck.py --ok EXT_ID     mark one as re-checked today (after confirming against its source)
   python3 livecheck.py --flag EXT_ID "what to check"   /  --unflag EXT_ID
If a number has moved: edit the puzzle (or swap it) in the bank, run checks.py and make_seed.py, preview, go live."""
import sqlite3, sys, os, datetime
c = sqlite3.connect(os.environ.get('TDKO_DB', '/home/claude/db/tdko.db'))
a = sys.argv[1:]
if a[:1] == ['--ok']:
    c.execute("UPDATE fact_question SET checked_on=date('now') WHERE ext_id=?", (a[1],)); c.commit(); print('checked', a[1]); sys.exit()
if a[:1] == ['--flag']:
    c.execute("UPDATE fact_question SET live=1, live_note=? WHERE ext_id=?", (a[2], a[1])); c.commit(); print('flagged', a[1]); sys.exit()
if a[:1] == ['--unflag']:
    c.execute("UPDATE fact_question SET live=0 WHERE ext_id=?", (a[1],)); c.commit(); print('unflagged', a[1]); sys.exit()
day = a[1] if a[:1] == ['--date'] else (datetime.date.today() + datetime.timedelta(days=1)).isoformat()
where, args = ("d.date>=date('now')", ()) if a[:1] == ['--all'] else ("d.date=?", (day,))
rows = c.execute(f"""SELECT d.date, g.name, q.ext_id, q.prompt, q.live_note, q.checked_on, s.url FROM fact_schedule f JOIN fact_question q USING(question_id)
    JOIN dim_date d USING(date_key) JOIN dim_game g ON g.game_id=q.game_id LEFT JOIN dim_source s ON s.source_id=q.source_id
    WHERE q.live=1 AND {where} ORDER BY d.date""", args).fetchall()
for r in rows: print(' | '.join(str(x) for x in r))
print(len(rows), 'to re-check' + ('' if a[:1] == ['--all'] else f' for {day}'))
