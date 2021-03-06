 #!/usr/bin/python3
from socket import*
import ast, math
import struct
import time
import http.client
import operator as op

server= 'atclab.esi.uclm.es'
direc="atclab.esi.uclm.es"
udport=14374
puertoudp=2000
operators = {ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul,
             ast.Div: op.floordiv, ast.Pow: op.pow, ast.BitXor: op.xor,
             ast.USub: op.neg}

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

And finally using: http://stackoverflow.com/questions/2371436/evaluating-a-mathematical-expression-in-a-string i get the code .
"""
def evaluateMathExpr(node):
	if isinstance(node, ast.Num): # <number>
        	return node.n
	elif isinstance(node, ast.BinOp): # <left> <operator> <right>
        	return operators[type(node.op)](evaluateMathExpr(node.left), evaluateMathExpr(node.right))
	elif isinstance(node, ast.UnaryOp): # <operator> <operand> e.g., -1
        	return operators[type(node.op)](evaluateMathExpr(node.operand))

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
				result=str(evaluateMathExpr(ast.parse(operation, mode='eval').body))
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
				result=str(evaluateMathExpr(ast.parse(operation, mode='eval').body))
				solution='('+result+')'
				solution=solution.encode()
				TCPs.sendto(solution,(server,TCport))
			else:
				break

	print(operation)
	TCPs.close()
		
	fourthmessage=operation.split("\n")[0]
	
	return fourthmessage
	
"""
		I take the code from :
		https://docs.python.org/3.1/library/http.client.html
		
"""
def step4(direec):
	porttt="/"+str(direec)
	conn = http.client.HTTPConnection(direc,5000)
	conn.request("GET",porttt)
	r1 = conn.getresponse()
	data1 = r1.read()
	lectura = str (data1.decode())
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
	stp5=step4(stp4)
	stp6=step5(stp5)
	print(stp6)


if __name__ == "__main__":
	main()




