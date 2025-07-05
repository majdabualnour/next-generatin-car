
import cv2
def signlang(sm):

    str(sm).lower().split()
    
    for m in sm:
        
        if m == ' ':m='_'
        elif m == '/':m='majdf'
        elif m == ':':m='majd'
        elif m == ',':m='majdn'
        elif m == '?':m='majdq'
        elif m == '"':m='majdh'
        imge_sign = cv2.imread(f'sign_lang\{m}.png')
        cv2.imshow('sign lang' , imge_sign)
        cv2.waitKey(400)
    cv2.destroyWindow('sign lang')


# img = cv2.imread('sign_lang\_.png')

# font                   = cv2.FONT_HERSHEY_SCRIPT_SIMPLEX
# position               = (110,280)
# fontScale              = 9
# fontColor              = (0,0,0)
# m = '"'


# cv2.putText(img,m,
#         position,
#         font,
#         fontScale,
#         fontColor,3)
# cv2.imwrite('sign_lang\majdh.png', img)
