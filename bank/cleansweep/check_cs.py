"""Clean Sweep checks for each day: list size/clock, no duplicate names, and no name that is one of that day's
small answer pools (1-4 players: Who's That Baller, In The Mixer, Shirt Swap, Offside odd one, Top Four),
plus the Link Up Play chain for safety. Clean Sweep itself has a large pool, so it may share names with other big-pool games (user, 18 Nov 2026)."""
import json,sys
sys.path.insert(0,'/home/claude/bank/final')
import os; os.chdir('/home/claude/bank/final')
import clash as C
LS=json.load(open('/home/claude/bank/cleansweep/lists.json')); W=C.W; bad=0
for d in range(7,28):
    L=LS[d]; ns=[x['n'] for x in L['names']]
    assert len(ns) in (10,15,20) and L['secs']=={10:180,15:240,20:300}[len(ns)] and len(set(ns))==len(ns), L['id']
    s={W['wtb'][d]['name'],W['mix'][d]['name'],W['off'][d]['odd'],W['link'][d]['start']['p'][0],*W['ss'][d].values(),*[l['p'][0] for l in W['link'][d]['links']],*[a for a,b in W['tf'][d]['items']]}
    s={C.n(x) for x in s}|({'ronaldo'} if 'ronaldo nazario' in {C.n(x) for x in s} else set())
    hit=[n for n in ns if C.n(n) in s]
    if hit: bad+=1; print('No.',d+1,L['id'],'clashes with a small-pool answer:',hit)
    if d>7:   # same list never two days running, and not repeated within the batch
        assert L['id']!=LS[d-1]['id']
ids=[LS[d]['id'] for d in range(7,28)]; assert len(set(ids))==21
print('clean sweep checks: %d problems'%bad)
