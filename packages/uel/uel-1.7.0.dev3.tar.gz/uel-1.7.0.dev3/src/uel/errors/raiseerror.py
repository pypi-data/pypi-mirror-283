from uel.builder.position import Position
from uel.errors.throwexception import ThrowException as A
__all__=['RaiseError']
class RaiseError:
	def __init__(B,et,em,pos):A.throw(et(em,pos))