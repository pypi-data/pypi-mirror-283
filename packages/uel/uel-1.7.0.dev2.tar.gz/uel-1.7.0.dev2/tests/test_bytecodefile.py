from uel.ueargparse import UEBuildBytecodesTask as C,UERunBytecodesTask as D
import unittest as B,os as A,io,contextlib as E
class F(B.TestCase):
	def test_bytecodefile(F):
		B='data/test_bytecodes/main'
		with E.redirect_stdout(io.StringIO()):C([A.path.join(A.path.dirname(__file__),'data/test_bytecodes/main.uel'),A.path.join(A.path.dirname(__file__),B)]).run();D([A.path.join(A.path.dirname(__file__),B)]).run()