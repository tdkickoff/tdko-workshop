/* The Daily Kick Off · Multiplayer (Phase 1). One script for the phone page (multiplayer.html) and the TV page (tv.html).
   The server owns the clock and every result; this file only sends actions and draws the view it is given. */
(function () {
  'use strict';
  const TV = document.body.dataset.mp === 'tv';
  const $ = s => document.querySelector(s);
  const app = $('#mp');
  const esc = s => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const GAMES = { fb: 'Fast Break', wtb: "Who's That Baller", cs: 'Clean Sweep', rh: 'Ranked Highly' };
  // game titles styled as on the Daily Puzzles page: condensed capitals, second word in the accent colour
  const TT = { fb: ['Fast', 'Break'], wtb: ["Who's That", 'Baller'], cs: ['Clean', 'Sweep'], rh: ['Ranked', 'Highly'] };
  const GT = g => `<span class="gt">${TT[g][0]} <i>${TT[g][1]}</i></span>`;
  const LAUNCH = Date.UTC(2026, 10, 30);  // Multiplayer opens to everyone at UK midnight on 30 Nov 2026 (the server checks too)
  const DESC = { fb: "You all get the same question and the same 10-second clock. A right answer scores 100, plus up to 50 more the quicker you are. When the clock hits zero, the next question starts.",
    wtb: "A new clue about the mystery player appears every 10 seconds. Name him on the first clue for 1,000, with 100 less for each clue after. Guess as often as you like; his surname is enough, his first name isn't.",
    cs: "Name the players on the list before anyone else does. Each name is worth 1,000 at the start, dropping to 100 as the clock runs down, and once a name is taken it's gone.",
    rh: "Call higher or lower before the 10 seconds run out. A right call scores up to 100, more the quicker you are; a wrong one puts you out of the round. It starts easy and gets harder." };
  const INFO = new Set(); // games whose details are open in the lobby
  const SHUT = new Set(); // lobby sections the viewer has collapsed ('players', 'quiz')
  const ARROW = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M3.5 6l4.5 4.5L12.5 6"/></svg>';
  const sec = (id, title, body, foot = '') => `<section class="card fold${SHUT.has(id) ? ' shut' : ''}"><h3 class="sech"><button type="button" data-a="sec" data-s="${id}" aria-expanded="${!SHUT.has(id)}">${title}${ARROW}</button></h3>${SHUT.has(id) ? '' : body}${foot}</section>`;
  const infoBtn = g => `<button class="info" type="button" data-a="info" data-g="${g}" aria-expanded="${INFO.has(g)}" aria-controls="d-${g}" aria-label="${INFO.has(g) ? 'Hide' : 'Show'} how ${GAMES[g]} works"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M3.5 6l4.5 4.5L12.5 6"/></svg></button>`;
  const infoBox = g => INFO.has(g) ? `<div class="gdesc" id="d-${g}"><p>${DESC[g]}</p><button class="link" type="button" data-a="info" data-g="${g}">Hide details ▴</button></div>` : '';
  const fmt = n => (n || 0).toLocaleString('en-GB');
  const LENS = { fb: { s: 10, m: 15, l: 20, u: 'questions' }, wtb: { s: 1, m: 3, l: 5, u: 'players' }, cs: { s: 1, m: 3, l: 5, u: 'lists' }, rh: { s: 1, m: 3, l: 5, u: 'rounds' } };
  // rough running time in seconds, from the engine's clocks plus kick-offs, reveals and host taps (Clean Sweep's clock grows with the number of players)
  const EST = (g, l, n) => { const k = LENS[g][l];
    if (g === 'fb') return 5 + k * 10;
    if (g === 'wtb') return k * 90;
    if (g === 'cs') return k * (20 + (n >= 6 ? 150 : n >= 4 ? 120 : 90));
    return k * 70; };
  const MIN = s => `${Math.max(1, Math.round(s / 60))} min`;
  const TOTAL = (games, n) => games.reduce((a, x) => a + EST(x.g, x.len, n) + 15, 0);
  const LN = { s: 'Short', m: 'Standard', l: 'Long' };
  const store = { get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }, set(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }, del(k) { try { localStorage.removeItem(k); } catch (e) {} } };
  let pid = TV ? 'tv' : store.get('tdko-mp-pid');
  if (!pid) { pid = 'p-' + (crypto.randomUUID ? crypto.randomUUID() : (Date.now().toString(36) + Math.random().toString(36).slice(2))).replace(/[^A-Za-z0-9-]/g, '').slice(0, 40); store.set('tdko-mp-pid', pid); }
  let pend = null; const qkey = () => V && V.game ? [V.round, V.gi, V.game.type, V.game.n, V.game.i, V.game.qn, V.game.cur && V.game.cur.n].join('|') : '';
  let code = null, V = null, offset = 0, polls = 0, timer = null, busy = false, flash = '', flashSeen = '', flashAt = 0, draftKey = '', typed = '';

  const now = () => Date.now() + offset;
  // the TV never scrolls: scale up to fill the screen, then shrink the whole page until it fits
  let fitT = 0;
  function tvFit() {
    if (!TV) return; const R = document.documentElement, H = () => Math.max(R.scrollHeight, document.body.scrollHeight);
    R.style.setProperty('--z', Math.max(1, Math.min(2.4, innerWidth / 760, innerHeight / 500)).toFixed(2));
    let f = 1; R.style.setProperty('--fit', 1);
    for (let i = 0; i < 6 && H() > innerHeight + 1; i++) { f = Math.max(.4, f * innerHeight / H() * .99); R.style.setProperty('--fit', f.toFixed(3)); }
    clearTimeout(fitT); fitT = setTimeout(() => { if (H() > innerHeight + 1) tvFit(); }, 400); // fonts and images can land late
  }
  // phones: the screens between rounds and games shrink to fit, so Ready is always on screen without scrolling
  function phoneFit() {
    if (TV || !V) return; const R = document.documentElement, g = V.game, mp = $('#mp');
    const on = V.phase === 'between' || (V.phase === 'game' && g && g.step === 'reveal' && g.wait);
    R.style.setProperty('--pfit', 1);
    if (on) { const need = mp.offsetHeight + 8; if (need > innerHeight) R.style.setProperty('--pfit', Math.max(.6, innerHeight / need * .99).toFixed(3)); }
    // the site's header and footer stay on the page, but each new screen of a quiz lands on the game itself
    const key = V.phase === 'lobby' ? 'lobby' : [V.phase, V.gi, g && g.type, g && g.n, g && g.step].join('|');
    if (key !== landKey) { landKey = key; if (V.phase !== 'lobby') scrollTo(0, Math.max(0, mp.getBoundingClientRect().top + scrollY - 6)); }
  }
  let landKey = '';
  if (!TV) addEventListener('resize', () => phoneFit());
  if (TV) { tvFit(); addEventListener('resize', tvFit); if (document.fonts) document.fonts.ready.then(tvFit); }
  async function call(path, body) {
    const opt = body ? { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify(body) } : {};
    const r = await fetch('/api/mp/' + path, opt); let j = {};
    try { j = await r.json(); } catch (e) { j = { error: 'Connection problem. Trying again…' }; }
    if (j.view) { offset = j.view.now - Date.now(); V = j.view; }
    return { ok: r.ok, ...j };
  }
  function go(c) { code = c; if (!TV) { store.set('tdko-mp-code', c); history.replaceState(null, '', '/multiplayer.html?c=' + c); } poll(); }
  async function poll() {
    clearTimeout(timer); if (!code) return;
    try {
      const r = await call(`state?code=${code}&pid=${encodeURIComponent(pid)}${polls++ % 4 === 0 ? '&ping=1' : ''}`);
      if (r.error && !r.view) { if (r.ok === false && /exist|finished/.test(r.error)) { leave(r.error); return; } flash = r.error; }
      else if (Date.now() - flashAt > 4000) flash = '';   // messages stay up for at least 4 seconds
    } catch (e) { flash = 'Connection lost. Reconnecting…'; }
    draw(); timer = setTimeout(poll, document.hidden ? 2500 : 900);
  }
  async function send(a, answer) {
    if (busy && !answer) return; busy = true;
    try { const r = await call('act', { code, pid, ...a }); flash = r.error || ''; if (r.error && answer) pend = null; }
    catch (e) { flash = 'Connection problem. Try again.'; if (answer) pend = null; }
    busy = false; draw();
  }
  function leave(msg) { clearTimeout(timer); code = null; V = null; if (!TV) { store.del('tdko-mp-code'); history.replaceState(null, '', '/multiplayer.html'); } home(msg); }

  // ---------- small parts ----------
  const me = () => V && V.players.find(p => p.pid === pid);
  const sideName = id => (V.sides.find(s => s.id === id) || {}).name || (V.players.find(p => p.pid === id) || {}).name || '?';
  const mySide = () => V && (V.mode === 'teams' ? (me() || {}).side : pid);
  const secs = until => Math.max(0, Math.ceil((until - now()) / 1000));
  const bar = (until, total) => `<div class="clock" data-until="${until}" data-total="${total}"><i style="width:${Math.max(0, Math.min(100, (until - now()) / total * 100))}%"></i></div>`;
  const cd = until => `<span class="secs" data-until="${until}">${secs(until)}</span>`;
  const teamCls = id => V.mode === 'teams' ? ' t-' + esc(id) : '';
  function standings(pointsOf) {
    return V.sides.slice().sort((a, b) => (pointsOf(b.id) - pointsOf(a.id)) || ((V.correct[b.id] || 0) - (V.correct[a.id] || 0)));
  }
  function table(title) {
    const rows = standings(id => V.quiz[id] || 0);
    const pos = s => rows.findIndex(x => (V.quiz[x.id] || 0) === (V.quiz[s.id] || 0) && (V.correct[x.id] || 0) === (V.correct[s.id] || 0)) + 1;
    return `<section class="card"><h3>${esc(title)}</h3><ol class="table">${rows.map((s, i) => `<li class="${s.id === mySide() ? 'me' : ''}${teamCls(s.id)}"><span class="pos">${i && pos(s) === pos(rows[i - 1]) ? '=' : pos(s)}</span><span class="nm">${esc(s.name)}</span><b>${fmt(V.quiz[s.id])}</b></li>`).join('')}</ol></section>`;
  }
  function hostBar() {
    if (TV || !V.isHost || V.phase !== 'game') return '';
    return `<div class="hostbar"><button data-a="pause">${V.game && V.game.paused ? 'Resume' : 'Pause'}</button><button data-a="skip">Skip</button><button data-a="end">End quiz</button></div>`;
  }
  function log(g) {
    if (!g.log || !g.log.length) return '';
    return `<ul class="log">${g.log.slice().reverse().map(l => `<li class="${l.t}"><b>${esc(l.who || sideName(l.side))}</b> ${l.t === 'right' ? '✓ ' + esc(l.text) + (l.pts ? ` <em>+${fmt(l.pts)}</em>` : '') : l.t === 'wrong' ? '✗ ' + esc(l.text) : l.t === 'dup' ? esc(l.text) + ' · already found' : l.t === 'time' ? 'ran out of time' : l.t === 'skip' ? 'skipped' : 'nobody got it'}</li>`).join('')}</ul>`;
  }

  // ---------- screens ----------
  function home(msg, joinOpen) {
    if (TV) {
      app.innerHTML = `<section class="tvjoin"><h1>The Daily Kick Off <i>on the TV</i></h1><p>Type the 4-letter room code from the host's phone.</p>
        <form id="tvf"><input id="tvc" maxlength="4" autocapitalize="characters" autocomplete="off" placeholder="CODE"><button>Show quiz</button></form><p class="err">${esc(msg || '')}</p></section>`;
      $('#tvf').onsubmit = e => { e.preventDefault(); const c = $('#tvc').value.trim().toUpperCase(); if (/^[A-Z]{4}$/.test(c)) go(c); };
      return;
    }
    app.innerHTML = `<section class="hero"><span class="eb">Multiplayer</span><h1>Play <i>together</i></h1><p class="lede">Play with up to five friends, each on your own phone. Host a quiz, share your room code so they can join, then kick off. Got a TV? Open <b>tdko.app/tv</b> on it and type in your room code to put the quiz on the big screen.</p></section>
      <section class="card" id="hostcard"><button class="btn big" id="host">Host a quiz</button><a class="howto" href="how-to-host.html">New to hosting? See how it works</a></section>
      <section class="card" id="joincard"><button class="btn big" id="joinbtn" type="button" aria-expanded="${joinOpen ? 'true' : 'false'}" aria-controls="jf">Join a quiz</button><form id="jf" class="row"${joinOpen ? '' : ' hidden'}><input id="jc" maxlength="4" autocapitalize="characters" autocomplete="off" placeholder="CODE" aria-label="Room code"><button class="btn">Join</button></form></section>
      <p class="err">${esc(msg || '')}</p><p class="faql"><a href="multiplayer-faq.html">Multiplayer FAQ and rules</a></p>`;
    const askPass = m => {
      $('#hostcard').innerHTML = `<p class="lede">Multiplayer is in the Training Ground for now. Enter your Training Ground code to host. Anyone can join with a room code.</p>
        <form id="pf" class="row"><input id="pc" autocapitalize="characters" autocomplete="off" spellcheck="false" placeholder="TDKO-XXXXX" aria-label="Training Ground code"><button class="btn">Unlock</button></form><p class="err">${esc(m || '')}</p>`;
      $('#pf').onsubmit = async e => { e.preventDefault();
        try { const r = await fetch('/api/tester', { headers: { 'x-tdko-tester': $('#pc').value.trim().toUpperCase() } }); const j = await r.json();
          if (!j.pass) return askPass("That code isn't right."); store.set('tdko-mp-pass', j.pass); store.set('tdko-tester', Date.now() >= LAUNCH ? '4' : '3'); home(); } catch (_) { askPass('Could not check the code. Try again.'); } };
    };
    $('#host').onclick = async () => { const pass = store.get('tdko-mp-pass'); if (!pass && Date.now() < LAUNCH) return askPass();
      const r = await call('create', { pid, pass }); if (r.code) go(r.code); else if (r.needPass) { store.del('tdko-mp-pass'); askPass(r.error); } else home(r.error); };
    $('#joinbtn').onclick = () => { const f = $('#jf'), open = f.hidden; f.hidden = !open; $('#joinbtn').setAttribute('aria-expanded', String(open)); if (open) $('#jc').focus(); };
    $('#jf').onsubmit = async e => { e.preventDefault(); const c = $('#jc').value.trim().toUpperCase(); if (!/^[A-Z]{4}$/.test(c)) return home('That code needs 4 letters.', true); join(c); };
  }
  async function join(c, quiet) {
    const r = await call('join', { code: c, pid });
    if (r.view) { if (r.error) flash = r.error; go(c); } else { if (quiet) store.del('tdko-mp-code'); home(quiet ? '' : r.error, !quiet); }
  }

  function lobby() {
    const host = V.isHost, link = `tdko.app/m/${V.code}`;
    const games = V.config.games, on = g => games.find(x => x.g === g);
    const np = Math.max(2, V.players.length), len = games.length ? `<p class="qlen">Quiz length: <b>about ${MIN(TOTAL(games, np))}</b></p>` : '';
    const pl = p => `<li class="${p.pid === pid ? 'me' : ''}${teamCls(p.side)}">${p.here ? '' : '<span class="away">away</span>'}<span class="nm">${esc(p.name)}</span>${p.pid === V.host ? '<em>host</em>' : ''}
        ${host && !TV && V.mode === 'teams' ? `<button class="mini" data-a="team" data-p="${esc(p.pid)}">Move</button>` : ''}${host && !TV && p.pid !== V.host ? `<button class="mini x" data-a="kick" data-p="${esc(p.pid)}" aria-label="Remove ${esc(p.name)}">✕</button>` : ''}</li>`;
    const players = V.mode === 'teams'
      ? V.teams.map(t => `<div class="team t-${esc(t.id)}"><h4>${esc(t.name)}${host && !TV ? ` <button class="mini" data-a="teamname" data-t="${esc(t.id)}">Rename</button>` : ''}</h4><ul class="people">${V.players.filter(p => p.side === t.id).map(pl).join('') || '<li class="empty">Nobody yet</li>'}</ul></div>`).join('')
      : `<ul class="people">${V.players.map(pl).join('')}</ul>`;
    if (TV) {
      app.innerHTML = `<section class="tvlobby"><div class="big-code"><span>Join at</span><b>${esc(link)}</b><span>or tdko.app → Multiplayer → code</span><strong>${esc(V.code)}</strong></div>
        <div class="tvpeople"><h2>${V.players.length} of 6 in</h2>${players}<p class="tvgames">${games.map(x => GT(x.g)).join('')}</p><p class="tvlen">${games.length ? `Quiz length: about ${MIN(TOTAL(games, np))}` : ''}</p></div></section>`;
      return;
    }
    const cfg = host ? `${sec('players', `Players <small>${V.players.length} of 6</small>`, `<div class="seg wide"><button data-a="mode" data-m="solo" class="${V.mode === 'solo' ? 'on' : ''}">Everyone for themselves</button><button data-a="mode" data-m="teams" data-n="2" class="${V.mode === 'teams' && V.teams.length === 2 ? 'on' : ''}">2 teams</button><button data-a="mode" data-m="teams" data-n="3" class="${V.mode === 'teams' && V.teams.length === 3 ? 'on' : ''}">3 teams</button></div>
        ${V.mode === 'teams' ? '<button class="mini" data-a="shuffle">Shuffle teams</button>' : ''}${players}`)}
      ${sec('quiz', 'The quiz', `${Object.keys(GAMES).map(g => { const x = on(g); return `<div class="game ${x ? 'on' : ''}"><div class="gh"><label><input type="checkbox" data-a="g" data-g="${g}" ${x ? 'checked' : ''}> ${GT(g)}</label>${infoBtn(g)}</div>${infoBox(g)}
        <div class="seg">${['s', 'm', 'l'].map(l => `<button data-a="len" data-g="${g}" data-l="${l}" class="${x && x.len === l ? 'on' : ''}" ${x ? '' : 'disabled'}>${LN[l]}<small>${LENS[g][l]} ${LENS[g][l] === 1 ? LENS[g].u.slice(0, -1) : LENS[g].u}</small><small class="t">about ${MIN(EST(g, l, np))}</small></button>`).join('')}</div></div>`; }).join('')}`, len)}`
      : `${sec('players', `Players <small>${V.players.length} of 6</small>`, players)}${sec('quiz', 'The quiz', `<ol class="plan">${games.map(x => `<li><div class="gh"><span>${GT(x.g)}<small class="pm">${LN[x.len]}, ${LENS[x.g][x.len]} ${LENS[x.g][x.len] === 1 ? LENS[x.g].u.slice(0, -1) : LENS[x.g].u} · about ${MIN(EST(x.g, x.len, np))}</small></span>${infoBtn(x.g)}</div>${infoBox(x.g)}</li>`).join('')}</ol>`, len)}<p class="note wait">Waiting for the host to kick off.</p>`;
    app.innerHTML = `<section class="codebox"><span class="eb">Room code</span><strong>${esc(V.code)}</strong>
        <button class="btn ghost" id="share">Share invite</button><p class="note">Others join at <b>${esc(link)}</b>. TV: open <b>tdko.app/tv</b>${V.tv ? ' · <span class="ok">TV connected</span>' : ''}</p></section>
      ${host ? `<button class="btn big" data-a="start" ${V.players.length < 2 ? 'disabled' : ''}>${V.players.length < 2 ? 'Waiting for players…' : 'Kick off'}</button>` : ''}
      <section class="card you"><span class="eb">You're playing as</span><button class="namebtn" data-a="rename">${esc((me() || {}).name || '')} <small>Change</small></button></section>
      ${cfg}<p class="err">${esc(flash)}</p><button class="link" id="leave">Leave room</button>`;
    $('#share').onclick = () => { const url = `https://${link}`, text = `Join my football quiz on The Daily Kick Off. Code ${V.code}`; if (navigator.share) navigator.share({ title: 'The Daily Kick Off', text, url }).catch(() => {}); else { navigator.clipboard && navigator.clipboard.writeText(`${text}: ${url}`); flash = 'Invite copied.'; draw(true); } };
    $('#leave').onclick = () => leave('');
  }

  function gameHead(g) {
    const cfg = V.config.games[V.gi], total = g.type === 'fb' ? (g.step === 'q' ? 15000 : 4000) : g.step === 'kick' ? 5000 : g.type === 'rh' ? (g.step === 'q' ? 10000 : g.step === 'res' ? 3500 : 4500) : g.type === 'cs' ? (g.step === 'play' ? g.dur : 4500) : g.type === 'wtb' ? ({ clue: 10000, final: 30000 }[g.step] || 7000) : (g.step === 'ready' ? 5000 : g.step === 'turn' ? 10000 : 4500);
    return `<header class="ghead"><span class="eb">Game ${V.gi + 1} of ${V.config.games.length} · ${esc(GAMES[g.type])}</span><span class="eb">${g.n} / ${g.of}</span></header>${g.paused ? '<p class="paused">Paused by the host</p>' : g.wait ? '' : bar(g.until, total)}`;
    void cfg;
  }
  function turnBanner(g) {
    const who = sideName(g.turn), mine = g.myTurn;
    if (g.step === 'ready') return `<div class="turn ${mine ? 'mine' : ''}"><span>${mine ? 'Your turn next' : esc(who) + ' next'}</span><b>${cd(g.until)}</b></div>`;
    if (g.step === 'turn') return `<div class="turn live ${mine ? 'mine' : ''}"><span>${mine ? 'Your turn' : esc(who) + "'s turn"}</span><b>${cd(g.until)}</b></div>`;
    return '';
  }
  // Touch phones: our own keyboard in a dock pinned to the bottom, so the phone's keyboard never covers the game.
  const OSK = !TV && window.matchMedia && matchMedia('(pointer: coarse)').matches;
  let dockPh = null;
  const KEYS = ['qwertyuiop', 'asdfghjkl', 'zxcvbnm'];
  function syncDock() {
    let d = $('#dock');
    if (!dockPh) { if (d) d.hidden = true; document.body.classList.remove('osk'); return; }
    if (!d) {
      d = document.createElement('div'); d.id = 'dock';
      d.innerHTML = `<form id="af" class="answer"><input id="ai" readonly tabindex="-1" autocomplete="off" spellcheck="false" aria-label="Your answer"></form>
        <div class="kbd" role="group" aria-label="Keyboard">${KEYS.map((r, i) => `<div class="r">${i === 2 ? '<button type="button" data-k="\'">’</button>' : ''}${[...r].map(c => `<button type="button" data-k="${c}">${c}</button>`).join('')}${i === 2 ? '<button type="button" data-k="del" class="wide" aria-label="Delete">⌫ Del</button>' : ''}</div>`).join('')}
        <div class="r"><button type="button" data-k="clear" class="clr">Clear</button><button type="button" data-k="-">-</button><button type="button" data-k=" " class="space" aria-label="Space">Space</button><button type="button" data-k="go" class="go">Enter</button></div></div>`;
      document.body.appendChild(d);
      const ai = d.querySelector('#ai');
      const press = k => {
        let v = ai.value;
        if (k === 'del') v = v.slice(0, -1);
        else if (k === 'clear') v = '';
        else if (k === 'go') { const f = $('#af'); if (f && f.requestSubmit) f.requestSubmit(); else if (f) f.dispatchEvent(new Event('submit', { cancelable: true })); return; }
        else if (k === ' ') { if (v && !/[ -]$/.test(v)) v += ' '; }
        else v += (!v || /[ -]$/.test(v)) ? k.toUpperCase() : k;
        ai.value = v.slice(0, 40); typed = ai.value;
      };
      d.querySelectorAll('[data-k]').forEach(btn => {
        btn.addEventListener('pointerdown', e => { e.preventDefault(); btn.classList.add('dn'); press(btn.dataset.k); });
        ['pointerup', 'pointerleave', 'pointercancel'].forEach(t => btn.addEventListener(t, () => btn.classList.remove('dn')));
        btn.addEventListener('click', e => { if (e.detail === 0) press(btn.dataset.k); }); // keyboard / switch access
      });
    }
    d.hidden = false; document.body.classList.add('osk');
    const ai = d.querySelector('#ai'); ai.placeholder = dockPh; if (ai.value !== typed) ai.value = typed;
    document.documentElement.style.setProperty('--dockh', d.offsetHeight + 'px');
  }
  function inputBox(ph) {
    if (OSK) { dockPh = ph; return ''; }
    return `<form id="af" class="row answer"><input id="ai" autocomplete="off" autocapitalize="words" spellcheck="false" placeholder="${esc(ph)}" value="${esc(typed)}"><button class="btn">Go</button></form>`;
  }
  function scores(g) {
    const pts = id => g.score[id] || 0, rows = standings(pts);
    return `<section class="lbwrap"><span class="eb">Leaderboard</span><ol class="table live">${rows.map((s, i) => `<li class="${s.id === mySide() ? 'me' : ''}${teamCls(s.id)}${g.alive && !g.alive.includes(s.id) ? ' out' : ''}"><span class="pos">${i && pts(rows[i - 1].id) === pts(s.id) ? '=' : i + 1}</span><span class="nm">${esc(s.name)}</span><b>${fmt(pts(s.id))}</b></li>`).join('')}</ol></section>`;
  }

  function fb(g) {
    const mine = g.mine || (pend && pend.k === qkey() ? { o: pend.o } : null), done = mine && 'ok' in mine;
    const opts = g.o.map(o => `<button class="opt ${mine && mine.o === o ? (done ? (mine.ok ? 'right' : 'wrong') : 'picked') : ''}" data-a="fb" data-o="${esc(o)}" ${mine || TV ? 'disabled' : ''}>${esc(o)}</button>`).join('');
    const res = done ? (mine.ok ? `<span class="ok">✓ Right · +${fmt(mine.pts)}</span>` : `<span class="bad">✗ Wrong · 0</span>`) : mine ? 'Locked in' : `${g.answered} of ${V.players.length} answered`;
    return `<h2 class="q">${esc(g.q)}</h2><div class="opts">${opts}</div><p class="status"><b>${cd(g.until)}s</b> · ${res}</p>${scores(g)}`;
  }
  function wtb(g) {
    const rev = g.step === 'reveal', live = g.step === 'clue' || g.step === 'final';
    if (g.step === 'kick') return roundKick(g);
    const clues = `<ol class="clues">${(rev ? g.clues : g.clues.slice().reverse()).map(([k, v], i) => `<li class="${i === 0 && !rev ? 'new' : ''}"><span>${esc(k)}</span><b>${esc(v)}</b></li>`).join('')}</ol>`;
    const gotList = (g.got || []).map(x => `<span class="${x.side === mySide() ? 'me' : ''}${teamCls(x.side)}"><b>${esc(V.mode === 'teams' ? sideName(x.side) : x.who)}</b> +${fmt(x.pts)}</span>`).join('');
    let top;
    if (rev) top = `<div class="answer-card"><span class="eb">${g.got && g.got.length ? 'It was' : 'Nobody got him · 0 points'}</span><h2>${esc(g.answer)}</h2><p>${esc(g.blurb || '')}</p>${gotList ? `<p class="gotlist">${gotList}</p>` : ''}</div>`;
    else {
      const worth = g.step === 'final' ? `<div class="turn live ${g.mine ? '' : 'mine'}"><span>Last chance · ${fmt(g.pts)} pts</span><b>${cd(g.until)}</b></div>`
        : `<div class="wtbhead"><div><span class="eb">${esc(g.position || '')} · clue ${g.clue} of ${g.total}</span><b class="worth">${fmt(g.pts)}</b><small>points if you name him now</small></div><div class="nextclue">${g.clue < g.total ? 'Next clue' : 'Last guess'} in <b>${cd(g.until)}s</b></div></div>`;
      const mineCard = g.mine && !TV ? `<div class="gotit"><b>✓ ${V.mode === 'teams' && g.mine.who !== (me() || {}).name ? esc(g.mine.who) + ' got him for your team' : 'You got him'} · +${fmt(g.mine.pts)}</b><span>Waiting for ${g.left} other${g.left === 1 ? '' : 's'}…</span></div>` : '';
      top = worth + mineCard + (gotList ? `<p class="gotlist">${gotList}</p>` : '');
    }
    const box = live && !TV && !g.mine ? inputBox('Who is it? Surname is fine') : '';
    const mine = live && !g.mine && g.wrong && g.wrong.length ? `<p class="wrongs">${g.wrong.slice().reverse().map(w => `<span>✗ ${esc(w)}</span>`).join('')}</p>` : '';
    const count = live ? `<p class="note">${g.guesses} guess${g.guesses === 1 ? '' : 'es'} so far</p>` : '';
    return `${top}${rev && g.wait ? nextBar('Start the next player') : ''}${box}${mine}${count}${clues}${scores(g)}`;
  }
  function cs(g) {
    if (g.step === 'kick') return roundKick(g);
    const rev = g.step === 'reveal', live = g.step === 'play';
    const slots = `<ol class="slots">${g.slots.map((s, i) => `<li class="${s.n ? (s.missed ? 'missed' : 'found' + teamCls(s.by) + (s.by === mySide() ? ' mine' : '')) : ''}"><span class="no">${i + 1}</span>${s.n ? `<b>${esc(s.n)}</b>${s.l ? `<small>${esc(s.l)}</small>` : ''}${s.who && !s.missed ? `<em>${esc(V.mode === 'teams' ? sideName(s.by) : s.who)} +${fmt(s.pts)}</em>` : ''}` : '<b>&nbsp;</b>'}</li>`).join('')}</ol>`;
    const head = live ? `<div class="wtbhead"><div><span class="eb">${g.found} of ${g.total} found</span><b class="worth">${fmt(g.pts)}</b><small>points per name right now</small></div><div class="nextclue">Time left <b>${cd(g.until)}s</b></div></div>`
      : rev ? `<div class="answer-card"><span class="eb">${g.found} of ${g.total} found</span><h2>List over</h2></div>` : '';
    const box = live && !TV ? inputBox('Name a player on the list') : '';
    const mine = live && g.wrong && g.wrong.length ? `<p class="wrongs">${g.wrong.slice().reverse().map(w => `<span>✗ ${esc(w)}</span>`).join('')}</p>` : '';
    return `${rev && g.wait ? nextBar('Start the next list') : ''}<h2 class="q">${esc(g.q)}</h2>${g.note ? `<p class="note">${esc(g.note)}</p>` : ''}${head}${box}${mine}${slots}${scores(g)}`;
  }
  function rh(g) {
    if (g.step === 'kick') return roundKick(g);
    const rev = g.step === 'reveal', q = g.step === 'q', res = g.step === 'res';
    const picked = g.mine ? g.mine.call : (pend && pend.k === qkey() ? pend.o : null);
    const nextV = g.next && g.next.v != null ? `<b>${fmt(g.next.v)}</b>` : '<b>?</b>';
    const card = g.cur && !rev ? `<div class="rh"><div class="rcard"><span class="eb">Now</span><h3>${esc(g.cur.n)}</h3><b>${fmt(g.cur.v)}</b><small>${esc(g.unit)}</small></div>
      <div class="rcard next ${res && g.last ? (g.last.v >= g.cur.v ? 'up' : 'down') : ''}"><span class="eb">Next</span><h3>${g.next ? esc(g.next.n) : '…'}</h3>${nextV}<small>${res ? esc(g.unit) : 'Higher or lower?'}</small></div></div>` : '';
    let top;
    if (rev) top = `<div class="answer-card"><span class="eb">Round ${g.n} of ${g.of} · ${esc(g.theme)}</span><h2>${g.winner ? esc(sideName(g.winner)) + (V.mode === 'teams' ? ' are' : ' is') + ' the last one standing' : g.alive && g.alive.length ? 'Made it to the end' : 'Everyone is out'}</h2>
      <p class="gotlist">${standings(id => (g.rpts || {})[id] || 0).map(s => `<span class="${s.id === mySide() ? 'me' : ''}${teamCls(s.id)}"><b>${esc(s.name)}</b> +${fmt((g.rpts || {})[s.id] || 0)}</span>`).join('')}</p></div>`;
    else top = `<div class="wtbhead"><div><span class="eb">${esc(g.theme)} · ${g.qn} of ${g.qs}</span><b class="worth">${q ? fmt(g.pts) : g.last && g.cur ? (g.last.v === g.cur.v ? 'Level' : g.last.v > g.cur.v ? '▲ Higher' : '▼ Lower') : ''}</b><small>${q ? 'points for a right call now' : 'next call coming up'}</small></div><div class="nextclue">${q ? `Time left <b>${cd(g.until)}s</b>` : ''}</div></div>`;
    let mid = '';
    if (q && !TV) mid = g.out ? `<p class="status bad">You're out this round. Watch on…</p>`
      : picked ? `<div class="hl"><button class="btn ${picked === 'higher' ? 'picked' : ''}" disabled>▲ Higher</button><button class="btn ${picked === 'lower' ? 'picked' : ''}" disabled>▼ Lower</button></div><p class="status">Locked in. ${g.answered} of ${g.alive.length} called…</p>`
      : `<div class="hl"><button class="btn" data-a="rh" data-c="higher">▲ Higher</button><button class="btn" data-a="rh" data-c="lower">▼ Lower</button></div>`;
    if (q && TV) mid = `<p class="status">${g.answered} of ${g.alive.length} called</p>`;
    if (res && g.last) mid = `<p class="gotlist">${Object.entries(g.last.res).map(([s, r]) => `<span class="${r.right ? '' : 'outx '}${s === mySide() ? 'me' : ''}${teamCls(s)}"><b>${esc(V.mode === 'teams' ? sideName(s) : r.who || sideName(s))}</b> ${r.right ? '✓ +' + fmt(r.pts) : r.call ? '✗ out' : 'no call · out'}</span>`).join('')}</p>`;
    const outs = !rev && g.start ? `<p class="note">${g.alive.length} of ${g.start.length} still in</p>` : '';
    return `${top}${rev && g.wait ? nextBar('Start the next round') : ''}${card}${mid}${outs}${scores(g)}`;
  }

  function countdown() {
    const gi = Math.max(0, V.gi), cfg = V.config.games[gi];
    return `<section class="kick"><span class="eb">${gi ? 'Next game in' : 'Kick off in'}</span><b class="secs" data-until="${V.until}">${secs(V.until)}</b><span class="eb">Game ${gi + 1} of ${V.config.games.length}</span><h2 class="gt big">${TT[cfg.g][0]} <i>${TT[cfg.g][1]}</i></h2><p class="note">${esc(DESC[cfg.g])}</p></section>`;
  }
  // the same 5-second countdown before every round (a new player, a new list, a new Ranked Highly round)
  const ROUND = { wtb: 'Player', cs: 'List', rh: 'Round' };
  function roundKick(g) {
    const sub = g.type === 'wtb' ? "Who's that baller?" : g.type === 'cs' ? esc(g.q) : g.type === 'rh' ? esc(g.theme) : g.myTurn ? 'You start' : esc(sideName(g.turn)) + ' starts';
    return `<section class="kick wkick"><span class="eb">${ROUND[g.type]} ${g.n} of ${g.of} · starts in</span><b class="secs" data-until="${g.until}">${secs(g.until)}</b><h2>${sub}</h2></section>${scores(g)}`;
  }
  // the host moves the quiz on: after each round's reveal, and from Full time to the next game
  // between rounds and games: everyone taps Ready (shown to all and on the TV); once all are in, the game moves on by itself.
  // The host can still start straight away.
  function nextBar(label) {
    const here = V.players.filter(p => p.here !== false), R = new Set(V.ready || []), mine = R.has(V.me), n = here.filter(p => R.has(p.pid)).length;
    const chips = `<ul class="readyl">${here.map(p => `<li class="${R.has(p.pid) ? 'on' : ''}${p.pid === V.me ? ' me' : ''}">${R.has(p.pid) ? '✓ ' : ''}${esc(p.name)}</li>`).join('')}</ul>`;
    const head = `<p class="readyh">${V.allReady ? "Everyone's ready" : `Ready: <b>${n} of ${here.length}</b>`}</p>`;
    const btn = TV || V.allReady ? '' : mine ? `<p class="status">You're ready. Waiting for the others…</p>` : `<button class="btn big" data-a="ready">I'm ready</button>`;
    const host = !TV && V.isHost && !V.allReady ? `<button class="link startnow" data-a="next">${esc(label)} now</button>` : '';
    return `<section class="readybox">${head}${chips}${btn}${host}</section>`;
  }
  function between() {
    const last = V.results[V.results.length - 1], next = V.config.games[V.gi + 1];
    const pts = id => last.score[id] || 0, st = last ? standings(pts) : [];
    const rows = st.map((s, i) => `<li class="${s.id === mySide() ? 'me' : ''}${teamCls(s.id)}"><span class="pos">${i && pts(st[i - 1].id) === pts(s.id) ? '=' : i + 1}</span><span class="nm">${esc(s.name)}</span><b>+${fmt(pts(s.id))}</b></li>`).join('');
    if (TV) return `<div class="betw"><section class="card"><h3>Full time · ${esc(GAMES[last.g])}</h3><ol class="table">${rows}</ol></section>${table('Quiz table')}</div>${upNext(next)}${nextBar('Start ' + GAMES[next.g])}`;
    // phones: one table (this game and the quiz total side by side) so the whole screen fits without scrolling
    const tot = id => V.quiz[id] || 0, qt = standings(tot);
    const one = qt.map((s, i) => `<li class="${s.id === mySide() ? 'me' : ''}${teamCls(s.id)}"><span class="pos">${i && tot(qt[i - 1].id) === tot(s.id) ? '=' : i + 1}</span><span class="nm">${esc(s.name)}</span><small class="gp">+${fmt(pts(s.id))}</small><b>${fmt(tot(s.id))}</b></li>`).join('');
    return `<section class="card ftc"><h3>Full time · ${esc(GAMES[last.g])}</h3><p class="cols"><span>This game</span><span>Quiz</span></p><ol class="table">${one}</ol></section>${upNext(next)}${nextBar('Start ' + GAMES[next.g])}`;
  }
  // what's coming, so everyone can read it before the host starts the countdown
  function upNext(x) {
    const n = Math.max(2, V.players.length), k = LENS[x.g][x.len];
    return `<section class="card upnext"><span class="eb"><b class="un">Up next</b> · Game ${V.gi + 2} of ${V.config.games.length}</span>${GT(x.g)}<p class="unmeta">${LN[x.len]} · ${k} ${k === 1 ? LENS[x.g].u.replace(/s$/, '') : LENS[x.g].u} · about ${MIN(EST(x.g, x.len, n))}</p><p>${DESC[x.g]}</p></section>`;
  }
  // Final whistle graph: running quiz totals after every score, one line per player or team
  const lineColour = id => V.mode === 'teams' ? `var(--${id})` : `var(--s${(V.sides.findIndex(s => s.id === id) % 6) + 1})`;
  // Final whistle: "The race", positions through the quiz (who led, who climbed), drawn like a game's leaderboard race
  function graph() {
    const tl = V.tl || []; if (tl.length < 2) return '';
    const ids = V.sides.map(s => s.id), games = V.config.games.slice(0, (V.results || []).length || 1), n = ids.length;
    // three checkpoints a game (a third in, two thirds in, full time) from the running totals
    const cps = []; let lastT = tl[0].t;
    games.forEach((_, gi) => { const ps = tl.filter(p => p.gi === gi); const pick = f => ps.length ? ps[Math.min(ps.length - 1, Math.max(0, Math.round(f * ps.length) - 1))].t : lastT;
      [1 / 3, 2 / 3, 1].forEach(f => cps.push({ gi, t: pick(f) })); if (ps.length) lastT = ps[ps.length - 1].t; });
    let prevOrder = ids.slice();
    const rankAt = t => { const o = ids.slice().sort((a, b) => ((t[b] || 0) - (t[a] || 0)) || (prevOrder.indexOf(a) - prevOrder.indexOf(b))); prevOrder = o; return Object.fromEntries(o.map((id, i) => [id, i])); };
    const ranks = cps.map(c => rankAt(c.t));
    // the last column follows the final table exactly (same tie-break), and players level on points share a medal
    const ft = standings(id => V.quiz[id] || 0), pts = id => V.quiz[id] || 0;
    ranks[ranks.length - 1] = Object.fromEntries(ft.map((x, i) => [x.id, i]));
    const place = Object.fromEntries(ft.map((x, i) => [x.id, ft.findIndex(y => pts(y.id) === pts(x.id))]));
    // lead changes across every score, and the biggest climb from after the first game to the end
    let leads = 0, leader = null; prevOrder = ids.slice();
    tl.slice(1).forEach(p => { const r = rankAt(p.t), top = ids.find(id => r[id] === 0); if ((p.t[top] || 0) > 0) { if (leader && top !== leader) leads++; leader = top; } });
    const firstEnd = ranks[2] || ranks[0], fin = ranks[ranks.length - 1];
    const climb = ids.map(id => ({ id, up: firstEnd[id] - fin[id] })).sort((a, b) => b.up - a.up)[0];
    const W = 480, L = 40, R = 118, T = 10, RH = 34, B = 30, H = T + RH * n + B, iw = W - L - R;
    const x = i => L + iw * (i + 0.5) / cps.length, y = r => T + RH * r + RH / 2;
    let svg = `<defs><filter id="glow" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="2.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>`;
    const bw = iw / games.length;
    games.forEach((g, gi) => { svg += `<rect x="${L + bw * gi}" y="${T - 4}" width="${bw}" height="${RH * n + 8}" rx="8" class="band${gi % 2 ? ' alt' : ''}"/><text x="${L + bw * (gi + .5)}" y="${H - 10}" class="gn" text-anchor="middle">${({ fb: 'Fast Break', wtb: 'Baller', cs: 'Sweep', rh: 'Ranked' })[g.g]}</text>`; });
    for (let r = 0; r < n; r++) svg += `<text x="${L - 10}" y="${y(r) + 5}" class="rk" text-anchor="end">${r + 1}${['st', 'nd', 'rd'][r] || 'th'}</text>`;
    for (const id of ids.slice().sort((a, b) => fin[b] - fin[a])) {
      const c = lineColour(id); let d = `M${x(0)},${y(ranks[0][id])}`;
      for (let i = 1; i < cps.length; i++) { const x0 = x(i - 1), x1 = x(i), y0 = y(ranks[i - 1][id]), y1 = y(ranks[i][id]), m = (x0 + x1) / 2; d += ` C${m},${y0} ${m},${y1} ${x1},${y1}`; }
      svg += `<path d="${d}" fill="none" stroke="${c}" stroke-width="${fin[id] === 0 ? 7 : 5}" stroke-linecap="round" filter="url(#glow)" opacity="${fin[id] === 0 ? 1 : .85}"/>`;
      cps.forEach((cp, i) => { if (i % 3 === 2) svg += `<circle cx="${x(i)}" cy="${y(ranks[i][id])}" r="${i === cps.length - 1 ? 8 : 5}" fill="${c}" stroke="var(--surface)" stroke-width="2.5"/>`; });
      svg += `<text x="${W - R + 16}" y="${y(fin[id]) + 5}" class="lb${id === mySide() ? ' me' : ''}" fill="${c}">${['🥇 ', '🥈 ', '🥉 '][place[id]] || ''}${esc(sideName(id))}</text>`;
    }
    const chips = [`<span>Lead changes <b>${leads}</b></span>`].concat(climb && climb.up > 0 ? [`<span>Biggest climb <b>${esc(sideName(climb.id))} ↑${climb.up}</b></span>`] : []).join('');
    return `<section class="card graph race"><h3>The race</h3><div class="chips">${chips}</div><svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Positions through the quiz">${svg}</svg></section>`;
  }
  function final() {
    const rows = standings(id => V.quiz[id] || 0), w = rows[0];
    const shareText = `⚽ The Daily Kick Off · Multiplayer\n${rows.map((s, i) => `${['🥇', '🥈', '🥉'][i] || (i + 1) + '.'} ${s.name} ${fmt(V.quiz[s.id])}`).join('\n')}\nHost your own: https://tdko.app/multiplayer.html`;
    return `<section class="hero"><span class="eb">Final whistle</span><h1>${w && w.id === mySide() && !TV ? (V.mode === 'teams' ? esc(w.name) : 'You') : esc(w ? w.name : '')} <i>win${V.mode === 'teams' || (w && w.id === mySide() && !TV) ? '' : 's'}</i></h1></section><div class="finw">${table('Final table')}${graph()}</div>
      ${TV ? '' : `<button class="btn big" id="sharefin">Share the result</button>${V.isHost ? '<button class="btn ghost" data-a="rematch">Rematch</button>' : '<p class="note">Waiting for the host to start a rematch…</p>'}<button class="link" id="leave">Leave room</button>`}
      <span hidden id="sharetext">${esc(shareText)}</span>`;
  }

  // ---------- draw ----------
  let lastSig = '';
  function draw(force) {
    if (!V) return;
    if (flash !== flashSeen) { flashSeen = flash; flashAt = Date.now(); }
    const sig = JSON.stringify({ ...V, now: 0 }) + flash;
    if (!force && sig === lastSig) return; lastSig = sig;
    const ai = $('#ai'); if (ai) typed = ai.value;
    const key = [V.phase, V.gi, V.game && V.game.type, V.game && V.game.n, V.game && V.game.step, V.game && V.game.turn].join('|');
    if (key !== draftKey) { typed = ''; draftKey = key; }
    let html = ''; dockPh = null;
    if (V.phase === 'lobby') { syncDock(); lobby(); bind(); tvFit(); return; }
    if (V.phase === 'game' && V.game) { const g = V.game; html = gameHead(g) + ({ fb, wtb, cs, rh }[g.type])(g) + hostBar(); }
    else if (V.phase === 'countdown') html = countdown();
    else if (V.phase === 'between') html = between();
    else if (V.phase === 'final') html = final();
    const focus = document.activeElement && document.activeElement.id === 'ai';
    app.innerHTML = `<div class="${TV ? 'tvgame' : 'pgame'}">${html}</div><p class="err">${esc(flash)}</p>`;
    syncDock();
    if (OSK) {}
    else if (focus && $('#ai')) { const el = $('#ai'); el.focus(); el.setSelectionRange(el.value.length, el.value.length); }
    else if (!TV && $('#ai') && V.game && (V.game.myTurn || (V.game.type === 'wtb' && V.game.clue === 1) || (V.game.type === 'cs' && V.game.found === 0))) $('#ai').focus();
    bind(); tvFit(); phoneFit();
  }
  function bind() {
    app.querySelectorAll('[data-a]').forEach(el => {
      const a = el.dataset.a;
      if (el.tagName === 'INPUT') { el.onchange = () => toggleGame(el.dataset.g, el.checked); return; }
      const fire = e => {
        e.preventDefault();
        if (a === 'sec') { const k = el.dataset.s; SHUT.has(k) ? SHUT.delete(k) : SHUT.add(k); lobby(); bind(); const b = app.querySelector(`[data-a="sec"][data-s="${k}"]`); if (b) b.focus(); return; }
        if (a === 'info') { const g = el.dataset.g; INFO.has(g) ? INFO.delete(g) : INFO.add(g); lobby(); bind(); const b = app.querySelector(`.info[data-g="${g}"]`); if (b) b.focus(); return; }
        if (a === 'len') return setLen(el.dataset.g, el.dataset.l);
        if (a === 'mode') return send({ type: 'mode', mode: el.dataset.m, teams: +el.dataset.n || 2 });
        if (a === 'team') { const p = V.players.find(p => p.pid === el.dataset.p), ids = V.teams.map(t => t.id); return send({ type: 'team', pid: el.dataset.p, team: ids[(ids.indexOf(p.side) + 1) % ids.length] }); }
        if (a === 'kick') return send({ type: 'kick', pid: el.dataset.p });
        if (a === 'teamname') { const n = prompt('Team name (16 characters max)', (V.teams.find(t => t.id === el.dataset.t) || {}).name || ''); if (n && n.trim().length > 16) { flash = 'Team names can be 16 characters at most.'; draw(true); return; } if (n) send({ type: 'teamname', team: el.dataset.t, name: n }); return; }
        if (a === 'rename') { const n = prompt('Your name (2 to 16 characters)', (me() || {}).name || ''); if (n && n.trim().replace(/\s+/g, ' ').length > 16) { flash = 'Names can be 16 characters at most.'; draw(true); return; } if (n) send({ type: 'name', name: n }); return; }
        // show the press straight away; the server confirms on the next reply
        if (a === 'fb') { if (pend && pend.k === qkey()) return; pend = { k: qkey(), o: el.dataset.o }; app.querySelectorAll('.opt').forEach(b => { b.disabled = true; if (b === el) b.classList.add('picked'); }); const st = $('.status'); if (st) st.textContent = 'Locked in. Waiting for the others…'; return send({ type: 'answer', o: el.dataset.o }, true); }
        if (a === 'rh') { if (pend && pend.k === qkey()) return; pend = { k: qkey(), o: el.dataset.c }; app.querySelectorAll('.hl .btn').forEach(b => { b.disabled = true; if (b === el) b.classList.add('picked'); }); return send({ type: 'answer', call: el.dataset.c }, true); }
        if (a === 'end' && !confirm('End the quiz now?')) return;
        send({ type: a });
      };
      // answers fire on touch-down so a screen refresh between press and release never swallows them
      if (a === 'fb' || a === 'rh') el.onpointerdown = fire; else el.onclick = fire;
    });
    const f = $('#af'); if (f) f.onsubmit = e => { e.preventDefault(); const t = $('#ai').value.trim(); if (t) { typed = ''; $('#ai').value = ''; send({ type: 'answer', text: t }); } };
    const s = $('#sharefin'); if (s) s.onclick = () => { const text = $('#sharetext').textContent; if (navigator.share) navigator.share({ text }).catch(() => {}); else if (navigator.clipboard) { navigator.clipboard.writeText(text); flash = 'Result copied.'; draw(true); } };
    const l = $('#leave'); if (l) l.onclick = () => leave('');
  }
  function toggleGame(g, on) {
    let games = V.config.games.filter(x => x.g !== g);
    if (on) games.push({ g, len: 'm' });
    const order = Object.keys(GAMES); games.sort((a, b) => order.indexOf(a.g) - order.indexOf(b.g));
    if (!games.length) { flash = 'Pick at least one game.'; return draw(true); }
    send({ type: 'config', games });
  }
  function setLen(g, l) { send({ type: 'config', games: V.config.games.map(x => x.g === g ? { g, len: l } : x) }); }

  // countdowns tick between polls
  setInterval(() => {
    app.querySelectorAll('.secs[data-until]').forEach(el => { el.textContent = secs(+el.dataset.until); });
    app.querySelectorAll('.clock[data-until]').forEach(el => { el.firstChild.style.width = Math.max(0, Math.min(100, (+el.dataset.until - now()) / +el.dataset.total * 100)) + '%'; });
  }, 250);
  document.addEventListener('visibilitychange', () => { if (!document.hidden) poll(); });

  // start: a link like /m/KICK or ?c=KICK joins that room; a saved room rejoins after a refresh
  const q = new URLSearchParams(location.search).get('c'), saved = TV ? null : store.get('tdko-mp-code');
  if (!TV && q && /^[A-Z]{4}$/i.test(q)) join(q.toUpperCase());
  else if (TV && q && /^[A-Z]{4}$/i.test(q)) go(q.toUpperCase());
  else if (saved) join(saved, true);
  else home('');
})();
