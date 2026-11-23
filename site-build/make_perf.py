"""Builds performance.html: the Stats and Scheduler pages as two tabs of one page (same stats code).
Sources stay as stats.html and scheduler.html here; package.py ships performance.html and turns
stats.html / scheduler.html on the site into redirects to the right tab.
Light/dark follows the site's own setting (localStorage 'tdko-theme', light unless set to dark)."""
import re
R = '/home/claude/site-build/'
st = open(R + 'stats.html').read(); sc = open(R + 'scheduler.html').read()

def css(s): return s.split('<style>', 1)[1].split('</style>', 1)[0]
def body(s): return s.split('<div class="wrap">', 1)[1].rsplit('</div>\n<script>', 1)[0]
def script(s): return s.rsplit('<script>', 1)[1].rsplit('</script>', 1)[0]

LIGHT = '--bg:#F2F4F1;--surface:#fff;--ink:#0E1712;--muted:#5D6A62;--line:#D7DDD8;--accent:#0A8A4A;--bad:#C93A2B;--soft:#E7ECE8;--done:#0A8A4A;--today:#8FDCA9;--ready:#F2C94C;--draft:#F08A3C;--none:#D9483B;--off:#E3E7E4;color-scheme:light'
DARK = '--bg:#0B110E;--surface:#121A16;--ink:#EAF0EC;--muted:#8A988F;--line:#24302A;--accent:#34D27F;--bad:#FF6B5A;--soft:#1A241F;--done:#1E9E5A;--today:#7FD39C;--ready:#E8BE45;--draft:#E8823A;--none:#E0564A;--off:#1E2823;color-scheme:dark'

def strip_theme(c):
    c = re.sub(r'@media \(prefers-color-scheme:dark\)\{:root\{[^}]*\}\}', '', c)
    return re.sub(r':root\{[^}]*\}', '', c, count=1)

def scope(c, pre):
    """prefix every selector with `pre`, inside @media blocks too (no nested braces beyond one @media level)."""
    out, i = [], 0
    def rules(block):
        res = []
        for sel, decl in re.findall(r'([^{}]+)\{([^{}]*)\}', block):
            sel = sel.strip()
            if not sel or sel.startswith(('*', 'body', '.wrap', ':root', 'h1', '.eyebrow', '.note')): continue   # shared page chrome comes from stats
            res.append(','.join(pre + ' ' + s.strip() for s in sel.split(',')) + '{' + decl + '}')
        return '\n'.join(res)
    for m in re.finditer(r'(@media[^{]+)\{((?:[^{}]*\{[^{}]*\})*)\s*\}', c):
        out.append(rules(c[i:m.start()])); out.append(m.group(1) + '{' + rules(m.group(2)) + '}'); i = m.end()
    out.append(rules(c[i:]))
    return '\n'.join(out)

stats_css = strip_theme(css(st))
sched_css = scope(strip_theme(css(sc)), '#sched')
stats_body = re.sub(r'^\s*<div style="display:flex[^\n]*?</div>\n', '', body(st), count=1)
assert '<h1>' not in stats_body
sched_body = re.sub(r'^\s*<div class="top"><h1>.*?</div>\n', '', body(sc), count=1)
assert '<h1>' not in sched_body
SUN = '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4.5"/><path d="M12 2.5v2M12 19.5v2M2.5 12h2M19.5 12h2M5.3 5.3l1.4 1.4M17.3 17.3l1.4 1.4M5.3 18.7l1.4-1.4M17.3 6.7l1.4-1.4"/></svg>'
MOON = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5Z"/></svg>'

