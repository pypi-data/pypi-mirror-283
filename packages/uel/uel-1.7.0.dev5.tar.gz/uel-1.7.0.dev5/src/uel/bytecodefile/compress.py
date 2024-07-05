import pickle as A
from uel.bytecodefile._compress import _compress as B,_decompress as C
__all__=['compress','decompress']
def compress(obj):return B(A.dumps(obj))
def decompress(bytes_):return A.loads(C(bytes_))