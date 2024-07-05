#!/usr/bin/python
R='src'
Q='uel'
P='objprint'
O='build_ext'
N=False
M='install'
L=EnvironmentError
G=OSError
F=open
D=True
try:import Cython as S,python_minifier as S
except:import pip;pip.main([M,'Cython','python-minifier'])
from Cython.Build import cythonize as T
from os import cpu_count as U
from setuptools import setup
from setuptools import Extension as B
from setuptools import find_namespace_packages as V
from setuptools.command.build_ext import build_ext as W
from setuptools._distutils import file_util as X
from setuptools._distutils.errors import DistutilsFileError as I
from setuptools.dist import Distribution as H
import os as A,sys as C,re,platform as J,contextlib,io,python_minifier as Y
with F('./README.md')as E:Z=E.read()
del E
def a(src,dst,buffer_size=16*1024):
	J=src;B=dst
	def K(data,file):
		B=data
		if file.endswith('.py'):
			if'nominify'in A.path.split(file)[0]:return B
			return Y.minify(B.decode(),remove_literal_statements=D,rename_globals=D).encode()
		return B
	E=None;H=None
	try:
		try:E=F(J,'rb')
		except G as C:raise I(f"could not open '{J}': {C.strerror}")
		if A.path.exists(B):
			try:A.unlink(B)
			except G as C:raise I(f"could not delete '{B}': {C.strerror}")
		try:H=F(B,'wb')
		except G as C:raise I(f"could not create '{B}': {C.strerror}")
		L=K(E.read(),J);H.write(L)
	finally:
		if H:H.close()
		if E:E.close()
with F('src/uel/nominify/version.py','rt',encoding='utf8')as E:b=re.search('__version__ = "(.*?)"',E.read()).group(1)
def c(old):
	def A(self,command):A=command;print(f" {str(A)} ".center(d(),'*'));old(self,A)
	return A
H.run_command=c(H.run_command)
j=U()or 1
def d():
	try:return A.get_terminal_size().columns
	except G:return 80
class e(W):
	def initialize_options(A,*B,**C):super().initialize_options(*B,**C);A.parallel=N
def f():
	A='CPython'
	if J.python_implementation()!=A or C.version_info<(3,11,0):
		if J.python_implementation()!=A:raise L('Python implementation must be CPython')
		else:raise L('Python version is too low')
def g():
	if len(C.argv)<2:return D
	A=['build','build_py',O,'build_clibbuild_scripts',M,'install_lib','install_headers','install_scripts','install_data','sdist','bdist','bdist_dumb','bdist_rpm','bdist_wheel','check','bdist_egg','develop'];return any(A in C.argv[1:]for A in A)
def h():F='src/uel/puel/dev-utils.c';C=[];G='build/uel';D=['src/uel/include/'];E=['--std=gnu11'];H=['--std=gnu++17'];C.extend(T(module_list=[B(name='uel.libary.sequence.module',sources=['src/uel/libary/sequence/module.pyx']),B(name='uel.ueargparse',sources=['src/uel/ueargparse.pyx']),B(name='uel.runner.ueval',sources=['src/uel/runner/ueval.pyx'])],build_dir=G,nthreads=A.cpu_count(),language_level='3str'));C.extend([B(name='uel.bytecodefile._compress',sources=['src/uel/bytecodefile/_compress.c',F],include_dirs=D,language='c',extra_compile_args=E),B(name='uel.impl.sequence',sources=['src/uel/impl/sequence/sequence.c',F],include_dirs=D,language='c',extra_compile_args=E)]);C.sort(key=lambda ext:sum(map(A.path.getsize,ext.sources)));return C
def i():
	if len(C.argv[1:])>1:return D
	if'dist'in C.argv[1]:return D
	return N
k={'install_requires':[P]}
K=dict(name=Q,version=b,author='XingHao. Li<3584434540@qq.com>',long_description=Z,packages=V(R),package_dir={'':R},package_data={Q:['**']},cmdclass={O:e},install_requires=[P],entry_points={'console_scripts':['uel = uel.cli:main']})
f()
if g():K['ext_modules']=h()
if i():X._copy_file_contents=a
setup(**K)