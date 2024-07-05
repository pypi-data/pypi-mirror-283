B=print
import atexit
from http.server import HTTPServer as D
from uel.colors import RED,RESET
import os.path
from http.server import BaseHTTPRequestHandler as E
from uel.constants import DIRNAME as F
__all__=['start']
G=False
A=F
if G:A='./src/uel'
C=os.path.join(A,'web')
class H(E):
	def do_GET(B):
		E='index.html';A=B.path[1:]
		if A==''or os.path.isdir(A):A=os.path.join(A,E)
		A=os.path.join(C,A)
		if not os.path.exists(A):A=os.path.join(C,E)
		with open(A,'rb')as F:D=F.read();G=len(D);B.send_response(200);B.send_header('Cache-Control','max-age=0');B.send_header('Content-Length',str(G));B.end_headers();B.wfile.write(D)
def start(address):
	A,C=address;B(f"Please open http://{A if A!='0.0.0.0'else'127.0.0.1'}:{C}/");E=D((A,int(C)),H)
	try:E.serve_forever()
	finally:B(f"{RED}The server was closed{RESET}");exit()