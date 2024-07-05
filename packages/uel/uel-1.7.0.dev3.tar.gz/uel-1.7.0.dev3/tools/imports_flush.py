I=sorted
F=isinstance
E=type
D=filter
import os,ast as A,re,sys,functools as J,importlib as K,multiprocessing as L,keyword,io,pprint
M=sys.argv[1]
G=sys.argv[2]
def N(string):
	A=string
	def C(m):
		if m.__name__ not in'.':return[]
		if hasattr(m,'__all__'):return m.__all__
		return[]
	def D():
		A=B.group(1)
		for C in B.group(2).split(','):
			if A.strip()==os.path.split(G)[1]:continue
			yield f"from {A} import {C.strip()}"
	def E(match):
		A=match.group(1)
		try:B=K.import_module(A.strip());return[f"from {A} import {B}"for B in C(B)]
		except:return[f"from {A} import *"]
	if(B:=re.fullmatch('from (.+?) import (.+)',string=A)):return[*D()]
	elif(B:=re.fullmatch('import ([^\\s]+)\\s*$',A)):return[*E(B),A]
	else:return[A]
def B(i):A=-1*len(i);return A
def O(x,y):
	if B(x)>B(y):return 1
	elif B(x)<B(y):return-1
	return 1 if x>y else-1
def P(args):
	C,O,F=args;B=[]
	for G in D(lambda x:x.endswith('.py')or x.endswith('.pyi'),F):
		H=os.path.join(C,G)
		with open(H,'rt')as I:J=I.read()
		K=[*D(lambda child:E(child)is A.Import or E(child)is A.ImportFrom,A.parse(J).body)]
		for L in K:M=A.unparse(L);B.extend(N(M))
	return B
def Q(imports):
	B=imports;C={}
	def E(_import):
		def C(alias):
			A=alias
			if A.asname is not None:return A.asname
			return A.name
		for B in A.parse(_import).body:
			if F(B,(A.Import,A.ImportFrom)):
				if F(B,A.Import):D=B.names[0];return C(D)
				elif F(B,A.ImportFrom):return C(B.names[0])
	I=[*D(lambda x:'.'not in x,map(E,B))]
	for G in B:H=E(G);C[H]=G
	return C
def H(f):
	A=[]
	for B in f:
		if E(B)is list:A.extend(H(B))
		else:A.append(B)
	return A
def R(where):
	with L.Pool()as B:global C;C=B.map(P,[*os.walk(where)],chunksize=50);C=H(C)
	A=Q(C);D=I(A.values(),key=J.cmp_to_key(O));return f"__all__ = {repr(I([A for A in A.keys()if A!='*'],key=len,reverse=True))}\n",'\n'.join([*D])
def S():
	with open(M,'wt')as D:C=io.StringIO();E,F=R(G);C.write(E);C.write(F);C.write('\n');B=C.getvalue();B=A.unparse(A.parse(B));B=f"# yapf: disable\n{B}";D.write(B)
if __name__=='__main__':S()