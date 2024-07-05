from typing import Any
from uel.builder.ast.abstractnode import AbstractNode as A
__all__=['SequenceNode']
class SequenceNode(A):
	def __init__(A,values):A.values=values;A.val=A