# -*- coding: utf-8 -*-
"""
Created on Fri Nov 12 13:57:54 2021

@author: Hitesh
"""
import cv2
import numpy as np
import matplotlib.pyplot as plt
red_light=False
green_light=False
yellow_light=False
img= cv2.imread('C:/all desktop folders/EMR/pics/traffic/red3.jpeg',1)
rectangle = cv2.imread('C:/all desktop folders/EMR/pics/traffic/red3.jpeg',1)
rectangle   = cv2.inRange(rectangle, (100,0,0) , (225,80,80))
#rectangle = cv2.imread('C:/all desktop folders/EMR/pics/traffic/red2.jpeg', cv2.IMREAD_GRAYSCALE)
def cornerPoints(rectangle,image):
    x_max=0
    x_min=1000
    y_min=1000
    y_max=0
    rectangle = np.where(rectangle > np.mean(rectangle), 255, 0).astype(np.uint8)    
    dst_rectangle = cv2.cornerHarris(rectangle, 2, 3, 0.04)
    dst_rectangle = cv2.dilate(dst_rectangle, None)
    mask = np.where(dst_rectangle > 0.01*np.max(dst_rectangle), 255, 0).astype(np.uint8)
    points = np.nonzero(mask)
    j=len(points[0])
    f=len(points[1])
    s=0
    k=0
    while k<j:
        x=points[0][k]
        y=points[1][k]
        if image[y,x,0]>128 and image[y,x,0]<= 255 and image[y,x,1]<127 and image[y,x,2]<127 :
            if x>x_max:
                x_max=x
            if x<x_min:
                x_min=x
        k=k+1
    y_min=x_min
    y_max=x_max
    t=(x_min,y_min,x_max,x_max)
    return t

print(cornerPoints(rectangle,img))
X_min=cornerPoints(rectangle,img)[0]
Y_min=cornerPoints(rectangle,img)[1]
X_max=cornerPoints(rectangle,img)[2]
Y_max=cornerPoints(rectangle,img)[3]
print(X_min,Y_min,X_max,Y_max)
gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
circles=cv2.HoughCircles(gray,cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=26, minRadius=0, maxRadius=0)
#print(circles)
circlesnumber=len(circles[0])
acc=0
while acc<circlesnumber:
    print("circle",acc+1)
    X=circles[0][acc][0]
    Y=circles[0][acc][1]
    X=int(X)
    Y=int(Y)
    if X>X_min and X<X_max and Y>Y_min and Y<Y_max:
        print('pass1')
        print(X,Y)
        print(img[Y,X])
        if img[Y,X,0]<20 and img[Y,X,1]>200 and img[Y,X,2]<20:
            print('pass2')
            green_light=True
        elif(img[Y,X,0]<127 and img[Y,X,1]>128 and img[Y,X,1]<=255 and img[Y,X,2]>128 and img[Y,X,2]<=255): 
            yellow_light=True
            print('pass3')
        elif(img[Y,X,0]<20 and img[Y,X,1]<20 and img[Y,X,2]>200):
            red_light=True
            print("pass4")
        acc=acc+1
#cv2.imshow('image',img)
#cv2.imshow('rectangle',rectangle)

print(circlesnumber)
if red_light==True and yellow_light==False and green_light==False:
    print("The light is red")
elif yellow_light==True and red_light==False and green_light==False:
    print("The light is yellow")
elif green_light==True and red_light==False and yellow_light==False:
    print("The light is green")
else:
    print("Try again")
cv2.waitKey(0)
cv2.destroyAllWindows()
