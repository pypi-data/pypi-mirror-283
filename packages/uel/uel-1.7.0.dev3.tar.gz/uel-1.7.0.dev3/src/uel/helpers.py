import builtins
from typing import*
from uel.builder.ast.importnode import ImportNode
from uel.builder.bytecode.bytecodeinfo import BytecodeInfo
from uel.errors.runtime.throw import throw
from uel.errors.runtime.uelruntimeerror import UELRuntimeError
from uel.objects import UEObject
from uel.runner.frame import Frame
__all__=['get_variable_from_frame','u_module_def']
def get_variable_from_frame(name,frame):
	current=frame
	while True:
		if current is None:throw(UELRuntimeError,f"Name {name} is not defined");raise SystemExit
		try:return current.variables[name]
		except KeyError:
			if current.prev_frame is None:throw(UELRuntimeError,f"Name {name} is not defined");raise SystemExit
			current=current.prev_frame