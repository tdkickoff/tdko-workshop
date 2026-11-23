"""Copies the built site into the tdko-site repository folder, ready to commit and push."""
import os, shutil
R='/home/claude/site-build/'; OUT='/home/claude/tdko-site/'
ICONS='<link rel="icon" type="image/png" href="/icon-512.png"><link rel="apple-touch-icon" href="/apple-touch-icon.png"><meta name="theme-color" content="#13221A">'
HEAD=('<!doctype html><html lang="en"><head><meta charset="utf-8">'
      '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'+ICONS+
      '<meta name="description" content="Nine daily football puzzles. New every midnight.">'
      '<meta property="og:title" content="The Daily Kick Off"><meta property="og:description" content="Nine daily football puzzles. New every midnight.">'
      '<meta property="og:image" content="https://tdko.app/og-image.png"><meta property="og:url" content="https://tdko.app/"><meta name="twitter:card" content="summary_large_image">')
h=open(R+'the-daily-kick-off.html').read()
open(OUT+'index.html','w').write(HEAD+'</head><body>'+h+'</body></html>')
for f in ['fast-break','whos-that-baller','in-the-mixer','link-up-play','squad-goals','shirt-swap','tiki-taka-toe','offside','top-four','ranked-highly','clean-sweep','cup-run','contact','privacy','performance','tester','training-ground','stats-login','terms']:
    s=open(R+f+'.html').read(); assert s.startswith('<!doctype html>'), f
    open(OUT+f+'.html','w').write(s.replace('<meta charset="utf-8">','<meta charset="utf-8">'+ICONS,1))
os.makedirs(OUT+'data',exist_ok=True)
for f in os.listdir(R+'data'): shutil.copy(R+'data/'+f, OUT+'data/'+f)
# old addresses go to the right tab of the Performance page
for f, to in [('stats', 'performance.html'), ('scheduler', 'performance.html#scheduler')]:
    open(OUT+f+'.html','w').write(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="robots" content="noindex,nofollow"><title>TDKO performance</title><script>location.replace("{to}")</script><meta http-equiv="refresh" content="0;url={to}"></head><body></body></html>')
print('packaged into', OUT)
