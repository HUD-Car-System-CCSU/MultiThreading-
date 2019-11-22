import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt


def canny(img, low_thresh, high_thresh, kernel=(5, 5), color_scale=cv.COLOR_BGR2GRAY):
    # convert_scale = cv.cvtColor(img, color_scale)
    blur = cv.GaussianBlur(img, kernel, 0)
    r_canny_img = cv.Canny(blur, low_thresh, high_thresh)

    return r_canny_img


def region_of_interest(img):
    img_width = img.shape[1]
    img_height = img.shape[0]

    vertices = np.array([
        [
            (320, (img_height / 2)+10),
            (img_width - 380, (img_height / 2)+10),

            (img_width - 380, img_height / 2 + 160),
            (320, img_height / 2 + 160),
        ]
    ], dtype='int32')

    poly_mask = np.zeros_like(img)
    cv.fillPoly(poly_mask, vertices, 255)
    masked_img = cv.bitwise_and(img, poly_mask)

    return masked_img


def display_lines(img, _lines):
    _line_img = np.zeros_like(img)

    if _lines is not None:
        for line in _lines:
            x1, y1, x2, y2 = line[0]
            avoid=range(y1,y1+300)

            if (y1-y2 >= 100 or y2-y1>=110):
                cv.line(_line_img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                print(line)

    return _line_img


testvidfilename = "people test2-converted.mp4"
video = cv.VideoCapture(testvidfilename)

while True:
    ret, frame = video.read()

    if not ret:
        video = cv.VideoCapture(testvidfilename)
        continue

    # print(frame.shape)
    fcrop = region_of_interest(frame)
    cv.imshow("t", fcrop)

    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    cv.imshow("t2", hsv[:, :, 2])

    sens = 125
    low_white = np.array([0, 0, 255 - sens])  # color looking for
    high_white = np.array([255, sens, 255])

    mask = cv.inRange(hsv, low_white, high_white)

    canny_img = canny(mask, 50, 170)

    cropped_img = region_of_interest(canny_img)

    lines = cv.HoughLinesP(cropped_img, 1, np.pi / 180, 100, maxLineGap=40)
    linear=[]
    linear=lines

    line_img = display_lines(frame, lines)
    #print(lines[0:1])

    comb_img = cv.addWeighted(frame, 1, line_img, .7, gamma=1)

    # cv.imshow("test", cropped_img)
    # cv.imshow("cropped", cropped_img)
    cv.imshow("res2", comb_img)

    key = cv.waitKey(1)
    if key == 27:
        break

    if key == 112:
        plt.imshow(frame)
        plt.show()
        cv.waitKey(0)

video.release()
cv.destroyAllWindows()
