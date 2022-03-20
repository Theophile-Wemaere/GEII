import cv2
import numpy as np
import matplotlib.pyplot as plt
from sys import exit
import random 

def showIMG(name,image):
    cv2.imshow(name, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

paper = cv2.imread('paperwithmessage.ppm')
bruce = cv2.imread('bruce_banner.png') 

if paper is None:
    print("le fichier paperwithmessage n'existe pas / le chemin indiqué est mauvais")
    exit()
    
if bruce is None:
    print("le fichier bruce_banner.jpg n'existe pas / le chemin indiqué est mauvais")
    exit()


def equalize_img(paper):
    r_image, g_image, b_image = cv2.split(paper)

    r_image_eq = cv2.equalizeHist(r_image)
    g_image_eq = cv2.equalizeHist(g_image)
    b_image_eq = cv2.equalizeHist(b_image)

    image_eq = cv2.merge((r_image_eq, g_image_eq, b_image_eq))


    all = np.concatenate((paper,image_eq),axis=1)
    showIMG("OG   -    equalized",all)

def steganographie(img):
    width = img.shape[0]
    height = img.shape[1]

    # img1 and img2 are two blank images
    img1 = np.zeros((width, height, 3), np.uint8)
    img2 = np.zeros((width, height, 3), np.uint8)
    
    for i in range(width):
        for j in range(height):
            for l in range(3):
                v1 = format(img[i][j][l], '08b')
                v3 = v1[5:] + chr(random.randint(0, 1)+48) * 5
                
                # Appending data to img1 and img2
                img2[i][j][l]= int(v3, 2)
    
        
    # These are two images produced from
    # the encrypted image
    all=np.concatenate((img,img2),axis=1)
    showIMG("hulk?",all)

equalize_img(paper)
steganographie(bruce)
