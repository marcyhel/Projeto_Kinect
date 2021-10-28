import socket, threading
import json
import time
import pika
clientes=[]

class Cliente:
	def __init__(self,sock,id):
		self.sock=sock
		self.id=id
		self.sock.send((json.dumps({'id':'id','num':self.id})).encode("UTF-8"))
		time.sleep(0.000002)
		self.x=0
		self.y=0
		self.acao=0
		self.att=False
		#self.atualiza()
	def atualiza(self):
		for i in clientes:
			time.sleep(0.003)
			if(i!=self):
				time.sleep(0.02)
				self.sock.send((json.dumps({'id':'inimigo','identifica':i.id,'x':i.x,'y':i.y,'acao':i.acao})).encode("UTF-8"))
		time.sleep(0.030)
		self.att=True

class ClientThread(threading.Thread):
	def __init__(self,clientAddress,clientsocket):
		threading.Thread.__init__(self)
		self.csocket = clientsocket
		print ("Nova conexao: ", clientAddress)
	def comando(self,cmd):
		##print(cmd)
		try:
			cmd=json.loads(cmd)
			if(cmd['id']=='att'):
				self.csocket.x=cmd['x']
				self.csocket.y=cmd['y']
				self.csocket.acao=cmd['acao']
				for i in clientes:
					time.sleep(0.0000004)
					if(i.sock!=self.csocket.sock and self.csocket.att and i.att):
						i.sock.send((json.dumps({'id':'att','identifica':self.csocket.id,'x':self.csocket.x,'y':self.csocket.y,'acao':self.csocket.acao})).encode("UTF-8"))
		except:
			pass
	def run(self):
		#print ("Conectado com : ", clientAddress)
		#self.csocket.send(bytes("Hi, This is from Server..",'utf-8'))
		msg = ''
		while True:
			data = self.csocket.sock.recv(1024)

			#msg = data.decode('UTF-8')
			self.comando(data)
			
			#for i in clientes:
			#	i.sock.send(bytes(msg,'UTF-8'))
		
LOCALHOST = "192.168.15.61"
PORT = 8080
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((LOCALHOST, PORT))
#print("Server started")
#print("Waiting for client request..")
contId=0
while True:
	server.listen(1)
	clientsock, clientAddress = server.accept()

	clientes.append(Cliente(clientsock,contId))
	clientes[len(clientes)-1].atualiza()
	contId+=1
	for i in clientes:
		if(i!=clientes[len(clientes)-1]):
			
			i.sock.send((json.dumps({'id':'inimigo','identifica':clientes[len(clientes)-1].id,'x':clientes[len(clientes)-1].x,'y':clientes[len(clientes)-1].y,'acao':clientes[len(clientes)-1].acao})).encode("UTF-8"))
	newthread = ClientThread(clientAddress, clientes[len(clientes)-1])
	newthread.start()