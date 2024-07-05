B=print
import os,sys
from typing import List
from uel.ueargparse import UEArgParser as C,UETask as D
__all__=['Main']
class Main:
	@staticmethod
	def main(argv):
		E=C(argv[1:])
		try:F=D(E);F.run()
		except KeyboardInterrupt:B('KeyboardInterrupt');os._exit(0)
		except Exception as A:B('UELRuntimeError(PythonError):',file=sys.stderr);sys.excepthook(type(A),A,A.__traceback__)