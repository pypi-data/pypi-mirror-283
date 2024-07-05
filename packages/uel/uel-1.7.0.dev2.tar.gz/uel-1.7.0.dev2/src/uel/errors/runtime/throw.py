import sys
from typing import*
from uel.errors.runtime.uelruntimeerror import UELRuntimeError
__all__=['throw']
@overload
def throw(e):...
@overload
def throw(e,string):...
def throw(e,string=None):
	if type(e)is type:e=e(string)
	sys.stderr.write(str(e));raise SystemExit