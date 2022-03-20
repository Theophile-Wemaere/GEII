import cv2
import numpy as np
import matplotlib.pyplot as plt
from sys import exit

def showIMG(name,image):
    cv2.imshow(name, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

img_lena=cv2.imread('lena.png')
img_lena_grey=cv2.imread('lena.png',0)
img_fabio=cv2.imread('fabio.pgm',0)

if img_fabio is None:
    print("le fichier fabio n'existe pas / le chemin indiqué est mauvais")
    exit()
    
if img_lena is None:
    print("le fichier lena n'existe pas / le chemin indiqué est mauvais")
    exit()
    
if img_lena_grey is None:
    print("le fichier lena n'existe pas / le chemin indiqué est mauvais")
    exit()
    
print("********************Fabio********************")

height,width=img_fabio.shape
print("Height : " + str(height))
print("Width : " + str(width))

min_lena=np.amin(img_fabio)
max_lena=np.amax(img_fabio)

print("Min of array : " + str(min_lena))
print("Max of array : " + str(max_lena))

showIMG('fabio',img_fabio)

print("********************Lena RGB********************")

height,width,channel=img_lena.shape
print("Height : " + str(height))
print("Width : " + str(width))
print("Channel : " + str(channel))

min_lena=np.amin(img_lena)
max_lena=np.amax(img_lena)

print("Min of array : " + str(min_lena))
print("Max of array : " + str(max_lena))

showIMG('lena.png',img_lena)


print("********************Lena grey********************")

height,width=img_lena_grey.shape
print("Height : " + str(height))
print("Width : " + str(width))

min_lena_grey=np.amin(img_lena_grey)
max_lena_grey=np.amax(img_lena_grey)

print("Min of array : " + str(min_lena_grey))
print("Max of array : " + str(max_lena_grey))

showIMG('lena.png',img_lena_grey)



panel_img=np.concatenate((img_lena[:,:,0],img_lena[:,:,1], img_lena[:,:,2]),axis=1)

cv2.imshow("original Lena",img_lena_grey)
cv2.imshow("grey channels",panel_img)

cv2.waitKey(0)
cv2.destroyAllWindows()

#3rd is the brightest (r) cause the original img is very red themed

print("********************YCbCr***********************")

YCrCbimg = cv2.cvtColor(img_lena, cv2.COLOR_BGR2YCR_CB)

panel_img_YCbCr=np.concatenate((YCrCbimg[:,:,0],YCrCbimg[:,:,1], YCrCbimg[:,:,2]),axis=1)

cv2.imshow("original Lena",YCrCbimg)
cv2.imshow("grey channels",panel_img_YCbCr)

cv2.waitKey(0)
cv2.destroyAllWindows()
