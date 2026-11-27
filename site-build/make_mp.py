"""Builds multiplayer.html and tv.html from mp.css + mp.js (shared by both). Run before package.py."""
import hashlib
R='/home/claude/site-build/'
theme=open(R+'theme-init.html').read()
css=open(R+'mp.css').read(); js=open(R+'mp.js').read()
v=hashlib.md5((css+js).encode()).hexdigest()[:8]
FOOT=open(R+'footer.html').read()
FONTS='<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..900&family=IBM+Plex+Mono:wght@500;600;700&display=swap">'
def page(title,desc,kind,top):
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{title}</title><meta name="description" content="{desc}"><meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:image" content="https://tdko.app/og-image.png">
{theme}{FONTS}<style>{css}</style></head><body data-mp="{kind}"><div class="wrap">{top}<main id="mp"></main></div><script src="/mp.js?v={v}"></script>{FOOT if kind=='phone' else ''}</body></html>'''
open(R+'multiplayer.html','w').write(page('Multiplayer · The Daily Kick Off','Play The Daily Kick Off with friends, each on your own phone.','phone','<div class="top"><a href="./">← The Daily Kick Off</a></div>'))
open(R+'tv.html','w').write(page('TV · The Daily Kick Off','Show a Daily Kick Off quiz on the big screen.','tv',''))
print('built multiplayer.html, tv.html', v)
