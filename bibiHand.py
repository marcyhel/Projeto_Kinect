
import cv2
import mediapipe as mp
import time
 
 
class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
 
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,
                                        self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
 
    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # print(results.multi_hand_landmarks)
 
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,
                                               self.mpHands.HAND_CONNECTIONS)
        return img
 
    def findPosition(self, img, handNo=0, draw=True):
 
        lmList = []
        if self.results.multi_hand_landmarks:
            for myHand in self.results.multi_hand_landmarks:
                for id, lm in enumerate(myHand.landmark):
                    # print(id, lm)
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    # print(id, cx, cy)
                    lmList.append([id, cx, cy])
                    if draw:
                        #cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
                        if (id == 4 or id== 8 or id== 12 or id== 16 or id== 20):
                            cv2.circle(img, (cx, cy), 7, (150, 50, 50), cv2.FILLED)
                        elif (id == 3 or id== 7 or id== 11 or id== 15 or id== 19):
                            cv2.circle(img, (cx, cy), 7, (150, 150, 50), cv2.FILLED)
                        elif (id == 2 or id== 6 or id== 10 or id== 14 or id== 18):
                            cv2.circle(img, (cx, cy), 7, (150, 120, 120), cv2.FILLED)
                        elif (id == 1 or id== 5 or id== 9 or id== 13 or id== 17):
                            cv2.circle(img, (cx, cy), 7, (100, 100, 100), cv2.FILLED)
                        elif (id == 0):
                            cv2.circle(img, (cx, cy), 7, (50, 50, 50), cv2.FILLED)
 
        return lmList
 
 
def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(1)
    detector = handDetector()
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img)
        if len(lmList) != 0:
            print(lmList[4])
 
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
 
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 255), 3)
 
        cv2.imshow("Image", img)
        cv2.waitKey(1)
 
 
if __name__ == "__main__":
    main()