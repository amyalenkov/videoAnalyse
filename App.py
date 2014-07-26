from Tools.pynche import ColorDB
from _ctypes import FormatError
from analyse.FindPlayers import Player, Analyse

__author__ = 'amyalenkov'

import cv2
import numpy as np


class App:
    def __init__(self, pathVideo, analyse):
        self.analyse = analyse
        self.cam = cv2.VideoCapture(pathVideo)
        self.window_name = "Movement Visual"
        cv2.namedWindow(self.window_name, cv2.CV_WINDOW_AUTOSIZE)

    def drowCircleMomets(self, img, contours):
        min_area = 1000
        for contour in contours:
            area = cv2.contourArea(contour)
            print area
            if area > min_area:
                moment = cv2.moments(contour)
                cx, cy = int(moment['m10'] / moment['m00']), int(moment['m01'] / moment['m00'])
                color = analyse.findPlayer(cx, cy)
                cv2.circle(img, (cx, cy), 10, color, -1)

    def findPlayers(self, cx, cy):
        print 'find players start'


    # Find the differential image
    def diffImg(self, t0, t1, t2):
        d1 = cv2.absdiff(t2, t1)
        d2 = cv2.absdiff(t1, t0)
        d_final = cv2.bitwise_and(d1, d2)
        d_binary = cv2.threshold(d_final, 35, 255, cv2.THRESH_BINARY)[1]
        d_blur = cv2.blur(d_binary, (15, 15))
        return d_blur

    def run(self):
        while True:
            s, img = self.cam.read()

            t_minus = cv2.cvtColor(self.cam.read()[1], cv2.COLOR_RGB2GRAY)
            t = cv2.cvtColor(self.cam.read()[1], cv2.COLOR_RGB2GRAY)
            t_plus = cv2.cvtColor(self.cam.read()[1], cv2.COLOR_RGB2GRAY)

            _, img2 = self.cam.read()
            cv2.imshow('origin', img2)

            # draw contours
            contours, hierarchy = cv2.findContours(self.diffImg(t_minus, t, t_plus), cv2.RETR_TREE,
                                                   cv2.CHAIN_APPROX_SIMPLE)
            print '------'
            print 'size' + str(len(contours))
            self.drowCircleMomets(img, contours)
            cv2.drawContours(img, contours, -1, (150, 150, 150), 2)
            cv2.imshow('Contours', img)
            cv2.imshow(self.window_name, self.diffImg(t_minus, t, t_plus))
            t_minus = t
            t = t_plus
            t_plus = cv2.cvtColor(self.cam.read()[1], cv2.COLOR_RGB2GRAY)

            key = cv2.waitKey(500)
            if key == 27:
                cv2.destroyWindow(self.window_name)
                break


if __name__ == '__main__':
    # video_src = 'video/1.avi'
    video_src = 'video/2.wmv'
    # video_src = 'video/soccer_mean_shift.mp4'

    player1 = Player('Vasya1')
    player2 = Player('Vasya2')
    player3 = Player('Vasya3')
    player4 = Player('Vasya4')
    player5 = Player('Vasya5')
    player6 = Player('Vasya6')

    analyse = Analyse((player1, player2, player3, player4, player5, player6))

    App(video_src, analyse).run()