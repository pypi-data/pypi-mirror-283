import typing
from uel.builder.ast.abstractnode import AbstractNode as A
from uel.builder.ast.constant import Constant
from uel.builder.ast.singlenode import SingleNode
__all__=['ExpressionNode']
class ExpressionNode(A):
	def __init__(A,val):A.val=val