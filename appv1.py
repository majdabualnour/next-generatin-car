from time import sleep
import cv2
import numpy as np
import anything 
import pygame
import main
import sendingusingthewifi as wifi
from theblinkcountet  import fun
import theblinkcountet  
pygame.init()

sur_obj=pygame.display.set_mode((10,10))
pygame.display.set_caption("Keyboard_Input")

def thresholding(img):
    imgHsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    lowerWhite = np.array([80,0,0])
    upperWhite = np.array([255,160,255])
    maskWhite = cv2.inRange(imgHsv,lowerWhite,upperWhite)
    return maskWhite
 
def warpImg(img,points,w,h,inv = False):
    pts1 = np.float32(points)
    pts2 = np.float32([[0,0],[w,0],[0,h],[w,h]])
    if inv:
        matrix = cv2.getPerspectiveTransform(pts2, pts1)
    else:
        matrix = cv2.getPerspectiveTransform(pts1,pts2)
    imgWarp = cv2.warpPerspective(img,matrix,(w,h))
    return imgWarp
 
def nothing(a):
    pass
 
def initializeTrackbars(intialTracbarVals,wT=480, hT=240):
    cv2.namedWindow("Trackbars")
    cv2.resizeWindow("Trackbars", 360, 240)
    cv2.createTrackbar("Width Top", "Trackbars", intialTracbarVals[0],wT//2, nothing)
    cv2.createTrackbar("Height Top", "Trackbars", intialTracbarVals[1], hT, nothing)
    cv2.createTrackbar("Width Bottom", "Trackbars", intialTracbarVals[2],wT//2, nothing)
    cv2.createTrackbar("Height Bottom", "Trackbars", intialTracbarVals[3], hT, nothing)
 
def valTrackbars(wT=480, hT=240):
    widthTop = cv2.getTrackbarPos("Width Top", "Trackbars")
    heightTop = cv2.getTrackbarPos("Height Top", "Trackbars")
    widthBottom = cv2.getTrackbarPos("Width Bottom", "Trackbars")
    heightBottom = cv2.getTrackbarPos("Height Bottom", "Trackbars")
    points = np.float32([(widthTop, heightTop), (wT-widthTop, heightTop),
                      (widthBottom , heightBottom ), (wT-widthBottom, heightBottom)])
    return points
 
def drawPoints(img,points):
    for x in range(4):
        cv2.circle(img,(int(points[x][0]),int(points[x][1])),15,(0,0,255),cv2.FILLED)
    return img
 
def getHistogram(img,minPer=0.1,display= False,region=1):
 
    if region ==1:
        histValues = np.sum(img, axis=0)
    else:
        histValues = np.sum(img[img.shape[0]//region:,:], axis=0)
 
    #print(histValues)
    maxValue = np.max(histValues)
    minValue = minPer*maxValue
 
    indexArray = np.where(histValues >= minValue)
    basePoint = int(np.average(indexArray))
    #print(basePoint)
 
    if display:
        imgHist = np.zeros((img.shape[0],img.shape[1],3),np.uint8)
        for x,intensity in enumerate(histValues):
            cv2.line(imgHist,(x,img.shape[0]),(x,img.shape[0]-intensity//255//region),(255,0,255),1)
            cv2.circle(imgHist,(basePoint,img.shape[0]),20,(0,255,255),cv2.FILLED)
        return basePoint,imgHist
 
    return basePoint
 
def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver
curveList = []
avgVal=10
def nothing(a):
    pass
def initializeTrackbars(intialTracbarVals,wT=480, hT=240):
    cv2.namedWindow("Trackbars")
    cv2.resizeWindow("Trackbars", 360, 240)
    cv2.createTrackbar("Width Top", "Trackbars", intialTracbarVals[0],wT//2, nothing)
    cv2.createTrackbar("Height Top", "Trackbars", intialTracbarVals[1], hT, nothing)
    cv2.createTrackbar("Width Bottom", "Trackbars", intialTracbarVals[2],wT//2, nothing)
    cv2.createTrackbar("Height Bottom", "Trackbars", intialTracbarVals[3], hT, nothing)
def getLaneCurve(img,display=2):
    thedirctionguid= []
 
    imgCopy = img.copy()
    imgResult = img.copy()
    #### STEP 1
    imgThres = thresholding(img)
 
    #### STEP 2
    hT, wT, c = img.shape
    points = valTrackbars()
    imgWarp = warpImg(imgThres,points,wT,hT)
    imgWarpPoints = drawPoints(imgCopy,points)
 
    #### STEP 3
    middlePoint,imgHist = getHistogram(imgWarp,display=True,minPer=0.5,region=4)
    curveAveragePoint, imgHist =getHistogram(imgWarp, display=True, minPer=0.9)
    curveRaw = curveAveragePoint - middlePoint
 
    #### SETP 4
    curveList.append(curveRaw)
    if len(curveList)>avgVal:
        curveList.pop(0)
    curve = int(sum(curveList)/len(curveList))
 
    #### STEP 5
    if display != 0:

        imgInvWarp = warpImg(imgWarp, points, wT, hT, inv=True)
        imgInvWarp = cv2.cvtColor(imgInvWarp, cv2.COLOR_GRAY2BGR)
        imgInvWarp[0:hT // 3, 0:wT] = 0, 0, 0
        imgLaneColor = np.zeros_like(img)
        imgLaneColor[:] = 0, 255, 0
        imgLaneColor = cv2.bitwise_and(imgInvWarp, imgLaneColor)
        imgResult = cv2.addWeighted(imgResult, 1, imgLaneColor, 1, 0)
        midY = 450
        # cv2.putText(imgResult, str(curve), (wT // 2 - 80, 85), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 255), 3)
        curve = int(str(curve))
        if 30 >=curve >= 20:
            cv2.putText(imgResult, 'right', (wT // 2 - 80, 85), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 255), 3)
            thedirctionguid.append('right')

        elif -30<= curve <= -20:
            cv2.putText(imgResult, 'left', (wT // 2 - 80, 85), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 255), 3)
            thedirctionguid.append('left')
        if curve >= 31:
            cv2.putText(imgResult, 'hright', (wT // 2 - 80, 85), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 255), 3)
            thedirctionguid.append('hright')
        elif   curve <= -31:
            cv2.putText(imgResult, 'hleft', (wT // 2 - 80, 85), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 255), 3)
            thedirctionguid.append('hleft')
        elif  20 > curve > -20:
            cv2.putText(imgResult, 'straight', (wT // 2 - 80, 85), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 255), 3)
            thedirctionguid.append('straight')

        cv2.line(imgResult, (wT // 2, midY), (wT // 2 + (curve * 3), midY), (255, 0, 255), 5)
        cv2.line(imgResult, ((wT // 2 + (curve * 3)), midY - 25), (wT // 2 + (curve * 3), midY + 25), (0, 255, 0), 5)
        for x in range(-30, 30):
            w = wT // 20
            cv2.line(imgResult, (w * x + int(curve // 50), midY - 10),
                     (w * x + int(curve // 50), midY + 10), (0, 0, 255), 2)
        #fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);
        #cv2.putText(imgResult, 'FPS ' + str(int(fps)), (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (230, 50, 50), 3);
    if display == 2:
        imgStacked = stackImages(0.7, ([img, imgWarpPoints, imgWarp],
                                             [imgHist, imgLaneColor, imgResult]))
        cv2.imshow('ImageStack', imgStacked)
    elif display == 1:
        cv2.imshow('Resutlt', imgResult)
 
    #### NORMALIZATION
    curve = curve/100
    if curve>1: curve ==1
    if curve<-1:curve == -1
 
    return curve , thedirctionguid
 

if __name__ == '__main__':
    ktemp = None
    
    counting_the_pressing = False
    cap = cv2.VideoCapture('vid1.mp4')
    cape = cv2.VideoCapture(1)
    intialTrackBarVals = [102, 80, 20, 214 ]
    initializeTrackbars(intialTrackBarVals)
    frameCounter = 0
    left = False
    right = False 
    up = False
    while True:
        

        
        frameCounter += 1
        if cap.get(cv2.CAP_PROP_FRAME_COUNT) == frameCounter:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            frameCounter = 0

        success, img = cap.read()
        img = cv2.resize(img,(480,240))
        curve , k = getLaneCurve(img,display=1)

        img , n = anything.majd(img)
        
        key_input = pygame.key.get_pressed()   
        if key_input[pygame.K_n]:
            if main.run_alexa() == 'save':
                counting_the_pressing = True
            elif main.run_alexa() == 'self':
                counting_the_pressing = False
            elif main.run_alexa() == 'os':
                counting_the_pressing = True
                up = True
            elif main.run_alexa() == 'ol':
                counting_the_pressing = True
                right = True
            elif main.run_alexa() == 'ofl':
                counting_the_pressing = True
                left = True
        if key_input[pygame.K_UP]:  
            up = True  
        else:up = False
        if  key_input[pygame.K_LEFT]:
            left = True 
        else:left = False
        if  key_input[pygame.K_RIGHT]:
            right = True  
        else:right = False       
        if  key_input[pygame.K_e] and not counting_the_pressing:
            counting_the_pressing = True
            print('save')
            sleep(1)      
        elif  key_input[pygame.K_e] and  counting_the_pressing:
            counting_the_pressing = False
            print('self')
            sleep(1)  
        
        if  counting_the_pressing:
            if left:
                if 'hleft' not in k and 'left' not in k  :
                    if  len(k) != 0:
                        k.pop()
                        print('you cannet turn into any direction excepet left')

            elif up:
                        
                if len(n) != 0 and n[len(n)-1] in anything.the_things:
                    n.pop()
                    print('you connet do that follow the instructures')
                if 'straight' not in k and len(k) != 0:
                    k.pop()
                    print('you cannet turn into any direction excpet straight ')
        
            elif right:
                if 'hright' not in k and 'right' not in k  :
                    if  len(k) != 0:
                        k.pop()
                        print('you cannet turn into any direction excepet right')
        

        if len(n) != 0 :
            k.pop()
        
        if theblinkcountet.theblinlcounterg == 1:
            wifi.send('stop')   

                
        elif len(n) != 0 :
            wifi.send('tone') 
        elif len(k) == 0 :
            wifi.send('stop')
        #cv2.imshow('Vid',img)                

        if len(n) != 0 :
            if n[len(n)-1]  == 'right_sign'    :
                
                wifi.send('rightsi') 
                if k[len(k)-1] == 'hright' or k[len(k)-1] == 'right':
                    pass
                elif k[len(k)-1] == 'hleft' or k[len(k)-1] == 'left':
                    k.pop()
            elif n[len(n)-1]  == 'left_sign':
                wifi.send('leftsi')
                if k[len(k)-1] == 'hright' or k[len(k)-1] == 'right':
                    k.pop()
                elif k[len(k)-1] == 'hleft' or k[len(k)-1] == 'left':
                    pass
        if len(k) != 0 and k[len(k)-1] != ktemp:
            wifi.send(k[len(k)-1]) 
            ktemp =  k[len(k)-1]          
        if counting_the_pressing:
            fun(cape)
        majd =cv2.waitKey(1)
        if majd == ord('d'):
            break