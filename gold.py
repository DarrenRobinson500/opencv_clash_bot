import pyautogui as pag
import cv2
import numpy as np
from collections import Counter
method = cv2.TM_CCOEFF_NORMED

# towns_str = ["attack 0153AM", "attack 0158AM", "attack 0226AM", "attack 0231AM", "attack 0252PM", "attack 0253PM", "attack 0257PM", "attack 0303PM", "attack 0309PM", "attack 0314PM", "attack 0320PM", "attack 0326PM", "attack 0329PM", "attack 0332PM", "attack 0333PM", "attack 0336PM", "attack 0941PM", "attack 1001PM", "attack 1023PM", "attack 1108PM", "attack 1131PM", "attack 1216AM", ]
towns_str = ["attack 0226AM", "attack 0231AM", "attack 0252PM", "attack 0253PM", "attack 0257PM", "attack 0303PM", "attack 0309PM", "attack 0314PM", "attack 0320PM", "attack 0326PM", "attack 0329PM", "attack 0332PM", "attack 0333PM", "attack 0336PM", "attack 0941PM", "attack 1001PM", "attack 1023PM", "attack 1108PM", "attack 1131PM", "attack 1216AM", ]
mines = ["gold1", "gold2", "gold3"]
# grass = ["grass", "tree1",]
grass = ["tree1",]

towns = []
buff = 0
for x in towns_str: towns.append((x, cv2.imread(f'attacks/{x}.png', 0), cv2.imread(f'attacks/{x}.png', 1)))

def find_many(templates, screen, region='all', confidence=0.6):
# Get screen
#     if region == 'all':
#         pag.screenshot('temp.png')
#     else:
#         pag.screenshot('temp.png', region=region)
#     screen = cv2.imread('temp.png', 0)

# Set up output array
    rects = []

# Loop through templates
    for template_str in templates:
        template = cv2.imread(f'images/{template_str}.png', 0)
        if template is None:
            print("click_cv2: couldn't find file:", template_str)
        else:
            h, w = template.shape
            result = cv2.matchTemplate(screen, template, method)
            yloc, xloc = np.where(result >= confidence)
            z = zip(xloc, yloc)

            for (x, y) in z:
                rects.append([int(x) - buff, int(y) - buff, int(w) + buff * 2, int(h) + buff * 2])
                rects.append([int(x) - buff, int(y) - buff, int(w) + buff * 2, int(h) + buff * 2])
    rects, weights = cv2.groupRectangles(rects, 1, 0.2)

    return rects

def simplify(i, gradients=2):
    factor = 256 / gradients
    new = i
    l = []
    for row in new:
        for pixel in row:
            for c in range(3):
                pixel[c] = int(pixel[c] / factor) * factor
            if pixel[2] > pixel[1] + 50 and pixel[2] > pixel[0] + 50:
                pixel[0], pixel[1], pixel[2] = 255,255,255
            l.append((pixel[0],pixel[1],pixel[2]))
    return new

def dist(a,b):
    result = ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5
    result = abs(a[0] - b[0]) * 0.75 + abs(a[1] - b[1])
    result = int(result / 5) * 5
    return result

