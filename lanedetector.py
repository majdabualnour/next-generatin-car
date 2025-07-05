import cv2
import numpy as np
thestart = 0




def canny(image):
    gray = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray,(5,5),0)
    canny = cv2.Canny(blur, 50, 150)
    return canny

def region_of_interest(image):
    height = image.shape[0]
    triangle = np.array([[
        (200, height),
        (550, 250),
        (1100, height), ]], np.int32)
    mask = np.zeros_like(image)
    cv2.fillPoly(mask,triangle,255)
    masked_image = cv2.bitwise_and(image,mask)
    return masked_image

def average_slope_intercept(image,lines):
    left_fit = []
    right_fit = []
    for line in lines:
        x1, y1, x2, y2 = line.reshape(4)
        parameters = np.polyfit((x1, x2), (y1, y2), 1)
        slope = parameters[0]
        intercept = parameters[1]
        if slope < 0:
            left_fit.append((slope,intercept))
        else:
            right_fit.append((slope,intercept))
    left_fit_average = np.average(left_fit,axis = 0)
    right_fit_average = np.average(right_fit,axis = 0)
    left_line = make_coordinates(image,left_fit_average)
    right_line = make_coordinates(image,right_fit_average)
    return np.array([left_line,right_line])

def make_coordinates(image,line_parameters):
    slope,intercept = line_parameters
    y1 = image.shape[0]
    y2 = int(y1*(3/5))
    x1 = int((y1 - intercept)/slope)
    x2 = int((y2 - intercept)/slope)
    return np.array([x1,y1,x2,y2])

def display_lines(image, lines):

    listd = []
    line_image = np.zeros_like(image)
    if lines is not None:
        #for line in lines:
        for line in lines:
            x1, y1, x2, y2 = line.reshape(4)
            listd.append(x1)
            #for x1, y1, x2, y2 in x:
            cv2.line(line_image,(x1, y1), (x2, y2), (0, 255 , 255), 10)

   
        o =  (max(listd) - min(listd))//2 +  min(listd)
        #cv2.circle(line_image,(o,100),110,(0,0,0),5)
        listd.clear()
    return line_image , o



# خطوط على الصورة
# image = cv2.imread('R.jpg')
# lane_image = np.copy(image)
# canny_image = canny(lane_image)
# cropped_image = region_of_interest(canny_image)
# lines = cv2.HoughLinesP(cropped_image, 2, np.pi/180, 10, np.array([]), minLineLength = 4, maxLineGap = 5)
# averaged_lines = average_slope_intercept(lane_image,lines)
# line_image , o = display_lines(lane_image, averaged_lines)
# print(o)
# if thestart == 0 :
#     the_fist_capturing = o
#     thestart +=1
# if  o +20< the_fist_capturing:
#     print('go_left')
# elif o - 20< the_fist_capturing< o + 20:print('forword')
# elif o -20> the_fist_capturing:print('go_lift')

# combo_image = cv2.addWeighted(lane_image, 0.8, line_image, 1, 1)
# h, w,c = combo_image.shape  
# print(the_fist_capturing)
# cv2.line(combo_image,(the_fist_capturing,h-200), (the_fist_capturing,h-200 +100),(0,255,0),5)
# cv2.circle(combo_image,(o,h-200 +50),10,(0,0,255),20)

# cv2.imshow("result", combo_image)
# cv2.waitKey(0)

# خطوط سوداء خلفية
# image = cv2.imread('a.jpg')
# lane_image = np.copy(image)
# canny_image = canny(lane_image)
# cropped_image = region_of_interest(canny_image)
# lines = cv2.HoughLinesP(cropped_image, 2, np.pi/180, 10, np.array([]), minLineLength = 30, maxLineGap = 7)
# #averaged_lines = average_slope_intercept(lane_image,lines)
# line_image = display_lines(lane_image, lines)
# combo_image = cv2.addWeighted(lane_image, 0.8, line_image, 1, 1)
# cv2.imshow("result", combo_image)
# cv2.waitKey(0)


# # لأخذ فيديو

cap = cv2.VideoCapture("test2.mp4")
while(cap.isOpened()):
    _, frame = cap.read()
    lane_image = frame.copy()
    canny_image = canny(frame)
    cropped_canny = region_of_interest(canny_image)
    lines = cv2.HoughLinesP(cropped_canny, 2, np.pi/180, 100, np.array([]), minLineLength=40,maxLineGap=5)
    averaged_lines = average_slope_intercept(frame, lines)
    line_image , o = display_lines(frame, averaged_lines)
    combo_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1)
    print(o)
    if thestart == 0 :
        the_fist_capturing = o
        thestart +=1
    if  o +20< the_fist_capturing:
        jn =' go right'
    elif o - 20< the_fist_capturing< o + 20: jn =' forword'
    elif o -20> the_fist_capturing:jn =' go left'

    combo_image = cv2.addWeighted(lane_image, 0.8, line_image, 1, 1)
    h, w,c = combo_image.shape  
    print(the_fist_capturing)
    cv2.line(combo_image,(the_fist_capturing,h-200), (the_fist_capturing,h-200 +100),(0,255,0),5)
    cv2.circle(combo_image,(o,h-200 +50),10,(0,0,255),20)
    cv2.putText(combo_image,jn,(the_fist_capturing-50,h-200-50),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
    cv2.imshow("result", combo_image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()