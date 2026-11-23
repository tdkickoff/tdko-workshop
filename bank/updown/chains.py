# Up and Down Season chains: start player + five calls. Values frozen (retired players / finished seasons).
# Gap rule (build-up): calls 1-3 differ by 20-30% from the previous player, calls 4-5 by 5-10%. Never a tie.
C = [
 dict(id='eng-goals', theme="England goals", unit="goals", chain=[["Wayne Rooney",53],["Michael Owen",40],["Frank Lampard",29],["Peter Crouch",22],["Geoff Hurst",24],["Bryan Robson",26]]),
 dict(id='pl-goals', theme="Premier League goals", unit="goals", chain=[["Thierry Henry",175],["Robbie Keane",126],["Matt Le Tissier",100],["Dwight Yorke",123],["Ian Wright",113],["Darren Bent",106]]),
 dict(id='pl-apps', theme="Premier League appearances", unit="apps", chain=[["David James",572],["Alan Shearer",434],["Gary Speed",535],["Gareth Southgate",426],["Shay Given",451],["Michael Carrick",481]]),
 dict(id='eng-caps', theme="England caps", unit="caps", chain=[["David Beckham",115],["Michael Owen",89],["Paul Scholes",66],["Gary Lineker",80],["David Seaman",75],["Rio Ferdinand",81]]),
 dict(id='arsenal-goals', theme="Goals for Arsenal (all competitions)", unit="goals", chain=[["Thierry Henry",228],["Cliff Bastin",178],["Robin van Persie",132],["Olivier Giroud",105],["Alan Smith",115],["Theo Walcott",108]]),
 dict(id='season-goals', theme="Premier League goals in one season", unit="goals", chain=[["Erling Haaland (2022–23)",36],["Wayne Rooney (2011–12)",27],["Nicolas Anelka (2008–09)",19],["Fernando Torres (2007–08)",24],["Sergio Agüero (2014–15)",26],["Robbie Fowler (1995–96)",28]]),
 dict(id='mufc-apps', theme="Appearances for Manchester United", unit="apps", chain=[["Paul Scholes",718],["Wayne Rooney",559],["Peter Schmeichel",398],["Roy Keane",480],["Rio Ferdinand",455],["Steve Bruce",414]]),
 dict(id='chelsea-goals', theme="Goals for Chelsea (all competitions)", unit="goals", chain=[["Frank Lampard",211],["Peter Osgood",150],["Eden Hazard",110],["Gianfranco Zola",80],["Jimmy Floyd Hasselbaink",87],["Eiður Guðjohnsen",78]]),
 dict(id='wales-caps', theme="Wales caps", unit="caps", chain=[["Gareth Bale",111],["Craig Bellamy",78],["Kevin Ratcliffe",59],["Ian Rush",73],["Ivor Allchurch",68],["Ryan Giggs",64]]),
 dict(id='ireland-caps', theme="Republic of Ireland caps", unit="caps", chain=[["Robbie Keane",146],["Kevin Kilbane",110],["Tony Cascarino",88],["Roy Keane",67],["Ray Houghton",73],["John Aldridge",69]]),
 dict(id='spurs-goals', theme="Goals for Tottenham (all competitions)", unit="goals", chain=[["Jimmy Greaves",266],["Bobby Smith",208],["Cliff Jones",159],["Teddy Sheringham",124],["Alan Gilzean",133],["Jermain Defoe",143]]),
 dict(id='lfc-apps', theme="Appearances for Liverpool", unit="apps", chain=[["Ian Callaghan",857],["Bruce Grobbelaar",628],["Phil Thompson",477],["Alan Hansen",620],["Emlyn Hughes",665],["Steven Gerrard",710]]),
 dict(id='eng-caps-2', theme="England caps", unit="caps", chain=[["Steven Gerrard",114],["Gary Neville",85],["Alan Shearer",63],["John Barnes",79],["Kenny Sansom",86],["John Terry",78]]),
 dict(id='ned-caps', theme="Netherlands caps", unit="caps", chain=[["Wesley Sneijder",134],["Arjen Robben",96],["Ruud van Nistelrooy",70],["Clarence Seedorf",87],["Patrick Kluivert",79],["Marc Overmars",86]]),
]
TEST = dict(id='sco-caps', theme="Scotland caps", unit="caps", chain=[["Kenny Dalglish",102],["Darren Fletcher",80],["Ally McCoist",61],["Alex McLeish",77],["Tom Boyd",72],["Christian Dailly",67]])
