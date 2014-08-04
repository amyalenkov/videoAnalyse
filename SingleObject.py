from array import array
from Plot import CreatePlot

__author__ = 'amyalenkov'

import cv2
import numpy

import math


class TrackSingleObject:
    allDetect = []

    def __init__(self, pathVideo):
        self.cam = cv2.VideoCapture(pathVideo)
        self.window_name = "TrackSingleObject"
        cv2.namedWindow(self.window_name, cv2.CV_WINDOW_AUTOSIZE)

    def showPlot(self, allPoints):
        print allPoints
        print allPoints.__len__()
        elems = 0
        xyElem = []
        for screen in allPoints:
            for i, xy in enumerate(screen):
                if elems == i:
                    xyElem.append(xy)
        print xyElem
        dx = []
        dy = []
        for xy in xyElem:
            dx.append(xy[0])
            dy.append(xy[1])
        print dx
        print dy
        plot = CreatePlot(dx, dy)
        plot.showPlot()

    # Find the differential image
    def diffImg(self, t0, t1, t2):
        d1 = cv2.absdiff(t2, t1)
        d2 = cv2.absdiff(t1, t0)
        d_final = cv2.bitwise_and(d1, d2)
        d_binary = cv2.threshold(d_final, 35, 255, cv2.THRESH_BINARY)[1]
        d_blur = cv2.blur(d_binary, (15, 15))
        return d_blur

    def drowCircleMomets(self, img, contours):
        min_area = 800
        allXYforContuors = []
        i = 0
        for contour in contours:
            area = cv2.contourArea(contour)
            print area
            if area > min_area:
                moment = cv2.moments(contour)
                cx, cy = int(moment['m10'] / moment['m00']), int(moment['m01'] / moment['m00'])
                print '-------'
                print 'cx - ' + str(cx)
                print 'cy - ' + str(cy)
                allXYforContuors.append([cx, -cy])
                cv2.circle(img, (cx, cy), 5 + i, (0, 250, 0), 1)
                i += 5
        return allXYforContuors

    def run(self):
        t_minus = cv2.cvtColor(self.cam.read()[1], cv2.COLOR_RGB2GRAY)
        t = cv2.cvtColor(self.cam.read()[1], cv2.COLOR_RGB2GRAY)
        t_plus = cv2.cvtColor(self.cam.read()[1], cv2.COLOR_RGB2GRAY)
        i = 0
        while True:
            s, img = self.cam.read()
            _, img2 = self.cam.read()
            cv2.imshow('origin', img2)

            # draw contours
            contours, hierarchy = cv2.findContours(self.diffImg(t_minus, t, t_plus), cv2.RETR_TREE,
                                                   cv2.CHAIN_APPROX_SIMPLE)

            cv2.drawContours(img, contours, -1, (0, 0, 250), 2)

            array = self.drowCircleMomets(img, contours)
            self.allDetect.append(array)

            cv2.imshow('Contours', img)
            cv2.imshow(self.window_name, self.diffImg(t_minus, t, t_plus))
            t_minus = t
            t = t_plus
            t_plus = cv2.cvtColor(self.cam.read()[1], cv2.COLOR_RGB2GRAY)

            if i == 30:
                self.showPlot(self.allDetect)
                break
            else:
                i += 1

            key = cv2.waitKey(100)
            if key == 27:
                cv2.destroyWindow(self.window_name)
                break


if __name__ == '__main__':
    # video_src = 1
    video_src = 'video/2.wmv'
    TrackSingleObject(video_src).run()