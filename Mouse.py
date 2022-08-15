import cv2
import mediapipe as mp
from HandTracker import HandDetection
import pyautogui as pag
import numpy as np

# Screen size check
# print(pag.size())

handDetector = HandDetection()

camera = cv2.VideoCapture(0)
# mirroredWebcam = cv2.flip(camera,0)


stablizier  = 3
locationX, locationY, oldX, oldY = 0,0,0,0
boxFrame = 50


while True:
    success, img = camera.read()
    landMarkList, img = handDetector.landMarkList(img)

    if landMarkList:
        fingers, img = handDetector.fingersUp(img, landMarkList, False)

        if(fingers == [0,1,0,0,0]):
            x1, y1 = landMarkList[8][1:]

            oldX = locationX
            oldY = locationY

            #Convert to correct range [640x480 >> 1920x1080]
            convertedX = np.interp(x1, (boxFrame,640 - boxFrame), (0,1920))
            convertedY = np.interp(y1, (boxFrame,480 - boxFrame), (0,1080))

            #Smoothen out the movement of the mouse
            locationX = oldX + (convertedX- oldX)/stablizier
            locationY = oldY + (convertedY - oldY)/stablizier

            #Make a box around it
            cv2.rectangle(img, (boxFrame,boxFrame), (540, 380), (255,170,170), 3)

            pag.moveTo(convertedX,convertedY)


    cv2.imshow("Webcam Feed",img)
    key = cv2.waitKey(1)
    
    if (key == 27):
        break

camera.release()
cv2.destroyAllWindows()