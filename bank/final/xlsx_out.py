import json,sys,datetime,openpyxl,copy
from openpyxl.styles import PatternFill,Font
sys.path.insert(0,'/home/claude/bank/sheet')
src=open('/home/claude/bank/sheet/rows.py').read().split('# No. 1–14')[0]
src=src.replace("import week1\nfrom fb_week1 import FB\n","").replace("plan,_=pickle.load(open('/home/claude/bank/plan_w1.pkl','rb'))\ntiki_w1=json.load(open('/home/claude/bank/tiki_w1.json'))\n","")
exec(src)
W=json.load(open('final28.json'))
Q=W['fb']['Q']
for d in range(28):
    n=d+1
    fb_rows(n,[Q[i] for i in W['fb']['DAYS'][d]['o']])
    wtb_row(n,W['wtb'][d]); mix_row(n,W['mix'][d]); link_row(n,W['link'][d]); squad_row(n,W['squad'][d]); ss_row(n,W['ss'][d]); tiki_row(n,W['tiki'][d])
    off_row(n,W['off'][d]); tf_row(n,W['tf'][d])
    if n>=8: rh_row(n,W['rh'][d])
ORDER=['Fast Break',"Who's That Baller",'In The Mixer','Link Up Play','Squad Goals','Shirt Swap','Tiki-Taka-Toe','Offside','Top Four','Ranked Highly']
new=rows
# the user's file
wb=openpyxl.load_workbook('/home/claude/review/signoff.xlsx'); ws=wb.worksheets[0]
old=[list(r) for r in ws.iter_rows(min_row=2,values_only=True)]
def key(r):
    if r[2]=='Fast Break': return (int(r[0]),'FB',r[3].split('. ',1)[1])
    return (int(r[0]),r[2])
OLD={key(r):r for r in old}
WIKI={10:"Wikipedia: Barcelona goals 28 (not 35); career 518 apps/81 goals",11:"Wikipedia: career 497/235",13:"Wikipedia: career 592/204",
 15:"Wikipedia: first three clubs are Haarlem, Feyenoord, PSV; career 470/174",16:"Wikipedia: first three clubs are Gladsaxe-Hero, Hvidovre, Brøndby; career 648/9",
 17:"Wikipedia: first three clubs are Nuorese, Torres, Napoli; youth club Corrasi Oliena",19:"Wikipedia: Liverpool first spell 182/109; career 601/254",
 20:"Wikipedia: Atlético 214/82; career 578/200",21:"Wikipedia: first three clubs are Cannes, AC Milan, Arsenal; youth club Tours",22:"Wikipedia: Sporting 129/16; career 570/93",
 23:"Wikipedia: Sparta 97/23; career 501/110",26:"Wikipedia: career 427/73",27:"Wikipedia: youth club Nooit Gedacht; career 449/249"}
out=openpyxl.Workbook(); o=out.active; o.title='Puzzles'
o.append(['No.','Date','Game','Question','Answer','Supporting details','OK?','Notes','What changed'])
Y=PatternFill('solid',fgColor='FFF2A8'); G=PatternFill('solid',fgColor='E5F4E4')
nchg=0
for r in sorted(new,key=lambda r:(r[0],ORDER.index(r[2]),0 if r[2]!='Fast Break' else int(r[3].split('.')[0][1:]))):
    k=key(r); ov=OLD.get(k); what=''
    if r[2]=='Fast Break':
        if not ov: what='Moved here from another day (to space out similar questions)'
        elif ov[3]!=r[3]: what='Reordered: now '+r[3].split('.')[0]
    else:
        if not ov: what='New row'
        elif [ov[3],ov[4],ov[5]]!=[r[3],r[4],r[5]]: what='Changed as you asked' if (ov[6]=='Change') else 'Updated'
    if what and r[2]=='Top Four':
        items_new=[x.strip() for x in r[4].split('>')]; items_old=[x.strip() for x in ov[4].split('>')] if ov else []
        if items_old and items_new==items_old[::-1]: what=('Changed as you asked: ' if ov[6]=='Change' else '')+'now most at the top'
        elif items_old==items_new: what=''
    if what and r[2]=='Ranked Highly': what='Moved from another day in this week (it shared a player with another game that day)'
    if what and r[2]=='Tiki-Taka-Toe': what='Example answer changed: Fàbregas only played in Serie B for Como'
    if r[2]=='Squad Goals' and r[0]==27: what='Changed as you asked. Wikipedia: Anthony Gordon was suspended for the final; Harvey Barnes started'
    if r[2]=='Squad Goals' and r[0]==24: what='Changed as you asked. Checked against Wikipedia line-up'
    if r[2]=='Squad Goals' and r[0] in (5,14,28): what='Changed as you asked. Checked against match line-up'
    if r[2]=='Offside' and r[0]==10: what='Changed as you asked. Note: Gordon was in Liverpool\'s academy as a boy and is now at Barcelona, but never played for Liverpool\'s first team'
    if r[2]=="Who's That Baller" and r[0] in WIKI: what=('Replaced as you asked. ' if ov and ov[6]=='Change' else '')+WIKI[r[0]]
    status=ov[6] if ov else None; notes=ov[7] if ov else None
    if what and status=='Change': status='Re-check'
    o.append([r[0],datetime.date.fromisoformat((datetime.date(2026,11,16)+datetime.timedelta(days=r[0]-1)).isoformat()),r[2],r[3],r[4],r[5],status,notes,what])
    if what and not what.startswith('Reordered'):
        nchg+=1
        for c in o[o.max_row]: c.fill=Y
for c in o[1]: c.font=Font(bold=True)
for col,w in zip('ABCDEFGHI',[5,11,16,50,40,60,10,40,45]): o.column_dimensions[col].width=w
o.freeze_panes='A2'
for row in o.iter_rows(min_row=2):
    row[1].number_format='ddd d mmm'
out.save('/home/claude/review/TDKO_Puzzle_Sign-off_updated.xlsx')
print('rows',o.max_row-1,'highlighted',nchg)
