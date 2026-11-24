/* The Daily Kick Off · Multiplayer (Phase 1). One script for the phone page (multiplayer.html) and the TV page (tv.html).
   The server owns the clock and every result; this file only sends actions and draws the view it is given. */
(function () {
  'use strict';
  const TV = document.body.dataset.mp === 'tv';
  const $ = s => document.querySelector(s);
  const app = $('#mp');
  const esc = s => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const GAMES = { fb: 'Fast Break', wtb: "Who's That Baller", cs: 'Clean Sweep', rh: 'Ranked Highly' };
  const DESC = { fb: 'Everyone answers the same question at once. Every right answer scores 100, plus up to 50 for speed.',
    wtb: 'Everyone guesses at once. A new clue every 10 seconds, first to name him wins: 1,000 on the first clue, 100 less for each new one. Guess as often as you like. Surname is fine, first name alone is not.',
    cs: 'Take turns to name a player on the list. 100 points for each one.',
    rh: 'Take turns to call higher or lower. Get one wrong and you are out. Last one standing scores 1,000.' };
  const fmt = n => (n || 0).toLocaleString('en-GB');
  const LENS = { fb: { s: 10, m: 15, l: 20, u: 'questions' }, wtb: { s: 3, m: 5, l: 7, u: 'players' }, cs: { s: 1, m: 2, l: 3, u: 'lists' }, rh: { s: 1, m: 2, l: 3, u: 'rounds' } };
  const LN = { s: 'Short', m: 'Standard', l: 'Long' };
  const store = { get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }, set(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }, del(k) { try { localStorage.removeItem(k); } catch (e) {} } };
  let pid = TV ? 'tv' : store.get('tdko-mp-pid');
  if (!pid) { pid = 'p-' + (crypto.randomUUID ? crypto.randomUUID() : (Date.now().toString(36) + Math.random().toString(36).slice(2))).replace(/[^A-Za-z0-9-]/g, '').slice(0, 40); store.set('tdko-mp-pid', pid); }
  let pend = null; const qkey = () => V && V.game ? [V.round, V.gi, V.game.type, V.game.n, V.game.i, V.game.cur && V.game.cur.n].join('|') : '';
  let code = null, V = null, offset = 0, polls = 0, timer = null, busy = false, flash = '', flashSeen = '', flashAt = 0, draftKey = '', typed = '';

  const now = () => Date.now() + offset;
  if (TV) { const fit = () => document.documentElement.style.setProperty('--z', Math.max(1, Math.min(2.4, innerWidth / 760, innerHeight / 500)).toFixed(2)); fit(); addEventListener('resize', fit); }
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
    return `<section class="card"><h3>${esc(title)}</h3><ol class="table">${rows.map(s => `<li class="${s.id === mySide() ? 'me' : ''}${teamCls(s.id)}"><span class="pos">${pos(s)}</span><span class="nm">${esc(s.name)}</span><b>${fmt(V.quiz[s.id])}</b></li>`).join('')}</ol></section>`;
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
  function home(msg) {
    if (TV) {
      app.innerHTML = `<section class="tvjoin"><h1>The Daily Kick Off <i>on the TV</i></h1><p>Type the 4-letter room code from the host's phone.</p>
        <form id="tvf"><input id="tvc" maxlength="4" autocapitalize="characters" autocomplete="off" placeholder="CODE"><button>Show quiz</button></form><p class="err">${esc(msg || '')}</p></section>`;
      $('#tvf').onsubmit = e => { e.preventDefault(); const c = $('#tvc').value.trim().toUpperCase(); if (/^[A-Z]{4}$/.test(c)) go(c); };
      return;
    }
    app.innerHTML = `<section class="hero"><span class="eb">Multiplayer</span><h1>Play <i>together</i></h1><p class="lede">Up to 6 players, each on their own phone. Host a quiz, share the code, kick off.</p></section>
      <section class="card" id="hostcard"><button class="btn big" id="host">Host a quiz</button></section>
      <section class="card"><form id="jf" class="row"><input id="jc" maxlength="4" autocapitalize="characters" autocomplete="off" placeholder="CODE" aria-label="Room code"><button class="btn">Join</button></form></section>
      <p class="err">${esc(msg || '')}</p>
      <p class="note">Got a TV? Open <b>tdko.app/tv</b> on it and type the room code to show the quiz on the big screen.</p>`;
    const askPass = m => {
      $('#hostcard').innerHTML = `<p class="lede">Multiplayer is in the Training Ground for now. Enter your Training Ground code to host. Anyone can join with a room code.</p>
        <form id="pf" class="row"><input id="pc" autocapitalize="characters" autocomplete="off" spellcheck="false" placeholder="TDKO-XXXXX" aria-label="Training Ground code"><button class="btn">Unlock</button></form><p class="err">${esc(m || '')}</p>`;
      $('#pf').onsubmit = async e => { e.preventDefault();
        try { const r = await fetch('/api/tester', { headers: { 'x-tdko-tester': $('#pc').value.trim().toUpperCase() } }); const j = await r.json();
          if (!j.pass) return askPass("That code isn't right."); store.set('tdko-mp-pass', j.pass); store.set('tdko-tester', '3'); home(); } catch (_) { askPass('Could not check the code. Try again.'); } };
    };
    $('#host').onclick = async () => { const pass = store.get('tdko-mp-pass'); if (!pass) return askPass();
      const r = await call('create', { pid, pass }); if (r.code) go(r.code); else if (r.needPass) { store.del('tdko-mp-pass'); askPass(r.error); } else home(r.error); };
    $('#jf').onsubmit = async e => { e.preventDefault(); const c = $('#jc').value.trim().toUpperCase(); if (!/^[A-Z]{4}$/.test(c)) return home('That code needs 4 letters.'); join(c); };
  }
  async function join(c, quiet) {
    const r = await call('join', { code: c, pid });
    if (r.view) { if (r.error) flash = r.error; go(c); } else { if (quiet) store.del('tdko-mp-code'); home(quiet ? '' : r.error); }
  }

  function lobby() {
    const host = V.isHost, link = `tdko.app/m/${V.code}`;
    const games = V.config.games, on = g => games.find(x => x.g === g);
    const pl = p => `<li class="${p.pid === pid ? 'me' : ''}${teamCls(p.side)}">${p.here ? '' : '<span class="away">away</span>'}<span class="nm">${esc(p.name)}</span>${p.pid === V.host ? '<em>host</em>' : ''}
        ${host && !TV && V.mode === 'teams' ? `<button class="mini" data-a="team" data-p="${esc(p.pid)}">Move</button>` : ''}${host && !TV && p.pid !== V.host ? `<button class="mini x" data-a="kick" data-p="${esc(p.pid)}" aria-label="Remove ${esc(p.name)}">✕</button>` : ''}</li>`;
    const players = V.mode === 'teams'
      ? V.teams.map(t => `<div class="team t-${esc(t.id)}"><h4>${esc(t.name)}${host && !TV ? ` <button class="mini" data-a="teamname" data-t="${esc(t.id)}">Rename</button>` : ''}</h4><ul class="people">${V.players.filter(p => p.side === t.id).map(pl).join('') || '<li class="empty">Nobody yet</li>'}</ul></div>`).join('')
      : `<ul class="people">${V.players.map(pl).join('')}</ul>`;
    if (TV) {
      app.innerHTML = `<section class="tvlobby"><div class="big-code"><span>Join at</span><b>${esc(link)}</b><span>or tdko.app → Multiplayer → code</span><strong>${esc(V.code)}</strong></div>
        <div class="tvpeople"><h2>${V.players.length} of 6 in</h2>${players}<p class="note">${games.map(x => GAMES[x.g]).join(' · ')}</p></div></section>`;
      return;
    }
    const cfg = host ? `<section class="card"><h3>The quiz</h3>${Object.keys(GAMES).map(g => { const x = on(g); return `<div class="game ${x ? 'on' : ''}"><label><input type="checkbox" data-a="g" data-g="${g}" ${x ? 'checked' : ''}> <b>${GAMES[g]}</b></label>
        <div class="seg">${['s', 'm', 'l'].map(l => `<button data-a="len" data-g="${g}" data-l="${l}" class="${x && x.len === l ? 'on' : ''}" ${x ? '' : 'disabled'}>${LN[l]}<small>${LENS[g][l]} ${LENS[g][l] === 1 ? LENS[g].u.slice(0, -1) : LENS[g].u}</small></button>`).join('')}</div><p class="note">${DESC[g]}</p></div>`; }).join('')}</section>
      <section class="card"><h3>Players</h3><div class="seg wide"><button data-a="mode" data-m="solo" class="${V.mode === 'solo' ? 'on' : ''}">Everyone for themselves</button><button data-a="mode" data-m="teams" data-n="2" class="${V.mode === 'teams' && V.teams.length === 2 ? 'on' : ''}">2 teams</button><button data-a="mode" data-m="teams" data-n="3" class="${V.mode === 'teams' && V.teams.length === 3 ? 'on' : ''}">3 teams</button></div>
        ${V.mode === 'teams' ? '<button class="mini" data-a="shuffle">Shuffle teams</button>' : ''}${players}</section>
      <button class="btn big" data-a="start" ${V.players.length < 2 ? 'disabled' : ''}>${V.players.length < 2 ? 'Waiting for players…' : 'Kick off'}</button>`
      : `<section class="card"><h3>Players</h3>${players}</section><section class="card"><h3>The quiz</h3><ol class="plan">${games.map(x => `<li><b>${GAMES[x.g]}</b> · ${LN[x.len]}, ${LENS[x.g][x.len]} ${LENS[x.g][x.len] === 1 ? LENS[x.g].u.slice(0, -1) : LENS[x.g].u}</li>`).join('')}</ol><p class="note">Waiting for the host to kick off.</p></section>`;
    app.innerHTML = `<section class="codebox"><span class="eb">Room code</span><strong>${esc(V.code)}</strong>
        <button class="btn ghost" id="share">Share invite</button><p class="note">Others join at <b>${esc(link)}</b>. TV: open <b>tdko.app/tv</b>${V.tv ? ' · <span class="ok">TV connected</span>' : ''}</p></section>
      <section class="card you"><span class="eb">You're playing as</span><button class="namebtn" data-a="rename">${esc((me() || {}).name || '')} <small>Change</small></button></section>
      ${cfg}<p class="err">${esc(flash)}</p><button class="link" id="leave">Leave room</button>`;
    $('#share').onclick = () => { const url = `https://${link}`, text = `Join my football quiz on The Daily Kick Off. Code ${V.code}`; if (navigator.share) navigator.share({ title: 'The Daily Kick Off', text, url }).catch(() => {}); else { navigator.clipboard && navigator.clipboard.writeText(`${text}: ${url}`); flash = 'Invite copied.'; draw(true); } };
    $('#leave').onclick = () => leave('');
  }

  function gameHead(g) {
    const cfg = V.config.games[V.gi], total = g.type === 'fb' ? (g.step === 'q' ? 15000 : 4000) : g.type === 'wtb' ? ({ ready: 3000, clue: 10000, final: 30000 }[g.step] || 4500) : (g.step === 'ready' ? 5000 : g.step === 'turn' ? 10000 : 4500);
    return `<header class="ghead"><span class="eb">Game ${V.gi + 1} of ${V.config.games.length} · ${esc(GAMES[g.type])}</span><span class="eb">${g.n} / ${g.of}</span></header>${g.paused ? '<p class="paused">Paused by the host</p>' : bar(g.until, total)}`;
    void cfg;
  }
  function turnBanner(g) {
    const who = sideName(g.turn), mine = g.myTurn;
    if (g.step === 'ready') return `<div class="turn ${mine ? 'mine' : ''}"><span>${mine ? 'Your turn next' : esc(who) + ' next'}</span><b>${cd(g.until)}</b></div>`;
    if (g.step === 'turn') return `<div class="turn live ${mine ? 'mine' : ''}"><span>${mine ? 'Your turn' : esc(who) + "'s turn"}</span><b>${cd(g.until)}</b></div>`;
    return '';
  }
  function inputBox(ph) {
    return `<form id="af" class="row answer"><input id="ai" autocomplete="off" autocapitalize="words" spellcheck="false" placeholder="${esc(ph)}" value="${esc(typed)}"><button class="btn">Go</button></form>`;
  }
  function scores(g) {
    return `<ol class="mini-table">${standings(id => g.score[id] || 0).map(s => `<li class="${s.id === mySide() ? 'me' : ''}${teamCls(s.id)}${g.alive && !g.alive.includes(s.id) ? ' out' : ''}"><span>${esc(s.name)}</span><b>${fmt(g.score[s.id])}</b></li>`).join('')}</ol>`;
  }

  function fb(g) {
    const rev = g.step === 'reveal', mine = g.mine || (!rev && pend && pend.k === qkey() ? { o: pend.o } : null);
    const opts = g.o.map(o => { const cls = rev ? (o === g.right ? 'right' : (mine && mine.o === o ? 'wrong' : '')) : (mine && mine.o === o ? 'picked' : ''); return `<button class="opt ${cls}" data-a="fb" data-o="${esc(o)}" ${mine || rev || TV ? 'disabled' : ''}>${esc(o)}</button>`; }).join('');
    const status = rev ? (TV ? `${g.who.length} of ${V.players.length} got it` : (mine && mine.pts ? `<span class="ok">Right · +${fmt(mine.pts)}</span>` : `<span class="bad">${mine && mine.o ? 'Wrong' : 'No answer'}</span>`))
      : (mine ? 'Locked in. Waiting for the others…' : `${cd(g.until)}s · ${g.answered} of ${V.players.length} answered`);
    return `<h2 class="q">${esc(g.q)}</h2><div class="opts">${opts}</div><p class="status">${status}</p>${scores(g)}`;
  }
  function wtb(g) {
    const rev = g.step === 'reveal', live = g.step === 'clue' || g.step === 'final';
    if (g.step === 'ready') return `<section class="kick wkick"><span class="eb">Player ${g.n} of ${g.of}</span><b class="secs" data-until="${g.until}">${secs(g.until)}</b><h2>Who's that baller?</h2><p class="note">First clue coming up. First to name him wins.</p></section>${scores(g)}`;
    const clues = `<ol class="clues">${(rev ? g.clues : g.clues.slice().reverse()).map(([k, v], i) => `<li class="${i === 0 && !rev ? 'new' : ''}"><span>${esc(k)}</span><b>${esc(v)}</b></li>`).join('')}</ol>`;
    let top;
    if (rev) top = `<div class="answer-card"><span class="eb">${g.winner ? esc(g.who || sideName(g.winner)) + ' got him · +' + fmt(g.won) : 'Nobody got him · 0 points'}</span><h2>${esc(g.answer)}</h2><p>${esc(g.blurb || '')}</p></div>`;
    else if (g.step === 'final') top = `<div class="turn live mine"><span>Last chance · ${fmt(g.pts)} pts</span><b>${cd(g.until)}</b></div>`;
    else top = `<div class="wtbhead"><div><span class="eb">${esc(g.position || '')} · clue ${g.clue} of ${g.total}</span><b class="worth">${fmt(g.pts)}</b><small>points if you name him now</small></div><div class="nextclue">${g.clue < g.total ? 'Next clue' : 'Last guess'} in <b>${cd(g.until)}s</b></div></div>`;
    const box = live && !TV ? inputBox('Who is it? Surname is fine') : '';
    const mine = !rev && g.wrong && g.wrong.length ? `<p class="wrongs">${g.wrong.slice().reverse().map(w => `<span>✗ ${esc(w)}</span>`).join('')}</p>` : '';
    const count = live ? `<p class="note">${g.guesses} guess${g.guesses === 1 ? '' : 'es'} so far</p>` : '';
    return `${top}${box}${mine}${count}${clues}${scores(g)}`;
  }
  function cs(g) {
    const rev = g.step === 'reveal';
    const slots = `<ol class="slots">${g.slots.map((s, i) => `<li class="${s.n ? (s.missed ? 'missed' : 'found' + teamCls(s.by)) : s.hint ? 'hint' : ''}"><span class="no">${i + 1}</span>${s.n ? `<b>${esc(s.n)}</b>${s.l ? `<small>${esc(s.l)}</small>` : ''}${s.by && !s.missed ? `<em>${esc(sideName(s.by))}</em>` : ''}` : s.hint ? `<b>${esc(s.hint)}</b>` : '<b>&nbsp;</b>'}</li>`).join('')}</ol>`;
    const found = g.slots.filter(s => s.n && !s.missed).length;
    return `<h2 class="q">${esc(g.q)}</h2><p class="note">${esc(g.note || '')} · ${found} of ${g.total} found</p>${rev ? '<p class="status">List over</p>' : turnBanner(g)}${g.myTurn && g.step === 'turn' ? inputBox('Name a player on the list') : ''}${slots}${log(g)}${scores(g)}`;
  }
  function rh(g) {
    const rev = g.step === 'reveal', mine = g.myTurn && g.step === 'turn' && !(pend && pend.k === qkey());
    const card = g.cur ? `<div class="rh"><div class="rcard"><span class="eb">${esc(g.theme)}</span><h3>${esc(g.cur.n)}</h3><b>${esc(g.cur.v)}</b><small>${esc(g.unit)}</small></div>
      <div class="rcard next"><span class="eb">Next</span><h3>${g.next ? esc(g.next.n) : '…'}</h3><b>?</b><small>Higher or lower?</small></div></div>` : '';
    const btns = mine ? `<div class="hl"><button class="btn" data-a="rh" data-c="higher">▲ Higher</button><button class="btn" data-a="rh" data-c="lower">▼ Lower</button></div>` : '';
    const top = rev ? `<div class="answer-card"><span class="eb">Round ${g.n}</span><h2>${g.winner ? esc(sideName(g.winner)) + ' is the last one standing' : 'Round over'}</h2></div>` : turnBanner(g);
    return `${top}${card}${btns}${log(g)}${scores(g)}`;
  }

  function countdown() {
    const first = V.config.games[0];
    return `<section class="kick"><span class="eb">Kick off in</span><b class="secs" data-until="${V.until}">${secs(V.until)}</b><h2>Game 1 · ${esc(GAMES[first.g])}</h2><p class="note">${esc(DESC[first.g])}</p></section>`;
  }
  function between() {
    const last = V.results[V.results.length - 1], next = V.config.games[V.gi + 1];
    const rows = last ? standings(id => last.score[id] || 0).map(s => `<li class="${s.id === mySide() ? 'me' : ''}${teamCls(s.id)}"><span class="nm">${esc(s.name)}</span><b>+${fmt(last.score[s.id])}</b></li>`).join('') : '';
    return `<div class="betw"><section class="card"><span class="eb">Full time · ${esc(GAMES[last.g])}</span><ol class="table res">${rows}</ol></section>${table('Quiz table')}</div><p class="status">Next: <b>${esc(GAMES[next.g])}</b> in ${cd(V.until)}s</p><p class="note">${esc(DESC[next.g])}</p>`;
  }
  // Final whistle graph: running quiz totals after every score, one line per player or team
  const lineColour = id => V.mode === 'teams' ? `var(--${id})` : `var(--s${(V.sides.findIndex(s => s.id === id) % 6) + 1})`;
  function graph() {
    const tl = V.tl || []; if (tl.length < 2) return '';
    const W = 480, H = 260, L = 50, R = 104, T = 26, B = 14, ids = V.sides.map(s => s.id);
    const max = Math.max(1, ...tl.map(p => Math.max(...ids.map(id => p.t[id] || 0))));
    const step = Math.pow(10, Math.floor(Math.log10(max))), nice = [1, 2, 2.5, 5, 10].map(m => m * step).find(m => max / m <= 4) || step * 10, top = Math.ceil(max / nice) * nice;
    const x = i => L + (W - L - R) * i / (tl.length - 1), y = v => T + (H - T - B) * (1 - v / top);
    let svg = '';
    for (let v = 0; v <= top; v += nice) svg += `<line x1="${L}" x2="${W - R}" y1="${y(v)}" y2="${y(v)}" class="gl"/><text x="${L - 8}" y="${y(v) + 4}" class="ax" text-anchor="end">${fmt(v)}</text>`;
    tl.forEach((p, i) => { if (i && p.gi !== tl[i - 1].gi || i === 0) { const g = V.config.games[p.gi]; svg += `<line x1="${x(Math.max(0, i - (i ? 1 : 0)))}" x2="${x(Math.max(0, i - (i ? 1 : 0)))}" y1="${T - 6}" y2="${H - B}" class="gd"/><text x="${x(Math.max(0, i - (i ? 1 : 0))) + 4}" y="${T - 10}" class="ax">${g ? esc(GAMES[g.g]) : ''}</text>`; } });
    const ends = ids.map(id => ({ id, v: tl[tl.length - 1].t[id] || 0 })).sort((a, b) => b.v - a.v);
    let prev = -1e9; ends.forEach(e => { e.ly = Math.max(y(e.v) + 5, prev + 18); prev = e.ly; });
    for (const id of ids) {
      const pts = tl.map((p, i) => `${x(i).toFixed(1)},${y(p.t[id] || 0).toFixed(1)}`).join(' '), e = ends.find(e => e.id === id);
      svg += `<polyline points="${pts}" fill="none" stroke="${lineColour(id)}" stroke-width="2.5" stroke-linejoin="round" stroke-linecap="round"/><circle cx="${x(tl.length - 1)}" cy="${y(e.v)}" r="4" fill="${lineColour(id)}" stroke="var(--surface)" stroke-width="2"/><text x="${W - R + 8}" y="${e.ly}" class="lb">${esc(sideName(id))}</text>`;
    }
    const legend = ids.map(id => `<span><i style="background:${lineColour(id)}"></i>${esc(sideName(id))}</span>`).join('');
    return `<section class="card graph"><h3>How it unfolded</h3><div class="legend">${legend}</div><svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Running totals through the quiz">${svg}</svg></section>`;
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
    let html = '';
    if (V.phase === 'lobby') { lobby(); bind(); return; }
    if (V.phase === 'game' && V.game) { const g = V.game; html = gameHead(g) + ({ fb, wtb, cs, rh }[g.type])(g) + hostBar(); }
    else if (V.phase === 'countdown') html = countdown();
    else if (V.phase === 'between') html = between();
    else if (V.phase === 'final') html = final();
    const focus = document.activeElement && document.activeElement.id === 'ai';
    app.innerHTML = `<div class="${TV ? 'tvgame' : 'pgame'}">${html}</div><p class="err">${esc(flash)}</p>`;
    if (focus && $('#ai')) { const el = $('#ai'); el.focus(); el.setSelectionRange(el.value.length, el.value.length); }
    else if (!TV && $('#ai') && V.game && (V.game.myTurn || V.game.type === 'wtb')) $('#ai').focus();
    bind();
  }
  function bind() {
    app.querySelectorAll('[data-a]').forEach(el => {
      const a = el.dataset.a;
      if (el.tagName === 'INPUT') { el.onchange = () => toggleGame(el.dataset.g, el.checked); return; }
      const fire = e => {
        e.preventDefault();
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
