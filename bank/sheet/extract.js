// Pull each game's daily data out of the source HTML into JSON (evaluates only the data literals)
const fs=require('fs');
function grab(file,name){ const s=fs.readFileSync('/home/claude/'+file,'utf8'); const i=s.indexOf('const '+name+' = '); if(i<0) throw file+name;
  let j=i+('const '+name+' = ').length, d=0, q=null;
  for(let k=j;k<s.length;k++){ const c=s[k];
    if(q){ if(c==='\\'){k++;continue;} if(c===q) q=null; continue; }
    if(c==='"'||c==="'"||c==='`'){q=c;continue;}
    if(c==='['||c==='{') d++; else if(c===']'||c==='}'){ d--; if(d===0) return eval('('+s.slice(j,k+1)+')'); } } }
const out={
 fb:{Q:grab('one-touch.html','Q'),DAYS:grab('one-touch.html','DAYS')},
 wtb:grab('whos-that-baller.html','PLAYERS'), mix:grab('scramble-head.html','PUZZLES'), link:grab('pass-and-connect.html','CHAINS'),
 squad:grab('who-playedle.html','XIS'), ss:grab('shirt-swap.html','ANSWERS'), tiki:grab('tiki-taka-toe.html','GRIDS'), off:grab('offside.html','PUZZLES'),
 tf:grab('top-four.html','QUESTIONS'), rh:grab('ranked-highly.html','CHAINS') };
fs.writeFileSync('/home/claude/bank/sheet/current.json',JSON.stringify(out));
console.log(Object.entries(out).map(([k,v])=>k+':'+(Array.isArray(v)?v.length:Object.keys(v).length)).join(' '));
