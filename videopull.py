from threading import Thread
import cv2
import numpy as np
import time

now = time.time()
future = now + 10
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
        sTime = 0

        while True:
            ret, frame = self.cap.read()

            if not ret:
                video = cv2.VideoCapture(testvidfilename)
                continue

            time.sleep(.018)  # for reading from file
            q += 1
            sTime = time.clock()

            # print(future)
            if time.time() > future and ftest ==0:
                print("++++++++++++++++++++++++++++++++++++")
                FPS = q / 10
                print(FPS)
                print("++++++++++++++++++++++++++++++++++++")
                ftest = ftest+1

            # if 60<sTime:

            #    print(" FPS")
            # print(q/sTime)
            #      print("     ")
            # print(time.clock())

            # print(q)

            (self.grabbed, self.frame) = self.cap.read()
            # print(q)
