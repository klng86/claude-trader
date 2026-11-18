# Rotation check: compare holding the current spread vs exiting and re-deploying into the best
# Dec-31 call spread (width >= 10) sized to hit $120k. Quotes are hard-coded per check-in.
import numpy as np,csv
from math import log,sqrt
from statistics import NormalDist
q={725:(24.21,24.31),726:(23.48,23.82),727:(22.73,23.4),728:(22.69,22.82),729:(21.23,22.01),730:(21.08,21.4),731:(20.4,20.84),732:(19.58,20.09),733:(18.83,19.37),734:(18.62,18.69),735:(17.94,18.11),736:(17.66,17.68),737:(16.55,16.79),738:(16.379,16.46),739:(15.92,16.0),740:(15.4,15.49),741:(14.43,14.51),742:(14.19,14.28),743:(13.56,13.77),744:(13.05,13.16),745:(12.61,12.69),746:(12.13,12.21),747:(11.4,11.85),748:(10.88,11.07),749:(10.49,10.85),750:(10.15,10.4),751:(9.84,9.93),752:(9.4,9.47),753:(8.76,9.11),754:(8.6,8.67),755:(8.0,8.21),756:(7.85,7.91),757:(7.42,7.45),758:(6.9,7.15),759:(6.61,6.79),760:(6.44,6.49),761:(6.05,6.17),762:(5.83,5.88),763:(5.53,5.58),764:(5.2,5.24),765:(4.85,4.86),766:(4.65,4.69),767:(4.33,4.45),768:(4.08,4.13),769:(3.86,3.99),770:(3.58,3.63)}
S=730.6; d=30; T=d/252
cash=60*100*(q[750][0]-q[770][1])+2540   # exit current at natural
print('exit cash %.0f ; fair ceiling %.1f%%'%(cash,100*cash/120000))
c=np.array([float(r['close']) for r in csv.DictReader(open('data/spy_daily.csv'))]); r=c[1:]/c[:-1]-1
rng=np.random.default_rng(1);n=200000;b=10;nb=-(-d//b)
st=rng.integers(0,len(r)-b,(n,nb));idx=(st[...,None]+np.arange(b)).reshape(n,-1)[:,:d]
ST=S*np.prod(1+r[idx],axis=1)
def pln(K,v=0.18): return 1-NormalDist().cdf(log(K/S)/(v*sqrt(T)))
res=[]
for k1 in q:
  for k2 in q:
    if k2<=k1: continue
    w=k2-k1; deb=q[k1][1]-q[k2][0]
    if deb<=0 or w<10: continue
    N=int(cash//(deb*100))
    left=cash-N*deb*100
    if N*w*100+left<120000: continue
    # choose minimal N reaching goal (bold)
    Nmin=int(np.ceil((120000-cash)/(100*(w-deb))))
    if Nmin>N: continue
    res.append((np.mean(ST>=k2),pln(k2),k1,k2,deb,Nmin))
res.sort(reverse=True)
print('hold current: boot %.1f%% ln %.1f%%'%(100*np.mean(ST>=770),100*pln(770)))
for x in res[:8]: print('boot %.1f%% ln18 %.1f%%  %d/%d debit %.2f N=%d'%(100*x[0],100*x[1],*x[2:]))
