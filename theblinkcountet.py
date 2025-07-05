

from time import sleep
import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
import sendingusingthewifi as wifi

import sendmassage
detector = FaceMeshDetector(maxFaces=1)
#plotY = LivePlot(640, 360, [20, 50], invert=True)

idList = [22, 23, 24, 26, 110, 157, 158, 159, 160, 161, 130, 243]
ratioList = []

blinkCounter = 0
counter = 0
coloral = (255, 0, 255)

theblinlcounterg = 0


def fun(cap):
    
    success, img = cap.read()
    img, faces = detector.findFaceMesh(img, draw=False)

    if faces:
        
        global coloral,counter,blinkCounter , theblinlcounterg 
        face = faces[0]
        for id in idList:
            cv2.circle(img, face[id], 5,coloral, cv2.FILLED)

        leftUp = face[159]
        leftDown = face[23]
        leftLeft = face[130]
        leftRight = face[243]
        lenghtVer, _ = detector.findDistance(leftUp, leftDown)
        lenghtHor, _ = detector.findDistance(leftLeft, leftRight)

        cv2.line(img, leftUp, leftDown, (0, 200, 0), 3)
        cv2.line(img, leftLeft, leftRight, (0, 200, 0), 3)

        ratio = int((lenghtVer / lenghtHor) * 100)
        ratioList.append(ratio)
        if len(ratioList) > 3:
            ratioList.pop(0)
        ratioAvg = sum(ratioList) / len(ratioList)
        
        if ratioAvg > 35 and counter != 0:
            blinkCounter = 0

            
        while ratioAvg < 35 and counter == 0:
            blinkCounter += 1
            coloral = (0,200,0)
            counter = 1
            
                
        
        if counter != 0:
            counter += 1
            if counter > 10:
                counter = 0
                coloral = (255,0, 255)
        
        cvzone.putTextRect(img, f'sleep for: {blinkCounter}', (50, 100),
                           colorR=coloral)

        #imgPlot = plotY.update(ratioAvg, color)
        img = cv2.resize(img, (640, 360))
        cv2.imshow('blink_counter', img)
        #imgStack = cvzone.stackImages([img, imgPlot], 2, 1)
       
       

        if blinkCounter ==14:
            
            wifi.send('sleep')
            theblinlcounterg =1
            sleep(3)
        elif blinkCounter ==20 and theblinlcounterg == 1:
            
            wifi.send('stop')
            print('sending.....')
            sendmassage.sendmassage()
        elif blinkCounter ==0:
            theblinlcounterg = 0
            
           
        #imgStack = cvzone.stackImages([img, img], 2, 1)

