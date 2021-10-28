import cv2
import mediapipe as mp
import time
import bibiHand as htm
import math

import threading
import pygame
import random
import socket, threading
import json

SERVER = "192.168.15.61"
PORT = 8080
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))
red=(150,50,50)
blue=(20,70,150)
green=(50,150,50)
yellow=(100,100,20)
roxo=(150,50,150)
grey=(80,80,80)






def distanciaEU(x,y,x1,y1):
	return math.sqrt(((x-x1)**2)+((y-y1)**2))
def capVideo():
	try:
		pTime = 0
		cTime = 0
		cap = cv2.VideoCapture(0)
		detector = htm.handDetector()
		dedos=[8,12,16,20]
		larg=2
		desenho=[]
		while True:
			success, img = cap.read()
			img=cv2.flip(img,1)
			img = detector.findHands(img, draw=True )
			lmList = detector.findPosition(img, draw=True,)
			dedo=[]
			if len(lmList) != 0:
				dedo=[]
				#cv2.circle(img, (lmList[4][1], lmList[4][2]), 10, (150, 150, 250), cv2.FILLED)
				if(lmList[4][1]<lmList[4-2][1]):
						dedo.append(1)
				else:
					dedo.append(0)
				for i in dedos:
					#cv2.circle(img, (lmList[i][1], lmList[i][2]), 10, (150, 150, 250), cv2.FILLED)
					if(lmList[i][2]<lmList[i-2][2]):
						dedo.append(1)
					else:
						dedo.append(0)
				##print(dedo.count(1))

			cTime = time.time()
			fps = 1 / (cTime - pTime)
			pTime = cTime
			cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,           (255, 0, 255), 3)		
			lista=[4,6,8,10,12]
			posi=[]
			for i in desenho:
				cv2.circle(img, (i[0],i[1]) , i[2], (150, 250, 250), cv2.FILLED)

			try:
				##print(dedo.count(1))
				tabuleiro.attPlay(tabuleiro.id,lmList[0][1],lmList[0][2],dedo.count(1))
			except:
				pass
			
			cv2.imshow("Image", img)
			cv2.waitKey(1)
			k = cv2.waitKey(30) & 0xff
			if k == 27:
				break
	except:
		
		while True:
			time.sleep(0.000000000000005)
			tabuleiro.attPlay(tabuleiro.id,tabuleiro.jogadores[0].x,0,2)
			tabuleiro.jogadores[0].x+=0.02


class Tabuleiro:
	def __init__(self):
		self.id=0
		self.jogadores=[]
		#self.addPlay(self.id)
		#self.addPlay(50)

	def attPlay(self,id,x,y,acao):
		for i in self.jogadores:
			if(i.id==id):
				i.attPosi(x,y,acao)
				break
	def addPlay(self,id,x=0,y=0,acao=0):
		self.jogadores.append(Play(self,x,y,id,acao))
	def render(self,screen):
		for i in self.jogadores:
			i.render(screen)
	
class Play:
	def __init__(self,tab,x,y,id,acao):
		self.tab=tab
		self.x=x
		self.y=y
		self.id=id
		self.acao=acao
		self.tam=20
	def attPosi(self,x,y,acao):
		self.x=x
		self.y=y
		self.acao=acao
	def render(self,screen):
		if(self.id==self.tab.id):
			
			if(self.acao==0):
				self.cor=grey
			elif(self.acao==1):
				self.cor=roxo
			elif(self.acao==2):
				self.cor=yellow
			elif(self.acao==3):
				self.cor=green
			elif(self.acao==4):
				self.cor=blue
			elif(self.acao==5):
				self.cor=red
		else:
			cont=100
			if(self.acao==0):
				self.cor=(grey[0]+cont,grey[1]+cont,grey[2]+cont)
			elif(self.acao==1):
				self.cor=(roxo[0]+cont,roxo[1]+cont,roxo[2]+cont)
			elif(self.acao==2):
				self.cor=(yellow[0]+cont,yellow[1]+cont,yellow[2]+cont)
			elif(self.acao==3):
				self.cor=(green[0]+cont,green[1]+cont,green[2]+cont)
			elif(self.acao==4):
				self.cor=(blue[0]+cont,blue[1]+cont,blue[2]+cont)
			elif(self.acao==5):
				self.cor=(red[0]+cont,red[1]+cont,red[2]+cont)
		pygame.draw.rect(screen,self.cor, pygame.Rect(self.x, self.y, self.tam-1, self.tam-1))
	   
tabuleiro=Tabuleiro()


class SendThread(threading.Thread):
	def __init__(self,clientsocket):
		threading.Thread.__init__(self)
		self.csocket = clientsocket
	
	

	def run(self):
		
		msg = ''
		while True:
			try:
				time.sleep(0.00000000005)
				self.csocket.send((json.dumps({'id':'att','identifica':tabuleiro.id,'x':tabuleiro.jogadores[0].x,'y':tabuleiro.jogadores[0].y,'acao':tabuleiro.jogadores[0].acao})).encode("UTF-8"))
			except:
		  		pass
		  #out_data = input()
		  #self.comandos(out_data)
		  #self.csocket.sendall(bytes(out_data,'UTF-8'))

class recebeThread(threading.Thread):
	def __init__(self,clientsocket):
		threading.Thread.__init__(self)
		self.csocket = clientsocket
	
	def comandos(self,cm):
		

		a=cm.decode().split('}')
		#print(a)
		try:
			for i in range(len(a)-1):
				cmd=json.loads(a[i]+'}')
				#print(cmd)
				
				if(cmd['id']=='id'):
					tabuleiro.id = cmd['num']
					tabuleiro.addPlay(tabuleiro.id)
				elif(cmd['id']=='inimigo'):
					#print("dd")
					tabuleiro.addPlay(cmd['identifica'],x=cmd['x'],y=cmd['y'],acao=cmd['acao'])
					#self.csocket.sendall((json.dumps({'id':2})).encode("UTF-8"))
				elif(cmd['id']=='att'):
					
					tabuleiro.attPlay(cmd['identifica'],x=cmd['x'],y=cmd['y'],acao=cmd['acao'])
					#self.csocket.sendall((json.dumps({'id':2})).encode("UTF-8"))
		except:
			pass
	def run(self):
	  
		#self.csocket.send(bytes("Hi, This is from Server..",'utf-8'))
		msg = ''
		while True:
			
			in_data =  self.csocket.recv(1024)
			self.comandos(in_data)
			##print("From Server :" ,in_data.decode())
send=SendThread(client)
send.start()

get=recebeThread(client)
get.start()
def jogo():

	pygame.init()
	screen = pygame.display.set_mode((600, 600))
	done = False
	clock = pygame.time.Clock()
	
	while not done:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True
			if (event.type == pygame.MOUSEBUTTONUP):
				# get a list of all sprites that are under the mouse cursor
				##print(int(pos[0]/100),int(pos[1]/100))
				#tabuleiro.tab[int(pos[1]/100)][int(pos[0]/100)].cor=yellow
				pos = pygame.mouse.get_pos()
			   
				#juiz.verificaGanhou(tabuleiro.tab)
				##print(tabuleiro.tab)

		pygame.display.flip()
		clock.tick(60)
		screen.fill((30,30,30))   

		tabuleiro.render(screen)


video = threading.Thread(target=capVideo, args=())
jojo = threading.Thread(target=jogo, args=())

video.start()

jojo.start()