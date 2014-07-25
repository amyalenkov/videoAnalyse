import cv2
import time
import numpy as np

#Find the differential image
def diffImg(t0, t1,t2):
    d1 = cv2.absdiff(t2, t1)
    d2 = cv2.absdiff(t1, t0)
    d_final = cv2.bitwise_and(d1,d2)
    d_binary = cv2.threshold(d_final, 35, 255,cv2.THRESH_BINARY)[1]
    d_blur =  cv2.blur(d_binary, (15,15))
    return d_blur

#Capture Video from camera
# cam = cv2.VideoCapture('1.avi')
# cam = cv2.VideoCapture('2.wmv')
cam = cv2.VideoCapture('soccer_mean_shift.mp4')
# s, img = cam.read()

window_name = "Movement Visual"
cv2.namedWindow(window_name, cv2.CV_WINDOW_AUTOSIZE)

#Read the first three images to find the differential image
# t_minus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
# t = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
# t_plus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)

while (1):
    s, img = cam.read()

    t_minus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
    t = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
    t_plus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)

    _, img2 = cam.read()
    cv2.imshow('11111', img2)

    #draw contours
    contours, hierarchy = cv2.findContours(diffImg(t_minus,t,t_plus),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    print '------'
    print 'size'+str(len(contours))
    # for elem in contours:
    #     print elem

    cv2.drawContours(img,contours,-1,(150,150,150),2)
    cv2.imshow('Contours', img)
    cv2.imshow(window_name,diffImg(t_minus,t,t_plus))
    t_minus = t
    t = t_plus
    t_plus = cv2.cvtColor(cam.read()[1],cv2.COLOR_RGB2GRAY)

    # time.sleep(1)

    key = cv2.waitKey(200)
    if key == 27: 
        cv2.destroyWindow(window_name)
        break
print "Bye"