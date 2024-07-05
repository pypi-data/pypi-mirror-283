import contextlib as B,io
from uel.ueargparse import _UERunTaskDesc as C
__all__=['UELRunMixin']
class UELRunMixin:
	def do_uel_test(D,code,rr,fn='<test-case>'):
		A=io.StringIO()
		with B.redirect_stdout(A):C.run_uel(None,fn,code,False)
		D.assertEqual(str(rr),A.getvalue())