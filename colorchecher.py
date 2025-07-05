# Python program to identify
#color in images

# Importing the libraries OpenCV and numpy
import cv2
import numpy as np


def jb(img):
    b = 0

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Defining lower and upper bound HSV values
    lower = np.array([-10, 100, 100])
    upper = np.array([10, 255, 255])

    # Defining mask for detecting color
    mask = cv2.inRange(hsv, lower, upper)
    mask =cv2.resize(mask, (50,50))
    for m in mask:
        for v in m:
            if v==255:
                b+=1
            if b == 10:
                return True
    return False
      

# Display Image and Mask


# Make python sleep for unlimited time
cv2.waitKey(0)
