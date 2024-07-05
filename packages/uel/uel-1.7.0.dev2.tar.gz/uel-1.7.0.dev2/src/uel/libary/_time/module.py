import time
from uel.libary.helpers import make_exports as A
__all__=['uel_export_time','bytecodes']
def uel_export_time(frame):from uel.objects import uel_new_object as A;return A('number',time.time())
bytecodes=A({'time':uel_export_time})