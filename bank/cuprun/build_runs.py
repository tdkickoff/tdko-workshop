import json,sys
sys.path.insert(0,'/home/claude/bank/cuprun')
from intl import RUNS as INTL, SCHED
from club import CLUB
ALL={**INTL,**CLUB}
NEXT=['mun-facup-2024','esp-euro-2024','whu-uecl-2023','arg-copa-2024','wig-facup-2013','liv-facup-2022','ger-euro-1996']   # No. 29-35
SPARE=[k for k in ['por-facup-2008','mun-uel-2017','esp-euro-2008','cmr-afcon-2017','bra-wc-1994'] if k not in NEXT]
def clean(r): r=dict(r); r.pop('lvl',None); return r
order=SCHED+NEXT
runs=[clean(ALL['esp-euro-2024'])]*7+[clean(ALL[k]) for k in order]
json.dump({'test':clean(ALL['esp-euro-2024']),'runs':runs,'schedule':{str(i+8):k for i,k in enumerate(order)},'spare':SPARE,'all':ALL},open('/home/claude/bank/cuprun/runs.json','w'),ensure_ascii=False,indent=1)
print(len(runs), SPARE)
