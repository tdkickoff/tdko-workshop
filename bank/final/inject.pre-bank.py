"""Moves each game's daily puzzles out of the game code into data/<game>.js (built from final28.json).
The game source keeps one line per array: const NAME = TDKO_DATA.NAME;"""
import json,os,hashlib
W=json.load(open('/home/claude/bank/final/final28.json'))
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
T={'one-touch':('fast-break',[('Q',W['fb']['Q']),('DAYS',W['fb']['DAYS'])]),'whos-that-baller':('whos-that-baller',[('PLAYERS',W['wtb'])]),
   'scramble-head':('in-the-mixer',[('PUZZLES',W['mix'])]),'pass-and-connect':('link-up-play',[('CHAINS',W['link'])]),'who-playedle':('squad-goals',[('XIS',W['squad'])]),
   'shirt-swap':('shirt-swap',[('ANSWERS',W['ss'])]),'tiki-taka-toe':('tiki-taka-toe',[('GRIDS',W['tiki'])]),'offside':('offside',[('PUZZLES',W['off'])]),
   'top-four':('top-four',[('QUESTIONS',W['tf'])]),'ranked-highly':('ranked-highly',[('CHAINS',W['rh'])]),
   'clean-sweep':('clean-sweep',[('LISTS',json.load(open('/home/claude/bank/cleansweep/lists.json')))])}  # public from No. 8
T['cup-run']=('cup-run',[('RUNS',json.load(open('/home/claude/bank/cuprun/runs.json'))['runs'])])  # public from Mon 23 Nov (No. 8)
os.makedirs('/home/claude/site-build/data',exist_ok=True)
for f,(gid,arrs) in T.items():
    p=f'/home/claude/{f}.html'; s=open(p).read()
    for name,val in arrs:
        a,b=span(s,name); s=s[:a]+'TDKO_DATA.'+name+s[b:]
    open(p,'w').write(s)
    js='/* The Daily Kick Off: daily puzzles for '+gid+'. Built from the approved sign-off sheet; one entry per day, No. 1 = Mon 16 Nov 2026. */\nwindow.TDKO_DATA = '+json.dumps({n:v for n,v in arrs},ensure_ascii=False)+';\n'
    open(f'/home/claude/site-build/data/{gid}.js','w').write(js)
    print(gid, len(js)//1024,'KB', hashlib.md5(js.encode()).hexdigest()[:8])
