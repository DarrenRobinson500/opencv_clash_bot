import cv2
import pyautogui as pag
import time
# from bot import click_cv2
from tracker import *
method = cv2.TM_CCOEFF_NORMED

frames = 20
def save_video():
    click_cv2('bluestacks_icon')
    time.sleep(.2)
    for x in range(frames):
        pag.screenshot(f'temp_tracker{x}.png')
    click_cv2('bluestacks_icon')

def get_video():
    video = []
    for x in range(frames):
        image = cv2.imread(f'temp_tracker{x}.png', 1)
        video.append(image)
    return video

def replay_video():
    tracker = EuclideanDistTracker()
    video = get_video()
    ad = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=120)
    detections = []
    for i in video:
        i = cv2.resize(i, (0,0), fx=0.85, fy=0.85)

        # Object detection
        mask = ad.apply(i)
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 30:
                # cv2.drawContours(i, [contour], -1, (0,255,0),2)
                x, y, w, h = cv2.boundingRect(contour)
                detections.append([x,y,w,h])

        # Object tracking
        ids = tracker.update(detections)
        print(ids)
        for id_info in ids:
            x, y, w, h, id = id_info
            cv2.putText(i, str(id), (x, y-15), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 2)
            cv2.rectangle(i, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # cv2.imshow("Mask", mask)
        cv2.imshow("Original", i)
        key = cv2.waitKey(30)
        if key == 27:
            break

    cv2.destroyAllWindows()

replay_video()