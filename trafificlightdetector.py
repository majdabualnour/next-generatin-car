#Import only if not previously imported
import cv2
cascade = cv2.CascadeClassifier('modules\\traffic_light.xml')
cap = cv2.VideoCapture(1)
if cap.isOpened() == False:
    print("Error in opening video stream or file")
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret:
        grayimage = cv2.cvtColor(frame , cv2.COLOR_BGR2GRAY)
        coor = cascade.detectMultiScale(grayimage, 1.2, 8)
        for (x, y, w, h) in coor:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
        # Display the resulting frame
        cv2.imshow('Frame',frame)
        # Press esc to exit
        if cv2.waitKey(20) & 0xFF == 27:
            break
    else:
        break
cap.release()
cv2.destroyAllWindows()
