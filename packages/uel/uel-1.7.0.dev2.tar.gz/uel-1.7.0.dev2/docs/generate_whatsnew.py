B=print
C='v'
from git import Repo,Tag
import os as A,time as D,semantic_version as E,functools as F
def G(tag):F='.md';E='whatsnew';B=tag;G=open(A.path.join(A.path.dirname(__file__),E,B.name.strip(C)+F)).read()if A.path.exists(A.path.join(A.path.dirname(__file__),E,B.name.strip(C)+F))else B.name.strip(C)+f" have no description'";return f"### {B.name} <small>{D.strftime('%B %d, %Y %P',D.localtime(B.commit.authored_date))}</small> {{#{B.name}}}\n- [Download](https://github.com/user-11150/puel/releases/tag/{B.name})\n\n{G}\n"
def H():
	H=Repo(A.path.dirname(A.path.dirname(__file__)));I=sorted(H.tags,key=F.cmp_to_key(lambda x,y:E.compare(x.name.strip(C),y.name.strip(C))),reverse=True)
	with open(A.path.join(A.path.dirname(__file__),'whatsnew.md'),'wt')as D:B("# What's new",file=D);B('## UEL',file=D);B('\n'.join(map(G,I)),file=D)
H()