import cv2

# Stop Sign Cascade Classifier xml
stop_sign = cv2.CascadeClassifier('modules\cascade_stop_sign.xml')
def majdp(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    stop_sign_scaled = stop_sign.detectMultiScale(gray, 1.3, 5)
    #print(stop_sign_scaled)
    # Detect the stop sign, x,y = origin points, w = width, h = height
    for (x, y, w, h) in stop_sign_scaled:
        return True
    return False

#Import only if not previously imported
