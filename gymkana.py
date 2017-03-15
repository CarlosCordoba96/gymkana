#!/usr/bin/python3
from socket import*
import ast, math
import operator
import struct
import time
import http.client
import os,_thread
import socketserver
import urllib.request

server= 'atclab.esi.uclm.es'
direc="http://atclab.esi.uclm.es:5000/"
udport=14374
puertoudp=2000


#Code author: David Villa
def cksum(data):
    def sum16(data):
        "sum all the the 16-bit words in data"
        if len(data) % 2:
            data += b'\0'
 
        return sum(struct.unpack("!%sH" % (len(data) // 2), data))
    retval = sum16(data)                       # sum
    retval = sum16(struct.pack('!L', retval))  # one's complement sum
    retval = (retval & 0xFFFF) ^ 0xFFFF        # one's complement
    return retval

"""In order to know how to eval operations using ast : http://eli.thegreenplace.net/2009/11/28/python-internals-working-with-python-asts, https://docs.python.org/3/library/ast.html.
In order to see the type of variable it is i use isinstance that i know how to use from_ http://www.ehowenespanol.com/revisar-tipos-variables-python-como_219393/ , https://svn.python.org/projects/python/tags/r32/Lib/ast.py.
.op => https://docs.python.org/3/library/ast.html col_offset and http://stackoverflow.com/questions/6009663/python-ast-how-to-get-the-children-of-a-node.
https://docs.python.org/3/library/ast.html  col_offset
"""
def evaluateExpr(msg):
	#Base case, it is a number
	if(isinstance(msg,ast.Num)):
		ope=msg.n 
		return ope

	elif(isinstance(msg,ast.BinOp)):
		r=evaluateExpr(msg.right)	
		l= evaluateExpr(msg.left)

		if (isinstance(msg.op, ast.Add)):# .op => https://docs.python.org/3/library/ast.html col_offset and http://stackoverflow.com/questions/6009663/python-ast-how-to-get-the-children-of-a-node
			ope=l+r
			return ope

		if (isinstance(msg.op, ast.Sub)):
			ope=l-r
			return ope

		if (isinstance(msg.op, ast.Mult)):
			ope=l*r
			return ope

		if (isinstance(msg.op, ast.Div)):
			ope=l//r
			return ope


def step1():
	sock = socket(AF_INET, SOCK_STREAM)
	sock.connect((server, 2000))
	firstmessage = (sock.recv(1024).decode())
	print(firstmessage)
	sock.close()
	Idfirstmess=firstmessage.split('\n')[0]
	return Idfirstmess

def step2(data):
	UDP = socket(AF_INET, SOCK_DGRAM)
	UDP.bind(('',udport))
	UDP.sendto(data.encode(),(server,puertoudp))
	msgudp=UDP.recv(1024)
	msudp=msgudp.decode()
	UDP.close()
	portmsg3=msudp.split('\n')[0]
	print(msudp)
	return portmsg3

def step3(port3):
	counter=0
	TCport=int(port3)
	TCPs=socket(AF_INET,SOCK_STREAM)
	TCPs.connect((server,TCport))
	while(1):
		operation=TCPs.recv(1024)
		operation=operation.decode()
		operation=operation.replace('[','(')
		operation=operation.replace(']',')')
		operation=operation.replace('{','(')
		operation=operation.replace('}',')')
		print(operation)
	
		for i in range (0, len(operation)):
			if operation[i] == "(":
				counter = counter +1
			elif operation[i] ==")":
				counter = counter -1

	#cont==0 complete operation
		if(counter==0):
			if operation[0]=="(":
				operation=operation.replace(' ','')
				result=str(evaluateExpr(ast.parse(operation, mode='eval').body))# http://stackoverflow.com/questions/6009663/python-ast-how-to-get-the-children-of-a-node, https://greentreesnakes.readthedocs.io/en/latest/tofrom.html
				solution='('+result+')'
				solution=solution.encode()
				TCPs.sendto(solution,(server,TCport))
			else:
				break
		elif(counter!=0):
			operation2=TCPs.recv(2048)
			operation2=operation2.decode()
			operation= operation + operation2
			operation=operation.replace('[','(')
			operation=operation.replace(']',')')
			operation=operation.replace('{','(')
			operation=operation.replace('}',')')
			if operation[0]=="(":
				operation=operation.replace(' ','')
				result=str(evaluateExpr(ast.parse(operation, mode='eval').body))
				solution='('+result+')'
				solution=solution.encode()
				TCPs.sendto(solution,(server,TCport))
			else:
				break

	print(operation)
	TCPs.close()
		
	fourthmessage=operation.split("\n")[0]
	
	return fourthmessage
		
def step4(direec):
	servee=direc+direec
	f=urllib.request.urlopen(servee)
	rd=f.read()
	f.close()	
	lectura = str (rd.decode())
	print (lectura)
	cad3=lectura.split("\n")[0]
	
	return cad3
	
def step5(msgstep5):
	raw=socket(AF_INET,SOCK_RAW,getprotobyname("icmp"))
 
	header=struct.pack('!bbHhh',8,0,0,3669,5) #1110  y el 1 numero que yo quiera
	timestamp=struct.pack('!d',time.time())

	checksum=cksum(header+timestamp+msgstep5.encode())

	packett=struct.pack('!bbHhh',8,0,checksum,3669,5)+timestamp+msgstep5.encode()
	raw.sendto(packett,('atclab.esi.uclm.es',80))
	raw.recv(2048)
	identificador=(raw.recv(2048)[36:]).decode()
	
	print(identificador)

	iden=identificador.split("\n")[0]
	return iden




def main():
	ID = step1()
	msg2= ID + " "+ str(udport)
	stp3=step2(msg2)
	stp4=step3(stp3)
	print ("HOlaaaa que tal")
	stp5=step4(stp4)
	stp6=step5(stp5)
	print(stp6)


if __name__ == "__main__":
	main()




#CLASS FROM JAVA
""" private static int  evaluateExpr
                             (BinTreeInterface<NodeElement<Integer,String>> t,
                             NodeBinTree<NodeElement<Integer, String>> node) {
    int res = 0;
    String op;
    int l, r;
    if (t.isExternal(node)) {//It is a number
      res = Integer.parseInt(node.getElement().getValue());
    } else {//It is not a number, an operation
     op = node.getElement().getValue();
      r = evaluateExpr(t, t.getRight(node));
      l = evaluateExpr(t, t.getLeft(node));
        if(op.equals("+")){
          res = l + r;
          }
        if(op.equals("-")){
          res = l - r;
          }
        if(op.equals("*")){
          res = l * r;
          }
        if(op.equals("/")){
          res = l / r;
      }
    }
    return res;
  }
"""





























