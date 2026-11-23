# Source-checked club cup runs (winner's score first). Crests are our own shields in kit colours, never club badges.
T = {  # name -> (code, main colour, second colour)
 'Wigan Athletic':('WIG','#1D59AF','#FFFFFF'),'AFC Bournemouth':('BOU','#DA291C','#000000'),'Macclesfield Town':('MAC','#0050A0','#FFFFFF'),
 'Huddersfield Town':('HUD','#0E63AD','#FFFFFF'),'Everton':('EVE','#003399','#FFFFFF'),'Millwall':('MIL','#001D5E','#FFFFFF'),
 'Manchester City':('MCI','#6CABDD','#FFFFFF'),'Portsmouth':('POR','#001489','#FFFFFF'),'Ipswich Town':('IPS','#0033A0','#FFFFFF'),
 'Plymouth Argyle':('PLY','#00573F','#FFFFFF'),'Preston North End':('PNE','#FFFFFF','#0A2240'),'Manchester United':('MUN','#DA291C','#FFFFFF'),
 'West Bromwich Albion':('WBA','#122F67','#FFFFFF'),'Cardiff City':('CAR','#0070B5','#FFFFFF'),'Newport County':('NPT','#F7A51C','#000000'),
 'Nottingham Forest':('NFO','#DD0000','#FFFFFF'),'Liverpool':('LIV','#C8102E','#FFFFFF'),'Coventry City':('COV','#59CBE8','#FFFFFF'),
 'Shrewsbury Town':('SHR','#0047AB','#F4B400'),'Norwich City':('NOR','#FFF200','#00A650'),'Chelsea':('CHE','#034694','#FFFFFF'),
 'West Ham United':('WHU','#7A263A','#1BB1E7'),'Viborg':('VIB','#00843D','#FFFFFF'),'FCSB':('FCS','#E30613','#0033A0'),'Silkeborg':('SIL','#E30613','#FFFFFF'),
 'Anderlecht':('AND','#4C2C92','#FFFFFF'),'AEK Larnaca':('AEK','#FFD100','#00704A'),'Gent':('GNT','#003F87','#FFFFFF'),'AZ':('AZ','#E30613','#FFFFFF'),
 'Fiorentina':('FIO','#5B2B82','#FFFFFF'),'Feyenoord':('FEY','#E30613','#FFFFFF'),'Zorya Luhansk':('ZOR','#111111','#FFFFFF'),
 'Fenerbahçe':('FEN','#FFED00','#002D72'),'Saint-Étienne':('STE','#00A650','#FFFFFF'),'Rostov':('ROS','#FFD200','#003D7D'),
 'Celta Vigo':('CEL','#8AC3EE','#FFFFFF'),'Ajax':('AJX','#D2122E','#FFFFFF'),
 'Crystal Palace':('CRY','#1B458F','#C4122E'),'Stockport County':('STO','#0E4FA0','#FFFFFF'),'Doncaster Rovers':('DON','#E21D24','#FFFFFF'),
 'Fulham':('FUL','#FFFFFF','#000000'),'Aston Villa':('AVL','#670E36','#95BFE5'),
}
def team(n): c,a,b=T[n]; return {'n':n,'code':c,'c':[a,b]}
def run(id, win, comp, year, final, src, lvl, rounds, a=()):
    return {'id':id,'lvl':lvl,'answer':{**team(win),'a':list(a)},'comp':comp,'year':year,'final':final,'src':src,
            'rounds':[{'r':r,'m':[{'t':team(o),**({'s':s} if s else {})} for o,s in ms]} for r,ms in rounds]}
R3='Third round'; R4='Fourth round'; R5='Fifth round'; QF='Quarter-final'; SF='Semi-final'; G='Group stage'
CLUB = {
'mun-facup-2024': run('mun-facup-2024','Manchester United','FA Cup','2024','2–1','Wikipedia: 2024 FA Cup final','E',
  [(R3,[('Wigan Athletic','2–0')]),(R4,[('Newport County','4–2')]),(R5,[('Nottingham Forest','1–0')]),(QF,[('Liverpool','4–3 aet')]),(SF,[('Coventry City','3–3 · 4–2 pens')]),('Final',[('Manchester City',None)])]),
'liv-facup-2022': run('liv-facup-2022','Liverpool','FA Cup','2022','0–0 (6–5 pens)','Wikipedia: 2022 FA Cup final','M',
  [(R3,[('Shrewsbury Town','4–1')]),(R4,[('Cardiff City','3–1')]),(R5,[('Norwich City','2–1')]),(QF,[('Nottingham Forest','1–0')]),(SF,[('Manchester City','3–2')]),('Final',[('Chelsea',None)])]),
'wig-facup-2013': run('wig-facup-2013','Wigan Athletic','FA Cup','2013','1–0','Wikipedia: 2013 FA Cup final','M',
  [(R3,[('AFC Bournemouth','1–1 · replay 1–0')]),(R4,[('Macclesfield Town','1–0')]),(R5,[('Huddersfield Town','4–1')]),(QF,[('Everton','3–0')]),(SF,[('Millwall','2–0')]),('Final',[('Manchester City',None)])]),
'por-facup-2008': run('por-facup-2008','Portsmouth','FA Cup','2008','1–0','Wikipedia: 2008 FA Cup final','H',
  [(R3,[('Ipswich Town','1–0')]),(R4,[('Plymouth Argyle','2–1')]),(R5,[('Preston North End','1–0')]),(QF,[('Manchester United','1–0')]),(SF,[('West Bromwich Albion','1–0')]),('Final',[('Cardiff City',None)])],
  a=('pompey',)),
'cry-facup-2025': run('cry-facup-2025','Crystal Palace','FA Cup','2025','1–0','Wikipedia: 2025 FA Cup final','E',
  [(R3,[('Stockport County','1–0')]),(R4,[('Doncaster Rovers','2–0')]),(R5,[('Millwall','3–1')]),(QF,[('Fulham','3–0')]),(SF,[('Aston Villa','3–0')]),('Final',[('Manchester City',None)])]),
'whu-uecl-2023': run('whu-uecl-2023','West Ham United','Conference League','2023','2–1','Wikipedia: 2023 UEFA Europa Conference League final; FourFourTwo (play-off)','M',
  [('Play-off',[('Viborg','agg 6–1')]),(G,[('FCSB','3–1, 3–0'),('Silkeborg','3–2, 1–0'),('Anderlecht','1–0, 2–1')]),('Round of 16',[('AEK Larnaca','agg 6–0')]),(QF,[('Gent','agg 5–2')]),(SF,[('AZ','agg 3–1')]),('Final',[('Fiorentina',None)])]),
'mun-uel-2017': run('mun-uel-2017','Manchester United','Europa League','2017','2–0','Wikipedia: 2017 UEFA Europa League final','M',
  [(G,[('Feyenoord','0–1, 4–0'),('Zorya Luhansk','1–0, 2–0'),('Fenerbahçe','4–1, 1–2')]),('Round of 32',[('Saint-Étienne','agg 4–0')]),('Round of 16',[('Rostov','agg 2–1')]),(QF,[('Anderlecht','agg 3–2 aet')]),(SF,[('Celta Vigo','agg 2–1')]),('Final',[('Ajax',None)])]),
}
