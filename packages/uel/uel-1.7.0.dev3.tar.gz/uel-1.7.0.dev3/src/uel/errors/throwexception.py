from os import _exit
from sys import stderr as A
from uel.errors.uelbaseexception import UELBaseException
B=1
__all__=['ThrowException']
class ThrowException:
	@staticmethod
	def throw(e):A.write(str(e));A.write('\n');A.flush();_exit(1)