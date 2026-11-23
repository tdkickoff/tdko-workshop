"""Adds approved puzzles for the one-a-day games to the bank (same shapes as load.py used), each with its source.
   import add_games as A; qid = A.wtb(p) / A.mix(p) / A.off(o) / A.tf(t) / A.rh(r) / A.squad(x) / A.ss(name, length)
   then optionally bank.sched(day_no, game, slot, qid); finally bank.done().
Questions added without a day are reserve; db/scheduler.py places them by rule."""
import bank as B

def _src(d): return B.source(d.get('src'), d.get('url')) if d.get('src') else None
def _clean(d): return {k: v for k, v in d.items() if k not in ('src', 'url', 'note')}

def wtb(p):
    qid, new = B.q(f'wtb:{p["name"]}', 'whos-that-baller', 'Guess the player from his career file', p['name'], _clean(p), narr=p.get('blurb'), src=_src(p))
    if new:
        pid = B.player(p['name'], p.get('position'), p.get('nationality'), p.get('aliases'))
        B.ans(qid, 0, p['name'], 1, pid=pid); [B.ans(qid, k + 1, a, 1, pid=pid) for k, a in enumerate(p.get('aliases', []))]
        B.bp(qid, pid, 'answer'); B.bn(qid, B.nation(p.get('nationality')), 'answer')
        for c in p.get('clubs', []): B.bc(qid, B.club(c[0]), 'clue')
    return qid

def mix(p):
    qid, new = B.q(f'mix:{p["name"]}', 'in-the-mixer', f'Unscramble: {p["phrase"]}', p['name'], _clean(p), narr=p.get('blurb'), src=_src(p))
    if new:
        pid = B.player(p['name'], aliases=p.get('aliases')); B.ans(qid, 0, p['name'], 1, pid=pid); B.bp(qid, pid, 'answer')
    return qid

def off(o):
    link = f'{o["a"]} / {o["b"]}' if 'a' in o else o.get('x', '')
    qid, new = B.q(f'off:{link}|{o["odd"]}', 'offside', f'Who is offside? Link: {link}', o['odd'], _clean(o), narr=o.get('note'), src=_src(o))
    if new:
        if o['kind'] == 'club' and 'a' in o: B.bc(qid, B.club(o['a']), 'category'); B.bc(qid, B.club(o['b']), 'category')
        pid = B.player(o['odd']); B.bp(qid, pid, 'answer'); B.ans(qid, 0, o['odd'], 1, pid=pid)
        for k, p in enumerate(o['eight'], 1): pp = B.player(p); B.bp(qid, pp, 'option'); B.ans(qid, k, p, 0, pid=pp)
    return qid

def tf(t):
    qid, new = B.q(f'tf:{t["id"]}', 'top-four', t['q'], ' > '.join(i[0] for i in t['items']), _clean(t), src=_src(t))
    if new:
        for k, (p, v) in enumerate(t['items']): pid = B.player(p); B.bp(qid, pid, 'in_list'); B.ans(qid, k, f'{p} ({v})', 1, pid=pid)
    return qid

def rh(r):
    qid, new = B.q(f'rh:{r["id"]}', 'ranked-highly', f'Higher or lower: {r["theme"]}', ', '.join(f'{p} {v}' for p, v in r['chain']), _clean(r), diff=r.get('d'), src=_src(r))
    if new:
        for k, (p, v) in enumerate(r['chain']): pid = B.player(p); B.bp(qid, pid, 'in_list'); B.ans(qid, k, f'{p}: {v} {r["unit"]}', 1, pid=pid)
    return qid

def squad(x):
    qid, new = B.q(f'squad:{x["id"]}', 'squad-goals', f'Name the {x["team"]} XI: {x["comp"]} {x["year"]}', x['team'], _clean(x),
                   comp_id=B.compname(x['comp']), season_id=B.season(x['year']), src=_src(x))
    if new:
        if x['type'] == 'club': B.bc(qid, B.club(x['team']), 'answer')
        else: B.bn(qid, B.nation(x['team']), 'answer')
        k = 0
        for row in x['rows']:
            for p in row:
                pid = B.player(p[0], p[1], B.CODES.get(p[2])); B.bp(qid, pid, 'answer'); B.ans(qid, k, p[0], 1, pid=pid); k += 1
    return qid

def ss(name, L, src=None):
    qid, new = B.q(f'ss:{name}', 'shirt-swap', f'{L}-letter surname on the back of the shirt', name, {'len': int(L), 'name': name},
                   diff={'5': 'E', '6': 'M', '7': 'H'}[str(L)], src=B.source(src) if src else None)
    if new: pid = B.player(name); B.bp(qid, pid, 'answer'); B.ans(qid, 0, name, 1, pid=pid)
    return qid
