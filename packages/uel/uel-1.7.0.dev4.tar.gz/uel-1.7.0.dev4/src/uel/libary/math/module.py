C='sin'
import math as A
from uel.objects import parse,UENumberObject as B
from uel.libary.helpers import make_exports as D
__all__=['PI',C,'bytecodes']
PI=B(A.pi)
def sin(f,n):C=parse(n,f);D=C.val;E=A.sin(D);F=B(E);return F
bytecodes=D({'PI':PI,C:sin})