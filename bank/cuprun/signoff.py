import sys,datetime,html,json
sys.path.insert(0,'/home/claude/bank/cuprun')
from build_runs import ALL,SCHED,NEXT,SPARE
e=html.escape; L={'E':'Easy','M':'Medium','H':'Hard'}
def ic(t,big=False):
    if 'c' in t: return f'<svg viewBox="0 0 26 30" class="cr{" big" if big else ""}" data-t=\'{e(json.dumps(t))}\'></svg>'
    return f'<svg viewBox="0 0 30 20" class="f{" big" if big else ""}" data-c="{t["code"]}"></svg>'
def card(no,k,date=None):
    r=ALL[k]
    route=''.join(f'<li><span class="rn">{e(x["r"])}</span><span class="ms">'+''.join(f'<span class="m">{ic(m["t"])}{e(m["t"]["n"])}<b>{e(m.get("s",""))}</b></span>' for m in x['m'])+'</span></li>' for x in r['rounds'])
    head=f'<span class="no">No. {no}</span><span class="dt">{date}</span>' if no else '<span class="no">Spare</span>'
    kind='Club' if 'c' in r['answer'] else 'International'
    return f'<article class="c lv{r["lvl"]}"><header>{head}<span class="lv">{kind} · {L[r["lvl"]]}</span></header><h3>{ic(r["answer"],True)}{e(r["answer"]["n"])}</h3><p class="sub">{e(r["comp"])} {r["year"]} · final {e(r["final"])}</p><ol>{route}</ol><p class="src">Source: {e(r["src"])}</p></article>'
d0=datetime.date(2026,11,23)
def day(i): return (d0+datetime.timedelta(days=i)).strftime('%a %-d %b')
nxt=''.join(card(29+i,k,day(21+i)) for i,k in enumerate(NEXT))
done=''.join(card(8+i,k,day(i)) for i,k in enumerate(SCHED))
spare=''.join(card(None,k) for k in SPARE)
head=open('/home/claude/bank/cuprun/signoff_head.html').read().replace('.f{{','.f{').replace('</style>','.cr{width:18px;height:21px;flex:none}.cr.big{width:30px;height:35px}\ndetails{margin-top:28px}summary{cursor:pointer;font-weight:800;font-stretch:78%;text-transform:uppercase;font-size:22px}\n</style>')
page=head+f'''<div class="wrap">
<span class="eb">The Daily Kick Off · Cup Run · updated 20 Nov</span>
<h1>Cup <i>Run</i> No. 29–35</h1>
<p class="lede">Next week (14–20 Dec) for sign-off. Club runs now join the mix: four club days, three international. Club teams use our own shields in kit colours, with no club badges. Two-legged ties show the aggregate, and European group games show both results. No. 8–28 are approved and listed below.</p>
<div class="key"><span><i style="background:var(--accent)"></i>Easy</span><span><i style="background:var(--warn)"></i>Medium</span><span><i style="background:var(--bad)"></i>Hard</span></div>
<h2>For sign-off: No. 29–35</h2><div class="g">{nxt}</div>
<h2>Spares (checked, not scheduled)</h2><div class="g">{spare}</div>
<details><summary>Approved: No. 8–28 (23 Nov – 13 Dec)</summary><div class="g" style="margin-top:12px">{done}</div></details>
</div>
<script>{open('/home/claude/bank/cuprun/flags.js').read()}
const esc=s=>String(s).replace(/[&<>"]/g,c=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}}[c]));
function crest(t){{ const [a,b]=t.c, light=(h=>{{ const n=parseInt(h.slice(1),16); return ((n>>16)*299+((n>>8)&255)*587+(n&255)*114)/1000>150; }})(a);
  return `<path d="M2 2h22v12c0 7-5 11-11 14C7 25 2 21 2 14z" fill="${{a}}" stroke="${{b}}" stroke-width="2"/><path d="M2 20c3 0 8-1 22-6v0c0 6-5 10-11 14C8 26 3 23 2 20z" fill="${{b}}" opacity=".35"/><text x="13" y="15" text-anchor="middle" font-family="IBM Plex Mono,monospace" font-weight="600" font-size="7" fill="${{light?'#0E1712':'#fff'}}">${{esc(t.code)}}</text>`; }}
document.querySelectorAll('svg[data-c]').forEach(s=>s.innerHTML=FLAG[s.dataset.c]||'');
document.querySelectorAll('svg[data-t]').forEach(s=>s.innerHTML=crest(JSON.parse(s.dataset.t)));</script>'''
open('/tmp/claude-0/-home-claude/dc39d1a6-6cbf-5f53-97ab-04ac97cd342b/scratchpad/cuprun-signoff.html','w').write(page)
