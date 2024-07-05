import typing as t
from copy import deepcopy
from typing import TypeAlias
from uel.builder.position import Position
from uel.tools.func.share.runtime_type_check import runtime_type_check
BT=int
BT_ADD=1
BT_MINUS=2
BT_MUL=3
BT_DIV=4
BT_STORE_NAME=5
BT_POP=6
BT_LOAD_CONST=7
BT_QPUT=8
BT_QTOP=9
BT_PUT=10
BT_JUMP=11
BT_IS=12
BT_CALL=13
BT_RETURN=14
BT_POP_JUMP_IF_FALSE=15
BT_MAKE_SEQUENCE=16
BT_SEQUENCE_APPEND=17
__all__=[*filter(lambda x:x.startswith('BT'),locals().keys()),'BytecodeInfo']
class BytecodeInfo:
	def __init__(self,bytecode_type,value,pos):assert pos>0,'the arg 1 must be great 0';self.bytecode_type=bytecode_type;self.value=value;self.pos=pos
	def copy(self):return deepcopy(self)
	def where(self,start,end):
		if abs(start)==start and abs(end)==end:return self.pos>=start and self.pos<=end
		raise ValueError('The arg 1 and arg 2 must be great 0')
	@staticmethod
	def pretty_with_bytecode_type(bt):mapping={BT_ADD:'add',BT_MINUS:'minus',BT_MUL:'multiply',BT_DIV:'division',BT_STORE_NAME:'store name',BT_POP:'pop',BT_LOAD_CONST:'load const',BT_QPUT:'queue put',BT_QTOP:'queue top',BT_PUT:'put',BT_JUMP:'jump to',BT_IS:'is',BT_CALL:'call',BT_RETURN:'return',BT_POP_JUMP_IF_FALSE:'pop jump if false',BT_MAKE_SEQUENCE:'make sequence',BT_SEQUENCE_APPEND:'sequence append'};mapping.setdefault('unknown');return mapping[bt].upper().replace(' ','_'),bt
	def __repr__(self):
		bt=self.pretty_with_bytecode_type(self.bytecode_type)[0]
		if self.value is not None:return f"Info({bt}, {self.value}, index={self.pos})"
		else:return f"Info({bt}, index={self.pos})"