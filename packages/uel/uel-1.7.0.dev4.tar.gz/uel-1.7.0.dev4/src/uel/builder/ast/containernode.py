from typing import Any,List
from uel.builder.ast.abstractnode import AbstractNode as A
__all__=['ContainerNode']
class ContainerNode(A):
	def __init__(A,childrens=None):A.childrens=childrens or[]
	def push(A,node):A.childrens.append(node)