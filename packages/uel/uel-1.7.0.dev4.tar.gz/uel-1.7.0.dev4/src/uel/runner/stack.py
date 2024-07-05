from queue import LifoQueue
from typing import Generic as A,TypeVar as B,Iterator
C=B('T')
__all__=['Stack']
class Stack(A[C]):
	def __init__(A):A._queue=[]
	@property
	def top(self):return self._queue.pop()
	def push(A,value):A._queue.append(value)
	def is_empty(A):return not A._queue