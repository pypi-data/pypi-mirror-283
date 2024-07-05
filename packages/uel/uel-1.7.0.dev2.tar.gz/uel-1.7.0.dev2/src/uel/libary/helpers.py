from uel.builder.bytecode.bytecodeinfo import BT_LOAD_CONST as D,BT_STORE_NAME as E,BytecodeInfo as A
from types import FunctionType
__all__=['make_exports']
def make_exports(exports):B=exports;C=range(1,len(B)<<1+1).__iter__();return[G for(B,F)in B.items()for G in(A(D,F,pos=next(C)),A(E,B,pos=next(C)))]