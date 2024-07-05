from typing import Callable,Any
import os as A
__all__=['BUILTIN_MODULES']
F=lambda name:lambda:C(name)
def G(names,root):
	for B in names:
		C=A.path.join(root,B)
		if not A.path.isdir(C):continue
		if any(map(lambda i:'module'in i,A.listdir(C))):yield B
def B():
	global C;from uel.runner.importlib import UEModuleNew,pymodule_get as C;D=A.path.dirname(__file__);E={}
	for B in G(A.listdir(D),D):
		if B=='__pycache__':continue
		E[B.strip('_')]=F(B)
	return E
BUILTIN_MODULES={}
D=BUILTIN_MODULES
D|=B()