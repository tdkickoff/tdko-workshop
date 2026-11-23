"""Builds the two info pages (contact, privacy) in the site's style."""
CONTACT_EMAIL = 'hello@tdko.app'   # the site's contact address; empty = 'Coming soon'
YEAR = '2026'

HEAD = ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><title>{title}</title>'
        '<link rel="preconnect" href="https://fonts.googleapis.com">'
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..900&family=IBM+Plex+Mono:wght@500;600&display=swap">'
        '<style>' + r'''
:root{--bg:#F2F4F1;--surface:#FFFFFF;--ink:#0E1712;--muted:#5D6A62;--line:#D7DDD8;--accent:#0A8A4A;--accent-ink:#FFFFFF;--bad:#C93A2B;--soft:#E7ECE8;
  --f-display:"Archivo","Arial Narrow",system-ui,sans-serif;--f-body:"Archivo",system-ui,-apple-system,"Segoe UI",sans-serif;--f-mono:"IBM Plex Mono",ui-monospace,Menlo,monospace;color-scheme:light}
@media (prefers-color-scheme: dark){:root[data-tdko="dark"]{--bg:#0B110E;--surface:#121A16;--ink:#EAF0EC;--muted:#8A988F;--line:#24302A;--accent:#34D27F;--accent-ink:#06120B;--bad:#FF6B5A;--soft:#1A241F;color-scheme:dark}}
:root[data-tdko="dark"]{--bg:#0B110E;--surface:#121A16;--ink:#EAF0EC;--muted:#8A988F;--line:#24302A;--accent:#34D27F;--accent-ink:#06120B;--bad:#FF6B5A;--soft:#1A241F;color-scheme:dark}
html,body{height:100%}
body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--f-body);font-size:16px;line-height:1.5;
  padding:env(safe-area-inset-top,0px) max(16px,env(safe-area-inset-right,0px)) env(safe-area-inset-bottom,0px) max(16px,env(safe-area-inset-left,0px));-webkit-font-smoothing:antialiased}
.wrap{max-width:560px;margin:0 auto;padding-block:20px 40px;display:flex;flex-direction:column;gap:18px}
.back{align-self:flex-start;font-family:var(--f-mono);font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);text-decoration:none;padding:4px 0;margin-bottom:-8px}
.back:hover{color:var(--ink)}
a:focus-visible,button:focus-visible,input:focus-visible,textarea:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.top{border-bottom:2px solid var(--ink);padding-bottom:10px}
h1{margin:0;font-family:var(--f-display);font-weight:900;font-stretch:66%;font-size:clamp(52px,16vw,88px);line-height:.86;text-transform:uppercase}
h1 i{font-style:normal;color:var(--accent)}
.card{background:var(--surface);border:1px solid var(--line);padding:20px;display:flex;flex-direction:column;gap:14px}
.lede{margin:0;color:var(--muted);font-size:17px}
h2{margin:6px 0 0;font-family:var(--f-display);font-weight:800;font-stretch:80%;font-size:19px;text-transform:uppercase;letter-spacing:.02em}
p{margin:0} ul{margin:0;padding-left:20px;display:grid;gap:6px}
.card a:not(.btn){color:var(--ink);text-underline-offset:3px}
.eyebrow{font-family:var(--f-mono);font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
label{display:flex;flex-direction:column;gap:6px;font-family:var(--f-mono);font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted)}
input,textarea,select{font:inherit;font-family:var(--f-body);font-size:16px;letter-spacing:0;text-transform:none;color:var(--ink);background:var(--surface);border:1.5px solid var(--line);border-radius:0;padding:12px 14px;-webkit-appearance:none}
input:focus,textarea:focus,select:focus{outline:none;border-color:var(--ink)}
textarea{min-height:150px;resize:vertical}
select{background-image:linear-gradient(45deg,transparent 50%,var(--muted) 50%),linear-gradient(135deg,var(--muted) 50%,transparent 50%);background-position:calc(100% - 22px) 52%,calc(100% - 16px) 52%;background-size:6px 6px;background-repeat:no-repeat;padding-right:44px}
.btn{all:unset;box-sizing:border-box;display:block;text-align:center;cursor:pointer;background:var(--ink);color:var(--bg);font-family:var(--f-display);font-weight:800;font-stretch:80%;font-size:18px;text-transform:uppercase;letter-spacing:.03em;padding:15px 12px}
.btn:hover{background:var(--accent);color:var(--accent-ink)}
.btn[aria-disabled="true"]{opacity:.4;cursor:default}
.hp{position:absolute;left:-9999px}
.note{font-size:13px;color:var(--muted)}
.foot{font-family:var(--f-mono);font-size:11px;color:var(--muted);text-align:center;letter-spacing:.04em;text-transform:uppercase}
''' + '</style>' + open('/home/claude/site-build/theme-init.html').read() + '</head><body>')

