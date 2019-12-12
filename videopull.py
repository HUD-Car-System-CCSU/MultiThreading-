from threading import Thread
import cv2
import numpy as np
import time
import keyboard
import sys
settime=False
#now = time.time()
#future = now + 10
cv2.setNumThreads(10)


class videopull:
    """
    Class that continuously gets frames from a VideoCapture object
    with a dedicated thread.
    IT PLAYS ALL WEIRD AND FAST BECAUSE ITS THROWING THE FRAMES AS FAST AS IT CAN READ IT !!!
    ADD TIME DELAY BETWEEN FRAME PULLS TO MIMIC THE KNOWN VIDEO FPS (30)
    """

    def __init__(self, src=0):
        self.cap = cv2.VideoCapture(src)
        (self.grabbed, self.frame) = self.cap.read()

    def start(self):
        Thread(target=self.get, args=()).start()
        return self

    def get(self):
        q = 0
        ftest = 0
        settime = False


        while True:
            ret, frame = self.cap.read()

            if settime == False:
                now = time.time()
                future = now + 10
                settime= True

            if not ret:
                video = cv2.VideoCapture(testvidfilename)
                continue

            time.sleep(.040)#For reading from file assume (or check the files FPS) that the video is ~30fps so one frame per.030s """
            q += 1

#================================FPS CALC=========================================

            if time.time() > future and ftest ==0:
                print("++++++++++++++++++++++++++++++++++++")
                FPS = q / 10
                print(FPS)
                print("++++++++++++++++++++++++++++++++++++")
                ftest = ftest+1
            if keyboard.is_pressed('f'):
                FPS = q/(time.time()-now)
                print(' New Average FPS')
                print(FPS)
                print('Total frames played: ')
                print(q)

#=================================================================================

            (self.grabbed, self.frame) = self.cap.read()
