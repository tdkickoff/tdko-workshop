"""Easy-leaning gap fill, sources fetched 23 Nov 2026 (Wikipedia pages named in SRC; 2025-26 PL title also checked against premierleague.com)."""
SRC={'pl':'https://en.wikipedia.org/wiki/List_of_English_football_champions','gb':'https://en.wikipedia.org/wiki/Premier_League_Golden_Boot',
 'wc':'https://en.wikipedia.org/wiki/List_of_FIFA_World_Cup_finals','eu':'https://en.wikipedia.org/wiki/List_of_UEFA_European_Championship_finals',
 'pl26':'https://en.wikipedia.org/wiki/2026%E2%80%9327_Premier_League','ch26':'https://en.wikipedia.org/wiki/2026%E2%80%9327_EFL_Championship',
 'eust':'https://en.wikipedia.org/wiki/List_of_European_stadiums_by_capacity','nick':'https://en.wikipedia.org/wiki/List_of_football_clubs_in_England',
 'uefa_n':'https://en.wikipedia.org/wiki/List_of_UEFA_national_association_football_teams_by_nickname','caf_n':'https://en.wikipedia.org/wiki/List_of_CAF_national_association_football_teams_by_nickname',
 'con_n':'https://en.wikipedia.org/wiki/List_of_CONMEBOL_national_association_football_teams_by_nickname'}
PL=[l.split('|') for l in """1993|Manchester United|Aston Villa
1994|Manchester United|Blackburn Rovers
1995|Blackburn Rovers|Manchester United
1996|Manchester United|Newcastle United
1997|Manchester United|Newcastle United
1998|Arsenal|Manchester United
1999|Manchester United|Arsenal
2000|Manchester United|Arsenal
2001|Manchester United|Arsenal
2002|Arsenal|Liverpool
2003|Manchester United|Arsenal
2004|Arsenal|Chelsea
2005|Chelsea|Arsenal
2006|Chelsea|Manchester United
2007|Manchester United|Chelsea
2008|Manchester United|Chelsea
2009|Manchester United|Liverpool
2010|Chelsea|Manchester United
2011|Manchester United|Chelsea
2012|Manchester City|Manchester United
2013|Manchester United|Manchester City
2014|Manchester City|Liverpool
2015|Chelsea|Manchester City
2016|Leicester City|Arsenal
2017|Chelsea|Tottenham Hotspur
2018|Manchester City|Manchester United
2019|Manchester City|Liverpool
2020|Liverpool|Manchester City
2021|Manchester City|Manchester United
2022|Manchester City|Liverpool
2023|Manchester City|Arsenal
2024|Manchester City|Arsenal
2025|Liverpool|Arsenal
2026|Arsenal|Manchester City""".split('\n')]
# Golden Boot: single winners only (shared seasons left out)
GB=[l.split('|') for l in """1993|Teddy Sheringham|Tottenham Hotspur|22
1994|Andy Cole|Newcastle United|34
1995|Alan Shearer|Blackburn Rovers|34
1996|Alan Shearer|Blackburn Rovers|31
1997|Alan Shearer|Newcastle United|25
2000|Kevin Phillips|Sunderland|30
2001|Jimmy Floyd Hasselbaink|Chelsea|23
2002|Thierry Henry|Arsenal|24
2003|Ruud van Nistelrooy|Manchester United|25
2004|Thierry Henry|Arsenal|30
2005|Thierry Henry|Arsenal|25
2006|Thierry Henry|Arsenal|27
2007|Didier Drogba|Chelsea|20
2008|Cristiano Ronaldo|Manchester United|31
2009|Nicolas Anelka|Chelsea|19
2010|Didier Drogba|Chelsea|29
2012|Robin van Persie|Arsenal|30
2013|Robin van Persie|Manchester United|26
2014|Luis Suárez|Liverpool|31
2015|Sergio Agüero|Manchester City|26
2016|Harry Kane|Tottenham Hotspur|25
2017|Harry Kane|Tottenham Hotspur|29
2018|Mohamed Salah|Liverpool|32
2020|Jamie Vardy|Leicester City|23
2021|Harry Kane|Tottenham Hotspur|23
2023|Erling Haaland|Manchester City|36
2024|Erling Haaland|Manchester City|27
2025|Mohamed Salah|Liverpool|29
2026|Erling Haaland|Manchester City|27""".split('\n')]
WC=[l.split('|') for l in """1930|Uruguay|Argentina|Uruguay
1934|Italy|Czechoslovakia|Italy
1938|Italy|Hungary|France
1950|Uruguay|Brazil|Brazil
1954|West Germany|Hungary|Switzerland
1958|Brazil|Sweden|Sweden
1962|Brazil|Czechoslovakia|Chile
1966|England|West Germany|England
1970|Brazil|Italy|Mexico
1974|West Germany|Netherlands|West Germany
1978|Argentina|Netherlands|Argentina
1982|Italy|West Germany|Spain
1986|Argentina|West Germany|Mexico
1990|West Germany|Argentina|Italy
1994|Brazil|Italy|USA
1998|France|Brazil|France
2002|Brazil|Germany|South Korea and Japan
2006|Italy|France|Germany
2010|Spain|Netherlands|South Africa
2014|Germany|Argentina|Brazil
2018|France|Croatia|Russia
2022|Argentina|France|Qatar
2026|Spain|Argentina|USA, Canada and Mexico""".split('\n')]
EU=[l.split('|') for l in """1960|Soviet Union|Yugoslavia|France
1964|Spain|Soviet Union|Spain
1968|Italy|Yugoslavia|Italy
1972|West Germany|Soviet Union|Belgium
1976|Czechoslovakia|West Germany|Yugoslavia
1980|West Germany|Belgium|Italy
1984|France|Spain|France
1988|Netherlands|Soviet Union|West Germany
1992|Denmark|Germany|Sweden
1996|Germany|Czech Republic|England
2000|France|Italy|Belgium and the Netherlands
2004|Greece|Portugal|Portugal
2008|Spain|Germany|Austria and Switzerland
2012|Spain|Italy|Poland and Ukraine
2016|Portugal|France|France
2020|Italy|England|
2024|Spain|England|Germany""".split('\n')]
# stadium -> club (grade by fame); src key
STAD=[('Old Trafford','Manchester United','e','pl26'),('Camp Nou','Barcelona','e','eust'),('the Metropolitano Stadium','Atlético Madrid','e','eust'),
 ('the Estádio da Luz','Benfica','e','eust'),('the Stade Vélodrome','Marseille','e','eust'),('the Johan Cruijff ArenA','Ajax','e','eust'),
 ('the Stadio Diego Armando Maradona','Napoli','e','eust'),('the Estádio do Dragão','Porto','e','eust'),('Hillsborough','Sheffield Wednesday','e','eust'),
 ('The Den','Millwall','e','ch26'),('Fratton Park','Portsmouth','e','ch26'),('Loftus Road','Queens Park Rangers','m','ch26'),('The Valley','Charlton Athletic','m','ch26'),
 ('St Andrew\'s','Birmingham City','m','ch26'),('Ashton Gate','Bristol City','m','ch26'),('Deepdale','Preston North End','m','ch26'),('the Racecourse Ground','Wrexham','m','ch26'),
 ('the Hill Dickinson Stadium','Everton','m','pl26'),('San Mamés','Athletic Bilbao','m','eust'),('the Estádio José Alvalade','Sporting CP','m','eust'),
 ('the Estadio Benito Villamarín','Real Betis','m','eust'),('the Ramón Sánchez Pizjuán','Sevilla','m','eust'),('De Kuip','Feyenoord','m','eust'),
 ('the Weserstadion','Werder Bremen','m','eust'),('the Stadio Artemio Franchi','Fiorentina','m','eust'),('the Stade Pierre-Mauroy','Lille','h','eust'),
 ('the BayArena','Bayer Leverkusen','e','eust'),('the Red Bull Arena in Leipzig','RB Leipzig','e','eust')]
