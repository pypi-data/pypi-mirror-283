__all__=['AttributeOnly']
class B(Exception):0
class AttributeOnly:
	def __init__(A,obj,names):A.__obj=obj;A.__names=names
	def __getattr__(A,name):
		if not name in A.__names:raise B(str(A.__names))
		return A.__obj.__getattribute__(name)
if __name__=='__main__':
	from dataclasses import dataclass as A
	@A
	class C:a:int
	D=AttributeOnly(C(1),['a']);print(D.a)