from typing import IO,Any
from uel.constants import DEBUG as A
from uel.runner.task.buildcode import BuildCode as B
from uel.runner.task.runcode import RunCode as C
__all__=['ExecuteContext']
class ExecuteContext:
	def run_code_from_basic(F,fn,code,debug):A=B(fn,code);D=A.run(debug=debug);E=C();E.run(D)
	def build_bytecodes(D,fn,code,debug):A=B(fn,code);C=A.run(debug=debug);return C
	def run_bytecodes(A,bytecodes):C().run(bytecodes)
	def run_code_from_fd(B,fd,source,debug=A):B.run_code_from_basic(source,fd.read(),debug=A)