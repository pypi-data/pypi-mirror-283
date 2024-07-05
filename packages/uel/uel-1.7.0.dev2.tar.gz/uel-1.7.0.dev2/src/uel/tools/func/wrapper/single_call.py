from ctypes import c_ulong,pointer
from typing import*
T=ParamSpec('T')
R=TypeVar('R')
__all__=['single_call']
def single_call(fn):
	run_count=pointer(c_ulong(0))
	def inner(*args,**kwargs):
		if 1<=run_count.contents.value:raise RuntimeError('This function is called at most once.')
		result=fn(*args,**kwargs);run_count.contents.value+=1;return result
	return inner