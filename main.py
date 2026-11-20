import json,os,sys,urllib.request,urllib.error as U
E=os.environ["MAKEFUN_ENV_URL"]
H={"content-type":"application/json"}
def R(p,b):
 try:return json.load(urllib.request.urlopen(urllib.request.Request(E+p,data=json.dumps(b).encode(),headers=H)))
 except U.HTTPError:sys.exit(0)
M88=0x88
A=[r*16+c for r in range(8) for c in range(8)]
PW="PNBRQK";PB="pnbrqk"
def pc(c):
 i=PW.find(c);return i if i>=0 else PB.find(c)+6
PP=PW+PB
V=[100,320,330,500,900,0,-100,-320,-330,-500,-900,0]
def lf(b,f):
 for i in range(128):b[i]=" "
 p=f.split();r=0;c=0
 for h in p[0]:
  if h=="/":r+=1;c=0;continue
  if h.isdigit():c+=int(h)
  else:b[r*16+c]=h;c+=1
 t=p[1]=="w";C=0
 for x in p[2]:
  if x=="K":C|=1
  elif x=="Q":C|=2
  elif x=="k":C|=4
  elif x=="q":C|=8
 e=-1
 if p[3]!="-":c="abcdefgh".index(p[3][0]);r=8-int(p[3][1]);e=r*16+c
 return t,C,e
def ka(s,b,w):
 if w:
  for d in(-1,1):
   t=s-16+d
   if(t&M88)==0 and b[t]=="P":return 1
 else:
  for d in(-1,1):
   t=s+16+d
   if(t&M88)==0 and b[t]=="p":return 1
 for d in(33,31,-31,-33,18,14,-14,-18):
  t=s+d
  if(t&M88)==0:
   if w and b[t]=="N":return 1
   if not w and b[t]=="n":return 1
 for d in(17,15,-15,-17,16,-16,1,-1):
  t=s
  while 1:
   t+=d
   if(t&M88)!=0:break
   c=b[t]
   if c==" ":continue
   if w:
    if c=="B" and d in(17,15,-15,-17) or c=="R" and d in(16,-16,1,-1) or c in"QK":return 1
   else:
    if c=="b" and d in(17,15,-15,-17) or c=="r" and d in(16,-16,1,-1) or c in"qk":return 1
   break
 return 0
def gl(b,t,e):
 mv=[]
 for s in A:
  p=b[s]
  if p==" ":continue
  if t and p in PB:continue
  if not t and p in PW:continue
  cc=pc(p)
  if cc==5 or cc==11:
   for d in(17,15,-15,-17,16,-16,1,-1):
    x=s+d
    if(x&M88)==0 and((b[x]==" ")or(t and b[x] in PB)or(not t and b[x] in PW))and not ka(x,b,t):mv.append((s,x,-1))
   continue
  if cc in(2,8):dl=(17,15,-15,-17)
  elif cc in(3,9):dl=(16,-16,1,-1)
  elif cc in(4,10):dl=(17,15,-15,-17,16,-16,1,-1)
  else:dl=None
  if dl:
   for d in dl:
    y=d
    while 1:
     x=s+y
     if(x&M88)!=0:break
     if b[x]!=" ":
      if(t and b[x] in PB)or(not t and b[x] in PW):mv.append((s,x,-1))
      break
     else:mv.append((s,x,-1))
     y+=d
  elif cc in(1,7):
   for n in(33,31,-31,-33,18,14,-14,-18):
    x=s+n
    if(x&M88)==0 and((b[x]==" ")or(t and b[x] in PB)or(not t and b[x] in PW)):mv.append((s,x,-1))
  elif cc in(0,6):
   f=16 if t else -16;s7=1 if t else 6
   x=s+f
   if(x&M88)==0 and b[x]==" ":
    if(t and x>>4==7)or(not t and x>>4==0):mv.append((s,x,1))
    else:mv.append((s,x,-1))
    if s>>4==s7:
     x2=s+2*f
     if(x2&M88)==0 and b[x2]==" ":mv.append((s,x2,-1))
   for d in(1,-1):
    c=s+f+d
    if(c&M88)==0:
     if(t and b[c] in PB)or(not t and b[c] in PW):
      if(t and c>>4==7)or(not t and c>>4==0):mv.append((s,c,1))
      else:mv.append((s,c,-1))
     elif c==e:mv.append((s,c,-1))
 return mv
def ev(b,t):
 sc=0
 for s in A:
  p=b[s]
  if p==" ":continue
  cc=pc(p)
  if cc<0:continue
  sc+=V[cc] if cc<6 else -V[cc-6]
 return sc if t else -sc
def nm(b,st,t,d,a,b2):
 if d<=0:return ev(b,t),None
 mv=gl(b,turn,st[2])
 if not mv:
  k="K" if t else "k";km=-1
  for s in A:
   if b[s]==k:km=s;break
  if km<0 or ka(km,b,t):return -100000+d,None
  return 0,None
 bm=None;bs=a
 for m in mv:
  s,x,pr=m
  ob=list(b);ost=list(st)
  b[x]=b[s];b[s]=" "
  if pr>=0:b[x]=PP[pr]
  k="K" if t else "k";ns=-1
  for y in A:
   if b[y]==k:ns=y;break
  if ns<0 or ka(ns,b,t):b[:]=ob;st[:]=ost;continue
  sc,_=nm(b,st,not t,d-1,-b2,-a)
  b[:]=ob;st[:]=ost
  if sc>bs:bs=sc;bm=m
 return bs,bm
while 1:
 g=R("/game",{})
 if g["status"]=="done":break
 if g["status"]=="your_move":
  b=[" "]*128;turn,C,e=lf(b,g["fen"]);st=[turn,C,e];bm=None
  for d in range(1,4):
   sc,bm2=nm(b,st,turn,d,-100000,100000)
   if sc==-100000+d:continue
   if bm2:bm=bm2;break
  if bm is None:ms=gl(b,turn,e);bm=ms[0] if ms else None
  if bm is None:print("e2e4")
  else:
   s,x,pr=bm;f="abcdefgh"
   print(f[s%16]+str(s//16+1)+f[x%16]+str(x//16+1)+{1:"N",2:"B",3:"R",4:"Q"}.get(pr,""))
