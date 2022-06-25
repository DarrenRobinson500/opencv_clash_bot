import cv2
from PIL import Image
import numpy as np
from collections import Counter

def simplify(i, gradients=2):
    factor = 256 / gradients
    new = i
    l = []
    for row in new:
        for pixel in row:
            for c in range(3):
                pixel[c] = int(pixel[c] / factor) * factor
            l.append((pixel[0],pixel[1],pixel[2]))
    return new

def quantify(i):
    new = i
    l = []
    for row in new:
        for pixel in row:
            l.append((pixel[0],pixel[1],pixel[2]))
    return Counter(l)

def only_wizard(i):
    WIZARD_COLOURS = [(85, 0, 85), (85, 85, 85),]
    new = i
    for row in new:
        for pixel in row:
            temp = (pixel[0],pixel[1],pixel[2])
            if temp not in WIZARD_COLOURS:
                pixel[0] = 0
                pixel[1] = 0
                pixel[2] = 0
    return new

def canny(i):
    i_gray = cv2.cvtColor(i, cv2.COLOR_BGR2GRAY)
    i_blur = cv2.GaussianBlur(i_gray, (5, 5), 0)
    return cv2.Canny(image=i_blur, threshold1=100, threshold2=200)


i = np.asarray(Image.open(f'whole_screen.png'))
i = cv2.resize(i, (0,0), fx=0.5, fy=0.5)
i = simplify(i, 3)
edges = canny(i)

i2 = only_wizard(i)
wizard = canny(i)

cv2.imshow('Simplified', i)
cv2.imshow('Canny', edges)
cv2.imshow('Only wizard', wizard)

cv2.waitKey(0)
cv2.destroyAllWindows()