"""Adds an approved Fast Break batch to the bank as reserve (not scheduled). Usage: python3 add_batch.py batch1.json"""
import json, sys
sys.path.insert(0,'/home/claude/db'); import bank
COMPS={'FA Cup','League Cup','Champions League','Europa League','World Cup','Euros'}   # real competitions; other shapes (stadiums, nicknames, transfers...) have none
B=json.load(open(sys.argv[1])); n0=bank.one("SELECT COUNT(*) FROM fact_question WHERE game_id=1")
nxt=n0
for q in B:
    ext=f"fast-break:{nxt}"
    qid,new=bank.q(ext,'fast-break',q['q'],q['a'],{'q':q['q'],'options':[q['a']]+q['wrong'],'d':q['d']},diff=q['d'],
                   comp_id=bank.compname(q['comp']+' final') if q['comp'] in COMPS else None,season_id=bank.season(str(q['year'])) if q.get('year') else None,src=bank.source(__import__('urllib.parse').parse.unquote(q['src'].rstrip('/').rsplit('/',1)[1]).replace('_',' ').replace('.html','').replace('.htm',''),q['src']),narr=q.get('note'))
    if new:
        nxt+=1
        for j,o in enumerate([q['a']]+q['wrong']): bank.ans(qid,j,o,1 if j==0 else 0)
bank.done(); print('added',nxt-n0,'Fast Break questions; bank now',bank.one("SELECT COUNT(*) FROM fact_question WHERE game_id=1"))
