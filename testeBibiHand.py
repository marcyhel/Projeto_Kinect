import cv2
import mediapipe as mp
import time
import bibiHand as htm
import math
 
pTime = 0
cTime = 0
cap = cv2.VideoCapture(0)
detector = htm.handDetector()

dedos=[8,12,16,20]
larg=2
desenho=[]
def distanciaEU(x,y,x1,y1):
    return math.sqrt(((x-x1)**2)+((y-y1)**2))
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

        #print(dedo.count(1))

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
 
    #cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
     #           (255, 0, 255), 3)
    
    lista=[4,6,8,10,12]
    posi=[]

    for i in desenho:
        cv2.circle(img, (i[0],i[1]) , i[2], (150, 250, 250), cv2.FILLED)
    if(dedo.count(1)>0):
        posi=[[lmList[0][1]-100,lmList[0][2]-200],
        [lmList[0][1]-55,lmList[0][2]-225],
        [lmList[0][1],lmList[0][2]-240],
        [lmList[0][1]+55,lmList[0][2]-225],
        [lmList[0][1]+100,lmList[0][2]-200]]
    

    if(dedo.count(1)==5):
        
        aux=2000

        for i in range(len(posi)):
            
            if(distanciaEU(lmList[12][1],lmList[12][2],posi[i][0],posi[i][1])<aux):
                aux=distanciaEU(lmList[12][1],lmList[12][2],posi[i][0],posi[i][1])

                larg=i

        cv2.circle(img, (posi[larg][0],posi[larg][1]), lista[larg]+5, (250, 150, 50), cv2.FILLED)

        cv2.circle(img, (posi[0][0],posi[0][1]), lista[0], (50, 50, 50), cv2.FILLED)
        cv2.circle(img, (posi[1][0],posi[1][1]), lista[1], (50, 50, 50), cv2.FILLED)
        cv2.circle(img, (posi[2][0],posi[2][1]), lista[2], (50, 50, 50), cv2.FILLED)
        cv2.circle(img, (posi[3][0],posi[3][1]), lista[3], (50, 50, 50), cv2.FILLED)
        cv2.circle(img, (posi[4][0],posi[4][1]), lista[4], (50, 50, 50), cv2.FILLED)


        #print(larg)
    #print(larg)
    if(dedo.count(1)==3 and (distanciaEU(lmList[8][1],lmList[8][2],lmList[12][1],lmList[12][2])) <45):

        print(lista,larg,lista[larg])
        cv2.circle(img, (int((lmList[8][1]+lmList[12][1])/2),int((lmList[8][2]+lmList[12][2])/2) ), lista[larg], (150, 150, 250), cv2.FILLED)
        desenho.append([int((lmList[8][1]+lmList[12][1])/2),int((lmList[8][2]+lmList[12][2])/2),lista[larg]])

        #print(int((lmList[8][1]+lmList[12][1])/2),lmList[8][1],lmList[12][1])


    cv2.imshow("Image", img)
    cv2.waitKey(1)