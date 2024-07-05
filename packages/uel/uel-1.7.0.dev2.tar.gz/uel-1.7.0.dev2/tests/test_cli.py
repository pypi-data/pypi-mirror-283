import unittest,contextlib as A,io
from uel.cli import main
from uel.ueargparse import UEBuildBytecodesTask
from uel.omit.testing.mixins import UELRunMixin as B
import unittest
class C(unittest.TestCase,B):
	def test_cli(B):
		with A.redirect_stdout(io.StringIO()):main()