CLUBNICK=[("The Citizens",'Manchester City','e'),("The Sky Blues",'Coventry City','e'),("The Swans",'Swansea City','e'),("The Lions",'Millwall','m'),
 ("The Addicks",'Charlton Athletic','m'),("The Robins",'Bristol City','m'),("The Hoops",'Queens Park Rangers','m'),("The Trotters",'Bolton Wanderers','m'),("The Imps",'Lincoln City','m')]
NATNICK=[('The Indomitable Lions','Cameroon','e','caf_n'),('The Elephants','Ivory Coast','e','caf_n'),('The Atlas Lions','Morocco','e','caf_n'),('The Pharaohs','Egypt','e','caf_n'),
 ('The Lions of Teranga','Senegal','m','caf_n'),('The Desert Warriors','Algeria','m','caf_n'),('The Eagles of Carthage','Tunisia','m','caf_n'),('The Leopards','DR Congo','m','caf_n'),
 ('La Celeste','Uruguay','e','con_n'),('Los Cafeteros','Colombia','m','con_n'),('La Albirroja','Paraguay','m','con_n'),('La Vinotinto','Venezuela','m','con_n'),
 ('Canarinho','Brazil','e','con_n'),('The Boys in Green','Republic of Ireland','e','uefa_n'),('The Crescent-Stars','Turkey','m','uefa_n'),('The White Eagles','Serbia','m','uefa_n')]
CITY=[('Lazio','Rome','e'),('Fiorentina','Florence','e'),('Sporting CP','Lisbon','e'),('Real Betis','Seville','e'),('Feyenoord','Rotterdam','e'),('PSV','Eindhoven','e'),
 ('Schalke 04','Gelsenkirchen','m'),('Beşiktaş','Istanbul','e'),('Hertha BSC','Berlin','e'),('Espanyol','Barcelona','e'),('Real Sociedad','San Sebastián','m'),
 ('Celta','Vigo','m'),('Young Boys','Bern','m'),('AEK','Athens','e'),('Olympiacos','Piraeus','h')]
