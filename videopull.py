from threading import Thread
import cv2
import numpy as np
import time

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
        sTime=0

        while True:
            time.sleep(.018)  #for reading from file
            q = q + 1
            sTime= time.clock()

            if 60<sTime:

                print(" FPS")
               # print(q/sTime)
                print("     ")
            #print(time.clock())

            #print(q)

            (self.grabbed, self.frame) = self.cap.read()
