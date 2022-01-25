from email.message import Message
from tkinter import N
import cv2
import mediapipe as mp
import time
from google.protobuf.json_format import MessageToDict

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

            for id, lm in enumerate(handLms.landmark): # for every landmark id
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                index_x = 0
                index_y = 0
                thumb_x = 0
                thumb_y = 0

                if id == 4:
                    cv2.putText(img, "RThumb: " + str(cx) + ", " + str(cy), (10,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 3)
                    thumb_x = cx;
                    thumb_y = cy;

                if id == 8:
                    cv2.putText(img, "RIndex: " + str(cx) + ", " + str(cy), (10,150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 3)
                    index_x = cx;
                    index_y = cy;

                if ((((thumb_x - index_x) ** 2) + ((thumb_y - index_y) ** 2)) ** (1/2) < 3000000):
                    #cv2.putText(img, "touch", (10,250), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 3)
                    print('touch')

            mpDraw.draw_landmarks(img, handLms)

    
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, "FPS:" + str(int(fps)), (10,450), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 3)


    # img_flip = cv2.flip(img, 1)
    cv2.imshow("Image", img)
    cv2.waitKey(1)







# the code below is the implementation for two hands 
# while True:
#     success, img = cap.read()  
#     imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#     results = hands.process(imgRGB)
#     #print(results.multi_hand_landmarks)
    
#     if results.multi_hand_landmarks: # if a hand is in the frame
#         for handLms in results.multi_hand_landmarks: # for every hand in the frame

#             hand_label = 'none'
#             for idx, hand_handedness in enumerate(results.multi_handedness): # find what hands are in the frame
#                 handedness_dict = MessageToDict(hand_handedness)
#                 hand_label_opp = handedness_dict['classification'][0]['label']
#                 hand_label = 'Left' if hand_label_opp == 'Right' else 'Right'
                
#                 if hand_label == 'Left':
#                     cv2.putText(img, "Left", (10,300), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 3)
#                     for id, lm in enumerate(handLms.landmark): # for every landmark id
#                         h, w, c = img.shape
#                         cx, cy = int(lm.x*w), int(lm.y*h)

#                         if id == 4:
#                             cv2.putText(img, "LThumb: " + str(cx) + ", " + str(cy), (10,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 3)

#                         if id == 8:
#                             cv2.putText(img, "LIndex: " + str(cx) + ", " + str(cy), (10,150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 3)



#                 if hand_label == 'Right':
#                     cv2.putText(img, "Right", (100,300), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 3)
#                     for id, lm in enumerate(handLms.landmark): # for every landmark id
#                         h, w, c = img.shape
#                         cx, cy = int(lm.x*w), int(lm.y*h)
#                         if id == 4:
#                             cv2.putText(img, "RThumb: " + str(cx) + ", " + str(cy), (10,250), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 3)

#                         if id == 8:
#                             cv2.putText(img, "RIndex: " + str(cx) + ", " + str(cy), (10,350), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 3)



#             mpDraw.draw_landmarks(img, handLms)

    
#     cTime = time.time()
#     fps = 1 / (cTime - pTime)
#     pTime = cTime

#     cv2.putText(img, "FPS:" + str(int(fps)), (10,450), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 3)


#     # img_flip = cv2.flip(img, 1)
#     cv2.imshow("Image", img)
#     cv2.waitKey(1)