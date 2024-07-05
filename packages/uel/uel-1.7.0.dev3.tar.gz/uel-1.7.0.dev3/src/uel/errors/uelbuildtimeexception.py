from uel.builder.position import Position
from uel.errors.uelexception import UELException as A
__all__=['UELBuildtimeException']
class UELBuildtimeException(A):
	def __init__(A,error_message,pos):B=pos;super().__init__(error_message);A.line=B.ln;A.file=B.fn;A.column=B.col
	def __str__(A):B=super().__str__();C=f"{A.file}, {A.line}:{A.column}\n";return C+B