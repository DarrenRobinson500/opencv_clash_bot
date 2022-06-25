import numpy as np
import cv2

img_str = ["attack 0153AM", "attack 0158AM", "attack 0226AM", "attack 0231AM", "attack 0252PM", "attack 0253PM", "attack 0257PM", "attack 0303PM", "attack 0309PM", "attack 0314PM", "attack 0320PM", "attack 0326PM", "attack 0329PM", "attack 0332PM", "attack 0333PM", "attack 0336PM", "attack 0941PM", "attack 1001PM", "attack 1023PM", "attack 1108PM", "attack 1131PM", "attack 1216AM", ]
# img_str = ["attack_th7", ]
template_str = ["wizard1"]

imgs = []
templates = []

for x in img_str: imgs.append((x, cv2.imread(f'attacks/{x}.png', 0)))
for x in template_str: templates.append((x, cv2.imread(f'templates/{x}.png', 0)))


methods = [cv2.TM_CCOEFF, cv2.TM_CCOEFF_NORMED, cv2.TM_CCORR,
            cv2.TM_CCORR_NORMED, cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]
method = methods[1]
units = 1

count = 1
for img_name, img in imgs:
    for name, template in templates:
        h, w = template.shape
        img2 = img.copy()
        result = cv2.matchTemplate(img2, template, method)
        min_val, val, min_loc, location = cv2.minMaxLoc(result)
        outcome = "Not found"
        if val > 0.7:
            bottom_right = (location[0] + w, location[1] + h)
            cv2.rectangle(img2, location, bottom_right, 255, 5)
            outcome = "Found"
        img2 = cv2.resize(img2, (0, 0), fx=0.5, fy=0.5)

        cv2.imshow(f'{img_name}: {outcome} {round(val,2)}', img2)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
