B=None
import typing as C
from queue import Queue
from uel.runner.stack import Stack
__all__=['Frame']
class Frame:
	def __init__(A,stack,idx,bytecodes,prev_frame=B,filename='<unknown>',variables=B,gqueue=B):
		A.stack=stack;A.idx=idx;A.bytecodes=bytecodes;A.filename=filename;A.prev_frame=prev_frame;A.variables=variables
		if A.variables is B:A.variables={}
		A.gqueue=Queue[C.Any]()