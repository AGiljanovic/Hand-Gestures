import cv2
from HandTracker import HandDetection
import pyautogui as pag

#Sourcing from https://pyautogui.readthedocs.io/en/latest/mouse.html#mouse-scrolling
handDetector = HandDetection()

#Using web cam for hand detection
#If the camera is not being recognized, change the 0 to a 1
webcam = cv2.VideoCapture(0)

#Read webcam frames
while True:
    #Frame grab
    success, img = webcam.read() 

    #Grab landMarkList
    landMarkList, img = handDetector.landMarkList(img)

    #if a hand is being detected
    if landMarkList:
        fingers, img = handDetector.fingersUp(img, landMarkList)

        #fingres closed
        if(fingers == [0,0,0,0,0]):
            pag.scroll(-50)
        #palm open
        elif(fingers == [1,1,1,1,1]):
            pag.scroll(50)

        #Checker for coord in case
        # print(fingers)

    cv2.imshow("Webcam Feed",img)
    key = cv2.waitKey(1)
    
    if (key == 27):
        break

webcam.release()
cv2.destroyAllWindows()
