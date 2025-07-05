import cv2
import back
import pytesseract
import d
thres = 0.6 # Threshold to detect object

the_things = ['person',
'bicycle',
'car',
'motorcycle',
'airplane',
'bus',
'train',
'truck',
'boat',
'traffic light',
'fire hydrant',
'street sign',
'stop sign',
'cat',
'dog',
'horse',
'sheep',
'cow',
'elephant',
'bear',
'zebra',
'giraffe']
the_signs = []
cap = cv2.VideoCapture(0)
left_sign = cv2.CascadeClassifier('modules\\left-sign.xml')
right_sign = cv2.CascadeClassifier('modules\\right-sign.xml')
classNames= []
classFile = 'coco.names'
with open(classFile,'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')

configPath = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
weightsPath = 'frozen_inference_graph.pb'

net = cv2.dnn_DetectionModel(weightsPath,configPath)
net.setInputSize(320,320)
net.setInputScale(1.0/ 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

def detecttrafficsigns(img):

    if len(the_signs) >2:
            cv2.putText(img,the_signs[len(the_signs)-1]+'<'+the_signs[len(the_signs)-2],( 30,400),
            cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
    imgg = img
    #img = cv2.imread('jjj.jpg')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    right_sign_scaled = right_sign.detectMultiScale(gray, 1.3, 5)
    left_sign_scaled = left_sign.detectMultiScale(gray, 1.3, 5)
    #Import only if not previously imported
    for (x, y, w, h) in right_sign_scaled:
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
        the_signs.append('right_sign')
    for (x, y, w, h) in left_sign_scaled:
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
        the_signs.append('left_sign')
    #stop_sign_scaled = _sign.detectMultiScale(gray, 1.3, 5)
    
    classIds, confs, bbox = net.detect(imgg,confThreshold=thres)
    

    if len(classIds) != 0:
        
        for classId, confidence,box in zip(classIds.flatten(),confs.flatten(),bbox):
            print(box)
            if classNames[classId-1] not in the_things:
                continue
            y , x = box[1] , box[0]
            ye,xe = box[2] , box[3]
            shap = img[y:ye+x, x:xe+y]
            print(ye-y ,  xe-x)
            #h , w = box[2]-box[0], box[3]-box[1]
           
             
            cv2.rectangle(img,box,color=(0,255,0),thickness=2)
            if shap.shape[1] != 0 and  shap.shape[0] != 0 :
                cv2.imshow(f'ae', img[y:ye+x, x:xe+y])
                # cv2.imshow(f'ae.jpg', img[y:y+h, x:x+w+50])
            cv2.putText(img,classNames[classId-1].upper(),(box[0]+10,box[1]+30),
            cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
            cv2.putText(img,str(round(confidence*100,2)),(box[0]+200,box[1]+30),
            cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
            if classNames[classId-1] =='stop sign':
                if back.majdp(imgg):
                    the_signs.append('stop')
                else:
                    pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
                    majf = pytesseract.image_to_string(img[y:ye+x, x:xe+y])
                    the_signs.append(majf)
            elif classNames[classId-1] =='traffic light':
                if d.jb(img):
                    the_signs.append('red traffic light')
    return img  , the_signs               




    
