const fs=require('fs');
const s=fs.readFileSync('/home/claude/tiki-taka-toe.html','utf8');
function grab(name){ const i=s.indexOf('const '+name+' = '); let j=i+('const '+name+' = ').length,d=0,q=null;
  for(let k=j;k<s.length;k++){const c=s[k]; if(q){if(c==='\\'){k++;continue} if(c===q)q=null; continue}
    if(c=='"'||c=="'"||c=='`'){q=c;continue} if(c=='['||c=='{')d++; else if(c==']'||c=='}'){d--; if(d===0) return eval('('+s.slice(j,k+1)+')');}}}
const PLAYERS=grab('PLAYERS'), LEAGUES=grab('LEAGUES'); const BY={}; PLAYERS.forEach(p=>BY[p.name]=p);
function test(p,[k,v]){ if(k==='club')return p.clubs.includes(v); if(k==='nat')return p.nat===v; if(k==='hon')return p[v]; if(k==='league')return p.clubs.some(x=>LEAGUES[v].includes(x)); }
const W=JSON.parse(fs.readFileSync('final28.json','utf8')); const fix=[];
W.tiki.forEach((g,d)=>{ for(let r=0;r<3;r++)for(let c=0;c<3;c++){ const n=g.ex[r*3+c], p=BY[n];
  const ok=p && test(p,g.r[r])===true && test(p,g.c[c])===true;
  if(!ok){ const alts=PLAYERS.filter(q=>test(q,g.r[r])===true&&test(q,g.c[c])===true&&!g.ex.includes(q.name)).map(q=>q.name);
    fix.push({day:d+1,cell:r*3+c,was:n,row:g.rl[r],col:g.cl[c],alts}); } } });
console.log(JSON.stringify(fix,null,0));
