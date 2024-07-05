import typing as A
from uel.builder.ast.abstractnode import AbstractNode
__all__=['SingleNode']
class SingleNode:
	def __init__(A,val,type=None):A.val=val;A.type=type
	def __repr__(A):return'%s<%s>(val=%s)'%(A.__class__.__name__,A.type,repr(A.val))