def bw(i):
    i2 = i.copy()
    factor = 256 / 8
    h, w, channel = i.shape
    center = (w//2, h//2)
    for y in range(h):
        for x in range(w):
            pixel = i2[y][x]
            for c in range(3):
                pixel[c] = int(pixel[c] / factor) * factor
            if dist(center, (x, y)) < 50:
                pixel[0], pixel[1], pixel[2] = 0, 0, 0
            if pixel[2] == 192 and pixel[1] == 128 and pixel[0] == 32 or pixel[2] == 192 and pixel[1] == 160 and pixel[0] == 64:
                pixel[0], pixel[1], pixel[2] = 255,255,255
            else:
                pixel[0], pixel[1], pixel[2] = 0,0,0
    # show(i)
    return i

def enhance(i):
    i2 = i.copy()
    h, w, channel = i.shape
    for y in range(h):
        for x in range(w):
            pixel = i2[y][x]
            if count_nearby(x, y, i, 2) >= 5:
                pixel[0], pixel[1], pixel[2] = 255,255,255
            else:
                pixel[0], pixel[1], pixel[2] = 0,0,0
    # show(i2)
    return i2

def count_nearby(x,y,i, r):
    count = 0
    for x1 in range(x-r, x+r):
        for y1 in range(y-r, y+r):
            try:
                if i[y1][x1][0] == 255: count += 1
            except:
                pass
    return count


RED_COLOURS = [(32, 96, 160),]
def find_drop_point(i):
    # show(i)
    factor = 256 / 8
    d = []
    h, w, channel = i.shape
    center = (w//2, h//2)
    min_dist = 500
    min_pixel = None
    i2 = bw(i)
    i3 = enhance(i2)
    i4 = enhance(i3)

    for y in range(h):
        for x in range(w):
            pixel = i4[y][x]
            if pixel[2] == 255:
                distance = dist(center, (x,y))
                d.append(distance)

    try:
        most_common = Counter(d).most_common(1)[0][0]
    except:
        most_common = 100

    for y in range(h):
        for x in range(w):
            pixel = i4[y][x]
            if pixel[2] == 255:
                distance = dist(center, (x,y))
                d.append(distance)
                if most_common <= distance < min_dist:
                    min_dist = distance
                    min_pixel = [x, y]

    if min_pixel:
        print(min_pixel, center)
        x, y = min_pixel
        min_pixel = [int(center[0] + (x - center[0]) * 1.4), int(center[1] + (y-center[1]) * 1.4 )]

        box_size = 6
        for x in range(min_pixel[0]-box_size, min_pixel[0]+box_size):
            for y in range(min_pixel[1] - box_size, min_pixel[1] + box_size):
                try:
                    i[y][x] = (0,0,255)
                except:
                    pass
    # show(i)
    return i

def find_drop_point_old(i):
    factor = 256 / 8
    l = []
    l_original = []
    h, w, channel = i.shape
    ne, nw, se, sw = 0,0,0,0
    for y in range(h):
        for x in range(w):
            pixel = i[y][x]
            for c in range(3):
                pixel[c] = int(pixel[c] / factor) * factor
            # if pixel[2] == 192 and pixel[1] == 160 and pixel[0] == 64:
            if pixel[2] == 192 and pixel[1] == 128 and pixel[0] == 32 or pixel[2] == 192 and pixel[1] == 160 and pixel[0] == 64:
            # if pixel[2] > pixel[1] + 50 and pixel[2] > pixel[0] + 50:
            #     l.append((pixel[0], pixel[1], pixel[2]))
            #     pixel[0], pixel[1], pixel[2] = 255,255,255
                if x > w / 2 and y < h / 2: ne += 1
                if x > w / 2 and y > h / 2: se += 1
                if x < w / 2 and y < h / 2: nw += 1
                if x < w / 2 and y < h / 2: sw += 1
            # else:
                # pixel[0], pixel[1], pixel[2] = 0,0,0

    max_dir = max(ne, nw, se, sw)
    if ne == max_dir: result = (1, -1)
    elif nw == max_dir: result = (-1, -1)
    elif se == max_dir: result = (1, 1)
    else: result = (-1, 1)
    print(result)
    coords = (w / 2 * (1 + result[0]), h / 2 * (1 + result[1]))
    print("Coords:", coords)
    rect_size = 10
    print(coords[1], rect_size/2, coords[1] + rect_size/2)
    rect = (int(coords[0]), int(coords[1]), int(coords[0]) + 1, int(coords[1]) + 1)
    print(rect)
    i = cv2.rectangle(i, rect, (0, 0, 255), 20)
    print(result, max_dir)
    # print(Counter(l))
    return i

def find_drop_point_old(i):
    factor = 256 / 8
    l = []
    h, w, channel = i.shape
    print(h, w)
    for row in i:
        for pixel in row:
            for c in range(3):
                pixel[c] = int(pixel[c] / factor) * factor
            if pixel[2] > pixel[1] + 50 and pixel[2] > pixel[0] + 50:
                pixel[0], pixel[1], pixel[2] = 255,255,255
            l.append((pixel[0],pixel[1],pixel[2]))
    return i


def quantify(i):
    new = i
    l = []
    for row in new:
        for pixel in row:
            l.append((pixel[0],pixel[1],pixel[2]))
    return Counter(l)

def create_region(i, region):
    x, y, h, w = region
    new = np.zeros((h,w,3), np.uint8)
    y2 = 0
    for y1 in range(y, y + h):
        x2 = 0
        for x1 in range(x, x + w):
            pixel = i[y1][x1]
            new[y2, x2] = pixel
            x2 += 1
        y2 += 1
    return new

def show(i):
    cv2.imshow("", i)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def add_rects(rectangles, image, shade=255):
    for x in rectangles:
        top_left = (x[0], x[1])
        bottom_right = (x[0] + x[2], x[1] + x[3])
        image = cv2.rectangle(image, top_left, bottom_right, (shade, shade, shade), 3)
    return image

def drop_points(r, image):
    range_y = 70
    range_x = int(range_y * 4/3)
    x, y, w, h = r
    center_x = x + w//2
    center_y = y + w//2
    town_center_h, town_center_w, channels = image.shape
    town_center_x = town_center_w // 2
    town_center_y = town_center_h // 2
    if center_x > town_center_x:
        dp_x = center_x + range_x
    else:
        dp_x = center_x - range_x
    if center_y > town_center_y:
        dp_y = center_y + range_y
    else:
        dp_y = center_y - range_y
    dp = (dp_x, dp_y)
    image = cv2.circle(image, dp, 3, (255,255,255), 3)
    # show(image)
    return dp

def main():
    no_of_towns = 1
    # count = 1
    for name, town, town_colour in towns:
        # if count <= no_of_towns:
            rectangles = find_many(mines, town)
            for r in rectangles:
                dps = drop_points(r, town_colour)
            #     region = create_region(town_colour, r)
            #     region = find_drop_point(region)
            #     show(region)
            add_rects(rectangles, town_colour)


            cv2.imshow(name, town_colour)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        # count += 1

main()