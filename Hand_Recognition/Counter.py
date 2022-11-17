import numpy as np
import os
import mediapipe as mp
import time
import cv2
import HandTrackingModule as htm


hCam, wCam = 720, 720
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0
detector = htm.HandDetector()
tipIds = [8,12,16,20]

while True:
    success, img = cap.read()
    detector.findHand(img)
    lmList = detector.findPosition(img)

    if len(lmList) != 0:
        fingers = []

        if lmList[4][1] > lmList[5][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        for id in tipIds:
            if lmList[id][2] < lmList[id-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        totalFingers = fingers.count(1)

        cv2.rectangle(img, (10,200), (150, 400), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, f'{totalFingers}', (35, 350),cv2.FONT_HERSHEY_COMPLEX, 5, (0, 0, 255), 10)



    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, f'{int(fps)}', (10, 50), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 255), 3)
    cv2.imshow("cam1", img)
    cv2.waitKey(1)
