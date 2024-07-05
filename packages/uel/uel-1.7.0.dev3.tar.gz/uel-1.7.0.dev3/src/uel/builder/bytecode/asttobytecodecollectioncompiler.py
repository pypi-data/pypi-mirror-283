from typing import Any
from uel.builder.ast.modulenode import ModuleNode
from uel.builder.bytecode.bytecodeinfo import BytecodeInfo
from uel.builder.bytecode.uelbytecodecompiler import UELBytecodeCompiler as A
from uel.tools.func.share.runtime_type_check import runtime_type_check
from uel.tools.func.wrapper.with_out import with_out as B
__all__=['ASTToByteCodeCollectionCompiler']
class ASTToByteCodeCollectionCompiler:
	@B
	def with_ast(self,ast,filename):A=self.createCompiler(filename);A.read(ast);return A.toBytecodes(),A.filename
	def createCompiler(D,*B,**C):return A(*B,**C)