"""Builds The Daily Kick Off site in tdko/: the menu plus a copy of each game wired to it.
Usage: python3 build.py <hub url>"""
import re, sys, os, json
LIVE_URL = sys.argv[1] if len(sys.argv) > 1 else 'https://claude.ai/artifact/THE_DAILY_KICK_OFF'
ROOT = '/home/claude/site-build'
GAMES = {  # source file -> published id
  '/home/claude/one-touch.html':        'fast-break',
  '/home/claude/whos-that-baller.html': 'whos-that-baller',
  '/home/claude/scramble-head.html':    'in-the-mixer',
  '/home/claude/pass-and-connect.html': 'link-up-play',
  '/home/claude/who-playedle.html':     'squad-goals',
  '/home/claude/shirt-swap.html':       'shirt-swap',
  '/home/claude/tiki-taka-toe.html':    'tiki-taka-toe',
  '/home/claude/offside.html':          'offside',
  '/home/claude/top-four.html':         'top-four',
  '/home/claude/ranked-highly.html':    'ranked-highly',
  '/home/claude/clean-sweep.html':      'clean-sweep',   # public from Mon 23 Nov 2026 (No. 8)
  '/home/claude/cup-run.html':          'cup-run',       # public from Mon 23 Nov (No. 8)
}
PREFIX = {'fast-break':'fastbreak:', 'whos-that-baller':'wtb:', 'in-the-mixer':'scramble:', 'link-up-play':'passconnect:',
          'squad-goals':'playedle:', 'shirt-swap':'shirtswap:', 'tiki-taka-toe':'tikitaka:', 'top-four':'topfour:', 'ranked-highly':'rankedhighly:', 'clean-sweep':'cleansweep:', 'cup-run':'cuprun:'}
HEAD = ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
        '<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px);color-scheme:light}'
        'body{margin:0;font:14px/1.4 system-ui,sans-serif}img{max-width:100%}[hidden]{display:none!important}</style>' + open('/home/claude/site-build/theme-init.html').read() + open('/home/claude/site-build/gate.html').read() + '</head><body>')
BACK_CSS = ('.back{align-self:flex-start;font-family:var(--f-mono);font-size:12px;letter-spacing:.06em;text-transform:uppercase;'
            'color:var(--muted);text-decoration:none;padding:4px 0;margin-bottom:-8px}'
            '.back:hover{color:var(--ink)}.back:focus-visible{outline:2px solid var(--accent);outline-offset:2px}\n')

