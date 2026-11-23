import json,random
exec(open('fborder.py').read().split('fails=[]')[0])
import clash as C
C.W=W
def orderable(D):
    for t in range(3000):
        o=greedy([D['e'],D['m'],D['h']])
        if o: return o
    return None
random.seed(7)
moved=[]
for rnd in range(40):
    fails=[d for d,D in enumerate(W['fb']['DAYS']) if not D.get('o') or not orderable(D)]
    if not fails: break
    d=fails[0]; D=W['fb']['DAYS'][d]; done=False
    for t in 'em':
        cnt=Counter(cat(Q[i][0]) for i in D[t]); cnt['other']=0
        top,c=cnt.most_common(1)[0]
        ans=Counter(Q[i][1][0] for i in D[t])
        for i in sorted(D[t],key=lambda i:-(cnt[cat(Q[i][0])]+3*ans[Q[i][1][0]])):
            for d2 in random.sample(range(28),28):
                if d2==d: continue
                D2=W['fb']['DAYS'][d2]
                for j in D2[t]:
                    if cat(Q[j][0])==cat(Q[i][0]) or Q[j][1][0] in ans: continue
                    D[t][D[t].index(i)]=j; D2[t][D2[t].index(j)]=i
                    if not C.clashes(d) and not C.clashes(d2):
                        o1=orderable(D); o2=orderable(D2)
                        if o1 and o2: D['o']=o1; D2['o']=o2; moved.append((Q[i][0],d+1,d2+1)); done=True; break
                    D[t][D[t].index(j)]=i; D2[t][D2[t].index(i)]=j
                if done: break
            if done: break
        if done: break
    if not done: print('stuck',d+1); break
print('moved',moved)
for D in W['fb']['DAYS']:
    D['o']=orderable(D)
print('unordered',[d+1 for d,D in enumerate(W['fb']['DAYS']) if not D['o']])
json.dump(W,open('final28.json','w'),ensure_ascii=False)
