from time import sleep
import pygame
import sys
#Import only if not previously imported
import cv2
# In VideoCapture object either Pass address of your Video file
# Or If the input is the camera, pass 0 instead of the video file
cap = cv2.VideoCapture(0)



pygame.init()

sur_obj=pygame.display.set_mode((10,10))
pygame.display.set_caption("Keyboard_Input")

p1=10
p2=10
step=5
while True:
    ret, frame = cap.read()


    
    for eve in pygame.event.get():
        if eve.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
    key_input = pygame.key.get_pressed()   
    if key_input[pygame.K_LEFT]:
        p1 -= step
    if key_input[pygame.K_UP]:
        p2 -= step
    if key_input[pygame.K_RIGHT]:
        p1 += step
    if key_input[pygame.K_DOWN]:
        p2 += step
    cv2.imshow('Frame',frame)
    print(p1)
    
    if cv2.waitKey(20) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()