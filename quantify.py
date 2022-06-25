import cv2
from collections import Counter
from PIL import Image
import numpy as np

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

for x in range(1,4):
    i = np.asarray(Image.open(f'images/account_{x}.png'))
    # cv2.imshow('Original', i)
    print(x)
    print(quantify(i))

# cv2.waitKey(0)
# cv2.destroyAllWindows()

# i = np.asarray(Image.open(f'whole_screen.png'))
# i = cv2.resize(i, (0,0), fx=0.5, fy=0.5)
# i_simple = simplify(i, 3)
# print(quantify(i))

# cv2.imshow('Simple', i_simple)
# i = only_wizard(i)
# cv2.imshow('OnlyWizard', i)
