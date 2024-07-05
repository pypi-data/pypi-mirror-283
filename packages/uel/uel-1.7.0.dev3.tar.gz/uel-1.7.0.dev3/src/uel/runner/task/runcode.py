from uel.builder.bytecode.bytecodeinfo import BytecodeInfo
from uel.runner.task.abstracttask import AbstractTask as A
from uel.runner.ueval import Ueval
__all__=['RunCode']
class RunCode(A):
	def run(D,tup):A,B=tup;C=Ueval(A,filename=B);C.uelEval_EvalBytecodeDefault()