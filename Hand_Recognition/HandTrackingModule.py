import cv2
import mediapipe as mp
import time


class HandDetector(object):
    def __init__(self, mode=False, maxHands=3, complexity=1, detectionCon=0.9, trackingCon=0.9):
        self.mode = mode
        self.maxHands = maxHands
        self.complexity = complexity
        self.detectionCon = detectionCon
        self.trackingCon = trackingCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.complexity, self.detectionCon, self.trackingCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHand(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLm in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLm, self.mpHands.HAND_CONNECTIONS)

        return img

    def findPosition(self, img, handNo = 0, draw = True):
        lmList = []
        if self.results.multi_hand_landmarks:
            hand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(hand.landmark):
                h, w, c = img.shape
                cx, cy = int(w * lm.x), int(h * lm.y)
                lmList.append([id, cx, cy])

        return lmList


def main():
    cTime = 0
    pTime = 0
    cap = cv2.VideoCapture(0)
    detector = HandDetector()
    while True:
        success, img = cap.read()
        img = detector.findHand(img)
        lmList = detector.findPosition(img)

        if len(lmList) != 0:
            print(lmList[4])

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 255), 3)

        cv2.imshow('Camera', img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
