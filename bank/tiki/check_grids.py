import json,re
s=open('/home/claude/tiki-taka-toe.html').read()
L=re.search(r'const LEAGUES = (\{.*?\});',s,re.S).group(1)
L=json.loads(re.sub(r'(\w+):\[',r'"\1":[',L).replace("'",'"'))
P=json.load(open('/home/claude/bank/tiki/players.json'))
T=json.load(open('/home/claude/bank/final/final28.json'))['tiki']
def one(p,c):
    k,v=c
    if k=='club': return v in p['clubs']
    if k=='nat': return v in p['nat']
    if k=='league': return any(x in L[v] for x in p['clubs'])
    if k=='hon': return bool(p[v])
def fits(p,a,b):
    if a[0]=='hon' and b[0]=='hon': return bool(p[a[1]]) and bool(p[b[1]])
    for h,o in ((a,b),(b,a)):
        if h[0]=='hon' and o[0]=='club': return o[1] in p[h[1]]
    return one(p,a) and one(p,b)
def cells(g):
    return [[p['name'] for p in P if fits(p,r,c)] for r in g['r'] for c in g['c']]
if __name__=='__main__':
    import sys
    for i,g in enumerate(T):
        cs=cells(g); counts=[len(x) for x in cs]
        flag=' <<< EMPTY' if min(counts)==0 else (' < thin' if min(counts)<3 else '')
        print(i+1,counts,flag)
        # examples still valid?
        bad=[ (k,n) for k,n in enumerate(g['ex']) if n not in cs[k]]
        if bad: print('   example invalid:',bad)