page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow">
<title>TDKO performance</title>
<script>try{{var t=localStorage.getItem('tdko-theme');document.documentElement.setAttribute('data-tdko',t==='dark'?'dark':'light')}}catch(e){{document.documentElement.setAttribute('data-tdko','light')}}
try{{if(!localStorage.getItem('tdko-stats-key'))location.replace('stats-login.html'+(location.hash==='#scheduler'?'?next=scheduler':''));}}catch(e){{location.replace('stats-login.html');}}</script>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..900&family=IBM+Plex+Mono:wght@500;600&display=swap">
<style>
:root{{{LIGHT};--f-display:"Archivo","Arial Narrow",system-ui,sans-serif;--f-mono:"IBM Plex Mono",ui-monospace,Menlo,monospace}}
:root[data-tdko="dark"]{{{DARK}}}
{stats_css}
/* page header + tabs */
.back{{align-self:flex-start;font-family:var(--f-mono);font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);text-decoration:none;padding:4px 0;margin-bottom:-8px}}
.back:hover{{color:var(--ink)}}
.phead{{display:flex;justify-content:space-between;align-items:flex-end;gap:12px;min-width:0}}
.phead h1{{font-size:clamp(34px,10vw,44px);min-width:0}}
.themebtn{{width:36px;height:36px;border:1.5px solid var(--ink);background:transparent;color:var(--ink);cursor:pointer;display:grid;place-items:center;padding:0;flex:none}}
.themebtn svg{{width:18px;height:18px;fill:none;stroke:currentColor;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}}
.tabs{{display:flex;border-bottom:2px solid var(--ink)}}
.tabs button{{font-family:var(--f-mono);font-size:12.5px;font-weight:600;letter-spacing:.05em;text-transform:uppercase;padding:10px 18px;border:0;background:transparent;color:var(--muted);cursor:pointer;margin-bottom:-2px;border-bottom:4px solid transparent}}
.tabs button[aria-selected="true"]{{color:var(--ink);border-bottom-color:var(--accent)}}
.panel{{display:flex;flex-direction:column;gap:14px}}.panel[hidden]{{display:none}}
{sched_css}
</style></head><body><div class="wrap">
<a class="back" href="./">← The Daily Kick Off</a>
<div class="phead"><h1>TDKO <i>performance</i></h1><button type="button" class="themebtn" id="themebtn"></button></div>
<div class="tabs" role="tablist"><button role="tab" id="t-stats" aria-controls="stats" aria-selected="true">Stats</button><button role="tab" id="t-sched" aria-controls="sched" aria-selected="false">Scheduler</button></div>
<div class="panel" id="stats" role="tabpanel">
{stats_body}
</div>
<div class="panel" id="sched" role="tabpanel" hidden>
{sched_body}
</div>
</div>
<script>
(function(){{
  var root=document.documentElement, b=document.getElementById('themebtn'), SUN='{SUN}', MOON='{MOON}';
  function paint(){{ var d=root.getAttribute('data-tdko')==='dark'; b.innerHTML=d?SUN:MOON; b.title=d?'Switch to light mode':'Switch to dark mode'; b.setAttribute('aria-label',b.title); }}
  b.onclick=function(){{ var n=root.getAttribute('data-tdko')==='dark'?'light':'dark'; root.setAttribute('data-tdko',n); try{{localStorage.setItem('tdko-theme',n)}}catch(e){{}} paint(); }};
  addEventListener('storage',function(e){{ if(e.key==='tdko-theme'&&(e.newValue==='light'||e.newValue==='dark')){{ root.setAttribute('data-tdko',e.newValue); paint(); }} }});
  paint();
  /* tabs: #scheduler opens the Scheduler tab; the choice is kept in the address so refresh and bookmarks land on it */
  window.tdkoTab=function(which,push){{
    var s=which==='sched';
    document.getElementById('stats').hidden=s; document.getElementById('sched').hidden=!s;
    document.getElementById('t-stats').setAttribute('aria-selected',String(!s)); document.getElementById('t-sched').setAttribute('aria-selected',String(s));
    if(push!==false) history.replaceState(null,'',s?'#scheduler':location.pathname+location.search);
    dispatchEvent(new Event(s?'tdko-sched-shown':'tdko-stats-shown'));
  }};
  document.getElementById('t-stats').onclick=function(){{ tdkoTab('stats'); }};
  document.getElementById('t-sched').onclick=function(){{ tdkoTab('sched'); }};
  if(location.hash==='#scheduler') tdkoTab('sched',false);
}})();
</script>
<script>{script(st)}
/* the charts measure their width, so redraw when the Stats tab is shown */
addEventListener('tdko-stats-shown',function(){{ try{{ if(S.data) draw(); }}catch(e){{}} }});
</script>
<script>{script(sc)}</script>
</body></html>'''
open(R + 'performance.html', 'w').write(page)
print('built performance.html', len(page) // 1024, 'KB')
