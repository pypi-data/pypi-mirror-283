A=str
import contextlib,math,unittest as B
from uel.omit.testing.mixins import UELRunMixin as C
class D(B.TestCase,C):
	def test_run(A):A.do_uel_test('put 5','5')
	def test_import(B):B.do_uel_test('import "math"\npush 1\ncall sin\nput TOP\n',A(math.sin(1)))
	def test_function(B):B.do_uel_test('function a;\n  put 5\nend\n\ncall a\n',A(5));B.do_uel_test('\nfunction a b;\n    function c;\n        put b\n    end\n    call c\nend\npush 1\ncall a\n',A(1))
	def test_calculator(B):B.do_uel_test('put 1 + 2 * 2',A(6));B.do_uel_test('a = 2\nb=3\nput a + b',A(5))
	def test_import2(A):A.do_uel_test('import "data/test_module/a.uel"\n','1',__file__)
	def test_if_statement(A):A.do_uel_test('if 1 put 5 end',5)