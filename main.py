import json,os,time
from urllib.request import Request,urlopen
U=os.environ['MAKEFUN_ENV_URL']
V='.PNBRQK'
W=0,100,320,330,500,900,60000
CE='0123321012455421246776423579975335799753246776421245542101233210'
B=(1,1),(1,-1),(-1,-1),(-1,1)
R=(0,1),(1,0),(0,-1),(-1,0)
Q=B+R
N8=(1,2),(2,1),(-1,2),(-2,1),(1,-2),(2,-1),(-1,-2),(-2,-1)
K8=(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1)
N=0
L=900000
DL=0
T={}
KK={}
def api(p,d):return json.load(urlopen(Request(U+p,json.dumps(d).encode(),{'content-type':'application/json'})))
def fen(f):
	C=['.']*64
	for(D,E)in enumerate(f.split('/')):
		A=0
		for B in E:
			if B in'12345678':A+=int(B)
			else:C[(7-D)*8+A]=B;A+=1
	return C
def gen(b,w,c):
	D=[]
	for(C,L)in enumerate(b):
		if L=='.'or(L<'a')!=w:continue
		M,I=C%8,C//8;F=L.upper()
		if F=='P':
			J=8 if w else-8;A=C+J
			if 0<=A<64 and b[A]=='.':
				D.append((C,A,'q'if A//8 in(0,7)else''))
				if(w and I==1 or not w and I==6)and b[C+2*J]=='.':D.append((C,C+2*J,''))
			for E in(-1,1):
				A=C+J+E
				if 0<=M+E<8 and 0<=A<64 and b[A]!='.'and(b[A]<'a')!=w:D.append((C,A,'q'if A//8 in(0,7)else''))
		elif F in'BRQ':
			for(E,K)in B if F=='B'else R if F=='R'else Q:
				G,H=M+E,I+K
				while 0<=G<8 and 0<=H<8:
					A=H*8+G
					if b[A]!='.':
						if(b[A]<'a')!=w:D.append((C,A,''))
						break
					D.append((C,A,''));G+=E;H+=K
		else:
			for(E,K)in N8 if F=='N'else K8:
				G,H=M+E,I+K
				if 0<=G<8 and 0<=H<8:
					A=H*8+G
					if b[A]=='.'or(b[A]<'a')!=w:D.append((C,A,''))
			if F=='K':
				if w and C==4:
					if'K'in c and b[5]+b[6]=='..'and b[7]=='R':D.append((4,6,''))
					if'Q'in c and b[1]+b[2]+b[3]=='...'and b[0]=='R':D.append((4,2,''))
				if not w and C==60:
					if'k'in c and b[61]+b[62]=='..'and b[63]=='r':D.append((60,62,''))
					if'q'in c and b[57]+b[58]+b[59]=='...'and b[56]=='r':D.append((60,58,''))
	return D
def mk(b,m):
	B,C,E=m;A=b[:];D=A[B];A[B]='.'
	if D.upper()=='K'and abs(C-B)==2:
		if C>B:A[B+1]=A[B+3];A[B+3]='.'
		else:A[B-1]=A[B-4];A[B-4]='.'
	if D.upper()=='P'and B%8!=C%8 and A[C]=='.':A[C+(-8 if D<'a'else 8)]='.'
	A[C]=E and(E if D>'Z'else E.upper())or D;return A
def ev(b,w):
	C=0
	for(D,A)in enumerate(b):
		if A!='.':
			E=A.upper();B=W[V.index(E)]
			if E in'PNB':B+=ord(CE[D])-48
			if E=='P':B+=(D//8 if A<'a'else 7-D//8)*8
			C+=B if A<'a'else-B
	return C if w else-C
def oms(b,ms,km):ms.sort(key=lambda m:(0 if m==km else 1,-(W[V.index(b[m[1]].upper())]if b[m[1]]!='.'else 0)+W[V.index(b[m[0]].upper())]))
def qs(b,a,be,w,c,q=4):
	global N;N+=1;A=ev(b,w)
	if A>=be or N>L or q<1 or time.time()>DL:return A
	if A>a:a=A
	C=gen(b,w,c);oms(b,C,None)
	for B in C:
		if b[B[1]]=='.'and not B[2]:continue
		D=-qs(mk(b,B),-be,-a,not w,c,q-1)
		if D>A:A=D
		if A>a:a=A
		if A>=be:break
	return A
def ne(b,d,a,be,w,c):
	D=be;global N;N+=1
	if d<1 or N>L or time.time()>DL:return qs(b,a,D,w,c)
	E=''.join(b)+('w'if w else'b');J=a;A=T.get(E)
	if A and A[0]>=d and(A[2]==0 or A[2]>0 and A[1]>=D or A[2]<0 and A[1]<=a):return A[1]
	G=gen(b,w,c)
	if not G:return-99000
	oms(b,G,KK.get(E));B=-999999;I=1
	for F in G:
		H=mk(b,F)
		if I:C=-ne(H,d-1,-D,-a,not w,c);I=0
		else:
			C=-ne(H,d-1,-a-1,-a,not w,c)
			if C>a and C<D:C=-ne(H,d-1,-D,-a,not w,c)
		if C>B:B=C
		if C>a:a=C
		if a>=D or N>L:break
	if B>=D:T[E]=d,B,1,F
	elif B<=J:T[E]=d,B,-1,F;KK[E]=F
	else:T[E]=d,B,0,F
	return B
def uci(m):return'abcdefgh'[m[0]%8]+str(m[0]//8+1)+'abcdefgh'[m[1]%8]+str(m[1]//8+1)+m[2]
def pick(fs,lg):
	global N,T,KK,DL;T={};KK={};B=fs.split();F=fen(B[0]);G=B[1]=='w'if len(B)>1 else True;H=B[2]if len(B)>2 else'-';C=[A for A in gen(F,G,H)if uci(A)in lg]
	if not C:return lg[0]
	I=C[0]
	for M in range(1,9):
		N=0;DL=time.time()+1.9;J=-999999;A=None;E=-999999
		for K in C:
			D=-ne(mk(F,K),M-1,-999999,-E,not G,H)
			if A is None or D>J:J=D;A=K
			if D>E:E=D
			if N>L:break
		if A and N<=L and time.time()<=DL:I=A;C.remove(A);C.insert(0,A)
		if N>L or time.time()>DL:break
	return uci(I)
while 1:
	g=api('/game',{})
	if g['status']=='done':break
	while g['status']=='your_move':g=api('/move',{'game':g['game'],'move':pick(g['fen'],g['legal_moves'])})