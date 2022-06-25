import cv2
import pytesseract
from collections import Counter

def quantify(i):
    new = i
    l = []
    for row in new:
        for pixel in row:
            l.append((pixel[0],pixel[1],pixel[2]))
    return Counter(l)

def only_colours(i, colours):
    new = i
    for row in new:
        for pixel in row:
            if (pixel[0],pixel[1],pixel[2]) not in colours:
                pixel[0] = 0
                pixel[1] = 0
                pixel[2] = 0
    return new

file = "army_troops.png"

pytesseract.pytesseract.tesseract_cmd = "c:\\Program Files\\Tesseract-OCR\\tesseract.exe"
img = cv2.imread(file)
cv2.imshow(f"Original", img)
print(quantify(img))

img = only_colours(img, [(255, 255, 255),(254, 254, 254),(253, 253, 253),(251, 251, 251), ])
print(pytesseract.image_to_string(img))

cv2.imshow(f"Only White", img)
cv2.waitKey(0)

