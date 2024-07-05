from uel.builder.ast.abstractnode import AbstractNode as A
__all__=['BinOpNode']
class BinOpNode(A):
	left:0;right:0
	def __init__(A,left,right):A.left=left;A.right=right