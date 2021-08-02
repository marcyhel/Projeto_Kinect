import cv2
import mediapipe as mp
import time
 
cap = cv2.VideoCapture(0)
 
mpHands = mp.solutions.pose
hands = mpHands.Pose()
mpDraw = mp.solutions.drawing_utils
 
pTime = 0
cTime = 0
 
while True:
    success, img = cap.read()
    img=cv2.flip(img,1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    # print(results.multi_hand_landmarks)
    #print(results.pose_landmarks)
    '''
    if results.pose_landmarks:
        
        for id, lm in enumerate(results.pose_landmarks):
            # print(id, lm)
            h, w, c = img.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            #print(id, cx, cy)
            if (id == 4 or id== 8 or id== 12 or id== 16 or id== 20):
                cv2.circle(img, (cx, cy), 7, (150, 50, 50), cv2.FILLED)
            elif (id == 3 or id== 7 or id== 11 or id== 15 or id== 19):
                cv2.circle(img, (cx, cy), 7, (150, 150, 50), cv2.FILLED)
            elif (id == 2 or id== 6 or id== 10 or id== 14 or id== 18):
                cv2.circle(img, (cx, cy), 7, (150, 150, 150), cv2.FILLED)
            elif (id == 1 or id== 5 or id== 9 or id== 13 or id== 17):
                cv2.circle(img, (cx, cy), 7, (100, 100, 100), cv2.FILLED)
        '''
    mpDraw.draw_landmarks(img, results.pose_landmarks, mpHands.POSE_CONNECTIONS)
 
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
 
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 255), 3)
 
    cv2.imshow("Image", img)
    cv2.waitKey(1)