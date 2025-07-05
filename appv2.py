import cv2
from matplotlib import pyplot as plt
import numpy as np
import imutils
import pytesseract
cap = cv2.VideoCapture(0)


#car_cascade = cv2.CascadeClassifier('cars.xml')
def majd(img):
    #img = cv2.imread('image4.jpg')
    #img = cv2.imread(img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #cars = car_cascade.detectMultiScale(gray, 1.1, 9)
    #print(cars)
    #if cars != ():
        
    bfilter = cv2.bilateralFilter(gray, 11, 17, 17) #Noise reduction
    edged = cv2.Canny(bfilter, 30, 200) #Edge detection

    keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(keypoints)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
    location = None
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 10, True)
        if len(approx) == 4:
            location = approx
            break

    
    print(str(type(location)))
    if str(type(location)) == "<class 'numpy.ndarray'>":
        print('p')
        mask = np.zeros(gray.shape, np.uint8)
        
        cv2.drawContours(mask, [location], 0,255, -1)
        cv2.bitwise_and(img, img, mask=mask)


        (x,y) = np.where(mask==255)
        (x1, y1) = (np.min(x), np.min(y))
        (x2, y2) = (np.max(x), np.max(y))
        cropped_image = gray[x1:x2, y1:y2-5]

        pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
        majf = pytesseract.image_to_boxes(cropped_image).split('\n')

            
        
        text=pytesseract.image_to_string(cropped_image )
        #reader = easyocr.Reader(['en'])
        #result = reader.readtext(cropped_image)
        
        print(text)
        text = text[:len(text)-1]
        font = cv2.FONT_HERSHEY_SIMPLEX
        he,we,=cropped_image.shape
        
        for m in majf:
            
            faf=m.split(' ')
            if faf[0]=='':break
            elif faf[1]=='0':
                text = text[1:len(text)]
                continue
            
        # x,y,w,h = int(faf[1]),int(faf[2]),int(faf[3]),int(faf[4])
            cv2.rectangle(cropped_image,(int(faf[1]),he-int(faf[2])),(int(faf[3]),he-int(faf[4])),(0,0,255),2)
        res = cv2.putText(img, text=text, org=(approx[0][0][0]-30, approx[1][0][1]-30), fontFace=font, fontScale=1, color=(0,255,0), thickness=2, lineType=cv2.LINE_AA)
        res = cv2.rectangle(img, tuple(approx[0][0]), tuple(approx[2][0]), (0,255,0),3)
        #cv2.imshow('majdwd',cropped_image)
        #else:res = img
        return res
    else:
        return img
    ##
   # if n == ord('q'):break


if cap.isOpened() == False:
    print("Error in opening video stream or file")
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret:
        cv2.flip(frame,1)
        # Display the resulting frame
        cv2.imshow('Frame',majd(frame))
        # Press esc to exit
        if cv2.waitKey(20) & 0xFF == ord('q'):
    
            break
    else:
        break
cap.release()
cv2.destroyAllWindows()
