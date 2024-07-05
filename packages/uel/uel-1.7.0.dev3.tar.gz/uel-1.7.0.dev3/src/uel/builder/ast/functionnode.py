from uel.builder.ast.abstractnode import AbstractNode
from uel.builder.ast.containernode import ContainerNode as A
__all__=['FunctionNode']
class FunctionNode(A):
	def __init__(A,children,name,args):super().__init__(children);A.args=args;A.name=name