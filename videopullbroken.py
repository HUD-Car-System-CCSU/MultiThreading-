from threading import Thread
import cv2
import numpy as np
import time
import keyboard
import sys

now = time.time()
future = now + 10
print(time.time())
print(future)
cv2.setNumThreads(10)
FromFile = float(input("If from file, enter delay (ex. 0.040) otherwise enter 0: "))

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
            fileview = False
            if not ret:
                video = cv2.VideoCapture(testvidfilename)
                continue

            time.sleep(FromFile)  # for reading from file
            q += 1
            sTime = time.clock()

            # print(future)
            if (time.time() > future and ftest ==0):
                print("++++++++++++++++++++++++++++++++++++\n\nFrames Per Second: ")
                FPS = q / (future-now)#10
                print(FPS)
               # print(now)
               # print(future)
                print("\n++++++++++++++++++++++++++++++++++++\n\n")
                ftest = ftest+1
                #future = future+10

            if keyboard.is_pressed('f'):
                FPS = q/(time.time()-now)
                print(' New Average FPS')
                print(FPS)
            if keyboard.is_pressed('r'):
                print("OH DAMN    prints 3 times... could be registering press hold and release?")


            # if 60<sTime:

            #    print(" FPS")
            # print(q/sTime)
            #      print("     ")
            # print(time.clock())

            # print(q)

            (self.grabbed, self.frame) = self.cap.read()
            # print(q)
