from email.message import Message
from tkinter import N
import cv2
import mediapipe as mp
import time
from google.protobuf.json_format import MessageToDict

# for i in range (3000000000000000):
#     time.sleep(0.5)
#     print(i)

cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands() # keep default confidence levels
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0

while True:
    success, img = cap.read()  
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    #print(results.multi_hand_landmarks)
    
    if results.multi_hand_landmarks: # if a hand is in the frame
        for handLms in results.multi_hand_landmarks: # for every hand in the frame

            hand_label = 'none'
            for idx, hand_handedness in enumerate(results.multi_handedness): # find what hands are in the frame
                handedness_dict = MessageToDict(hand_handedness)
                hand_label_opp = handedness_dict['classification'][0]['label']
                hand_label = 'Left' if hand_label_opp == 'Right' else 'Right'

                for id, lm in enumerate(handLms.landmark): # for every landmark id
                    h, w, c = img.shape
                    cx, cy = int(lm.x*w), int(lm.y*h)

                    if id == 4:
                        cv2.putText(img, "RThumb: " + str(cx) + ", " + str(cy), (10,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 3)
                    if id == 8:
                        cv2.putText(img, "RIndex: " + str(cx) + ", " + str(cy), (10,100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 3)
                    if id == 12:
                        cv2.putText(img, "RMiddle: " + str(cx) + ", " + str(cy), (10,150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 3)
                    if id == 16:
                        cv2.putText(img, "RRing: " + str(cx) + ", " + str(cy), (10,200), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 3)
                    if id == 20:
                        cv2.putText(img, "RPinky: " + str(cx) + ", " + str(cy), (10,250), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 3)
                    
                    cv2.putText(img, hand_label, (10,300), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 3)

            mpDraw.draw_landmarks(img, handLms)

    
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, "FPS:" + str(int(fps)), (10,450), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 3)


    # img_flip = cv2.flip(img, 1)
    cv2.imshow("Image", img)
    cv2.waitKey(1)