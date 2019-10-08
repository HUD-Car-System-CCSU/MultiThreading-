from threading import Thread
import cv2
import numpy as np
cv2.setNumThreads(1)
 #thread for output 
class videopush:
    
    #2get passed frame from multi(hog)
    def __init__(self, frame=None):
        self.frame = frame
    #begin new thread   
    def start(self):
        Thread(target=self.show, args=()).start()
        return self
    #show frame
    def show(self):
        while True:
            cv2.imshow("Modified Out", self.frame)
            if cv2.waitKey(1) == ord("q"):
               break


