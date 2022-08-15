import cv2
import mediapipe as mp
import math
import numpy as np

#Source from https://google.github.io/mediapipe/solutions/hands.html

mpHands =  mp.solutions.hands
hands = mpHands.Hands()
drawTools = mp.solutions.drawing_utils

class HandDetection():
    def landMarkList(self, img, draw = True):
        landMarkList = []
        #Conversion of BGR to RGB
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # read it correctly 
        results = hands.process(imgRGB)

        if (results.multi_hand_landmarks):
            for handLandMarks in results.multi_hand_landmarks:
                #Turn every landmark dictionary into a value
                for id, lm in enumerate(handLandMarks.landmark):
                    height,width,channel = img.shape #480x640x3
                    coordx, coordy = int(lm.x*width), int(lm.y*height)

                    landMarkList.append([id, coordx, coordy])
                
                if draw:
                    drawTools.draw_landmarks(img, handLandMarks, mpHands.HAND_CONNECTIONS)

        return landMarkList, img

    def fingersUp (self, img, landMarkList, draw=True):
        fingers = []
        fingerTipIds = [8,12,16,20]
        count = 0
        if(landMarkList[4][1] < landMarkList[3][1]): #tip of thumb [4] below last thumb knuckle [3]
            fingers.append(0)
        else:
            fingers.append(1)
            count+=1
            
        #Add count if finger tip goes below last knuckle
        for id in fingerTipIds:
            if(landMarkList[id][2] < landMarkList[id - 2][2]):
                fingers.append(1)
                count+=1
            else:
                fingers.append(0)

        # Display on screen how many fingers are up
        # ref: https://www.geeksforgeeks.org/python-opencv-cv2-puttext-method/
        if draw:
            cv2.putText(img, str(count), (100,250), cv2.FONT_HERSHEY_PLAIN, 3, (255,255,255), 2)
        return fingers, img

    def distanceCalculator(self, p1, p2, img, landMarkList, draw=False):
        #id, x coord, y coord
        x1, y1 = landMarkList[p1][1:]
        x2, y2 = landMarkList[p2][1:]

        # Take the difference of x2 and x1 and difference of y2 and y2
        # and calculate the hypotenuse, and store in var length
        length = math.hypot(x2-x1, y2-y1)

        #Make a line between pointer and thumb
        #Sourcing from https://www.geeksforgeeks.org/python-opencv-cv2-line-method/
        if(draw):
            cv2.line(img, (x1,y1), (x2,y2), (255,170,170), 3)
        return length, img
