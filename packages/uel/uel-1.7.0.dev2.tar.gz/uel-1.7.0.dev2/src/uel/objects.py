_F='function'
_E='boolean'
_D='number'
_C='string'
_B='object'
_A=False
from typing import*
from uel.errors.runtime.throw import throw
from uel.errors.runtime.uelmakeobjecterror import UELMakeObjectError
from queue import Empty
from typing import Tuple
from uel.errors.runtime.throw import throw
from uel.errors.runtime.uelruntimeerror import UELRuntimeError
from uel.runner.frame import Frame
from uel.tools.func.share.runtime_type_check import runtime_type_check
from uel.builder.bytecode.bytecodeinfo import BytecodeInfo
from uel.runner.frame import Frame
from uel.runner.stack import Stack
from uel.impl.sequence import Sequence
from objprint import objstr
import typing as t
T=TypeVar('T')
__all__=['UEObject','UEBooleanObject','UECallableObject','UEFunctionObject','UENumberObject','UESequenceObject','UEStringObject','IS_CAN_MAKE_OBJECT','uel_new_object','parse']
TRUE='true'
FALSE='false'
class UEObject:
	_create:0
	def __new__(cls,*args):obj=object.__new__(cls);obj._create=args;return obj
	def __reduce__(self):return self.__class__,self._create
	def __repr__(self):return self.tp_str()
	def __eq__(self,other):return self.tp_equal(other).val
	def tp_bytecode(self):return _B,self
	def tp_str(self):return_string=hex(id(self));classname=self.__class__.__name__[2:-6];return f"[{classname.lower()} {classname.title()}]"
	def tp(self,typ):return self
class UEBooleanObject(UEObject):
	def tp_str(self):return str(self.val)
	def tp_add(self,other):from uel.objects import UENumberObject;return UENumberObject(self.val+other.val)
	def __init__(self,val):
		if type(val)is str:self.val=True if val==TRUE else _A
		elif type(val)is bool:self.val=val
		else:raise TypeError(f"Unable to convert {type(val)} to Boolean")
class UECallableObject(UEObject):
	def __init__(self):0
	def tp_call(self,*args,**kwargs):raise NotImplementedError
class UEFunctionObject(UECallableObject):
	def __init__(self,args,bytecodes):self.args=args;self.bytecodes=bytecodes
	def tp_call(self,ueval,frame,args):
		from uel.runner.ueval import Ueval
		if len(args)!=len(self.args):throw(UELRuntimeError(f"Only {len(self.args)} parameters are accepted,but there are {args} arguments."))
		frame=Frame(stack=Stack(),idx=0,bytecodes=self.bytecodes,prev_frame=frame,filename=frame.filename,variables=dict(zip(self.args,(parse(x,frame)for x in args))));ueval.frame=frame
class UENumberObject(UEObject):
	def tp_str(self):return str(self.val)
	def tp_add(self,other):return UENumberObject(self.val+(other.val if isinstance(other,UENumberObject)else other))
	def tp_minus(self,other):return UENumberObject(self.val-(other.val if isinstance(other,UENumberObject)else other))
	def tp_mult(self,other):return UENumberObject(self.val*(other.val if isinstance(other,UENumberObject)else other))
	def tp_div(self,other):return UENumberObject(self.val/(other.val if isinstance(other,UENumberObject)else other))
	def tp_equal(self,other):
		if not runtime_type_check(other,type(self)):return UEBooleanObject(_A)
		return UEBooleanObject(self.val==other.val)
	def __init__(self,string):
		if type(string)in(int,float):self.val=string
		elif'.'not in string:self.val=int(string)
		else:self.val=float(string)
class UESequenceObject(UEObject):
	def __init__(self):self.val=Sequence()
	def tp_str(self):string=', '.join(map(lambda x:x.tp_str(),self.val.as_list()));return f"sequence({string})"
class UEStringObject(UEObject):
	def tp_str(self):return self.val
	def tp_add(self,other):
		if runtime_type_check(other,UEStringObject)or runtime_type_check(other,str):
			if runtime_type_check(other,UEStringObject):return UEStringObject(self.val+other.val)
			else:return UEStringObject(self.val+other)
		else:throw(UELRuntimeError('Type Error: Cannot add'))
	def __init__(self,string):self.val=string
	def tp_equal(self,other):
		if runtime_type_check(other,UEStringObject)and other.val==self.val:return UEBooleanObject(True)
		return UEBooleanObject(_A)
def _CHECKOUT_TYP_TYPE(typ):
	assert IS_CAN_MAKE_OBJECT(typ),'Fuck you'
	if type(typ)is not str:raise TypeError('Arg 1 must be str')
def IS_CAN_MAKE_OBJECT(typ):
	if typ!=_C and typ!=_D and typ!=_E and typ!=_F:return _A
	return True
def ueObjectGetConstructor(typ):
	if typ==_C:return UEStringObject
	elif typ==_D:return UENumberObject
	elif typ==_E:return UEBooleanObject
	elif typ==_F:return UEFunctionObject
	return UEObject
def __UEObjectNew(typ,val):
	constructor=ueObjectGetConstructor(typ)
	if constructor is UEFunctionObject:return constructor(*val)
	return constructor(val)
def uel_new_object(typ,val):_CHECKOUT_TYP_TYPE(typ);return __UEObjectNew(typ,val)
def parse(info,frame):
	from uel.helpers import get_variable_from_frame
	if not isinstance(info,tuple):return info
	typ,val=info
	if typ=='stack_top':
		try:return parse(frame.gqueue.get_nowait(),frame)
		except Empty:throw(UELRuntimeError('[ValueError] At least one PUSH before TOP'))
	elif typ==_B:return val
	elif typ=='name':return get_variable_from_frame(val,frame)
	raise ValueError