# The user's sign-off changes (sheet uploaded 11 Nov) plus my replacements
OFF_ODD = {1:("Zvonimir Boban",None), 3:("Samir Nasri",None), 5:("Joan Capdevila","Espanyol"), 7:("Ledley King",None),
           10:("Anthony Gordon",None), 15:("Emmanuel Adebayor",None), 24:("Kolo Touré",None), 27:("Sergio Ramos",None)}
def xi(id,team,typ,comp,year,cap,rows): return dict(id=id,team=team,type=typ,comp=comp,year=year,cap=cap,rows=rows)
SQUAD = {
 5: xi("che15","Chelsea","club","League Cup final",2015,"John Terry",[
   [["Diego Costa","ST","ESP"]],[["Eden Hazard","LW","BEL"],["Cesc Fàbregas","AM","ESP"],["Willian","RW","BRA"]],
   [["Kurt Zouma","DM","FRA"],["Ramires","DM","BRA"]],
   [["César Azpilicueta","LB","ESP"],["John Terry","CB","ENG"],["Gary Cahill","CB","ENG"],["Branislav Ivanović","RB","SRB"]],[["Petr Čech","GK","CZE"]]]),
 14: xi("lei21","Leicester City","club","FA Cup final",2021,"Kasper Schmeichel",[
   [["Kelechi Iheanacho","ST","NGA"],["Jamie Vardy","ST","ENG"]],[["Ayoze Pérez","AM","ESP"]],
   [["Luke Thomas","LWB","ENG"],["Youri Tielemans","CM","BEL"],["Wilfred Ndidi","CM","NGA"],["Timothy Castagne","RWB","BEL"]],
   [["Çağlar Söyüncü","CB","TUR"],["Jonny Evans","CB","NIR"],["Wesley Fofana","CB","FRA"]],[["Kasper Schmeichel","GK","DEN"]]]),
 24: xi("por08","Portsmouth","club","FA Cup final",2008,"Sol Campbell",[
   [["Kanu","ST","NGA"]],
   [["Niko Kranjčar","LM","CRO"],["Sulley Muntari","CM","GHA"],["Lassana Diarra","CM","FRA"],["John Utaka","RM","NGA"]],
   [["Hermann Hreiðarsson","LB","ISL"],["Sylvain Distin","CB","FRA"],["Sol Campbell","CB","ENG"],["Glen Johnson","RB","ENG"]],[["David James","GK","ENG"]]]),
 27: xi("new25","Newcastle United","club","League Cup final",2025,"Bruno Guimarães",[
   [["Harvey Barnes","LW","ENG"],["Alexander Isak","ST","SWE"],["Jacob Murphy","RW","ENG"]],
   [["Joelinton","CM","BRA"],["Bruno Guimarães","CM","BRA"],["Sandro Tonali","CM","ITA"]],
   [["Tino Livramento","LB","ENG"],["Dan Burn","CB","ENG"],["Fabian Schär","CB","SUI"],["Kieran Trippier","RB","ENG"]],[["Nick Pope","GK","ENG"]]]),
 28: xi("tot25","Tottenham Hotspur","club","Europa League final",2025,"Cristian Romero",[
   [["Richarlison","LW","BRA"],["Dominic Solanke","ST","ENG"],["Brennan Johnson","RW","WAL"]],
   [["Pape Matar Sarr","CM","SEN"],["Yves Bissouma","CM","MLI"],["Rodrigo Bentancur","CM","URU"]],
   [["Destiny Udogie","LB","ITA"],["Micky van de Ven","CB","NED"],["Cristian Romero","CB","ARG"],["Pedro Porro","RB","ESP"]],[["Guglielmo Vicario","GK","ITA"]]]),
}
WTB = {
 10: dict(name="Cesc Fàbregas",aliases=["fabregas","fàbregas","cesc"],position="Midfielder",nationality="Spain",youth="Barcelona",
      clubs=[["Arsenal",212,35],["Barcelona",96,35],["Chelsea",138,15]],caps=110,capGoals=15,apps=499,goals=87,
      honour=["FIFA World Cup winner","2010"],award=["PFA Young Player of the Year","2007–08"],
      blurb="Left Barcelona's academy for Arsenal at 16, captained the club, then went home to the Camp Nou before winning two titles at Chelsea."),
 11: dict(name="Andriy Shevchenko",aliases=["shevchenko","sheva"],position="Forward",nationality="Ukraine",youth="Dynamo Kyiv",
      clubs=[["Dynamo Kyiv",117,60],["AC Milan",208,127],["Chelsea",48,9]],caps=111,capGoals=48,apps=446,goals=219,
      honour=["Champions League winner (AC Milan)","2003"],award=["Ballon d'Or","2004"],
      blurb="Scored the winning penalty in the 2003 Champions League final and later became Ukraine's head coach."),
 13: dict(name="Kevin Keegan",aliases=["keegan","kk"],position="Forward",nationality="England",youth="Scunthorpe United",
      clubs=[["Scunthorpe United",124,18],["Liverpool",230,68],["Hamburg",90,32]],caps=63,capGoals=21,apps=590,goals=203,
      honour=["European Cup winner (Liverpool)","1977"],award=["Ballon d'Or","1978, 1979"],
      blurb="Two-time European Footballer of the Year who later managed Newcastle's 'Entertainers' and England."),
}
LINK25 = {'d':'m','start':{'p':["Ronaldinho","Forward","Brazil",["ronaldinho","dinho"]],'clubs':"Grêmio, Paris Saint-Germain, Barcelona, AC Milan"},'links':[
  {'p':["Frank Rijkaard","Midfielder","Netherlands",["rijkaard"]],'t':'boss','x':"Managed him at Barcelona (2003–08)"},
  {'p':["Marco van Basten","Forward","Netherlands",["van basten","basten"]],'t':'club','x':"AC Milan teammates (1988–93)"},
  {'p':["Ruud Gullit","Midfielder","Netherlands",["gullit"]],'t':'club','x':"AC Milan teammates (1987–93)"},
  {'p':["Gianfranco Zola","Forward","Italy",["zola"]],'t':'boss','x':"Played under him at Chelsea (1996–98)"}]}
