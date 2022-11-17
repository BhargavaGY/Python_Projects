import math
import cv2
import mediapipe as mp
import numpy as np
import time
import HandTrackingModule as htm
import pycaw
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))


#volume.GetMute()
#volume.GetMasterVolumeLevel()
volR = volume.GetVolumeRange()

minVol = volR[0]
maxVol = volR[1]

capw = 1080
caph = 720
cap = cv2.VideoCapture(0)
cap.set(3,capw)
cap.set(4, caph)
detector = htm.HandDetector()
pTime = 0

while True:
    success, img = cap.read()
    detector.findHand(img)
    lmList = detector.findPosition(img)

    if len(lmList) != 0:
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1+x2)//2, (y1+y2)//2
        cv2.circle(img, (x1,y1), 12, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2,y2), 12, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (cx,cy), 12, (255, 0, 255), cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(255, 0, 255), 3)

        length = math.hypot(x2-x1, y2-y1)

        if length < 30:
            cv2.circle(img, (cx, cy), 12, (0, 255, 0), cv2.FILLED)

        vol = np.interp(length, [30, 200], [minVol, maxVol])
        volume.SetMasterVolumeLevel(vol, None)
        volB = np.interp(vol, [minVol, maxVol], [465, 225])
        cv2.rectangle(img, (50, 220), (85, 470),(0, 255, 0))
        cv2.rectangle(img, (55, int(volB)), (80, 465), (0, 255, 0), cv2.FILLED)
        per = np.interp(vol, [minVol, maxVol], [0, 100])
        cv2.putText(img, f'{int(per)}%', (40,500), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, f'{int(fps)}', (10,50), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 255), 3)

    cv2.imshow("cam1", img)
    cv2.waitKey(1)