for src, gid in GAMES.items():
    base = open(src).read()
    for mode, url, out in (('live', LIVE_URL, ROOT),):
        s = re.sub(r"const GAME_URL = '[^']*';", f"const GAME_URL = '{url}';", base, count=1)
        assert s.count('${GAME_URL}#c${dayNo}-') == 1, src
        s = s.replace('${GAME_URL}#c${dayNo}-', '${GAME_URL}#' + gid + '-c${dayNo}-')
        s = s.replace('</style>', BACK_CSS + '' + '</style>', 1)
        assert s.count('<header class="top">') == 1
        bar = ''
        s = s.replace('<header class="top">', bar + '<a class="back" href="./">← The Daily Kick Off</a>\n  <header class="top">', 1)
        # test day (testers only): fixed puzzle, always in replay mode, so nothing is reported to scores or streaks
        assert s.count("function tdkoIsReplay(gid, dayKey, dayNo){ ") == 1, src
        s = s.replace("function tdkoIsReplay(gid, dayKey, dayNo){ ", "function tdkoIsReplay(gid, dayKey, dayNo){ if(window.TDKO_TEST) return true; ", 1)
        assert s.count("function tdkoReplayBox(on){ return") == 1, src
        s = s.replace("function tdkoReplayBox(on){ return", "function tdkoReplayBox(on){ if(window.TDKO_TEST) return tdkoTestBox(); return", 1)
        assert s.count("dayNo = LAUNCH==null ? 1 :") == 1, src
        s = s.replace("dayNo = LAUNCH==null ? 1 :", "dayNo = window.TDKO_TEST ? TDKO_TEST_NO : LAUNCH==null ? 1 :", 1)
        # test day content: its own puzzle for each game, used instead of the daily one when TDKO_TEST is on
        TD = json.load(open(ROOT+'/test-day.json'))[gid]
        s = s.replace('<script>', '<script>var TDKO_T=' + json.dumps(TD, ensure_ascii=False) + ';</script>\n<script>', 1)
        if gid == 'fast-break':
            a = "const d = (dayNo-1) % DAYS.length;"
            assert s.count(a) == 1
            s = s.replace(a, a + "\n  let DD = DAYS[d]; if(window.TDKO_TEST){ const b=Q.length; TDKO_T.forEach(x=>Q.push(x)); DD={e:[...Array(10).keys()].map(i=>b+i), m:[...Array(9).keys()].map(i=>b+10+i), h:[b+19]}; }", 1)
            a = "QUIZ = (DAYS[d].o || [...shuffle(DAYS[d].e), ...shuffle(DAYS[d].m), ...DAYS[d].h]).map(make);"
            assert s.count(a) == 1
            s = s.replace(a, "QUIZ = (DD.o || [...shuffle(DD.e), ...shuffle(DD.m), ...DD.h]).map(make);", 1)
            a = "hash('fastbreak:'+dayKey)"; assert s.count(a) == 1
            s = s.replace(a, "hash(window.TDKO_TEST ? 'fastbreak:test-day' : 'fastbreak:'+dayKey)", 1)
        else:
            s, n = re.subn(r"const (\w+) = (\w+)\[\(dayNo-1\) % \2\.length\];", r"const \1 = window.TDKO_TEST ? TDKO_T : \2[(dayNo-1) % \2.length];", s, count=1)
            assert n == 1, src
        # record kick-off / full-time times whenever the game reports its daily status
        i = s.index('function report(){'); a = 'localStorage.setItem(k, JSON.stringify(all));'; j = s.index(a, i)
        assert j - i < 600, src
        s = s[:j] + f"if(REPLAY){{ tdkoReplayDone('{gid}',dayKey,all['{gid}']); return; }} " + a + f" tdkoStamp(k,'{gid}',all['{gid}']);" + s[j+len(a):]
        # replays run report() too (into a throwaway record) so a finished replay can be counted; the saved first result is never touched
        a = "function report(){ if(REPLAY) return; try{ const k='tdko:'+dayKey+'#'+dayNo, all=JSON.parse(localStorage.getItem(k)||'{}');"
        assert s.count(a) == 1, src
        s = s.replace(a, "function report(){ try{ const k='tdko:'+dayKey+'#'+dayNo, all=REPLAY?{}:JSON.parse(localStorage.getItem(k)||'{}');", 1)
        a = "try{ if(tdkoReplayKey) localStorage.removeItem(tdkoReplayKey); }catch(_){}"
        assert s.count(a) == 1, src
        s = s.replace(a, a + f" tdkoReplayNew('{gid}');", 1)
        # share box wording (user, 19 Nov 2026): one message for every game, button opens the share sheet for friends or stories
        s, n = re.subn(r"<p>Your friend gets today's[^<]*</p>", "<p>Share today's puzzle and your score with friends and see if they can beat it.</p>", s, count=1); assert n == 1, src
        assert s.count('<h3>Challenge a friend</h3>') == 1 and s.count('id="shareBtn">Challenge a friend</button>') == 1, src
        s = s.replace('<h3>Challenge a friend</h3>', '<h3>Challenge &amp; share</h3>').replace('id="shareBtn">Challenge a friend</button>', 'id="shareBtn">Share now</button>')
        # test puzzles show no day number on screen
        s = s.replace("Full time · No. ${dayNo}", "Full time${window.TDKO_TEST?' · Training Ground':' · No. '+dayNo}")
        s = s.replace("File No. ${String(dayNo).padStart(3,'0')}", "${window.TDKO_TEST?'Training file':'File No. '+String(dayNo).padStart(3,'0')}")
        s = s.replace("Scramble No. ${String(dayNo).padStart(3,'0')}", "${window.TDKO_TEST?'Training scramble':'Scramble No. '+String(dayNo).padStart(3,'0')}")
        s = s.replace('<script>', open(ROOT+'/reset.html').read() + open(ROOT+'/streak.html').read() + '<script>', 1)  # site reset runs before the game reads its save
        # the day's puzzles live in data/<game>.js (see bank/final/inject.py); the ?v= hash makes browsers fetch a new copy when it changes
        _d = open(f'{ROOT}/data/{gid}.js').read(); import hashlib as _hl
        s = f'<script src="data/{gid}.js?v={_hl.md5(_d.encode()).hexdigest()[:8]}"></script>\n' + s
        if gid == 'tiki-taka-toe':   # the 1,200-player list lives in its own file so phones keep it between days
            _pl = '/* Tiki-Taka-Toe players: bank/tiki/build_players.py */\nwindow.TDKO_PLAYERS = ' + json.dumps(json.load(open('/home/claude/bank/tiki/players.json')), ensure_ascii=False, separators=(',',':')) + ';\n'
            open(f'{ROOT}/data/tiki-players.js','w').write(_pl)
            s = f'<script src="data/tiki-players.js?v={_hl.md5(_pl.encode()).hexdigest()[:8]}"></script>\n' + s
        # "Report a problem": opens an email to hello@tdko.app with the game, puzzle number and date filled in
        NAMES = {'fast-break':'Fast Break','whos-that-baller':"Who's That Baller",'in-the-mixer':'In The Mixer','link-up-play':'Link Up Play','squad-goals':'Squad Goals',
                 'shirt-swap':'Shirt Swap','tiki-taka-toe':'Tiki-Taka-Toe','offside':'Offside','top-four':'Top Four','ranked-highly':'Ranked Highly','clean-sweep':'Clean Sweep','cup-run':'Cup Run'}
        REPORT = ('<p class="tdko-report"><a id="tdko-report" href="mailto:hello@tdko.app" target="_blank" rel="noopener">Report a problem</a></p>'
                  '<style>.tdko-report{text-align:center;margin:8px 0 0;padding:0 16px}.tdko-report a{font-family:var(--f-mono,ui-monospace,monospace);font-size:12px;letter-spacing:.06em;'
                  'text-transform:uppercase;color:var(--muted,#5D6A62);text-decoration:underline;text-underline-offset:3px}.tdko-report a:hover{color:var(--ink,#0E1712)}</style>'
                  '<script>(function(){try{var d=new Date(),L=Date.UTC(2026,10,16),n=Math.max(1,Math.round((Date.UTC(d.getFullYear(),d.getMonth(),d.getDate())-L)/864e5)+1);'
                  'var g=' + json.dumps(NAMES[gid]) + ',when=window.TDKO_TEST?"Training Ground":"No. "+n+" ("+d.toLocaleDateString("en-GB",{weekday:"short",day:"numeric",month:"short",year:"numeric"})+")";'
                  'var sub="Problem: "+g+" · "+when, body="Game: "+g+"\\nPuzzle: "+when+"\\n\\nWhat went wrong? (e.g. a wrong answer, a correct answer that wasn\'t accepted, a typo)\\n\\n";'
                  'var m=document.querySelector("main"),r=document.querySelector(".tdko-report");if(m&&r)m.insertAdjacentElement("afterend",r);'
                  'document.getElementById("tdko-report").href="mailto:hello@tdko.app?subject="+encodeURIComponent(sub)+"&body="+encodeURIComponent(body);}catch(e){}})();</script>')
        open(f'{out}/{gid}.html', 'w').write(HEAD + s + REPORT + open(ROOT+'/footer.html').read() + '</body></html>')
    print('built', gid)


# keep the menu's copy of the shared chrome in step with footer.html
import re as _re
_h = open(ROOT+'/the-daily-kick-off.html').read()
_h = _re.sub(r"<!--tdko-gate-->.*?<!--/tdko-gate-->\n", lambda m: open(ROOT+'/gate.html').read(), _h, count=1, flags=_re.S)
_h, _n = _re.subn(r"<!--tdko-chrome-->.*?<!--/tdko-chrome-->\n", lambda m: open(ROOT+'/footer.html').read(), _h, flags=_re.S)
assert _n == 1
open(ROOT+'/the-daily-kick-off.html','w').write(_h)
print('menu footer refreshed')
