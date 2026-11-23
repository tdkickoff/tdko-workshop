"""Picks each day's puzzles from the approved bank by rule. You approve questions once, when they enter the bank; this decides the days.

Rules (agreed with the owner, 23 Nov 2026):
  * Reuse gap: Fast Break 8 weeks (56 days); every other game 6 months (182 days). Checked both ways around the day.
  * Fast Break mix from No. 36: 15 Easy, 4 Medium, 1 Hard, played in that order (easy first).
  * No same-day answer clash across the small-pool games (Who's That Baller, In The Mixer, Shirt Swap, Offside odd one out, Top Four).
  * Fast Break: one question per final/tournament a day, no answer repeated in a day, and at most 2 of the same shape a day
    (e.g. 'who won the FA Cup final'), so a day stays varied.
  * No missing days: days are filled in order; if a game runs out of stock the run stops for that game and says so.
  * Choice: questions never used come first, then the longest-unused; ties broken by a fixed shuffle so a run can be repeated exactly.

Use:  python3 scheduler.py --to 42            fill every game up to No. 42 (dry run, prints the plan)
      python3 scheduler.py --to 42 --write    write it to the bank (then run checks.py)
      python3 scheduler.py --stock            how far the stock can go for each game"""
import sqlite3, json, random, sys, datetime, argparse, collections
import os
DB = os.environ.get('TDKO_DB', '/home/claude/db/tdko.db')
LAUNCH = datetime.date(2026, 11, 16)
GAP = collections.defaultdict(lambda: 182, {'fast-break': 56})
FB_MIX = {'e': 15, 'm': 4, 'h': 1}
FB_MIX_FROM = 36
SMALL_POOL = {'whos-that-baller', 'in-the-mixer', 'shirt-swap', 'offside', 'top-four'}
SLOTS = {'shirt-swap': [5, 6, 7]}
FB_SAME_SHAPE = 2   # Fast Break variety: at most 2 questions of the same shape a day (e.g. 'who won the FA Cup final')
import re
_COMP=[('Champions League',r"champions league|european cup"),('Europa League',r"europa league|uefa cup"),("Cup Winners' Cup",r"cup winners"),('FA Cup',r"fa cup"),
 ('League Cup',r"league cup|carabao|carling"),("Women's World Cup",r"women's world cup"),("Women's Euros",r"women's euro"),('World Cup',r"world cup"),('Euros',r"\beuros?\b|european championship"),
 ('Copa América',r"copa am"),('AFCON',r"afcon|africa cup of nations"),('Premier League',r"premier league|title"),("Ballon d'Or",r"ballon"),('Golden Boot',r"golden boot"),('PFA',r"pfa")]
def _shape(t):
    tl=t.lower(); comp=next((n for n,rx in _COMP if re.search(rx,tl)),None)
    m=re.search(r"\b(19[5-9]\d|20[0-2]\d)",t); yr=int(m.group(1)) if m else None
    kind=('runner-up' if re.search(r"\b(who|which \w+) did .* beat|against whom|runners?-up",tl) else 'venue' if re.search(r"city|stadium|where|hosted",tl)
          else 'manager' if re.search(r"manag|coach",tl) else 'scorer' if re.search(r"scor|golden boot|goals",tl) else 'winner' if re.search(r"\bwon\b|\bwin\b|winners?|champions",tl) else 'other')
    return (comp,kind) if comp else ('other',kind), (comp,yr) if comp and yr else None   # Shirt Swap: one name of each length a day (slot = letters)

def connect(db=DB):
    c = sqlite3.connect(db); c.row_factory = sqlite3.Row; return c

def date_key(no):
    d = LAUNCH + datetime.timedelta(days=no - 1); return int(d.strftime('%Y%m%d')), d

def ensure_day(c, no):
    k, d = date_key(no)
    c.execute('INSERT OR IGNORE INTO dim_date VALUES(?,?,?,?,NULL)', (k, d.isoformat(), no, d.strftime('%A'))); return k

