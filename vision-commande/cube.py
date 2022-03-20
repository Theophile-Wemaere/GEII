import cv2
import numpy as np
import matplotlib.pyplot as plt
from sys import exit

import tkinter as tk
from tkinter import *

def showIMG(name,image):
    cv2.imshow(name, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def testRGB(image):
    blurred = cv2.GaussianBlur(image,(11,11),0)
    hsv = cv2.cvtColor(blurred,cv2.COLOR_RGB2HSV)

    root1=Tk()
    root2=Tk()
    lower=RGB_selector(root1,"mininmum")
    higher=RGB_selector(root2,"maximum")

    while True:
        #
        b_m,g_m,r_m=lower.b.get(),lower.g.get(),lower.r.get()
        b_p,g_p,r_p=higher.b.get(),higher.g.get(),higher.r.get()

        moins=(b_m,g_m,r_m)
        plus=(b_p,g_p,r_p)

        print(moins,plus)

        mask = cv2.inRange(hsv,moins,plus)
        mask = cv2.erode(mask,None,iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        cv2.imshow("Frame",mask)

        lower.page.update()
        higher.page.update()

        lower.button.config(bg=_from_rgb((lower.r.get(),lower.g.get(),lower.b.get())))
        higher.button.config(bg=_from_rgb((higher.r.get(),higher.g.get(),higher.b.get())))

        key = cv2.waitKey(1) & 0xFF
        # if the 'q' key is pressed, stop the loop
        if key == ord("q"):
            break

    cv2.destroyAllWindows()
    lower.page.destroy()
    higher.page.destroy()


def mouseRGB(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDOWN: #checks mouse left button down condition
        colorsB = image[y,x,0]
        colorsG = image[y,x,1]
        colorsR = image[y,x,2]
        colors = image[y,x]
        print("Red: ",colorsR)
        print("Green: ",colorsG)
        print("Blue: ",colorsB)
        print("BRG Format: ",colors)
        print("Coordinates of pixel: X: ",x,"Y: ",y)
        print("")
 
def getPixel(image):
    # Read an image, a window and bind the function to window
    cv2.namedWindow('mouseRGB')
    cv2.setMouseCallback('mouseRGB',mouseRGB)

    #Do until esc pressed
    while(1):
        cv2.imshow('mouseRGB',image)
        if cv2.waitKey(20) & 0xFF == 27:
            break
    #if esc pressed, finish.
    cv2.destroyAllWindows()

def _from_rgb(rgb):
    """translates an rgb tuple of int to a tkinter friendly color code
    """
    r, g, b = rgb
    return f'#{r:02x}{g:02x}{b:02x}'

class RGB_selector(tk.Frame):
    def __init__(self, page, titre):
        self.page=page
        self.titre=titre
        self.page.title(self.titre)
        self.page.geometry("210x310")
        self.b = Scale(page, from_=0, to=255, orient=HORIZONTAL, length=200)
        self.b.pack()
        self.g = Scale(page, from_=0, to=255, orient=HORIZONTAL, length=200)
        self.g.pack()
        self.r = Scale(page, from_=0, to=255, orient=HORIZONTAL, length=200)
        self.r.pack()

        self.button=Button(page, text="",width=20,height=10)
        self.button.pack(pady=20)


##########################################################

cube = cv2.imread("cube.jpg")

if cube is None:
    print("le fichier cube n'existe pas / le chemin indiqué est mauvais")
    exit()    


def getContour(img):
    edges = cv2.Canny(img, 100, 200, apertureSize = 3)
    #showIMG("test",edges)
    #https://stackoverflow.com/questions/56781635/find-extreme-outer-points-in-image-with-python-opencv

    # Load image, grayscale, Gaussian blur, threshold
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3,3), 0)
    thresh = cv2.threshold(blur, 220, 255, cv2.THRESH_BINARY_INV)[1]

    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    # create hull array for convex hull points

    hull = []

    areas=[cv2.contourArea(c) for c in contours]
    max_index=np.argmax(areas)
    cnt=contours[max_index]

    hull.append(cv2.convexHull(cnt, False))

    drawing = np.zeros((thresh.shape[0], thresh.shape[1], 3), np.uint8)

    color = (255, 0, 0) # blue - color for convex hull
    # draw ith convex hull object
    cv2.drawContours(edges, hull, 0, color, 1, 8)
    cv2.drawContours(drawing, hull, 0, color, 1, 8)

    #showIMG("hull",drawing)
    #showIMG("edges+hull",edges)

    return hull


image = cube

#getPixel(cube)

white_m,white_p = (0,0,93),(255,94,255)
orange_m,orange_p = (97, 184, 235),(150,255,255) #(70,190,220),(150,255,255)
red_m,red_p = (120,140,190),(180,245,255) #(120,140,200),(180,245,255)
yellow_m,yellow_p = (70,100,80),(100,255,255) #(70,180,190),(100,255,255)
blue_m,blue_p = (15,0,0), (20, 255, 255)
green_m,green_p = (36, 0, 0), (70, 255,255)

#testRGB(cube)

all_colors=[(orange_m,orange_p,"orange"),(red_m,red_p,"red"),(yellow_m,yellow_p,"yellow"),(blue_m,blue_p,"blue"),(green_m,green_p,"green"),(white_m,white_p,"white")]

#filter the white background https://grauonline.de/wordpress/?page_id=3065
hull=getContour(image)           
filter_mask = np.zeros_like(image)
cv2.drawContours(filter_mask, [hull[-1]], -1, (255,255,255), cv2.FILLED, 1)
#remove white border with a bigger contours *trollface*
#showIMG("test",filter_mask)
cv2.drawContours(filter_mask, hull, 0, 0, 5, 8)
filtered=image.copy()
filtered[filter_mask == 0] = 0

#showIMG("test",filtered)

blurred = cv2.GaussianBlur(filtered,(11,11),0)
hsv = cv2.cvtColor(blurred,cv2.COLOR_RGB2HSV)

#apply mask on each color
for i in range(6):
    colors=all_colors[i]
    color=colors[2]
    mask = cv2.inRange(hsv,colors[0],colors[1])
    mask = cv2.erode(mask,None,iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    #showIMG("mask",mask)
    #https://www.pyimagesearch.com/2016/02/01/opencv-center-of-contour/

    cnts, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    for c in cnts:
        # compute the center of the contour
        M = cv2.moments(c)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        # draw the contour and center of the shape on the image
        cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
        cv2.circle(image, (cX, cY), 7, (255, 255, 255), -1)
        cv2.putText(image, color, (cX-10 , cY-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
    
showIMG("color",image)
