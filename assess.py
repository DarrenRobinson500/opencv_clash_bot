import numpy as np
import cv2
import os
method = cv2.TM_CCOEFF_NORMED

# img_str = ["attack 0153AM", "attack 0158AM", "attack 0226AM", "attack 0231AM", "attack 0252PM", "attack 0253PM", "attack 0257PM", "attack 0303PM", "attack 0309PM", "attack 0314PM", "attack 0320PM", "attack 0326PM", "attack 0329PM", "attack 0332PM", "attack 0333PM", "attack 0336PM", "attack 0941PM", "attack 1001PM", "attack 1023PM", "attack 1108PM", "attack 1131PM", "attack 1216AM", ]
# img_str = ["attack 0153AM", "attack 1001PM", "attack 1023PM", "attack 1108PM", "attack 1131PM", "attack 1216AM", ]
img_str = ["0109PM", "0112PM", "0125PM", "0133AM", "0135PM", "0138PM", "0145PM", "0147PM", "0151PM", "0153PM", "0154PM", "0217PM", ]

directory = os.fsencode('attacks')


imgs = []
templates = []
wizard = []

def find_many_img(templates, img, confidence=0.6):
# Set up output array
    rects = []

# Loop through templates
    for template_str in templates:
        template = cv2.imread(f'images/{template_str}.png', 0)
        if template is None:
            print("click_cv2: couldn't find file:", template_str)
        else:
            h, w = template.shape
            result = cv2.matchTemplate(img, template, method)
            yloc, xloc = np.where(result >= confidence)
            z = zip(xloc, yloc)

            for (x, y) in z:
                rects.append([int(x), int(y), int(w), int(h)])
                rects.append([int(x), int(y), int(w), int(h)])
    rects, weights = cv2.groupRectangles(rects, 1, 0.2)
    return rects

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


WIZARD_LOW = ["wizard1", "wizard3"]
WIZARD_MED = ["wizard_med", ]
WIZARD_HIGH = ["wizard8", "wizard10"]
INFERNO_LOW = ["inferno_low", "inferno_low2", "inferno_low3", "inferno_low4", "inferno_low5"]
INFERNO_HIGH = ["inferno_high", "inferno_high2", "inferno_high3", "inferno_high4", ]
CROSS_LOW = ["cross_low", "cross_low2", "cross_low3", "cross_low4", "cross_low5",]
CROSS_HIGH = ["cross_high", "cross_high2"]
EAGLE = ["eagle", "eagle2", "eagle3", "eagle4"]
TH6 = ["th6"]
TH7 = ["th7", "th7b", "th7c",]
TH8 = ["th8"]
TH9 = ["th9"]
TH10 = ["th10"]
TH11 = ["th11"]
TH12 = ["th12"]
TH13 = ["th13"]
TH_EAGLE = TH6 + TH7 + TH8 + TH9 + TH10 + TH11 + TH12 + TH13 + EAGLE

TOWERS = [
    ("Low Wizards", WIZARD_LOW, 2, "Wizard"),
    ("Med Wizards", WIZARD_MED, 3, "Wizard"),
    ("High Wizards", WIZARD_HIGH, 4, "Wizard"),
    ("Low Inferno", INFERNO_LOW, 6, "Inferno"),
    ("High Inferno", INFERNO_HIGH, 8, "Inferno"),
    ("Low Cross", CROSS_LOW, 5, "Cross"),
    ("High Cross", CROSS_HIGH, 7, "Cross"),
    ("Eagle", EAGLE, 14, "Inferno"),
    ("TH6", TH6, 1, "TH"),
    ("TH7", TH7, 2, "TH"),
    ("TH8", TH8, 3, "TH"),
    ("TH9", TH9, 5, "TH"),
    ("TH10", TH10, 7, "TH"),
    ("TH11", TH11, 10, "TH"),
    ("TH12", TH12, 13, "TH"),
    ("TH13", TH13, 17, "TH"),
]

def max2(list):
    try:
        return max(list)
    except:
        return 0

def calc_score_sub(defences):
    wizard = [item[1] for item in defences if item[0] == "Wizard"]
    inferno = [item[1] for item in defences if item[0] == "Inferno"]
    cross = [item[1] for item in defences if item[0] == "Cross"]
    eagle = [item[1] for item in defences if item[0] == "Eagle"]
    th = [item[1] for item in defences if item[0] == "TH"]
    result = max2(wizard) + max2(inferno) + max2(cross) + max2(eagle) + max2(th)
    print("TH:", max2(th), "Result", result)
    return result

# Add rects to screenshots
for img_name, img in imgs:
    img_orig = img.copy()
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    defences = []
    for name, templates, score, type in TOWERS:
        rects = find_many_img(templates, img, 0.63)
        for x in rects: cv2.rectangle(img_orig, x, (255,255,255), 1)
        if len(rects) > 0:
            defences.append((type, score))
    defence_score = calc_score_sub(defences)
    print(img_name, ":", defences)
    # img_orig = cv2.resize(img_orig, (0, 0), fx=0.6, fy=0.6)
    cv2.imshow(f'{img_name}: {defence_score}', img_orig)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


