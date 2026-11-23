"""Checks the bank export matches the daily files the site serves now, game by game."""
import json, sys
sys.path.insert(0,'/home/claude/db'); from export import export
o=export(); bad=0
def fbdays(d): return [[d['Q'][i] for i in x['o']] for x in d['DAYS']]   # what players actually get each day
for g,d in o.items():
    t=open(f'/home/claude/site-build/data/{g}.js').read(); cur=json.loads(t[t.index('window.TDKO_DATA = ')+19:].strip().rstrip(';'))
    if g=='fast-break':
        t=open(f'/home/claude/site-build/data/{g}.js').read(); cur=json.loads(t[t.index('window.TDKO_DATA = ')+19:].strip().rstrip(';'))
        same=fbdays(cur)==fbdays(d); print(f"{g:17} days     {'identical' if same else 'DIFFERS'} (each day's 20 questions, in order)"); bad+=0 if same else 1; continue
    for k,v in d.items():
        a,b=cur[k],v
        if g=='fast-break' and k=='DAYS':   # the game plays each day in 'o' order; e/m/h are only a fallback, so compare them as sets
            a=[{**x,'e':sorted(x['e']),'m':sorted(x['m']),'h':sorted(x['h'])} for x in a]; b=[{**x,'e':sorted(x['e']),'m':sorted(x['m']),'h':sorted(x['h'])} for x in b]
        if a==b: print(f'{g:17} {k:9} identical ({len(a)} entries)'); continue
        bad+=1; print(f'{g:17} {k:9} DIFFERS: site {len(a)} vs bank {len(b)}')
        for i,(x,y) in enumerate(zip(a,b)):
            if x!=y: print('   first diff at', i, json.dumps(x,ensure_ascii=False)[:200], '|', json.dumps(y,ensure_ascii=False)[:200]); break
    extra=set(cur)-set(d)
    if extra: print('   site has extra keys', extra)
print('ALL IDENTICAL' if not bad else f'{bad} differences')