class Bank:
    def __init__(self, c):
        self.c = c
        self.games = {r['slug']: r['game_id'] for r in c.execute('SELECT game_id, slug FROM dim_game')}
        # every approved question with what the rules need
        self.q = {}
        for r in c.execute("""SELECT q.question_id, g.slug, q.answer, q.payload, d.code AS diff, q.competition_id, q.season_id
                              FROM fact_question q JOIN dim_game g USING(game_id) LEFT JOIN dim_difficulty d USING(difficulty_id)
                              WHERE q.status = 'approved'"""):
            p = json.loads(r['payload'])
            self.q[r['question_id']] = dict(id=r['question_id'], game=r['slug'], answer=r['answer'], diff=(r['diff'] or '').lower(),
                                            final=(r['competition_id'], r['season_id']) if r['competition_id'] and r['season_id'] else None,
                                            length=p.get('len'))
            if r['slug'] == 'fast-break':
                sh, topic = _shape(p.get('q', ''))
                self.q[r['question_id']].update(shape=sh, topic=topic or self.q[r['question_id']]['final'])
        self.players = collections.defaultdict(set)   # answer players, for the same-day clash rule
        for r in c.execute("SELECT question_id, p.name FROM bridge_question_player b JOIN dim_player p USING(player_id) WHERE b.role IN ('answer','in_list')"):
            self.players[r['question_id']].add(r['name'])
        self.used = collections.defaultdict(list)     # question -> day numbers it is scheduled on
        self.days = collections.defaultdict(dict)     # game -> {day_no: [(slot, qid)]}
        for r in c.execute('SELECT g.slug, d.day_no, s.slot, s.question_id FROM fact_schedule s JOIN dim_date d USING(date_key) JOIN dim_game g USING(game_id)'):
            self.used[r['question_id']].append(r['day_no']); self.days[r['slug']].setdefault(r['day_no'], []).append((r['slot'], r['question_id']))

    def free(self, qid, no):
        return all(abs(no - u) >= GAP[self.q[qid]['game']] for u in self.used[qid])

    def last_used(self, qid):
        return max(self.used[qid]) if self.used[qid] else -10**6

    def day_players(self, no, skip_game):
        out = set()
        for g in SMALL_POOL - {skip_game}:
            for _, q in self.days[g].get(no, []): out |= self.players[q]
        return out

    def pick(self, game, no, seed):
        rnd = random.Random(f'{seed}:{game}:{no}')
        pool = [q for q in self.q.values() if q['game'] == game and self.free(q['id'], no)]
        rnd.shuffle(pool); pool.sort(key=lambda q: self.last_used(q['id']))        # never used first, then longest unused
        taken = self.day_players(no, game) if game in SMALL_POOL else set()
        if game == 'fast-break':
            mix = FB_MIX if no >= FB_MIX_FROM else None
            if mix is None: return None, 'before No. %d the Fast Break mix was set by hand' % FB_MIX_FROM
            chosen, finals, answers, shapes = [], set(), set(), collections.Counter()
            for lvl in ('e', 'm', 'h'):
                got = 0
                for q in pool:
                    if got == mix[lvl]: break
                    if q['diff'] != lvl or q['id'] in [x['id'] for x in chosen]: continue
                    if q['topic'] and q['topic'] in finals: continue          # one question per final/tournament a day
                    if q['answer'].lower() in answers: continue
                    if q['shape'][0] != 'other' and shapes[q['shape']] >= FB_SAME_SHAPE: continue
                    chosen.append(q); got += 1; answers.add(q['answer'].lower()); shapes[q['shape']] += 1
                    if q['topic']: finals.add(q['topic'])
                if got < mix[lvl]: return None, f'not enough {lvl.upper()} questions free (needs {mix[lvl]}, found {got})'
            return [(i + 1, q['id']) for i, q in enumerate(chosen)], None
        slots = SLOTS.get(game, [1]); out = []
        for s in slots:
            ok = [q for q in pool if (q['length'] == s if game == 'shirt-swap' else True)
                  and not (self.players[q['id']] & taken) and q['id'] not in [x for _, x in out]]
            if not ok: return None, f'no puzzle free for slot {s}'
            out.append((s, ok[0]['id'])); taken |= self.players[ok[0]['id']]
        return out, None

    def place(self, game, no, picks):
        self.days[game][no] = picks
        for _, q in picks: self.used[q].append(no)

def run(to, write=False, seed=2026, db=DB, games=None):
    c = connect(db); b = Bank(c); report = {}
    order = sorted(b.games, key=lambda g: (g not in SMALL_POOL, g))   # small-pool games first so clashes are settled early
    for g in (games or order):
        days = b.days[g]; start = (max(days) + 1) if days else 1; filled, why = [], None
        for no in range(start, to + 1):
            picks, why = b.pick(g, no, seed)
            if picks is None: break
            b.place(g, no, picks); filled.append(no)
            if write:
                k = ensure_day(c, no)
                for s, q in picks: c.execute('INSERT INTO fact_schedule VALUES(?,?,?,?)', (k, b.games[g], s, q))
        report[g] = dict(from_=start, filled=filled, stopped=why if filled[-1:] != [to] and start <= to else None)
    if write: c.commit()
    return report, b

def stock():
    c = connect(); b = Bank(c)
    for g in sorted(b.games):
        qs = [q for q in b.q.values() if q['game'] == g]
        need = GAP[g] * (sum(FB_MIX.values()) if g == 'fast-break' else len(SLOTS.get(g, [1])))
        line = f'{g:17} approved {len(qs):4}  needed for a {GAP[g]}-day gap {need:5}'
        if g == 'fast-break':
            cnt = collections.Counter(q['diff'] for q in qs)
            line += '   ' + '  '.join(f"{l.upper()} {cnt[l]}/{FB_MIX[l] * GAP[g]}" for l in 'emh')
        print(line)

if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--to', type=int); ap.add_argument('--write', action='store_true'); ap.add_argument('--stock', action='store_true')
    ap.add_argument('--db', default=DB); a = ap.parse_args()
    if a.stock: stock(); sys.exit()
    rep, _ = run(a.to, a.write, db=a.db)
    for g, r in sorted(rep.items()):
        f = r['filled']; print(f"{g:17} " + (f"No. {f[0]}-{f[-1]} filled" if f else 'nothing filled') + (f"; stopped at No. {(f[-1] + 1) if f else r['from_']}: {r['stopped']}" if r['stopped'] else ''))
    print('WRITTEN' if a.write else 'dry run: nothing written')
