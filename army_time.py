import cv2
import numpy as np
import pyautogui as pag
method = cv2.TM_CCOEFF_NORMED

WHITE = [(255, 255, 255),(254, 254, 254),(253, 253, 253),]

def only_colours(i, colours):
    new = i
    for row in new:
        for pixel in row:
            if (pixel[0],pixel[1],pixel[2]) not in colours:
                pixel[0], pixel[1], pixel[2] = 255, 255, 255
            else:
                pixel[0], pixel[1], pixel[2] = 0, 0, 0
    return new

def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver

def find_many_image(template, i, confidence=0.6):
    template = cv2.imread(f'numbers/{template}.png', 0)
    h, w = template.shape

    # print("ishape", i.shape)
    # print("templateshape", template.shape)
    result = cv2.matchTemplate(i, template, method)
    yloc, xloc = np.where(result >= confidence)
    z = zip(xloc, yloc)

    rectangles = []
    for (x, y) in z:
        rectangles.append([int(x), int(y), int(w), int(h)])
        rectangles.append([int(x), int(y), int(w), int(h)])
    rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)

    return rectangles


pre = []
post = []

SCALE = 1.29

def read_army_time():
    for x in [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, ]:
        i = cv2.imread(f"time{x}.png", 1)
        i = cv2.resize(i, (0,0), fx=SCALE, fy=SCALE)
        i = only_colours(i, WHITE)
        i = cv2.cvtColor(i, cv2.COLOR_BGR2GRAY)
        # i1 = i.copy()
        # pre.append(i)

        found = []
        for y in [0,1,2,3,4,5,6,7,8,9,"m"]:
            rects = find_many_image(str(y), i, 0.75)
            if len(rects) > 0:
                for rect in rects:
                    found.append((str(y), rect[0]))
        result = ""

        found.sort(key=lambda tup: tup[1])
        for y in found:
            result += y[0]
        print(x, "=>", result)

        # rects = find_many("x", i, 0.8)
        # for x in rects: cv2.rectangle(i1, (x[0], x[1]), (x[0]+x[2], x[1]+x[3]), (255,0,0), 1)
        # post.append(i1)

# read_army_time()

i = cv2.imread(f"time2s.png", 1)
# print("Number", i.shape[1])
# i3 = cv2.imread(f"numbers/3.png", 1)
# print("Time", i.shape[1])

scaled = cv2.resize(i, (0, 0), fx=SCALE, fy=SCALE)
white = only_colours(scaled, WHITE)

# stacked_image = stackImages(1, (i, scaled))

# cv2.imshow("Original", i)
cv2.imshow("Scaled", scaled)
cv2.imshow("White", white)
# cv2.imshow("Three", i3)
cv2.waitKey(0)


# stacked_image = stackImages(1, (pre, post,post))
# cv2.imshow("Results", stacked_image)
# cv2.waitKey(0)

