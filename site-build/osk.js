/* On-page keyboard for the typing games (Who's That Baller, Squad Goals, Link Up Play, In The Mixer, Tiki-Taka-Toe).
   Touch phones: the phone's own keyboard never opens; this one is docked at the bottom and types into the answer box (#gin),
   and Enter sends the answer form. The game is squeezed to fit above it, so there's no scrolling while you play.
   Mouse and keyboard: the answer box keeps the cursor after every answer, so you can keep typing. */
(function(){
  var TOUCH = matchMedia('(pointer: coarse)').matches, kb = null, raf = 0, seen = null;
  var box = function(){ return document.getElementById('gin'); };
  function css(){
    var s = document.createElement('style');
    s.textContent =
      '#osk{position:fixed;left:0;right:0;bottom:0;z-index:50;background:var(--bg);border-top:1px solid var(--line);padding:6px 4px calc(6px + env(safe-area-inset-bottom));display:none;flex-direction:column;gap:6px;user-select:none;-webkit-user-select:none;touch-action:manipulation}' +
      'body.osk-on #osk{display:flex}' +
      '#osk .r{display:flex;gap:5px;justify-content:center}' +
      '#osk button{all:unset;box-sizing:border-box;flex:1 1 0;max-width:44px;height:40px;display:grid;place-items:center;background:var(--surface);border:1px solid var(--line);color:var(--ink);font-family:var(--f-display,inherit);font-weight:800;font-size:18px;border-radius:3px;cursor:pointer}' +
      '#osk button:active,#osk button.hit{background:var(--ink);color:var(--bg)}' +
      '#osk .w{max-width:64px;flex:1.5 1 0;font-family:var(--f-mono,monospace);font-size:11px;font-weight:600;letter-spacing:.04em;text-transform:uppercase}' +
      '#osk .sp{max-width:none;flex:4 1 0}#osk .go{max-width:none;flex:2 1 0;background:var(--accent);color:var(--accent-ink);border-color:var(--accent)}' +
      /* make room: no page chrome while a game is on, tighter spacing, the answer box stays in view */
      'body.osk-on{padding-bottom:var(--oskh,210px)!important}' +
      'body.osk-on #app{zoom:var(--oskz,1)}' +
      /* per game: drop empty space so less shrinking is needed */
      'body.osk-on .clue.locked{display:none}body.osk-on .pitch{gap:4px;padding-top:20px;padding-bottom:6px}' +
      'body.osk-on #gin{caret-color:transparent;border-color:var(--ink)}';
    document.head.appendChild(s);
  }
  function build(){
    kb = document.createElement('div'); kb.id = 'osk'; kb.setAttribute('aria-hidden', 'true');
    var rows = ['qwertyuiop', 'asdfghjkl', "'zxcvbnm<", '- >'];
    kb.innerHTML = rows.map(function(r){ return '<div class="r">' + r.split('').map(function(c){
      if (c === '<') return '<button class="w" data-k="back">Del</button>';
      if (c === ' ') return '<button class="sp" data-k=" ">Space</button>';
      if (c === '>') return '<button class="w go" data-k="enter">Enter</button>';
      return '<button data-k="' + c + '">' + (c === "'" ? '’' : c.toUpperCase()) + '</button>'; }).join('') + '</div>'; }).join('');
    // keys act on touch-down so fast typing never loses a letter to a screen refresh
    kb.addEventListener('pointerdown', function(e){ var b = e.target.closest('button'); if (!b) return; e.preventDefault();
      b.classList.add('hit'); setTimeout(function(){ b.classList.remove('hit'); }, 90); press(b.dataset.k); });
    document.body.appendChild(kb);
  }
  function press(k){
    var i = box(); if (!i || i.disabled) return;
    if (k === 'enter') { var f = i.form; if (f) { if (f.requestSubmit) f.requestSubmit(); else f.dispatchEvent(new Event('submit', {cancelable: true})); } return; }
    var v = i.value;
    if (k === 'back') v = v.slice(0, -1);
    else if (k === ' ') { if (v && !/[ \-]$/.test(v)) v += ' '; }
    else { var start = !v || /[ \-]$/.test(v); v += start ? k.toUpperCase() : k; }
    i.value = v; i.dispatchEvent(new Event('input', {bubbles: true}));
  }
  function sync(){
    raf = 0; var i = box();
    if (TOUCH) {
      var on = !!i && !!kb;
      document.body.classList.toggle('osk-on', on);
      if (i && !i.readOnly) { i.readOnly = true; i.setAttribute('inputmode', 'none'); }
      if (on) { var B = document.body.style, h = kb.offsetHeight + 8, app = document.getElementById('app');
        B.setProperty('--oskh', h + 'px');
        // the header stays on the page; the game is shrunk (evenly) to fit the screen above the keyboard,
        // and each new question scrolls it into place so the game and keyboard are all in view
        if (app) { B.setProperty('--oskz', 1); var vh = window.visualViewport ? visualViewport.height : innerHeight, avail = vh - h - 10, need = app.scrollHeight;
          var z = need > avail ? Math.max(0.55, avail / need) : 1; B.setProperty('--oskz', z.toFixed(3));
          if (seen !== i) { seen = i; window.scrollTo(0, Math.max(0, app.getBoundingClientRect().top + window.scrollY - 6)); } } }
      else { document.body.style.removeProperty('--oskz'); seen = null; }
    } else if (i && !i.disabled) {
      // after an answer the game redraws and the box loses the cursor: put it straight back
      var a = document.activeElement;
      if (!a || a === document.body || a === document.documentElement) i.focus({preventScroll: true});
    }
  }
  function start(){
    if (TOUCH) { css(); build(); }
    new MutationObserver(function(){ if (!raf) raf = requestAnimationFrame(sync); }).observe(document.body, {childList: true, subtree: true});
    sync();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start); else start();
})();
