/* Small hand-drawn flags for Squad Goals (club XIs show each player's nationality). viewBox 30x20, simplified for 14px display.
   Codes are FIFA codes as used in the data. Missing code -> no flag, the code alone shows. */
const FLAG_SVG = (()=>{
  const h3=(a,b,c)=>`<rect width="30" height="20" fill="${b}"/><rect width="30" height="6.67" fill="${a}"/><rect y="13.33" width="30" height="6.67" fill="${c}"/>`;
  const v3=(a,b,c)=>`<rect width="30" height="20" fill="${b}"/><rect width="10" height="20" fill="${a}"/><rect x="20" width="10" height="20" fill="${c}"/>`;
  const nordic=(bg,c,inner)=>`<rect width="30" height="20" fill="${bg}"/><rect x="8" width="6" height="20" fill="${c}"/><rect y="7" width="30" height="6" fill="${c}"/>`+(inner?`<rect x="9.5" width="3" height="20" fill="${inner}"/><rect y="8.5" width="30" height="3" fill="${inner}"/>`:'');
  const star=(cx,cy,r,f)=>{ let p=''; for(let i=0;i<10;i++){ const a=-Math.PI/2+i*Math.PI/5, rr=i%2?r*0.42:r; p+=`${(cx+rr*Math.cos(a)).toFixed(2)},${(cy+rr*Math.sin(a)).toFixed(2)} `; } return `<polygon points="${p}" fill="${f}"/>`; };
  const ujack=`<rect width="15" height="10" fill="#012169"/><path d="M0 0L15 10M15 0L0 10" stroke="#fff" stroke-width="2"/><path d="M0 0L15 10M15 0L0 10" stroke="#C8102E" stroke-width="0.8"/><path d="M7.5 0V10M0 5H15" stroke="#fff" stroke-width="3"/><path d="M7.5 0V10M0 5H15" stroke="#C8102E" stroke-width="1.6"/>`;
  return {
    ARG:h3('#74ACDF','#fff','#74ACDF')+'<circle cx="15" cy="10" r="2.2" fill="#F6B40E"/>',
    AUS:'<rect width="30" height="20" fill="#012169"/>'+ujack+star(7.5,15,2.4,'#fff')+star(23,5,1.3,'#fff')+star(20,10,1.3,'#fff')+star(26,9,1.3,'#fff')+star(23,16,1.3,'#fff'),
    AUT:h3('#C8102E','#fff','#C8102E'),
    BEL:v3('#000','#FDDA24','#EF3340'),
    BLR:'<rect width="30" height="20" fill="#4AA657"/><rect width="30" height="13.3" fill="#C8313E"/><rect width="4" height="20" fill="#fff"/><path d="M2 0v20" stroke="#C8313E" stroke-width="1.6" stroke-dasharray="1.6 1.2"/>',
    BRA:'<rect width="30" height="20" fill="#009C3B"/><polygon points="15,2.5 27.5,10 15,17.5 2.5,10" fill="#FFDF00"/><circle cx="15" cy="10" r="4.2" fill="#002776"/>',
    CIV:v3('#F77F00','#fff','#009E60'),
    CMR:v3('#007A5E','#CE1126','#FCD116')+star(15,10,2.6,'#FCD116'),
    CRO:h3('#FF0000','#fff','#171796')+'<rect x="12" y="5" width="6" height="7" fill="#fff" stroke="#FF0000" stroke-width=".6"/><path d="M12 5h2v2h-2zM16 5h2v2h-2zM14 7h2v2h-2zM12 9h2v2h-2zM16 9h2v2h-2z" fill="#FF0000"/>',
    CZE:'<rect width="30" height="20" fill="#D7141A"/><rect width="30" height="10" fill="#fff"/><polygon points="0,0 15,10 0,20" fill="#11457E"/>',
    DEN:nordic('#C8102E','#fff'),
    EGY:h3('#CE1126','#fff','#000')+'<circle cx="15" cy="10" r="1.8" fill="#C09300"/>',
    ENG:'<rect width="30" height="20" fill="#fff"/><rect x="12.5" width="5" height="20" fill="#CE1124"/><rect y="7.5" width="30" height="5" fill="#CE1124"/>',
    ESP:'<rect width="30" height="20" fill="#AA151B"/><rect y="5" width="30" height="10" fill="#F1BF00"/><rect x="7" y="7.5" width="3.5" height="5" fill="#AA151B" opacity=".75"/>',
    FIN:nordic('#fff','#002F6C'),
    FRA:v3('#002654','#fff','#CE1126'),
    GER:h3('#000','#DD0000','#FFCE00'),
    GHA:h3('#CE1126','#FCD116','#006B3F')+star(15,10,3,'#000'),
    IRL:v3('#169B62','#fff','#FF883E'),
    ISL:nordic('#02529C','#fff','#DC1E35'),
    ITA:v3('#009246','#fff','#CE2B37'),
    MLI:v3('#14B53A','#FCD116','#CE1126'),
    NED:h3('#AE1C28','#fff','#21468B'),
    NGA:v3('#008751','#fff','#008751'),
    NOR:nordic('#BA0C2F','#fff','#00205B'),
    POL:'<rect width="30" height="20" fill="#DC143C"/><rect width="30" height="10" fill="#fff"/>',
    POR:'<rect width="30" height="20" fill="#FF0000"/><rect width="12" height="20" fill="#006600"/><circle cx="12" cy="10" r="3.6" fill="#FFCC00"/><circle cx="12" cy="10" r="2.2" fill="#fff" stroke="#FF0000" stroke-width=".8"/>',
    SCO:'<rect width="30" height="20" fill="#005EB8"/><path d="M0 0L30 20M30 0L0 20" stroke="#fff" stroke-width="3.6"/>',
    SEN:v3('#00853F','#FDEF42','#E31B23')+star(15,10,2.8,'#00853F'),
    SRB:h3('#C6363C','#0C4076','#fff')+'<rect x="7" y="5" width="4" height="8" rx="1" fill="#fff" stroke="#C6363C" stroke-width=".6"/>',
    SUI:'<rect width="30" height="20" fill="#DA291C"/><rect x="13" y="4" width="4" height="12" fill="#fff"/><rect x="9" y="8" width="12" height="4" fill="#fff"/>',
    SWE:nordic('#006AA7','#FECC00'),
    TRI:'<rect width="30" height="20" fill="#DA1A35"/><path d="M2 0L28 20" stroke="#fff" stroke-width="8"/><path d="M2 0L28 20" stroke="#000" stroke-width="5"/>',
    TUR:'<rect width="30" height="20" fill="#E30A17"/><circle cx="11" cy="10" r="5" fill="#fff"/><circle cx="12.3" cy="10" r="4" fill="#E30A17"/>'+star(17.6,10,2.2,'#fff'),
    URU:'<rect width="30" height="20" fill="#fff"/><path d="M0 3.3h30M0 7.8h30M0 12.2h30M0 16.7h30" stroke="#0038A8" stroke-width="2.2"/><rect width="12" height="10" fill="#fff"/><circle cx="6" cy="5" r="2.6" fill="#FCD116"/>',
    WAL:'<rect width="30" height="20" fill="#00AB39"/><rect width="30" height="10" fill="#fff"/><path d="M8 13c2-4 5-6 9-5 2-2 4-2 5 0-1 0-2 1-2 2 2 1 2 3 0 4-1-1-2-1-3 0-3 1-6 1-9-1z" fill="#C8102E"/>',
  };
})();
const flagHTML = code => FLAG_SVG[code] ? `<svg class="flg" viewBox="0 0 30 20" aria-hidden="true">${FLAG_SVG[code]}</svg>` : '';
