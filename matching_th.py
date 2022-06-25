import numpy as np
import cv2

img_str = ["attack 0153AM", "attack 0158AM", "attack 0226AM", "attack 0231AM", "attack 0252PM", "attack 0253PM", "attack 0257PM", "attack 0303PM", "attack 0309PM", "attack 0314PM", "attack 0320PM", "attack 0326PM", "attack 0329PM", "attack 0332PM", "attack 0333PM", "attack 0336PM", "attack 0941PM", "attack 1001PM", "attack 1023PM", "attack 1108PM", "attack 1131PM", "attack 1216AM", ]
# img_str = ["attack_th7", ]
th_str = ["th6", "th7", "th8", "th9"]

imgs = []
templates = []

for x in img_str: imgs.append((x, cv2.imread(f'attacks/{x}.png', 0)))
for x in th_str: templates.append((x, cv2.imread(f'templates/{x}.png', 0)))


methods = [cv2.TM_CCOEFF, cv2.TM_CCOEFF_NORMED, cv2.TM_CCORR,
            cv2.TM_CCORR_NORMED, cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]
method = methods[1]
units = 1

count = 1
for img_name, img in imgs:
    max_value = 0
    max_name = ""
    max_location = None
    bottom_right = (0,0)
    for name, template in templates:
        h, w = template.shape
        img2 = img.copy()

        result = cv2.matchTemplate(img2, template, method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            location = min_loc
            val = min_val
        else:
            location = max_loc
            val = max_val
        if val > max_value:
            max_value = val
            max_name = name
            max_location = location
    bottom_right = (max_location[0] + w, max_location[1] + h)
    cv2.rectangle(img2, max_location, bottom_right, 255, 5)
    if max_value < 0.5: max_name = "Unidentified"
    cv2.imshow(f'{img_name}: {max_name} {round(max_value/units,1)}', img2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    count += 1