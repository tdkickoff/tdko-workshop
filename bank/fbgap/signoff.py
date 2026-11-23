"""Sign-off page for a Fast Break batch. Usage: python3 signoff.py batch2.json out.html "Title" "Heading" "Lede html" """
import json,html,collections,sys,re
B=json.load(open(sys.argv[1])); out=sys.argv[2]; title,head,lede=sys.argv[3],sys.argv[4],sys.argv[5]
css=open('/tmp/claude-0/-home-claude/dc39d1a6-6cbf-5f53-97ab-04ac97cd342b/scratchpad/fb-signoff.html').read(); css=css[css.index('<link'):css.index('</style>')+8]
E=html.escape; LV={'e':'Easy','m':'Medium','h':'Hard'}
KN={'winner':'Who won','runner-up':'Who they beat / finished second','venue':'Hosts','scorer':'Golden Boot','other':''}
cnt=collections.Counter(q['d'] for q in B)
body=f'<div class="wrap"><span class="eb">The Daily Kick Off · Fast Break bank · for sign-off</span><h1>{head}</h1><p class="lede">{lede}</p><p class="lede"><b>Totals:</b> {cnt["e"]} Easy, {cnt["m"]} Medium, {cnt["h"]} Hard ({len(B)} questions). Tell me any to cut, re-grade or reword.</p>'
groups=collections.OrderedDict()
for q in B: groups.setdefault((q['comp'],q['kind']),[]).append(q)
n=0
for (comp,kind),qs in groups.items():
    qs.sort(key=lambda q:(q['year'] or 0, {'e':0,'m':1,'h':2}[q['d']]))
    body+=f'<section><h2>{E(comp)}{(" · "+KN[kind]) if KN.get(kind) else ""} <span>{len(qs)}</span></h2><div class="tw"><table><thead><tr><th>#</th><th>Question and options (correct first)</th><th>Level</th><th>Source</th></tr></thead><tbody>'
    for q in qs:
        n+=1; sname=re.sub(r'_',' ',q['src'].rsplit('/',1)[1]); sname=html.unescape(__import__('urllib.parse').parse.unquote(sname))
        body+=f'<tr class="{q["d"]}"><td class="n">{n}</td><td><b>{E(q["q"])}</b><div class="opts"><span class="ok">{E(q["a"])}</span>'+''.join(f'<span>{E(w)}</span>' for w in q['wrong'])+'</div>'+(f'<div class="eb" style="margin-top:4px;text-transform:none;letter-spacing:0">{E(q["note"])}</div>' if q.get('note') else '')+f'</td><td class="lv">{LV[q["d"]]}</td><td class="src"><a href="{q["src"]}" target="_blank" rel="noopener">{E(sname)}</a></td></tr>'
    body+='</tbody></table></div></section>'
open(out,'w').write(f'<title>{title}</title>\n'+css+'\n'+body+'</div>'); print(n)
