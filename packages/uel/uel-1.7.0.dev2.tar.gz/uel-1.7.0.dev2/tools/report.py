O='.md'
N='.html'
M='.py'
L='.css'
K='.js'
I=filter
H=Exception
F=str
E=staticmethod
D=int
import os as A,sys,time as C,re
try:import rich;del rich
except ImportError as Y:from pip import main as B;B(['install','rich']);del B
from rich.console import Console as P
from rich.table import Table
from functools import lru_cache as Q
from concurrent.futures import ThreadPoolExecutor as R
from threading import Lock
from concurrent.futures import Future
import sys
def S():
	try:A=sys.argv;C,*B=A;return B[0]
	except IndexError:return'./'
J=S()
sys.setrecursionlimit(1000000)
def T(p):return'.git'in p or'.obsidian'in p or'mypy_cache'in p
def U(path,end):
	D=[]
	for(E,G,F)in A.walk(path):
		for B in F:
			C=A.path.join(E,B)
			if T(C):continue
			for B in end:
				if C.endswith(B):D.append(C);break
	return D
@Q()
def V(path):
	with open(path,'rb')as A:B=A.read();return B.count(b'\n')+1
G=[('Code',(K,L,M,N,O)),('Documentation',(O,)),('Python',(M,'.pyi')),('Configuration',('.json','.ini')),('HTML CSS JS',(K,L,N)),('Binary assets',('.png','.svg','.mp4','.mp3','.ttf','.jpg')),('Shell',('.sh',)),('Logs',('.log',*[f".log.{A}"for A in range(2,3)])),('C C++',('.c','.h','.cpp','.hpp')),('Cython(Pyx)',('.pyx',))]
G.insert(0,('All',tuple(set((lambda x:[B for A in x for B in A])([A for(B,A)in G])))))
class W:
	def __init__(B,items):
		B.start_time=C.mktime(C.strptime('2024-2-24 22:0:0','%Y-%m-%d %H:%M:%S'));B.dev_days=(C.time()-B.start_time)/60/60/24;B.items=items;B.console=P();B.pool=R();B.futures=None;D=80
		try:D=A.get_terminal_size().columns
		except H:pass
		B.terminal_width=D
	def remove_pycache_files(C):
		def B():
			def F(path):
				B=[]
				for D in A.listdir(path):
					C=A.path.join(path,D);B.append(C)
					if A.path.isdir(C):B+=F(C)
				return B
			def C(n):
				if A.path.split(n)[1]=='__pycache__'or n.endswith('.pyc'):return True
				return False
			D=F(J);E=I(C,D)
			for B in E:
				if A.path.isfile(B):A.remove(B)
			E,G=I(C,D),I(C,D)
			for B in E:
				if A.path.isdir(B):A.rmdir(B)
		B()
	def day(A):A.console.print('Number of dev days: ',A.dev_days)
	def create_task(A,item):[B,C]=item;D=X(B,C,A);return D.report()
	def report(A):
		B=C.time();A.remove_pycache_files();A.day();A.futures=[]
		for E in A.items:A.futures.append(A.create_task(E))
		A.wait_for(A.futures);F=C.time();G=D((F-B)*1000);A.console.print(f"Time of this report {G} MS")
	@E
	def wait_for(fs):
		for A in fs:A.result()
class X:
	def __init__(A,name,ends,report):A.name=name;A.ends=ends;A.__report=report;A.table=None
	def report(A):
		def B():
			L=1.1;A.table=Table(title=A.name,width=D(A.__report.terminal_width//L));A.table.add_column('Name',justify='left');A.table.add_column('Value',justify='center')
			class E(H):0
			class G(H):0
			try:
				C=U(J,A.ends);B=len(C)
				if B==0:raise G()
				I=sum(A.get_file_size(B)for B in C);M=A.stringSize(I);K=sum(V(A)for A in C);N=A.seg(F(K));O=A.seg(D(K/B));P=A.stringSize(I/B);A.table.add_row('Number of files',F(B));A.table.add_row('Size',M);A.table.add_row('Line number',N);A.table.add_row('Average number of rows',O);A.table.add_row('Average number of size',P);raise E()
			except E:A.__report.console.print(A.table)
			except G:return
		return A.__report.pool.submit(B)
	@E
	def get_file_size(i):return A.path.getsize(i)
	@E
	def stringSize(byte):
		B=byte;D='B',1;E='KB',1024;F='MB',1024*1024;G='GB',1024*1024*1024;A=D;C=.85
		if B>1024*C:A=E
		if B>1024*1024*C:A=F
		if B>1024*1024*1024*C:A=G
		H=round(B/A[1],2);return f"{H}{A[0]}"
	@E
	def seg(number):
		A=number
		if type(A)is float or type(A)is D:A=F(A)
		return re.sub('(?=\\B\\d{3}+$)',',',F(A))
def B():A=W(G);A.report()
if __name__=='__main__':B()