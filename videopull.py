from threading import Thread
import cv2
import numpy as np
cv2.setNumThreads(1)
class videopull:
    """
    Class that continuously gets frames from a VideoCapture object
    with a dedicated thread.
    """

    def __init__(self, src=0):
        self.cap = cv2.VideoCapture(src)
        (self.grabbed, self.frame) = self.cap.read()
        

    def start(self):    
        Thread(target=self.get, args=()).start()
        return self

    def get(self):
        while True:
            (self.grabbed, self.frame) = self.cap.read()

    
