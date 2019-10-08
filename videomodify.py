import sys
import cv2
import numpy as np
#import my stuff
import videopull as videopull
import videopush as videopush
#set a max amount of threads-- python uses like 40-60 threads for some odd reason
#but setting it to 10 uses little more than half (38) while having the same performance
#as set to 100 (63-64) [i7-9750H 6 core(12logical) - CPU set to low power = 3.1x GHz]
#i have no idea why....
#    maxthread-----Observed threads---cpu usage and notes 
        # 1000----590    o  pinned 100% @2.98GHz-somewhat unstable 50/50 chance of crash
        # 100-----64     o      -81% @2.98GHz  
        # 10------38     o      -75% @2.98GHz
        # 8-------37   \ o /    -75% @2.98GHz
        # 6-------34    \o/     -65% @2.98GHz
        # 4-------32  Literally the same as 1000 but stable cpu max 58% @2.99GHz
        # 2-------29 -- bad performance
        #best is push and pull limited to 1 thread and 4-6 in the main 
cv2.setNumThreads(6)

hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())


#set the sauce 
#start the threads

source = "people test-converted.mp4"
#cv2.startWindowThread()
v_pull = videopull.videopull(source).start()
v_push = videopush.videopush(v_pull.frame).start()


while (True):
	key = cv2.waitKey(28)
	if key ==27:
		break

	frame = v_pull.frame
	frame = cv2.resize(frame,(720,480))
	#change the color to gray for quicker scanning
	gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
	
	#search the gray picture
	boxes, weights = hog.detectMultiScale(gray, winStride=(8,8) )
	boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])
	
	for (xA, yA, xB, yB) in boxes:
        # display the detected boxes in the colour picture
		cv2.rectangle(frame, (xA, yA), (xB, yB),
                          (0, 255, 0), 2)

	
	v_push.frame = frame

