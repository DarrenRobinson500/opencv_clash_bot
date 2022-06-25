import numpy as np
import cv2
import os
import pyautogui as pag
method = cv2.TM_CCOEFF_NORMED

# img_str = ["attack 0153AM", "attack 0158AM", "attack 0226AM", "attack 0231AM", "attack 0252PM", "attack 0253PM", "attack 0257PM", "attack 0303PM", "attack 0309PM", "attack 0314PM", "attack 0320PM", "attack 0326PM", "attack 0329PM", "attack 0332PM", "attack 0333PM", "attack 0336PM", "attack 0941PM", "attack 1001PM", "attack 1023PM", "attack 1108PM", "attack 1131PM", "attack 1216AM", ]
# img_str = ["attack 0153AM", "attack 1001PM", "attack 1023PM", "attack 1108PM", "attack 1131PM", "attack 1216AM", ]
img_str = ["0109PM", "0112PM", "0125PM", "0133AM", "0135PM", "0138PM", "0145PM", "0147PM", "0151PM", "0153PM", "0154PM", "0217PM", ]

directory = os.fsencode('attacks')

imgs = []
templates = []
wizard = []

def find_cv2(image_str, region='all'):
    # if not PRINT_CV2:
    #     print("Find cv2", image_str)
    if region == 'all':
        pag.screenshot('temp.png')
    else:
        pag.screenshot('temp.png', region=region)
    screen = cv2.imread('temp.png', 0)
    template = cv2.imread(f'images/{image_str}.png', 0)
    if template is None:
        print("click_cv2: couldn't find file:", image_str)
        return 0, (0,0), (0,0,0,0)
    y, x = template.shape
    result = cv2.matchTemplate(screen, template, method)
    min_val, val, min_loc, loc = cv2.minMaxLoc(result)
    val = round(val,2)
    if region == 'all':
        region_start = (0,0)
    else:
        region_start = (region[0],region[1])

    loc = (region_start[0] + loc[0], region_start[1] + loc[1])
    rect = (loc[0], loc[1], x, y)
    print(f"find_cv2: {image_str} val={round(val,2)} loc={loc} rect={rect}")
    return val, loc, rect

count = 0
for file in os.listdir(directory):
    if count < 20:
        filename = os.fsdecode(file)
        file = f'attacks/{filename}'
        print(file)
        img = cv2.imread(file, 1)
        img = img[200:650, 500:1300]
        imgs.append((filename, img))
    count += 1

EAGLE = ["eagle", "eagle2", "eagle3", "eagle4"]
TH6 = ["th6"]
TH7 = ["th7", "th7b", "th7c",]
TH8 = ["th8"]
TH9 = ["th9"]
TH10 = ["th10"]
TH11 = ["th11"]
TH12 = ["th12"]
TH13 = ["th13"]
TH = TH6+ TH7+ TH8+ TH9+ TH10+ TH11+ TH12+ TH13

# Add rects to screenshots
def find_tower(i, array):
    max_val = 0
    max_rect = None
    for template in array:
        val, loc, rect = find_cv2(i, template)
        if val > max_val:
            max_val = val
            max_rect = rect
    return max_val, max_rect

def find_th(img, array=TH):
    img_orig = img.copy()
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    for x in array:
        val, rect = find_tower(img, x)


    defences = []
    max_val = 0
    max_rect = None
    for template in TH:
        rects = find_cv2(templates, img, 0.63)
        for x in rects: cv2.rectangle(img_orig, x, (255,255,255), 1)
        if len(rects) > 0:
            defences.append((type, score))
    defence_score = calc_score_sub(defences)
    print(img_name, ":", defences)
    # img_orig = cv2.resize(img_orig, (0, 0), fx=0.6, fy=0.6)
    cv2.imshow(f'{img_name}: {defence_score}', img_orig)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


