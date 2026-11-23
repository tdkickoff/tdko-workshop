"""Writes each game's daily puzzles to data/<game>.js FROM THE QUESTION BANK (db/tdko.db, via db/export.py). The bank is the master copy.
The game source keeps one line per array: const NAME = TDKO_DATA.NAME;"""
import json,os,hashlib
import sys; sys.path.insert(0,'/home/claude/db'); from export import export
E=export()
def span(s,name):
    i=s.index('const '+name+' = ')+len('const '+name+' = '); d=0;q=None;k=i
    if s.startswith('TDKO_DATA.',i): return i, s.index(';',i)
    while k<len(s):
        c=s[k]
        if q:
            if c=='\\': k+=2; continue
            if c==q: q=None
        elif c in '"\'`': q=c
        elif c in '[{': d+=1
        elif c in ']}':
            d-=1
            if d==0: return i,k+1
        k+=1
SRC={'one-touch':'fast-break','whos-that-baller':'whos-that-baller','scramble-head':'in-the-mixer','pass-and-connect':'link-up-play','who-playedle':'squad-goals',
     'shirt-swap':'shirt-swap','tiki-taka-toe':'tiki-taka-toe','offside':'offside','top-four':'top-four','ranked-highly':'ranked-highly','clean-sweep':'clean-sweep','cup-run':'cup-run'}
T={f:(gid,list(E[gid].items())) for f,gid in SRC.items()}
os.makedirs('/home/claude/site-build/data',exist_ok=True)
for f,(gid,arrs) in T.items():
    p=f'/home/claude/{f}.html'; s=open(p).read()
    for name,val in arrs:
        a,b=span(s,name); s=s[:a]+'TDKO_DATA.'+name+s[b:]
    open(p,'w').write(s)
    js='/* The Daily Kick Off: daily puzzles for '+gid+'. Built from the approved sign-off sheet; one entry per day, No. 1 = Mon 16 Nov 2026. */\nwindow.TDKO_DATA = '+json.dumps({n:v for n,v in arrs},ensure_ascii=False)+';\n'
    open(f'/home/claude/site-build/data/{gid}.js','w').write(js)
    print(gid, len(js)//1024,'KB', hashlib.md5(js.encode()).hexdigest()[:8])
