from functools import wraps
from typing import Any,Callable,Generic as B,ParamSpec as C,TypeVar as A
G=C('P')
H=A('R')
D=A('E')
__all__=['Withable','with_out']
class Withable(B[D]):
	def __init__(A,value):A.value=value
	def __repr__(A):return f"Withable<{A.value.__class__.__name__}>({A.value})"
	def __enter__(A):return A.value
	def __exit__(A,a,b,c):0
def with_out(func):
	@wraps(func)
	def A(*A,**B):return Withable(func(*A,**B))
	return A
if __name__=='__main__':
	@with_out
	def E(m):return m+3
	with E(3)as F:print(F)