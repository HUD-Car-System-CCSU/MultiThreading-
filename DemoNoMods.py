
import cv2
import numpy as np
import time

vid = cv2.VideoCapture('fin.mp4')
current = time.time()
printers = 0
FCount = 0

while (vid.isOpened()):

    ret, frame = vid.read()
    frame = cv2.resize(frame,(720,480))
    if ret == True:
        FCount=FCount+1

        if (time.time() >= current + .5):
            printers = FCount / .5
            FCount = 0
            # print(str(printers)+"  "+str(time.time()-start))

            # cv2.putText(frame, str(printers), (105, 105), cv2.FONT_HERSHEY_COMPLEX_SMALL, .7, (0, 255, 0))
            current = time.time()
        cv2.putText(frame, str(printers) + " FPS", (105, 445), cv2.FONT_HERSHEY_COMPLEX_SMALL, .97, (0, 255, 0))
        cv2.imshow('Frame', frame)# Press Q on keyboard to  exit
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    else:
        break
vid.release()
cv2.destroyAllWindows()