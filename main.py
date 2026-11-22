import json,os,urllib.request as u
U=os.environ["MAKEFUN_ENV_URL"]
post=lambda p,b:json.load(u.urlopen(U+p,json.dumps(b).encode()))
V=(0,100,320,330,500,900,0)
T=('<<<<FFFF>>@B==>A<<<@=;:<=>>8<<<<','246648<<6<>?6=?@6<?@6=>?48<=2466')
KN=((1,2),(2,1),(2,-1),(1,-2),(-1,-2),(-2,-1),(-2,1),(-1,2))
KI=((1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1))
DS=((),(),KN,KI[1::2],KI[::2],KI,KI)
N=[0];K=[0]*64;CR={63:1,56:2,7:4,0:8};H={}
D=OSError
sq=lambda n:ord(n[0])-33-int(n[1])*8
def parse(f):
 b=[0]*64;p=f.split();i=0
 for ch in p[0].replace("/",""):
  if ch.isdigit():i+=int(ch)
  else:v="pnbrqk".index(ch.lower())+1;b[i]=(v,-v)[ch>"Z"];i+=1
 w=p[1]=="w";c=sum(1<<i for i,k in enumerate("KQkq") if k in p[2])
 return b,w,c,sq(p[3]) if p[3]!="-" else -1
def atk(b,s,w):
 f=s&7;r=s>>3
 for df,dr in KN:
  f2=f+df;r2=r+dr
  if not(f2&~7 or r2&~7) and b[r2*8+f2]==(2,-2)[not w]:return 1
 for df,dr in KI:
  f2,r2=f,r;k=0
  while 1:
   f2+=df;r2+=dr;k+=1
   if f2&~7 or r2&~7:break
   q=b[r2*8+f2]
   if q:
    if (q>0)==w and (abs(q) in(5,(4,3)[df and dr]) or (k==1 and (abs(q)==6 or (df and dr and (dr>0)==w and abs(q)==1)))):return 1
    break
 return 0
def gen(b,w,c,e,ck):
 m=[];A=m.append
 for s,p in enumerate(b):
  if not p or (p>0)^w:continue
  t=abs(p);f=s&7;r=s>>3
  if t==1:
   d=(-8,8)[not w];t1=s+d;pr=r==(1,6)[not w]
   if b[t1]==0:
    if pr:m+=[(s,t1,q)for q in(5,4,3,2)]
    else:
     A((s,t1,0))
     if r==(6,1)[not w] and b[s+2*d]==0:A((s,s+2*d,0))
   for t1 in(s+d-1,s+d+1):
    if t1&7 in(f-1,f+1):
     q=b[t1]
     if q and(q>0)^w:
      if pr:m+=[(s,t1,q)for q in(5,4,3,2)]
      else:A((s,t1,0))
     elif t1==e:A((s,t1,0))
  else:
   for df,dr in DS[t]:
    f2,r2=f,r
    while 1:
     f2+=df;r2+=dr
     if f2&~7 or r2&~7:break
     t1=r2*8+f2;q=b[t1]
     if not q:A((s,t1,0))
     else:
      if(q>0)^w:A((s,t1,0))
      break
     if t in(2,6):break
   if t==6:
    for bit,ks,ds in((1,60,62),(2,60,58),(4,4,6),(8,4,2)):
     ps=(ks+ds)//2
     if s==ks and c&bit and not ck and not(b[ps]or b[ds]) and (ds>ks or not b[ds-1]) and not atk(b,ps,not w) and not atk(b,ds,not w):A((ks,ds,0))
 return m
def app(b,w,c,e,m):
 f,t,p=m;nb=b[:];pc=nb[f];nb[f]=0;a=abs(pc)
 if a==1 and t==e:nb[t+(8,-8)[not w]]=0
 nb[t]=(p,-p)[not w] if p else pc
 if a==6 and abs(t-f)==2:
  r=(t+1,t-2)[t<f];nb[(f+t)//2]=nb[r];nb[r]=0
 nc=(c&(12,3)[not w] if a==6 else c)&~(CR.get(f,0)|CR.get(t,0))
 return nb,nc,(f+t)//2 if a==1 and abs(t-f)==16 else -1
def ev(b):
 s=0
 for i,p in enumerate(b):
  if p:
   t=abs(p);v=V[t]
   if t<3:j=i if p>0 else i^56;v+=5*(ord(T[t-1][j//8*4+min(j&7,7-j%8)])-60)
   s+=(v,-v)[p<0]
 return s+25*(b.count(3)>1)-25*(b.count(-3)>1)
def sr(b,w,c,e,d,a,be,pl):
 N[0]+=1
 if N[0]>15e4:raise D
 if atk(b,b.index((-6,6)[not w]),w):return 99998
 ks=b.index((6,-6)[not w]);ck=atk(b,ks,not w);q=d<=0 and not ck
 if d<-3 and not ck:return(ev(b),-ev(b))[not w]
 ms=gen(b,w,c,e,ck)
 if q and not ms:return 0
 if q:
  st=(ev(b),-ev(b))[not w]+len(ms)
  if st>=be:return be
  if st>a:a=st
 if q:ms=[m for m in ms if b[m[1]] or m[2]]
 elif d>2 and not ck and sr(b,not w,c,-1,d-3,-be,1-be,pl+1)<=-be:return be
 h=H.get(tuple(b))
 ms.sort(key=lambda m:(m!=h,-abs(b[m[1]])*10+abs(b[m[0]])if b[m[1]]else-m[2],m!=K[pl]))
 bs=(a,-99999)[not q];n=0;bm=0
 for m in ms:
  nb,nc,ne=app(b,w,c,e,m)
  n+=1;s=-sr(nb,not w,nc,ne,d-1,-be,-a,pl+1)
  if s>bs:bs=s;bm=m
  if s>a:a=s
  if a>=be:K[pl]=m;break
 if not n:return(a,(-99999+pl,0)[not ck])[not q]
 H[tuple(b)]=bm
 return bs
def choose(x,L):
 b,w,c,e=parse(x)
 if len(L)==1:return L[0]
 ms=[(u,sq(u[:2]),sq(u[2:4]),(u[4:]and"nbrq".index(u[4])+2)or 0) for u in L]
 N[0]=0;H.clear();best=L[0]
 for d in range(1,9):
  try:
   bs=-99999;bm=best;a=-99999
   ms.sort(key=lambda x:x[0]!=best)
   for u,f,t,p in ms:
    nb,nc,ne=app(b,w,c,e,(f,t,p))
    s=-sr(nb,not w,nc,ne,d-1,-99999,-a,1)
    if s>bs:bs=s;bm=u
    if s>a:a=s
   best=bm
  except D:break
 return best
while(g:=post("/game",{}))["status"]!="done":
 while g["status"]=="your_move":g=post("/move",{"game":g["game"],"move":choose(g["fen"],g["legal_moves"])})
