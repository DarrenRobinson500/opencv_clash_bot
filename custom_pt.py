import cv2
import pytesseract
import numpy as np

pytesseract.pytesseract.tesseract_cmd = "c:\\Program Files\\Tesseract-OCR\\tesseract.exe"
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

def add_border(i):
    new = i.copy()
    h, w, channels = new.shape
    for x in range(w):
        for y in [0,1,h-2,h-1]:
            pixel = new[y][x]
            pixel[0], pixel[1], pixel[2] = 0, 0, 0
    for y in range(h):
        for x in [0,1,w-2,w-1]:
            pixel = new[y][x]
            pixel[0], pixel[1], pixel[2] = 0, 0, 0
    # cv2.imshow("", new)
    # cv2.waitKey(0)
    return new


def read_text():
    config = r'--oem 3 --psm 8'
    i = only_colours(cv2.imread(f"temp21.png", 1), WHITE)
    cv2.imshow("", i)
    cv2.waitKey(0)
    result21 = pytesseract.image_to_string(i,config=config)
    i = only_colours(cv2.imread(f"temp26.png", 1), WHITE)
    cv2.imshow("", i)
    cv2.waitKey(0)

    result26 = pytesseract.image_to_string(i,config=config)
    print(config)
    print(result21, result26)

def number(str):
    try:
        return int(str)
    except:
        return 0

def get_numbers(string):
    new_string = "0"
    for x in string:
        if x.isdigit():
            new_string += x
    return int(new_string)


def read_text2():
    fx1 = 1.1
    fx2 = 1.15
    config = '--psm 13 --oem 3 --dpi 300 -c tessedit_char_whitelist=0123456789'
    for x in [19, 21, 22, 23, 24, 25, 26, 27, 28,]:
    # for x in [21, 24, 25, ]:
        i = cv2.imread(f"temp{x}.png", 1)
        i = only_colours(i, WHITE)
        i = add_border(i)
        i1 = cv2.resize(i, (0, 0), fx=fx1, fy=1)
        i2 = cv2.resize(i, (0, 0), fx=fx2, fy=1)
        result0 = pytesseract.image_to_string(i1)
        result1 = pytesseract.image_to_string(i1, lang='eng', config=config)
        result2 = pytesseract.image_to_string(i2, lang='eng', config=config)
        result1 = number(result1)
        result2 = number(result2)
        result0num = get_numbers(result0)
        result = max(result0num, result1, result2, )

        if result < 10 and len(result0) >= 2:
            if result0[2] in ["d", "4"]:
                result = result * 10 + 4
            if result0[2] in ["s", "S", "5",]:
                result = result * 10 + 5

        # print(result0, result1, result2)
        print(x, "=>", result)

COLOURS = ((255,0,0), (0,255,0), (0,0,255))
def getContours(i):
    contours, hierarchy = cv2.findContours(i, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    count = 0
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 10:
            colour =COLOURS[count]
            cv2.drawContours(i0,contour,-1,colour, 1)
            peri = cv2.arcLength(contour,False)
            approx = cv2.approxPolyDP(contour, 0.05*peri, False)

            print(round(peri,0))
            print(approx)
            count += 1



# for x in [19, 21, 22, 23, 24, 25, 26, 27, 28,]:
for x in [21, ]:
    i = cv2.imread(f"temp{x}.png", 1)
    i = only_colours(i, WHITE)
    i0 = i.copy()
    i = cv2.cvtColor(i, cv2.COLOR_BGR2GRAY)
    i = cv2.GaussianBlur(i, (3,3), 1)
    i = cv2.Canny(i, 50, 50)
    getContours(i)

    cv2.imshow("", i)
    cv2.waitKey(0)
    cv2.imshow("", i0)
    cv2.waitKey(0)


