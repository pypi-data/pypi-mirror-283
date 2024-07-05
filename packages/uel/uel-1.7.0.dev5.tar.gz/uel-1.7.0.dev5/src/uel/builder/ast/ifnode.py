from uel.builder.ast.abstractnode import AbstractNode as A
__all__=['IfNode']
class IfNode(A):
	def __init__(A,condition,body,orelse):A.condition=condition;A.body=body;A.orelse=orelse