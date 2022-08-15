import cv2
import mediapipe as mp
import numpy as np
from HandTracker import HandDetection

#Sourcing from AndreMiras pycaw https://github.com/AndreMiras/pycaw
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volumeRange = volume.GetVolumeRange()
minVolume = volumeRange[0]
maxVolume = volumeRange[1]

handDetector = HandDetection()

#Webcam for hand detection, if not being recognized > change the 0 to a 1
webcam = cv2.VideoCapture(0)

#Read webcam frames
while True:
    #Frame grab
    success, img = webcam.read() 

    #Grab landMarkList
    landMarkList, img = handDetector.landMarkList(img)

    #if a hand is being detected
    if landMarkList:
        fingers, img = handDetector.fingersUp(img, landMarkList, False)

        #If all fingers are up
        if (fingers == [1,1,1,1,1]):
            
            #Look at the distance between pointer and thumb [8,4]
            length, img = handDetector.distanceCalculator(4,8, img, landMarkList, True)  
            print(length)

            #Take the length of the fingers' distance, find it in interval
            # and map it to min/max volume ranges
            calculatedVol = np.interp(length, (10, 160), (minVolume, maxVolume))

            #Translate finger length to a percentage and write it down
            volumePercentage = np.interp(length, (10, 160), (0, 100))
            volumeBar = np.interp(length, (10, 160), (260, 110)) 
            cv2.putText(img, str(int(volumePercentage)) + "%", (50,100), cv2.FONT_HERSHEY_DUPLEX, 1, (255,170,170), 2)

            #Volume bar
            cv2.rectangle(img, (50,110), (80, 260), (255,170,170), 3)
            cv2.rectangle(img, (50, int(volumeBar)), (80, 260), (255,170,170), cv2.FILLED)

            volume.SetMasterVolumeLevel(calculatedVol, None)

    #Display webcam feeds
    cv2.imshow("Webcam Feed",img)
    key = cv2.waitKey(1)
    
    if (key == 27):
        break
    
webcam.release()
cv2.destroyAllWindows()