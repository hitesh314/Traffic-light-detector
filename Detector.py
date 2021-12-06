import numpy as np
import pyautogui
import cv2
prev_pos="neutral"

vid=cv2.VideoCapture(0)
while(1):
    _,frame=vid.read()
    frame=cv2.flip(frame,1)
    frame=frame[:300,0:400]
    frame=cv2.GaussianBlur(frame,(5,5),0)
    lower_skin=np.array([13,16,28])
    upper_skin=np.array([87,93,125])
    mask=cv2.inRange(frame,lower_skin,upper_skin)
    _,thresh=cv2.threshold(mask, 127, 255,cv2.THRESH_BINARY)
    contours,hierarchy=cv2.findContours(thresh, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    img = cv2.drawContours(frame , contours , -1 , (0,0,255) , 2)
    if len(contours)==0:
        continue
    max_contour=max(contours,key=cv2.contourArea)
    epsilon=0.01*cv2.arcLength(max_contour,True)
    approx=cv2.approxPolyDP(max_contour,epsilon,True)
    M=cv2.moments(approx)
    try:
        x=int(M['m10']/M['m00'])
        y=int(M['m01']/M['m00'])
    except ZeroDivisionError:
        continue
    frame=cv2.circle(frame,(x,y),10,(0,255,0),3)
    frame=cv2.line(frame,(125,0),(125,400),(0,0,255),2)
    frame=cv2.line(frame,(225,0),(225,400),(0,0,255),2)
    frame=cv2.line(frame,(0,200),(400,200),(0,0,255),2)
    frame=cv2.line(frame,(0,250),(400,250),(0,0,255),2)
    cv2.imshow('Contoors',frame)

    if x<125:
        curr_pos="left"
    elif x>225:
        curr_pos="right"
    elif y<200 and x>125 and x>225:
        curr_pos="up"
    elif y>255 and x>125 and x<225:
        curr_pos="down"
    else:
        curr_pos="neutral"
    if curr_pos!=prev_pos:
        if curr_pos !="neutral":
            pyautogui.press(curr_pos)
        prev_pos=curr_pos


    if cv2.waitKey(1)==ord('q'):
         break
vid.release()
cv2.destroyAllWindows()
