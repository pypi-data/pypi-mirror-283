import sys
from string import ascii_letters as C
from unicodedata import lookup
__all__=['is_start','is_identifier_center_char_or_end_char']
def is_start(char):
	B=True;A=char
	if sys.version_info.major<3:raise EnvironmentError("Python 3's string is UTF-8,while Python 2's is not.To ensure accuracy,Python 2 reports an error directly.")
	if A in C:return B
	elif'一'<=A<='鿿':return B
	elif'_'==A:return B
	elif'$'==A:return B
	return False
def is_identifier_center_char_or_end_char(char):return is_start(char)or char.isdigit()