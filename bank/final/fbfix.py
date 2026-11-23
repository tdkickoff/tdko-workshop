import json,random,time
exec(open('fborder.py').read().split('fails=[]')[0])
import clash as C
C.W=W
GP=[set().union(*[s for k,s in C.day_items(d,skip_fb=True)]) for d in range(28)]
def men(i): return C.mentions(C.fbtext(i))
def orderable(D,tries=300):
    for t in range(tries):
        o=greedy([D['e'],D['m'],D['h']])
        if o: return o
for D in W['fb']['DAYS']: D['o']=orderable(D)
random.seed(3); t0=time.time()
for d in [x for x in range(28) if not W['fb']['DAYS'][x]['o']]:
    D=W['fb']['DAYS'][d]
    for attempt in range(6):
        if D['o']: break
        cnt=Counter(cat(Q[i][0]) for i in D['e']); cnt['other']=0; ans=Counter(Q[i][1][0] for i in D['e'])
        i=max(D['e'],key=lambda i:cnt[cat(Q[i][0])]+3*(ans[Q[i][1][0]]-1))
        mi=men(i); done=False
        for d2 in random.sample(range(28),28):
            if d2==d or (mi & GP[d2]): continue
            D2=W['fb']['DAYS'][d2]
            for j in random.sample(D2['e'],len(D2['e'])):
                if cat(Q[j][0])!='other' or Q[j][1][0] in ans or (men(j)&GP[d]): continue
                D['e'][D['e'].index(i)]=j; D2['e'][D2['e'].index(j)]=i
                o2=orderable(D2)
                if o2: D2['o']=o2; D['o']=orderable(D); print('moved',Q[i][0],'->',d2+1,'| in',Q[j][0]); done=True; break
                D['e'][D['e'].index(j)]=i; D2['e'][D2['e'].index(i)]=j
            if done: break
print('unordered',[x+1 for x in range(28) if not W['fb']['DAYS'][x]['o']], round(time.time()-t0))
json.dump(W,open('final28.json','w'),ensure_ascii=False)
