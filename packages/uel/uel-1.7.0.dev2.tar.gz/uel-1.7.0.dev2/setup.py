#!/usr/bin/python
Q='src'
P='uel'
O='objprint'
N='build_ext'
M=False
L='install'
K=EnvironmentError
I=open
E=OSError
D=True
try:import Cython as R,python_minifier as R
except:import pip;pip.main([L,'Cython','python-minifier'])
from Cython.Build import cythonize as S
from os import cpu_count as T
from setuptools import setup
from setuptools import Extension as B
from setuptools import find_namespace_packages as U
from setuptools.command.build_ext import build_ext as V
from setuptools._distutils import file_util as W
from setuptools._distutils.errors import DistutilsFileError as H
from setuptools.dist import Distribution as F
import os as A,sys as C,re,platform as G,contextlib,io,python_minifier as X
Y='<iframe src="https://user-11150.github.io/puel">'
def Z(src,dst,buffer_size=16*1024):
	J=src;B=dst
	def K(data,file):
		B=data
		if file.endswith('.py'):
			if'nominify'in A.path.split(file)[0]:return B
			return X.minify(B.decode(),remove_literal_statements=D,rename_globals=D).encode()
		return B
	F=None;G=None
	try:
		try:F=I(J,'rb')
		except E as C:raise H(f"could not open '{J}': {C.strerror}")
		if A.path.exists(B):
			try:A.unlink(B)
			except E as C:raise H(f"could not delete '{B}': {C.strerror}")
		try:G=I(B,'wb')
		except E as C:raise H(f"could not create '{B}': {C.strerror}")
		L=K(F.read(),J);G.write(L)
	finally:
		if G:G.close()
		if F:F.close()
with I('src/uel/nominify/version.py','rt',encoding='utf8')as a:b=re.search('__version__ = "(.*?)"',a.read()).group(1)
def c(old):
	def A(self,command):A=command;print(f" {str(A)} ".center(d(),'*'));old(self,A)
	return A
F.run_command=c(F.run_command)
j=T()or 1
def d():
	try:return A.get_terminal_size().columns
	except E:return 80
class e(V):
	def initialize_options(A,*B,**C):super().initialize_options(*B,**C);A.parallel=M
def f():
	A='CPython'
	if G.python_implementation()!=A or C.version_info<(3,11,0):
		if G.python_implementation()!=A:raise K('Python implementation must be CPython')
		else:raise K('Python version is too low')
def g():
	if len(C.argv)<2:return D
	A=['build','build_py',N,'build_clibbuild_scripts',L,'install_lib','install_headers','install_scripts','install_data','sdist','bdist','bdist_dumb','bdist_rpm','bdist_wheel','check','bdist_egg','develop'];return any(A in C.argv[1:]for A in A)
def h():F='src/uel/puel/dev-utils.c';C=[];G='build/uel';D=['src/uel/include/'];E=['--std=gnu11'];H=['--std=gnu++17'];C.extend(S(module_list=[B(name='uel.libary.sequence.module',sources=['src/uel/libary/sequence/module.pyx']),B(name='uel.ueargparse',sources=['src/uel/ueargparse.pyx']),B(name='uel.runner.ueval',sources=['src/uel/runner/ueval.pyx'])],build_dir=G,nthreads=A.cpu_count(),language_level='3str'));C.extend([B(name='uel.bytecodefile._compress',sources=['src/uel/bytecodefile/_compress.c',F],include_dirs=D,language='c',extra_compile_args=E),B(name='uel.impl.sequence',sources=['src/uel/impl/sequence/sequence.c',F],include_dirs=D,language='c',extra_compile_args=E)]);C.sort(key=lambda ext:sum(map(A.path.getsize,ext.sources)));return C
def i():
	if len(C.argv[1:])>1:return D
	if'dist'in C.argv[1]:return D
	return M
k={'install_requires':[O]}
J=dict(name=P,version=b,author='XingHao. Li<3584434540@qq.com>',long_description=Y,packages=U(Q),package_dir={'':Q},package_data={P:['**']},cmdclass={N:e},install_requires=[O],entry_points={'console_scripts':['uel = uel.cli:main']})
f()
if g():J['ext_modules']=h()
if i():W._copy_file_contents=Z
setup(**J)