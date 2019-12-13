import sys
import cv2
import numpy as np
# import my stuff
import videopull as videopull
import videopush as videopush
import time
import keyboard
import datetime
logging = "off"
FCount = 0
boxem = 0
print(datetime.datetime.now())

'''
#set a max amount of threads-- python uses like 40-60 threads for some odd reason
#but setting it to 10 uses little more than half (38) while having the same performance
#as set to 100 (63-64) [i7-9750H 6 core(12logical) - CPU set to low power = 3.1x GHz]
#i have no idea why....
#    maxthread-----Observed threads---cpu usage and notes 
        # 1000----590    o  pinned 100% @2.98GHz-somewhat unstable 50/50 chance of crash
        # 100-----64     o      -81% @2.98GHz  
        # 10------38     o      -75% @2.98GHzff
        # 8-------37   \ o /    -75% @2.98GHz
        # 6-------34    \o/     -65% @2.98GHz
        # 4-------32  Literally the same as 1000 but stable cpu max 58% @2.99GHz
        # 2-------29 -- bad performance
        #best is push and pull limited to 1 thread and 4-6 in the main 

'''

if logging == "on":
    logData = open("allThatGoodDataLogFileAndSomeOtherStuff look i could have put spaces.txt", "w")
    numDet = 0
    logData.write("Logging enabled")
    logData.write("         \n")

cv2.setNumThreads(20)

hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# set the sauce
# start the threads
# source= input("Input(or 0 for live):  ")
"""test vid file names 
input.mp4
lane1.mp4
lanecent.mp4
lanes2enterhi.mp4
lanetest2.mp4
people test2-converted.mp4
people test-converted.mp4
fin.mp4
"""
#srcs = input("enter video name : ")
source = "fin.mp4" #0 #srcs
# cv2.startWindowThread()
v_pull = videopull.videopull(source).start()                    #start & pass src to vidpull
v_push = videopush.videopush(v_pull.frame).start()              #start video push
Vinfo = cv2.VideoCapture(source)                                #test purpose video data
tFrame = Vinfo.get(cv2.CAP_PROP_FRAME_COUNT)                    #test purpose video data
kFrame = Vinfo.get(cv2.CAP_PROP_FPS)                            #test purpose video data
#print(kFrame)
#print(tFrame)
totalframe=0                                                    #test purpose video data
fcounter = True                                                 #test purpose video data
print(kFrame)                                                   #test purpose video data
print(tFrame)                                                   #test purpose video data
# print(FCount)
test = True                                                     #test purpose video data
#testing = input("Testing (y/n): ")
#if testing == ('y' or 'Y'):
    #test = not test

print(datetime.datetime.now())
def canny(img, low_thresh, high_thresh, kernel=(5, 5), color_scale=cv2.COLOR_BGR2GRAY):
    # convert_scale = cv.cvtColor(img, color_scale)
    blur = cv2.GaussianBlur(img, kernel, 0)
    r_canny_img = cv2.Canny(blur, low_thresh, high_thresh)

    return r_canny_img


def region_of_interest(img):                                                                #define an area to scan for lanes
    img_width = img.shape[1]
    img_height = img.shape[0]

    vertices = np.array([
        [
            (220, (img_height / 2) + 220),
            (img_width - 180, (img_height / 2) + 220),

            (img_width - 180, img_height / 2 + 80 ),
            (220, img_height / 2 + 80),
            #subaru settings
            #(520, (img_height / 2) + 0),
            #(img_width - 580, (img_height / 2) + 0),

            #(img_width - 580, img_height / 2 + 90),
            #(520, img_height / 2 + 90),
        ]
    ], dtype='int32')

    poly_mask = np.zeros_like(img)
    cv2.fillPoly(poly_mask, vertices, 255)
    masked_img = cv2.bitwise_and(img, poly_mask)

    return masked_img


def display_lines(img, _lines):
    _line_img = np.zeros_like(img)

    if _lines is not None:
        for line in _lines:
            x1, y1, x2, y2 = line[0]
            avoid = range(y1, y1 + 300)
            lineframe = line+1
            if\
                    (y1 - y2 >= 100 or y2 - y1 >= 110):
                cv2.line(_line_img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                #print(line)


    return _line_img



start = time.time()
current = time.time()
printers=0
while True:

    skipper = 0
    key = cv2.waitKey(3)
    if key == 27:
        break
    if keyboard.is_pressed('f'):
        print(datetime.datetime.now())
        print('total boxes: ')
        print(boxem)
    frame = v_pull.frame
    FCount = FCount + 1
    # print(FCount)
    frame = cv2.resize(frame, (720, 480))
    # change the color to gray for quicker scanning
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    skipper = skipper + 1
    # search the gray picture
    boxes, weights = hog.detectMultiScale(gray, winStride=(8, 8))
    boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])
    for (xA, yA, xB, yB) in boxes:
        # display the detected boxes in the color picture
        cv2.rectangle(frame, (xA, yA), (xB, yB),
                      (0, 255, 0), 2)
        if test == True:
            boxem = boxem+1



    fcrop = region_of_interest(frame)

    #cv2.imshow("t", fcrop)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)



    sens = 160#125
    low_white = np.array([0, 0, 255 - sens])  # color looking for
    high_white = np.array([255, sens, 255])

    mask = cv2.inRange(hsv, low_white, high_white)

    canny_img = canny(mask, 50, 170)

    cropped_img = region_of_interest(canny_img)

    lines = cv2.HoughLinesP(cropped_img, 1, np.pi / 180, 100, maxLineGap=40)
    linear = []
    linear = lines

    line_img = display_lines(frame, lines)
    if(time.time()>= current+.5):
        printers = FCount/.5
        FCount=0
        #print(str(printers)+"  "+str(time.time()-start))

        #cv2.putText(frame, str(printers), (105, 105), cv2.FONT_HERSHEY_COMPLEX_SMALL, .7, (0, 255, 0))
        current = time.time()
    cv2.putText(frame, str(printers)+" FPS", (105, 445), cv2.FONT_HERSHEY_COMPLEX_SMALL, .97, (0, 255, 0))
    comb_img = cv2.addWeighted(frame, 1, line_img, .7, gamma=1)
    v_push.frame = comb_img


    #print(totalframe)
    # cv.imshow("test", cropped_img)
#    cv2.imshow("cropped", cropped_img)
    # cv2.imshow("res2", comb_img)
logData.close()