def page(title, mark, body):
    return (HEAD.replace('{title}', title) + '<div class="wrap"><a class="back" href="./">← The Daily Kick Off</a>'
            f'<header class="top"><h1>{mark}</h1></header>{body}'
            '</div>' + open('/home/claude/site-build/footer.html').read() + '</body></html>')

contact_body = (f'''
<section class="card">
  <p class="lede">Spotted a wrong answer, got an idea for a puzzle, or just want to say hello? Drop us a line.</p>
  <a class="btn" href="mailto:{CONTACT_EMAIL}?subject=The%20Daily%20Kick%20Off" target="_blank" rel="noopener">Email us</a>
  <p class="note">Or write to us at <b>{CONTACT_EMAIL}</b></p>
  <p class="note">We'll only use your details to reply to you. See our <a href="privacy.html">privacy information</a>.</p>
</section>''' if CONTACT_EMAIL else '''
<section class="card">
  <p class="lede">Spotted a wrong answer, got an idea for a puzzle, or just want to say hello?</p>
  <span class="btn" aria-disabled="true">Coming soon</span>
  <p class="note">Our contact details are on their way. Check back shortly.</p>
</section>''')

OPTOUT = open('/home/claude/site-build/privacy_optout.html').read()
privacy = f'''
<section class="card">
  <p class="lede">Short version: we don't ask who you are, we don't track you, and your game progress stays on your own device.</p>
  <h2>Your game progress</h2>
  <p>Your scores, streaks and today's progress are saved in your browser's local storage on your device. They are never sent to us. Clearing your browser data, or switching device, starts you afresh.</p>
  <h2>No accounts, ads or tracking</h2>
  <p>There are no logins, no adverts and no tracking cookies on The Daily Kick Off. We use Cloudflare Web Analytics, which counts visits without cookies or personal data.</p>
  <h2>Visit and play counts</h2>
  <p>To count visits and unique players, your device gets a random ID stored in your browser. It isn't linked to your name, email or location, and we only keep the ID and the date it was first seen.</p>
  <p>We also count how many players start and finish each game each day (and whether they gave up), using the same random ID so each device is counted once, and how many times games are finished, replays included. This helps us see which games people enjoy and where they stop. Your scores and answers are not sent.</p>
  <h2>Don't want to be counted?</h2>
  <p>You can switch the counting off for this device. You'll still see the counters, but your visits and plays won't be added to them. It's free and doesn't change how the games work.</p>
  <label style="flex-direction:row;align-items:center;gap:10px;text-transform:none;letter-spacing:0;font-family:var(--f-body);font-size:16px;color:var(--ink)"><input type="checkbox" id="nocount" style="width:22px;height:22px;padding:0;accent-color:var(--accent)"> Don't count my visits and plays on this device</label>
  <p class="note" id="nocount-msg" aria-live="polite"></p>
{OPTOUT}
  <h2>Other things saved on your device</h2>
  <p>Your light or dark mode choice is saved so the site looks the way you picked. If you use a tester or stats code, that's saved too so you don't have to enter it again.</p>
  <h2>Emailing us</h2>
  <p>If you email us, we receive your email address and whatever you write so that we can reply. We don't use it for anything else or share it.</p>
  <h2>Other services</h2>
  <ul>
    <li>Fonts are loaded from Google Fonts, which receives your IP address when the page loads.</li>
    <li>The site is hosted on Cloudflare.</li>
    <li>Share buttons, our Facebook, Instagram and X links and our Ko-fi link take you to those sites (and WhatsApp, X or Telegram), whose own privacy policies apply.</li>
  </ul>
  <h2>Your rights</h2>
  <p>You can ask what we hold about you, or ask us to delete it, through our <a href="contact.html">contact page</a>.</p>
  <h2>Changes</h2>
  <p>If we add accounts, streaks across devices or stats, we'll update this page first. Last updated November {YEAR}.</p>
</section>'''

open('/home/claude/site-build/contact.html','w').write(page('Contact', 'Contact <i>us</i>', contact_body))
open('/home/claude/site-build/privacy.html','w').write(page('Privacy', 'Your <i>privacy</i>', privacy))
open('/home/claude/site-build/training-ground.html','w').write(page('Training Ground', 'Training <i>Ground</i>', open('/home/claude/site-build/training_body.html').read()))
open('/home/claude/site-build/tester.html','w').write('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta http-equiv="refresh" content="0; url=training-ground.html"><link rel="canonical" href="training-ground.html"><title>Training Ground</title></head><body><a href="training-ground.html">Training Ground</a></body></html>')
open('/home/claude/site-build/stats-login.html','w').write(page('Stats login', 'Stats <i>login</i>', open('/home/claude/site-build/stats_body.html').read()))
open('/home/claude/site-build/terms.html','w').write(page('Terms', 'Terms of <i>use</i>', open('/home/claude/site-build/terms_body.html').read()))
print('built contact, privacy, tester, stats login, terms')

# (the pre-launch coming-soon holding page was retired on 18 Nov 2026; /coming-soon.html redirects to the menu)
