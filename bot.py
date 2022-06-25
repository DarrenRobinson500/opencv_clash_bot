import cv2
import pyautogui as pag
import time
import os
import psutil
from datetime import datetime, timedelta
import pytesseract
import numpy as np
from PIL import Image
from collections import Counter
import sqlite3


pytesseract.pytesseract.tesseract_cmd = "c:\\Program Files\\Tesseract-OCR\\tesseract.exe"
method = cv2.TM_CCOEFF_NORMED

PRINT_CV2 = True
VERBOSE_LOG = False

TROOPS = ["barb", "archer", "giant","bomb", "wizard", "dragon", "edrag", "super_barb", "super_goblin",]
SPELLS = ["lightening",]
SIEGE = ["ram",]
MINES = ["gold1", "gold2", "gold3"]
ALL_TROOPS = TROOPS + SPELLS + SIEGE

HEROES_AND_RAMS = ["king", "queen","warden", "champ", "clan", "clan_ram", "ram", "ram_empty"]

DONT_DONATE = ["bomb", "super_goblin", ]
TROOP_TRAIN_EXT = ["wizard", "bomb", "super_goblin", "super_barb", "lightening", "dragon", ]
TROOP_ATTACK_EXT = ["super_goblin", "super_barb", ]
TROOP_DONATE_EXT = ["super_barb",]

# ===============
# === Regions ===
# ===============

ALL = (0,0,1919,1008)

# Main Screen
BUILDER_REGION = (655, 60, 225, 100)
BUILDER_LIST_REGION = (560, 239, 400, 300)
BUILDER_LIST_TIMES = (800, 239, 160, 50)
RESOURCES_G = (1426,80, 260, 47)
RESOURCES_E = (1426,172, 260, 47)
RESOURCES_D = (1514,261, 170, 47)
RESOURCES = (1420,60, 350, 250)
LEVEL = (115,67, 80, 80)

# Accounts
ACCOUNT_ICONS = (1136, 467, 110, 420)

# Donations
DONATE_BUTTONS =(520, 140, 205, 760)
DONATE_AREA = (795, 15, 860, 700)

# Main Screen - Build
BUILDER_LIST_TIMES_B = (1000, 240, 100, 30)
WIN_ZONE = (869,808, 130, 50)

# Army screen
ARMY_TABS = (151, 59, 1170, 85)
ARMY_TIME = (1079, 172, 90, 28)
ARMY_TIME_B = (900, 907, 154, 40)
ARMY_TROOPS = (318, 168, 150, 45)
CLAN_TROOPS = (631, 706, 75, 45)
TRAIN_RANGE = (166, 535, 1500, 370)
DELETE_REGION = (1650, 200, 50, 50)
ARMY_EXISTING = (160,221, 1030, 165)
SPELLS_EXISTING = (155,473, 950, 165)
ARMY_CREATE = (167, 544, 1500, 350)

# Army screen - builder

# Capital Coin
CAPITAL_COIN_TIME = (250,270, 175,50)
COIN_REGION = (150, 165, 150, 40)

# Attacking
TROOP_ZONE = (259, 831, 1350, 165)
DAMAGE = (1650,740, 75, 45)

# === COLOURS ===
AVAILABLE_GOLD_COLOURS = [(204, 251, 255),]
WHITE = [(255, 255, 255),(254, 254, 254),(253, 253, 253),]


# ================
# === DEFENCES ===
# ================

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
WIZARDS = WIZARD_HIGH + WIZARD_MED + WIZARD_LOW

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

# === ATTACKS ===
GIANT200 = {
            "gold_objective": 300000,
            "max_th": 8,
            "wizard_check": True,
            "bomb": True,
            "bomb_target": WIZARDS,
            "lightening": 7,
            "initial_troops": ["king", "clan",],
            "troop_group": [("giant", 5), ("bomb", 2), ("wizard", 5), ],
            "troop_groups": 4,
            "final_troops": ["wizard",],
            "troop_pause": 0,
            "drop_points": False,
            "drop_point_troops": ["super_goblin,"],
            "th_gold_adj": True,
        }

GIANT240 = {
            "gold_objective": 400000,
            "max_th": 9,
            "wizard_check": False,
            "bomb": True,
            "bomb_target": WIZARDS,
            "lightening": 11,
            "initial_troops": ["king", "clan", "clan_ram", "queen"],
            "troop_group": [("giant", 6), ("bomb", 2), ("wizard", 6), ],
            "troop_groups": 4,
            "final_troops": ["wizard", "wizard", ],
            "troop_pause": 0,
            "drop_points": False,
            "drop_point_troops": [],
            "th_gold_adj": False,
        }

BARBS = {
            "gold_objective": 300000,
            "max_th": 100,
            "wizard_check": False,
            "bomb": True,
            "bomb_target": EAGLE,
            "lightening": 11,
            "initial_troops": ["king", "ram_empty", "clan_ram", "queen", "warden", "champ"],
            "troop_group": [("super_barb", 56), ],
            "troop_groups": 1,
            "final_troops": [],
            "troop_pause": 0.45,
            "drop_points": False,
            "drop_point_troops": [],
            "th_gold_adj": False,
        }

GOBLIN = {
            "gold_objective": 500000,
            "max_th": 101,
            "wizard_check": False,
            "bomb": False,
            "bomb_target": [],
            "lightening": 0,
            "initial_troops": [],
            "troop_group": [("super_goblin", 12), ("edrag", 2), ("dragon", 2), ("giant", 15)], # This is used to define the min number required
            "troop_groups": 1,
            "final_troops": [],
            "drop_points": True,
            "drop_point_troops": ["super_goblin",],
            "th_gold_adj": False,
        }

FAV_ATTACK = [None, BARBS, GIANT240, GIANT200]


# === RESET ===
def reset():
    if "BlueStacksWeb.exe" in (p.name() for p in psutil.process_iter()):
        print("Bluestacks Running")
        timed_click('bluestacks_icon')
        timed_click('red_cross', (0,0), 0)
        timed_click('okay', (0,0), 0)
        timed_click('reload_game', (0, 0), 0)
        timed_click('try_again', (0, 0), 0)
        timed_click('bluestacks_message', (0, 0), 0)
    else:
        os.startfile("C:\Program Files (x86)\BlueStacks X\BlueStacks X.exe")
        wait('start_d')
        pag.click((338,603)) # this is the love heart
        wait_and_click('start_eyes')
        wait_and_click('maximise')
        wait("attack")

# === CLICKS ===
def wait(image):
    found = False
    count = 0
    while not found:
        image_location = pag.locateCenterOnScreen(f'images/{image}.png', confidence=0.8)
        if image_location:
            found = True
            # print(f"Found {image}")
            return image_location
        else:
            # print(f"{image} {count}")
            time.sleep(1)
            count += 1
        if count > 6:
            count = 0
            timed_click('bluestacks_icon', (0, 0), 2)
            timed_click('reload_game', (0, 0), 2)
    return

def find(image, confidence=0.55):
    result = pag.locateCenterOnScreen(f'images/{image}.png', confidence=confidence)
    # if not result:
    #     try:
    #         result = pag.locateCenterOnScreen(f'images/{image}1.png', confidence=confidence)
    #     except:
    #         pass
    # print(image, result)
    if result:
        result = True
    else:
        result = False
    return result

def wait_and_click(image, confidence=0.6):
    # print("Wait and click:", image)
    found = False
    count = 0
    while not found:
        image_location = pag.locateCenterOnScreen(f'images/{image}.png', confidence=confidence)
        if image_location:
            pag.click(image_location)
            found = True
        else:
            # print(f"{image} {count}")
            time.sleep(1)
            count += 1
        if count > 6:
            count = 0
            wait_and_click('bluestacks_icon')
    return

def timed_click(image, offset=(0,0), dur=0, confidence=0.6):
    found = False
    count = 0
    while not found and count <= dur:
        location = pag.locateCenterOnScreen(f'images/{image}.png', confidence=confidence)
        # if not location: # see if there's an alt image
        #     try:
        #         location = pag.locateCenterOnScreen(f'images/{image}1.png', confidence=confidence)
        #     except:
        #         pass
        if location:
            pag.click((location[0] + offset[0], location[1] + offset[1]))
            return True
        # else:
            # print(f"{image} {count}")
        time.sleep(1)
        count += 1
    return False

def intelligent_click(image1, offset1, image2, offset2, confidence=0.6):
    if timed_click(image2, offset2, 0): return
    timed_click(image1, offset1, 3, confidence)
    time.sleep(2)
    timed_click(image2, offset2, 3, confidence)
    return

def dual_click(image1, image2, confidence=0.6):
    for x in range(5):
        if find(image2):
            click_cv2(image2)
            time.sleep(0.15)
            return

        if find(image1):
            click_cv2(image1)
            time.sleep(0.15)
            dual_click(image1, image2, confidence)
        time.sleep(0.1)
    return False

# === 1. ACCOUNTS AND NAVIGATION ===
def change_accounts(account, target_base="main"):
    global current_account
    print("Change accounts")
    if account != current_account:
        if account == 1: loc = (1184, 651)
        elif account == 2: loc = (1184, 792)
        elif account == 3: loc = (1184, 524)
        else: return
        goto("switch_account")
        pag.click(loc)
        time.sleep(0.2)
        wait_many(["main","master", "otto", "okay"])
        if find_cv2("okay")[0] > 0.5:
            click_cv2("okay")
    goto(target_base)
    time.sleep(1)
    current_account = account
    print(f"Account check. Current '{current_account}'. Desired '{account}'")
    if current_account != account:
        change_accounts(account)
    return

# def goto_old(destination):
#     current_location = status()
#     if current_location == "main" and destination == "main":
#         # print("You desired to go to main and you're already there")
#         return
#     if current_location == "builder" and destination == "builder":
#         # print("You desired to go to builder and you're already there")
#         return
#     if destination == "builder":
#         # print("In main, trying to go to builder.")
#         pag.click(95, 985)
#         pag.drag(250, -450, 0.5, button='left')
#         click_cv2('boat')
#     if destination == "main":
#         # print("In builder, trying to go to main.")
#         pag.click(1780,234)
#         pag.drag(-250, 250, 0.5, button='left')
#         click_cv2('boat')

# === 2. REQUEST ===
def request(account):
    if account == 1: return
    print("Request")
    goto("army_tab")
    if click_cv2('request') > 0.7:
        if check_colour('request'):
            time.sleep(1)
            click_cv2('request_send')
    job_time = datetime.now()
    if account == 2 or account == 3:
        db_update(1, "donate", job_time)
    if account == 1:
        db_update(2, "donate", job_time)

# === 3. ATTACK ===
def attack(account, data=GIANT200):
    print("Attack Start")
    goto("main")
    db_update(account, "attack", datetime.now() + timedelta(minutes=30))

    # resource = current_resources()
    # resource_max = resource_limit()
    # if resource_max is None: resource_max = [10000000,0,0]
    # if resource is not None and 0.9 * resource_max[0] < resource[0] <= resource_max[0]:
    #     print("attack: over-resourced", )
    #     print(resource)
    #     result = db_read(account, 'build')
    #     if result:
    #         result += timedelta(minutes=5)
    #         db_update(account, "attack", result)
    #     else:
    #         print("Couldn't find time when build finishes")
    #     return
    if not attack_prep(account, data):
        print("attack: Troops not ready")
        db_update(account, "attack", get_time_attack())
        return
    print("Attack")
    goto("find_a_match")
    assess_village(account, data)
    time.sleep(.2)

def attack_prep(account, data):
    print("Attack prep")
    sufficient_troops = True
    troops_required = []
    troops_to_build = []
    for x in data['initial_troops']:
        troops_required.append(x)
    for x, no in data['troop_group']:
        for y in range(data['troop_groups'] * no):
            troops_required.append(x)
    for x in data['final_troops']:
        troops_required.append(x)
    requ = Counter(troops_required)
    time.sleep(0.2)
    print("A", datetime.now())
    goto("army_tab")

    # Lightening spells
    print("Lightening spells")
    print("B", datetime.now())
    actual = troop_count("lightening")
    required = data['lightening']
    print("C", datetime.now())
    print("Attack prep - create required", "lightening", required, actual)
    if actual < required:
        sufficient_troops = False
        text = f"Need more of these - make {required - actual} more"
        print("lightening", required, actual, text)
        troops_to_build += ["lightening"] * (required - actual)
        # troop_create("lightening", required - actual)
        # time.sleep(0.2)
        print("D", datetime.now())

    backlog_deleted = False
    # Delete unneeded troops
    print("Delete unneeded troops")
    print("E", datetime.now())

    for x in TROOPS:
        print("F", x, datetime.now())

        actual = troop_count(x)
        required = requ[x]
        print("Attack prep - delete unneeded", x, required, actual)
        if actual > required:
            text = f"Too many of these - get rid of {actual - required}"
            print(x, required, actual, text)
            if not backlog_deleted:
                troop_delete_backlog()
                backlog_deleted = True
            troop_delete(x, actual - required)

    # Create needed troops
    print("Create required troops")
    for x in requ:
        if x not in HEROES_AND_RAMS:
            print("Troop:", x)
            actual = troop_count(x)
            required = requ[x]
            if actual == required:
                text = "Perfect"
                print(x, required, actual, text)
            if actual < required:
                sufficient_troops = False
                text = f"Need more of these - make {required - actual} more"
                print(x, required, actual, text)
                if not backlog_deleted:
                    troop_delete_backlog()
                    backlog_deleted = True
                # troop_create(x, required - actual)
                troops_to_build += [x] * (required - actual)
                if account == 1:
                    troops_to_build += ["ram"]
    restock(troops_to_build)
    return sufficient_troops

def troop_delete_backlog():
    print("Troop delete backlog")
    goto("troops_tab")
    remaining_troops = True
    while remaining_troops:
        val, loc, rect = find_cv2("remove_troops", DELETE_REGION)
        center = pag.center(rect)
        if val > 0.7:
            for x in range(5): pag.click(center)
        else:
            remaining_troops = False

def troop_delete(troop, count):
    print("Troop delete")
    goto("army_tab")
    click_cv2("edit_army")
    for x in range(count):
        click_cv2(troop, ARMY_EXISTING)
    click_cv2("edit_army_okay")
    click_cv2("surrender_okay")

def restock(required_troops):
    print(required_troops)
    count = Counter(required_troops)

    for x in count:
        if x in TROOPS:
            goto("troops_tab")
            add_troops(x, count[x])

    for x in count:
        if x in SPELLS:
            goto("spells_tab")
            add_troops(x, count[x])

    for x in count:
        if x in SIEGE:
            goto("siege_tab")
            add_troops(x, count[x])

def add_troops(name, count):
    if name in TROOP_TRAIN_EXT: name += "_train"
    if name in SIEGE: name += "_big"
    val, loc, rect = find_cv2(name, ARMY_CREATE)
    center = pag.center(rect)
    for x in range(count):
        pag.click(center)
        time.sleep(0.05)



def troop_create(troop, count):
    print("Troop create: ", troop)
    if troop in SPELLS:
        goto("spells_tab")
    else:
        goto("troops_tab")

    name = troop
    if name in TROOP_TRAIN_EXT: name += "_train"
    val, loc, rect = find_cv2(name, ARMY_CREATE)
    center = pag.center(rect)
    for x in range(count):
        pag.click(center)
        time.sleep(0.05)

def troop_count(troop):
    goto("army_tab")
    time.sleep(.2)
    if troop in TROOPS:
        region = ARMY_EXISTING
    else:
        region = SPELLS_EXISTING

    val, loc, rect = find_cv2(troop, region)
    print("troop_count", val)
    if val < 0.6: return 0
    region = (loc[0] - 30, loc[1] - 70, 130, 80)
    result = read_num(region, troop, WHITE)
    try:
        return int(result)
    except:
        return 0

def assess_village(account, data):
    print("Assess village")
    time.sleep(0.5)

    # Need to check if its returned to main (due to a reload)
    if not wait_cv2("coin"): return

    post = datetime.now().strftime('%I%M%p')
    x = f'attacks/attack {post}.png'
    pag.screenshot(x)
    pag.screenshot("attacks/attack.png")

    # calc_score(cv2.imread("attacks/attack.png", 1))

    # Gold Check
    th = town_hall()
    if not wait_cv2("coin"): return
    gold_adj = 0
    if data['th_gold_adj']:
        gold_adj = (data['max_th'] - th) * 100000
    gold = available_gold() + gold_adj
    if gold < data['gold_objective']:
        print("Not enough gold")
        next_village(account, data)
        return

    # Advanced Town Hall
    if th > data['max_th']:
        print("Town Hall too high")
        next_village(account, data)
        return

    # Aggressive defences
    wizard_check = bad_wizards()
    if not wait_cv2("coin"): return
    if data['wizard_check'] and wizard_check:
        print("Bad wizards")
        next_village(account, data)
        return

    if data['drop_points']:
        mines = find_many_array(MINES)
        if len(mines) == 0:
            print("No identified mines")
            next_village(account, data)
            return

    # Good to go
    if data['drop_points']:
        launch_attack_dps(account, data)
    else:
        launch_attack(account, data)
    finish_attack(account, data)
    attack_prep(account, data)
    request(account)
    return

def next_village(account, data):
    print("Next attack")
    time.sleep(0.25)
    wait_and_click('next_attack')
    wait("end_battle")
    data['gold_objective'] -= 10000
    print("New gold objective:", data['gold_objective'])
    assess_village(account, data)

def launch_attack_dps(account, data):
    print("Launch attack dps")
    pag.click(1000, 1000)
    pag.drag(0, -400, 0.25, button='left')

    mines = find_many_array(MINES)
    town = cv2.imread('temp.png', 0)
    print(data)
    for m in mines:
        dp = drop_point(m, town)
        for troop in data["drop_point_troops"]:
            place(troop, 1, dp)
    time.sleep(10)
    click_cv2("surrender")
    click_cv2("surrender_okay")

def drop_point(r, image):
    range_y = 70
    range_x = int(range_y * 4/3)
    x, y, w, h = r
    center_x = x + w//2
    center_y = y + w//2
    town_center_h, town_center_w = image.shape
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

def launch_attack(account, data):
    standard_pace = True
    print("Launch attack: bomb wizards")
    if data['bomb']: bomb(data['bomb_target'])
    troop_pause = data['troop_pause']

    print("Launch attack: initial troops")
    for x in data['initial_troops']:
        place(x, 1)

    print("Launch attack: main troops")
    for x in range(data['troop_groups']):
        for troop, n in data['troop_group']:
            place(troop, n, troop_pause=troop_pause)
        damage = read_text(DAMAGE, WHITE,True)
        try:
            if int(damage) > 60:
                standard_pace = False
        except:
            pass
        print("launch_attack Damage:", damage)
        if standard_pace: time.sleep(3)
    if standard_pace: time.sleep(10)

    print("Launch attack: final troops")
    for x in data['final_troops']:
        place(x, 1)
    wait_cv2("return_home")

def place(troop, count, dp=[400,400], troop_pause=0):
    if troop in TROOP_ATTACK_EXT: troop = troop + "_attack"
    print("Place troops")
    dp1 = (dp[0],min(dp[1],815))
    val, loc, rect = find_cv2(troop, TROOP_ZONE)
    print("Place troops:", troop, val, loc)
    if val > 0.7:
        click_cv2(troop, TROOP_ZONE)
        time.sleep(1)
        for x in range(count):
            pag.click(dp1)
            time.sleep(troop_pause)
            time.sleep(0.2)

def has_spells():
    print("Has spells")
    lightening_buttons = find_many("lightening", TROOP_ZONE, 0.5)
    for x in lightening_buttons:
        if check_colour_rect(x):
            print("Has spells - True")
            return True, x
    print("Has spells - False")
    return False, None

def bomb_thrice(target):
    val, loc, rect = find_cv2(target)
    loc = (loc[0] + 10, loc[1] + 10)
    if val > 0.55:
        for x in range(3):
            pag.click(loc)
            time.sleep(0.1)

def bomb(targets):
    spells, loc = has_spells()
    click_cv2("lightening", TROOP_ZONE, 0.50)
    print("Bomb (initial):", spells)
    count = 0
    for x in targets:
        if count < 4:
            result = find_cv2(x)[0]
            if result > 0.7:
                print("Found target")
                bomb_thrice(x)
                count += 1

            result = find_cv2(x)[0]
            if result > 0.7:
                print("Found target again")
                bomb_thrice(x)
                count += 1
            else:
                print("Did not find {x}}. Val:", result)
        spells, loc = has_spells()
        print("Bomb (loop):", x, spells)
    return

def finish_attack(account, data):
    global current_location
    wait_cv2("return_home",max_time=80)
    current_location = "return_home"
    goto("main")

def train():
    print("Train")
    pag.click(95, 985)
    time.sleep(0.25)
    intelligent_click('army', (0,0), 'quick_train', (0,0))
    wait_and_click('train')
    timed_click('red_cross_training')


# def restock_old(required_troops):
#     goto("troops_tab")
#     print(required_troops)
#     for x in required_troops:
#         if x in TROOPS:
#             name = x
#             if name in TROOP_TRAIN_EXT: name += "_train"
#             click_cv2(name, ARMY_CREATE)
#
#     goto("spells_tab")
#     for x in required_troops:
#         if x in SPELLS:
#             click_cv2(x, TRAIN_RANGE)
#
#     if current_account == 1:
#         goto('siege_tab')
#         for x in required_troops:
#             if x in SIEGE:
#                 click_cv2('big_' + x, TRAIN_RANGE)

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

def calc_score(img):
    img_orig = img.copy()
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    defences = []
    for name, templates, score, type in TOWERS:
        rects = find_many_img(templates, img, 0.63)
        for x in rects: cv2.rectangle(img_orig, x, (255,255,255), 1)
        if len(rects) > 0:
            defences.append((type, score))
    result = calc_score_sub(defences)
    print("Calc score:", result)
    return result

# =================
# === 4. DONATE ===
# =================

def donate():
    print("Donate")
    goto("chat")
    requests = find_many("donate",DONATE_BUTTONS, 0.8)
    donations = []
    for x in requests:
        click_rect(x, DONATE_BUTTONS)
        for x in ALL_TROOPS:
            print("Donate:", x, DONT_DONATE)
            if x not in DONT_DONATE:
                name = x
                if name in TROOP_DONATE_EXT: name += "_donate"
                val, loc, rect = find_cv2(name, DONATE_AREA)
                while val > 0.65 and check_colour_rect(rect):
                    click_cv2(name, DONATE_AREA)
                    donations.append(x)
                    time.sleep(0.1)
                    val, loc, rect = find_cv2(name, DONATE_AREA)
        if find_cv2("donate_cross")[0] > 0.5:
            click_cv2("donate_cross")
    time.sleep(0.1)
    if len(donations) > 0:
        restock(donations)

# =============
# === Build ===
# =============
def build(account):
    goto("main")
    if find_cv2("builder_zero", BUILDER_REGION)[0] > 0.8:
        print("All builders occupied")
        job_time = get_time_build()
        if job_time is None:
            db_update(account, "build", datetime.now() + timedelta(minutes=20))
        else:
            db_update(account, "build", job_time)
        return
    resources = current_resources()
    if resources[0] > resources[1]:
        y_adj = 53
    else:
        y_adj = 100
    result = click_cv2("main", BUILDER_REGION)
    val, loc, rect = find_cv2("suggested_upgrades", BUILDER_LIST_REGION)
    print("Build. Value of suggested upgrades", val)
    if val > 0.5:
        pag.click(loc[0] + 50, loc[1] + y_adj)

    wait_and_click("upgrade")
    pag.click((933,877))
    timed_click("red_cross", (0,0), 3)
    if find_cv2("builder_zero", BUILDER_REGION)[0] > 0.8:
        print("All builders occupied")
        job_time = get_time_build()
        if job_time is None:
            db_update(account, "build", datetime.now() + timedelta(minutes=20))
        else:
            db_update(account, "build", job_time)
        return

# ============
# === COIN ===
# ============

def capital_coin():
    goto("coin")
    if find_cv2("collect_capital_coin")[0] > 0.7:
        click_cv2("collect_capital_coin")
    # capital_coin_time()

# ==========================
# === Object recognition ===
# ==========================

def check_colour_rect(region):
    print("Check colour rect")
    pag.screenshot('temp_colour.png', region)
    image = cv2.imread('temp_colour.png', 1)
    # cv2.imshow(f'Colour Check', image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    y, x, channels = image.shape

    count = 0
    spots =[(1/4, 1/4), (1/4, 3/4), (3/4, 1/4), (3/4, 3/4),]
    for s_x, s_y in spots:
        pixel = image[int(y * s_y)][int(x * s_x)]
        blue, green, red = int(pixel[0]), int(pixel[1]), int(pixel[2])
        if abs(blue-green) > 5 or abs(blue-red) > 5: count += 1
        print("Check colour (pixel):", pixel, count)
    colour = False
    if count > 1: colour = True
    print("Check colour", region, colour)
    return colour

def check_colour(image_str):
    pag.screenshot('temp_colour.png')
    screen = cv2.imread('temp_colour.png', 0)
    template = cv2.imread(f'images/{image_str}.png', 0)
    if template is None:
        print("check_colour: couldn't find file:", image_str)
        return 0
    y, x = template.shape
    result = cv2.matchTemplate(screen, template, method)
    min_val, val, min_loc, loc = cv2.minMaxLoc(result)
    region = (loc[0], loc[1], x, y)
    pag.screenshot('temp.png', region=region)
    image = cv2.imread('temp.png', 1)

    colour = False
    spots =[(1/4, 1/4), (1/4, 3/4), (3/4, 1/4), (3/4, 3/4),]
    for s_x, s_y in spots:
        pixel = image[int(y * s_y)][int(x * s_x)]
        if abs(pixel[0] - pixel[1]) > 5 or abs(pixel[0] - pixel[2]) > 5:  colour = True
        print("Check colour (pixel):", pixel, colour)
    print("Check colour", image_str, colour)
    return colour

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
        if PRINT_CV2:
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
    if PRINT_CV2:
        print(f"find_cv2: {image_str} val={round(val,2)} loc={loc} rect={rect}")
    return val, loc, rect

def find_many_image(template, i, confidence=0.6):
    template = cv2.imread(f'numbers/{template}.png', 0)
    h, w = template.shape

    result = cv2.matchTemplate(i, template, method)
    yloc, xloc = np.where(result >= confidence)
    z = zip(xloc, yloc)

    rectangles = []
    for (x, y) in z:
        rectangles.append([int(x), int(y), int(w), int(h)])
        rectangles.append([int(x), int(y), int(w), int(h)])
    rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)

    return rectangles

def find_many(image_str, region='all', confidence=0.6):
    print("find_many", region)
    if region == 'all':
        pag.screenshot('temp.png')
    else:
        pag.screenshot('temp.png', region=region)
    screen = cv2.imread('temp.png', 0)
    template = cv2.imread(f'images/{image_str}.png', 0)
    if template is None:
        print("click_cv2: couldn't find file:", image_str)
        return 0
    h, w = template.shape
    result = cv2.matchTemplate(screen, template, method)
    yloc, xloc = np.where(result >= confidence)
    if region != "all":
        z = zip(xloc, yloc)
    else:
        z = zip(region[0]+xloc, region[1]+yloc)

    rectangles = []
    for (x, y) in z:
        rectangles.append([int(x), int(y), int(w), int(h)])
        rectangles.append([int(x), int(y), int(w), int(h)])
    rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)

    # print("find_many", image_str, z)
    return rectangles

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

def find_many_array(templates, region='all', confidence=0.6):
# Get screen
    if region == 'all':
        pag.screenshot('temp.png')
    else:
        pag.screenshot('temp.png', region=region)
    screen = cv2.imread('temp.png', 0)

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
                rects.append([int(x), int(y), int(w), int(h)])
                rects.append([int(x), int(y), int(w), int(h)])
    rects, weights = cv2.groupRectangles(rects, 1, 0.2)

    return rects

def wait_cv2(image_str, region='all', confidence=0.7, max_time=20):
    template = cv2.imread(f'images/{image_str}.png', 0)
    if template is None:
        print("click_cv2: couldn't find file:", image_str)
        return 0
    found = False
    count = 0
    while not found:
        if region == 'all':
            pag.screenshot('temp.png')
        else:
            pag.screenshot('temp.png', region=region)
        screen = cv2.imread('temp.png', 0)

        result = cv2.matchTemplate(screen, template, method)
        min_val, val, min_loc, loc = cv2.minMaxLoc(result)
        val = round(val, 2)

        if val > confidence:
            print("wait_cv2", image_str, val)
            return val
        else:
            time.sleep(1)
            count += 1
        if count > max_time:
            return False
    return

def wait_many(images, region='all', confidence=0.7):
    print("Wait many")
    templates = []
    for x in images:
        template = cv2.imread(f'images/{x}.png', 0)
        if template is None:
            print("click_cv2: couldn't find file:", x)
        else:
            templates.append(template)

    found = False
    count = 0
    while not found:
        # Update the screenshot
        if region == 'all':
            pag.screenshot('temp_wait.png')
        else:
            pag.screenshot('temp_wait.png', region=region)
        screen = cv2.imread('temp_wait.png', 0)

        # Loop through the templates
        for template in templates:
            result = cv2.matchTemplate(screen, template, method)
            min_val, val, min_loc, loc = cv2.minMaxLoc(result)
            if val > confidence:
                print("wait_many", images, round(val, 2))
                return val

        # Iterate every second
        time.sleep(1)
        count += 1

        # Panic every 10 seconds
        if count % 10 == 0:
            count = 0
            timed_click('bluestacks_icon', (0, 0), 0)
            timed_click('reload_game', (0, 0), 0)
            timed_click('try_again', (0, 0), 0)
    return

def click_cv2(image_str, region='all', confidence=0.6):
    if region == 'all':
        pag.screenshot('temp.png')
    else:
        pag.screenshot('temp.png', region=region)
    screen = cv2.imread('temp.png', 0)
    template = cv2.imread(f'images/{image_str}.png', 0)
    if template is None:
        print("click_cv2: couldn't find file:", image_str)
        return
    y, x = template.shape
    # print(x,y)
    result = cv2.matchTemplate(screen, template, method)
    min_val, val, min_loc, loc = cv2.minMaxLoc(result)
    val = round(val,2)
    if val > confidence:
        if region == 'all':
            pag.click(loc[0] + x/2, loc[1] + y/2)
        else:
            pag.click(region[0] + loc[0] + x / 2, region[1] + loc[1] + y / 2)
    if PRINT_CV2:
        print("click_cv:", image_str, val, loc)
    time.sleep(0.25)
    # print(f"click_cv2: {image_str} val={round(val,2)} loc={loc}")
    return val

def click_rect(rectangle,region):
    x, y, w, h = rectangle
    pag.click(region[0] + x + w/2, region[1] + y + h/2)
    return

# def status():
#     if "BlueStacksWeb.exe" in (p.name() for p in psutil.process_iter()):
#         return base()
#     else:
#         return "Not running"

# def base():
#     # Get screenshot of builder region
#     pag.screenshot('builder_info.png', region=BUILDER_REGION)
#     screen = cv2.imread('builder_info.png', 0)
#
#     # Get templates
#     template_str = ["main", "builder", "otto"]
#     templates = []
#     for x in template_str: templates.append((x, cv2.imread(f'images/{x}.png', 0)))
#
#     method = cv2.TM_CCOEFF_NORMED
#
#     max_value = 0
#     max_name = ""
#     for name, template in templates:
#         result = cv2.matchTemplate(screen, template, method)
#         min_val, val, min_loc, loc = cv2.minMaxLoc(result)
#         # print(name, round(val,2))
#         if val > max_value:
#             max_value = val
#             max_name = name
#     if max_name == "otto": max_name = "builder"
#     if max_value > 0.7: return max_name
#     return "unidentified"

def town_hall():
    img = cv2.imread(f'attacks/attack.png', 0)
    template_str = [("th6",6), ("th7",7), ("th8",8), ("th9",9),]
    templates = []
    for name, number in template_str: templates.append((number, cv2.imread(f'templates/{name}.png', 0)))
    method = cv2.TM_CCOEFF_NORMED

    max_value = 0.5
    max_th = 100
    for number, template in templates:
        result = cv2.matchTemplate(img, template, method)
        min_val, val, min_loc, location = cv2.minMaxLoc(result)
        if val > max_value:
            max_value = val
            max_th = number
    print("Town Hall Identified as:", max_th)
    return max_th

def bad_wizards():
    img = cv2.imread(f'attacks/attack.png', 0)
    template_str = [("wizard8",8), ]
    templates = []
    for name, number in template_str: templates.append((number, cv2.imread(f'templates/{name}.png', 0)))
    method = cv2.TM_CCOEFF_NORMED

    max_value = 0
    for number, template in templates:
        result = cv2.matchTemplate(img, template, method)
        min_val, val, min_loc, location = cv2.minMaxLoc(result)
        if val > max_value:
            max_value = val
    if max_value > 0.7:
        print("Found a bad wizard")
        return True
    return False

def get_resources():
    goto("main")
    finished = False
    result = [500, 300]
    while not finished:
        time.sleep(1)
        pag.screenshot('whole_screen.png')
        i = np.asarray(Image.open('whole_screen.png'))
        background_colour = [(215, 220, 184), (176, 186, 120), (176, 188, 120)]
        result = see_resources_background(i, background_colour, result[0], result[1])
        if result:
            pag.click(result)
        else:
            finished = True
    return

# ===========
# === OCR ===
# ===========
def read_text(region, text_colours, numbers=False):
    pag.screenshot('temp2.png', region=region)
    i = cv2.imread("temp2.png", 1)
    # cv2.imshow("", i)
    if text_colours:
        i = only_colours(i, text_colours)
        # cv2.imshow("", i)
        # cv2.waitKey(0)
    result = pytesseract.image_to_string(i)
    if result == "'xl": result = '21'
    if VERBOSE_LOG: print(f"read_text pre number adj: '{result}'")

    if numbers:
        try:
            result = alpha_to_numbers(result)
            result = get_numbers(result)
        except:
            result = 0
    # print("read_text", result)
    return result

def number(str):
    try:
        return int(str)
    except:
        return 0

def read_num(region, troop, colour=WHITE):
    print("Read num")
    pag.screenshot('temp2.png', region=region)
    i = cv2.imread(f"temp2.png", 1)
    i = only_colours(i, colour)
    i = cv2.cvtColor(i, cv2.COLOR_BGR2GRAY)
    cv2.imshow("Image", i)
    # cv2.waitKey(0)

    found = []
    for y in range(10):
        rects = find_many_image(str(y), i, 0.8)
        if len(rects) > 0:
            for rect in rects:
                found.append((y, rect[0]))
    result = 0
    print(found)
    if len(found) == 2:
        if found[1][1] > found[0][1]: result = found[0][0] * 10 + found[1][0]
        else: result = found[1][0] * 10 + found[0][0]
    elif len(found) == 1:
        result = found[0][0]

    print(result)
    # cv2.imshow("Image", i)
    # cv2.waitKey(0)

    return result

def read_army_time(region, colour=WHITE):
    SCALE = 1.29
    pag.screenshot('temp2.png', region=region)
    i = cv2.imread(f"temp2.png", 1)
    i = cv2.resize(i, (0,0), fx=SCALE, fy=SCALE)
    i = only_colours(i, colour)
    i = cv2.cvtColor(i, cv2.COLOR_BGR2GRAY)

    found = []
    for y in [0,1,2,3,4,5,6,7,8,9,"m","s",]:
        rects = find_many_image(str(y), i, 0.75)
        if len(rects) > 0:
            for rect in rects:
                found.append((str(y), rect[0]))
    result = ""
    found.sort(key=lambda tup: tup[1])
    for y in found:
        result += y[0]
    print("Read army time:", found, "=>", result)
    return result

def available_gold():
    wait("end_battle")
    time.sleep(1)
    result = read_text(COIN_REGION, AVAILABLE_GOLD_COLOURS, True)
    # print("Available Gold:", result)
    return result

def current_resources():
    time.sleep(1)
    result_array = []
    for x in [RESOURCES_G, RESOURCES_E, RESOURCES_D]:
        result_array.append(read_text(x, WHITE, True))
    if result_array[0] > 20000000: result_array[0] = result_array[0]/10
    # print("Current Resources:", result_array)
    return result_array

def resource_limit():
    time.sleep(1)
    result_array = []
    for x in [RESOURCES_G, RESOURCES_E, RESOURCES_D, ]:
        pag.click(pag.center(x))
        region = x[0]+100, x[1]+70, x[2], x[3]
        result = read_text(region, WHITE, True)
        print(result)
        pag.click(95, 985)
        time.sleep(0.1)
        result_array.append(result)
    return result_array

def waiting(seconds):
    time.sleep(seconds)

def time_to_army_ready():
    goto("army_tab")
    time = army_time() + 1
    print("time_to_army_ready:", time)
    return time

# def army_troops():
#     click_cv2("army")
#     wait_cv2("army_tab")
#     time.sleep(3)
#     result = read_text(ARMY_TROOPS, WHITE, False)
#     print(result[0:3])
#     if result[0:3] == "rii": result = "200/200"
#     space = result.find("/")
#     for x in range(5):
#         if space < 0:
#             time.sleep(2)
#             result = read_text(ARMY_TROOPS, WHITE, False)
#             space = result.find("/")
#
#     if space > 0:
#         max_troops = result[space+1:]
#         if max_troops == 0: max_troops = 200
#         current_troops = result[0:space]
#         # print(current_troops, max_troops)
#     try:
#         result = round(int(current_troops) / int(max_troops),2)
#     except:
#         result = 0
#     return result

def clan_troops():
    click_cv2("army")
    wait_cv2("army_tab")
    time.sleep(3)
    result = read_text(CLAN_TROOPS, WHITE, False)
    space = result.find("/")
    pag.click(95, 985)

    if space > 0:
        max_troops = result[space+1:]
        if max_troops == 0: max_troops = 20
        current_troops = result[0:space]
        # print(current_troops, max_troops)
    try:
        result = round(int(current_troops) / int(max_troops),2)
    except:
        result = 0
    print("clan_troops", result)
    return result

def army_time():
    result = read_army_time(ARMY_TIME, WHITE)
    try:
        if result[-1] == "s":
            print("army_time:", 1)
            return 1 # ie 1 minute
        else:
            result = int(result[0:-1])
            result = min(20, result)
            print("army_time:", result)
            return result
    except:
        print("army_time: Failed to read screenshot")
        return 0

def capital_coin_time():
    goto("coin")
    result = read_text(CAPITAL_COIN_TIME, WHITE)
    try:
        result = alpha_to_numbers(result[0][1])
        result = string_to_time(result)
        print("Capital coin time:",result)
    except:
        print("Failed to read screenshot")
        print(result)
    return result

def get_numbers(string):
    new_string = "0"
    for x in string:
        if x.isdigit():
            new_string += x
    return int(new_string)

def alpha_to_numbers(string):
    if len(string) == 0: return ""
    if VERBOSE_LOG: print("alpha_to_numbers Pre:", string)
    string = string.replace("xl", "21")
    string = string.replace("xs", "20")
    string = string.replace("[", "0")
    # string = string.replace("d", "0")
    string = string.replace("I", "1")
    string = string.replace("T", "1")
    string = string.replace("t", "1")
    string = string.replace("l", "1")
    string = string.replace("i", "1")
    string = string.replace("J", "1")
    string = string.replace("e", "2")
    string = string.replace("é", "2")
    string = string.replace("Z", "2")
    string = string.replace("z", "2")
    string = string.replace("A", "4")
    string = string.replace("S", "5")
    string = string.replace("Q", "4")
    string = string.replace("B", "8")
    string = string.replace("g", "9")
    string = string.replace("O", "0")
    string = string.replace("o", "0")
    string = string.replace("u", "H")
    string = string.replace("q ", " ")
    string = string.replace("-", "")
    string = string.replace("~", "")
    string = string.replace("//", "/")
    string = string.replace("/p", "/")
    if string[-1] == "5": string = string[0:-2] + "s"
    if VERBOSE_LOG: print("alpha_to_numbers Post:", string)
    return string

def text_to_time(string):
    print(f"text_to_time:{string}")
    space = string.find(" ")

    if string[space-1].isdigit():
        if string[-1] == "M":
            string = string.replace(" ", "H ")
            space = string.find(" ")
        if string[-1] == "s":
            string = string.replace(" ", "M ")
            space = string.find(" ")

    days, hours, minutes, seconds = 0,0,0,0
    mode = string[space-1]
    print("Mode:", mode)
    if mode == "t": mode = "H"
    if mode == "M":
        minutes = string[0:space-1]
        seconds = string[space+1:-2]
    if mode.lower() == "h":
        hours = string[0:space-1]
        minutes = string[space+1:-2]
    if mode == "d":
        days = string[0:space-1]
        hours = string[space+1:-2]

    try:
        days = int(days)
        hours = int(hours)
        minutes = int(minutes)
        seconds = int(seconds)
    except:
        return None
    if days == 0 and hours == 0 and minutes == 0 and seconds == 0: return None
    print("Clean time", days, hours, minutes, seconds)
    finish = datetime.now() + timedelta(days=days) + timedelta(hours=hours) + timedelta(minutes=minutes) + timedelta(seconds=seconds)
    print("Finish time", finish)

    return finish


# === IMAGE MANAGEMENT ===
def simplify(i, gradients=2):
    factor = 256 / gradients
    new = i
    l = []
    for row in new:
        for pixel in row:
            for c in range(3):
                pixel[c] = int(pixel[c] / factor) * factor
            l.append((pixel[0],pixel[1],pixel[2]))
    return new, Counter(l)

def only_colours(i, colours):
    new = i
    for row in new:
        for pixel in row:
            if (pixel[0],pixel[1],pixel[2]) not in colours:
                pixel[0], pixel[1], pixel[2] = 255, 255, 255
            else:
                pixel[0], pixel[1], pixel[2] = 0, 0, 0
    return new

def see_resources_background(i, background_colour, x, y):
    x_max, y_max = len(i[0]), len(i)
    found = False
    while not found:
        pixel = i[y][x]
        if (pixel[0], pixel[1], pixel[2]) in background_colour: return [x,y]
        x += 1
        if x > x_max - 500:
            x = 200
            y += 1
            if y > y_max - 300:
                return

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
    return new


# === DATABASE ===
def db(db_str):
    con = sqlite3.connect('data.db')
    c = con.cursor()
    print(db_str)
    c.execute(db_str)
    output = c.fetchall()
    con.commit()
    con.close()
    return output

def db_update(account, job, time):
    db_str = f"SELECT * FROM jobs WHERE account='{account}' and job = '{job}'"
    existing = len(db(db_str))
    print("Current Records: ", existing)
    if existing == 1:
        db_str = f"UPDATE jobs SET time='{time}' WHERE account = {account} AND job = '{job}'"
        db(db_str)
    else:
        print("Records not updated")

def db_next_job():
    db_str = "SELECT * FROM jobs ORDER BY time"
    return db(db_str)[0]

def db_view(account='all'):
    if account == 'all':
        db_str = "SELECT * FROM jobs ORDER BY time"
    else:
        db_str = f"SELECT * FROM jobs WHERE account='{account}' ORDER BY time"
    output = db(db_str)
    count = 0
    for x in output:
        if count < 5:
            time = string_to_time(x[2])
            time = time_to_string(time)
            tabs = "\t"
            if len(x[1]) <= 5: tabs += "\t"
            if len(x[1]) <= 9: tabs += "\t"
            print("Account:", x[0], " Job:", x[1], tabs + "Time:", time)
        count += 1

def string_to_time(time):
    try:
        return datetime.fromisoformat(time)
    except:
        return datetime.now()

def time_to_string(time):
    if time <= datetime.now():
        return "Now"
    else:
        return time.strftime('%d %b %I:%M%p')

def db_read(account, job):
    db_str = f"SELECT * FROM jobs WHERE account='{account}' AND job = '{job}' ORDER BY time"
    x = db(db_str)
    if len(x) == 1 and x[0][2] is not None and x[0][2] != "None":
        time = datetime.fromisoformat(x[0][2])
    else:
        time = None
    # print(time)
    # print(time.astimezone().isoformat())
    return time

# === JOBS ===
def run_job(job):
    print("Job:", job)
    account, job, job_time = job
    job_time = string_to_time(job_time)
    if time_to_string(job_time) == "Now":
        if job == "attack":
            if account in [2,3 ]:
                db_update(account, job, datetime.now() + timedelta(hours=1))
            else:
                change_accounts(account)
                troops = FAV_ATTACK[account]
                attack(account, troops)
        elif job == "donate":
            if account in [3,]:
                db_update(account, job, datetime.now() + timedelta(hours=1))
            else:
                change_accounts(account)
                donate()
                db_update(account, 'donate', datetime.now() + timedelta(minutes=20))
        elif job == "build":
            change_accounts(account)
            build(account)
        elif job == "build_b":
            change_accounts(account, "builder")
            job_time = get_time_build_b()
            if not job_time:
                job_time = datetime.now() + timedelta(hours=1)
            db_update(account, "build_b", job_time)
            print(f"Updated time for next builder build for account {account}")
        elif job == "attack_b":
            change_accounts(account, "builder")
            job_time = get_time_attack_b()
            default = datetime.now() + timedelta(hours=1)
            if not job_time:
                job_time = default
            else:
                job_time = max(default, job_time)
            db_update(account, "attack_b", job_time)
            print(f"Updated time for next builder attack for account {account}")
        elif job == "coin":
            change_accounts(account, "main")
            capital_coin()
            job_time = get_time_coin()
            default = datetime.now() + timedelta(hours=1)
            if not job_time:
                job_time = default
            else:
                job_time = max(default, job_time)
            db_update(account, "coin", job_time)
            print(f"Updated time for next coin collection for account {account}")
        elif job == "clock":
            change_accounts(account, "builder")
            if find_cv2('clock')[0] > 0.65:
                print("Clock found")
                click_cv2('clock')
                click_cv2('free_boost')
                click_cv2('boost')
                job_time = datetime.now() + timedelta(hours=23)
                print(f"Clicked the clock")
            else:
                print("Clock not found")
                job_time = datetime.now() + timedelta(hours=1)
            db_update(account, "clock", job_time)
            print(f"Updated time for next clock click for account {account}")

        else:
            job_time = datetime.now() + timedelta(hours=24)
            db_update(account, job, job_time)
            print(f"Job type '{job}' not coded yet.")
    else:
        rest_time = job_time - datetime.now()
        print("Rest time:", rest_time)

        timed_click("pycharm")
        time.sleep(rest_time.seconds)
        reset()
        time.sleep(0.2)

def get_times(accounts):
    print("Get times")
    for account in accounts:
        change_accounts(account)
        db_update(account, "build", get_time_build())
        db_update(account, "attack", get_time_attack())
        db_update(account, "build_b", get_time_build_b())
        db_update(account, "attack_b", get_time_attack_b())
        db_update(account, "coin", get_time_coin())

def get_time_attack():
    print("Get time until attack is ready")
    result = time_to_army_ready()

    if result:
        result = datetime.now() + timedelta(minutes=result)
    else:
        result = datetime.now()
    return result

def get_time_attack_b():
    print("Get time attack - builder")
    goto("builder")
    click_cv2("attack_b")
    if find_cv2("builder_attack_wins")[0] > 0.7:
        print("Ready for attack")
        result = datetime.now()
        pag.click(95, 985)
        return result
    result = read_text(ARMY_TIME_B, WHITE)
    result = alpha_to_numbers(result)
    result = text_to_time(result)
    pag.click(95, 985)
    return result

def get_time_build():
    print("Get build time")
    goto("main")
    click_cv2("builder", BUILDER_REGION, 0.5)
    time.sleep(0.2)
    result = read_text(BUILDER_LIST_TIMES, WHITE)
    try:
        result = alpha_to_numbers(result)
        result = text_to_time(result)
    except:
        print("Failed to read screenshot")
        print(result)
        result = datetime.now() + timedelta(minutes=5)
    db_update(current_account, "build", result)
    time.sleep(0.2)

    click_cv2("builder", BUILDER_REGION, 0.5)
    print("Final:", result)
    return result

def click_builder():
    if find_cv2("master", BUILDER_REGION)[0] > 0.5:
        click_cv2("master")
    elif find_cv2("otto", BUILDER_REGION)[0] > 0.5:
        click_cv2("otto")

def get_time_build_b():
    print("Get build time - Builder Base")
    goto("builder")
    click_builder()
    time.sleep(0.2)
    result = read_text(BUILDER_LIST_TIMES_B, WHITE)
    print("Raw:", result)
    try:
        result = alpha_to_numbers(result)
        result = text_to_time(result)
        print("after text_to_time:", result)
    except:
        print("Failed to read screenshot")
        print(result)
        time.sleep(0.2)
    click_builder()
    print("Builder build time:", result)
    return result

def get_time_coin():
    print("Get time to next coin")
    goto("coin")
    time.sleep(0.2)
    result = read_text(CAPITAL_COIN_TIME, WHITE)
    print("Raw:", result)
    try:
        result = alpha_to_numbers(result)
        result = text_to_time(result)
        print("after text_to_time:", result)
    except:
        print("Failed to read screenshot")
        print(result)
        time.sleep(0.2)
    print("Coin time:", result)
    return result

# ==================
# === NAVIGATION ===
# ==================
current_location = None

NON_DESTINATIONS = [
    # location and image, region
    ("okay", ALL),
    ("donate", ALL),
    ("attacking", ALL),
    ("log_in_with_supercell", ALL),
    ("splash", ALL),
    ("return_home", ALL),
    ("return_home_2", ALL),
    ("reload_game", ALL),
    ("try_again", ALL),
    ("red_cross", ALL),
    ("bluestacks_message", ALL),
]

DESTINATIONS = [
    # location and image, region
    ("chat", ALL),
    ("main", BUILDER_REGION),
    ("builder", BUILDER_REGION),
    ("army_tab", ARMY_TABS),
    ("troops_tab", ARMY_TABS),
    ("spells_tab", ARMY_TABS),
    ("siege_tab", ARMY_TABS),
    ("attack", ALL),
    ("find_a_match", ALL),
    ("switch_account", ALL),
    ("settings", ALL),
    ("coin", ALL),
    ("attack_b", ALL),
]

LOCATIONS = DESTINATIONS + NON_DESTINATIONS

def loc(guess="main"):
    global current_location
    if guess in ["Unknown", "", "wait",]:
        guess = None
    if guess in ["army_tab", "troops_tab", "spells_tab", "siege_tab"]:
        region = ARMY_TABS
    elif guess in ["main", "builder"]:
        region = BUILDER_REGION
    else:
        region = ALL
    if guess and find_cv2("nav/" + guess, region)[0] > 0.7:
        print("Loc:", guess)
        return guess
    if find_cv2("otto", BUILDER_REGION)[0] > 0.7:
        current_location = "builder"
        print("Loc", current_location)
        return current_location
    for location, region in LOCATIONS:
        if find_cv2("nav/" + location, region)[0] > 0.75:
            current_location = location
            print("Loc:", location)
            return location

    print("Loc: Unknown")
    post = datetime.now().strftime('%I%M%p')
    x = f'images/unknown/unknown_{post}.png'
    pag.screenshot(x)

    return "Unknown"

def next_step(location, destination):
    if location == destination:
        return "None"
    map_question = f"{location}|{destination}"
    try:
        result = PATHS[map_question]
    except:
        map_question = f"{location}|other"
        try:
            result = PATHS[map_question]
        except:
            result ="Unknown path"
            result = "No path"
    # print(f"Next step: {location} => {destination}: {result}" )
    return result

def track_loc():
    while True:
        print(loc(current_location))
        time.sleep(1)

def goto(destination):
    print("Goto:", destination)
    global current_location
    current_location = loc(current_location)
    if current_location == destination: return True
    not_there = True
    while not_there:
        next = next_step(current_location, destination)
        move(next)
        time.sleep(0.1)
        current_location = loc(current_location)
        if current_location == destination: not_there = False

PATHS = {
    # current|destination: next action
    "main|chat": "c",
    'main|donate': 'c',
    "main|army_tab": "army",
    "main|troops_tab": "army",
    "main|spells_tab": "army",
    "main|siege_tab": "army",
    "main|settings": "settings",
    "main|switch_account": "settings",
    'main|attack': 'attack',
    'main|find_a_match': 'attack',
    'main|attacking': 'attack',
    'main|coin': 'coin',
    'main|builder': 'boat_to_builder',
    'main|attack_b': 'boat_to_builder',

    'chat|donate': 'donate',
    'chat|other': 'esc',

    'army_tab|troops_tab': 'troops_tab_dark',
    'army_tab|spells_tab': 'spells_tab_dark',
    'army_tab|siege_tab': 'siege_tab_dark',
    'army_tab|other': 'esc',

    'troops_tab|army_tab': 'army_tab_dark',
    'troops_tab|spells_tab': 'spells_tab_dark',
    'troops_tab|siege_tab': 'siege_tab_dark',
    'troops_tab|other': 'esc',

    'spells_tab|army_tab': 'army_tab_dark',
    'spells_tab|troops_tab': 'troops_tab_dark',
    'spells_tab|siege_tab': 'siege_tab_dark',
    'spells_tab|other': 'esc',

    'siege_tab|army_tab': 'army_tab_dark',
    'siege_tab|troops_tab': 'troops_tab_dark',
    'siege_tab|spells_tab': 'spells_tab_dark',
    'siege_tab|other': 'esc',

    'attack|find_a_match': 'find_a_match',
    'attack|attacking': 'find_a_match',
    'attack|other': 'esc',

    'find_a_match|attacking': 'find_a_match',
    'find_a_match|other': 'end_battle',

    'attacking|other': 'end_battle',

    'settings|switch_account': 'switch',
    'settings|other': 'esc',

    'switch_account|other': 'esc',

    'coin|other': 'esc',

    'builder|attack_b': 'attack_b',
    'builder|chat': 'c',
    'builder|settings': 'settings',
    'builder|switch_account': 'settings',
    'builder|other': 'boat_to_main',

    'attack_b|other': 'esc',

    'unknown|other': 'wait',

    'reload_game|other': 'reload_game',
    'red_cross|other': 'red_cross',
    'okay|other': 'okay',
    'try_again|other': 'try_again',
    'return_home|other': 'return_home',
    'return_home_2|other': 'return_home_2',
    'bluestacks_message|other': 'bluestacks_message',
    'log_in_with_supercell|other': 'log_in_with_supercell',
}

NEEDS_DELAY = ["reload_game", "red_cross", "okay", "try_again", "return_home","return_home_2","bluestacks_message",]

def move(code):
    global current_location
    print("Move:", code)
    if code in ["army", "army_tab", "army_tab_dark", "troops_tab", "spells_tab", "siege_tab", "troops_tab_dark", "spells_tab_dark", "siege_tab_dark", "settings", "switch", "attack", "attack_b", "find_a_match",
                "end_battle", "reload_game", "red_cross", "okay", "try_again", "return_home", "return_home_2", "log_in_with_supercell",]:
        click_cv2(code)
    elif code in ["c", "esc"]:
        pag.press(code)
    elif code == 'coin':
        pag.click(95, 985)
        pag.drag(250, -450, 0.5, button='left')
        if find_cv2("forge")[0] > 0.5:
            click_cv2("forge")
        elif find_cv2("capital_coin1")[0] > 0.5:
            click_cv2("capital_coin1")
    elif code == "boat_to_builder":
        pag.click(95, 985)
        pag.drag(250, -450, 0.5, button='left')
        click_cv2('boat')
    elif code == "boat_to_main":
        pag.click(1780, 234)
        pag.drag(-250, 400, 0.5, button='left')
        click_cv2('boat')
    elif code == "bluestacks_message":
        pag.click(1856,769)
    elif code in ["Unknown", "", "wait",]:
        time.sleep(1)
    else:
        print("Code not coded")
    if code in NEEDS_DELAY:
        time.sleep(3)
    if code in ["settings", "attack", "find_a_match"]:
        current_location = code
    if code in ["army_tab_dark", "spells_tab_dark", "siege_tab_dark",]:
        current_location = code[0:-5]
    if code == "army": current_location = "army_tab"
    if code == "switch": current_location = "switch_account"

def test_goto(destination):
    # reset()

    timed_click('bluestacks_icon')
    time.sleep(0.2)
    # pag.click(95, 985)
    # print(find_cv2("nav/" + 'switch_account', ARMY_TABS))
    goto(destination)
    timed_click("pycharm")

def test_next_step(current):
    for loc1, region1 in [(current, ALL),]:
        for loc2, region2 in DESTINATIONS:
            print(f"'{loc1}|{loc2}': '{next_step(loc1, loc2)}',")

# ====================
# === MAIN CONTROL ===
# ====================
current_account = 0
def account_level():
    global current_account
    goto("main")
    level = read_text(LEVEL,WHITE, True)
    if level >= 206 or level == 20: result = 1
    elif level >= 90: result = 2
    else: result = 3
    print("Account level:", level)
    current_account = result
    print("Current account:", current_account)
    return current_account

def mini():
    # reset()
    db_view()
    time.sleep(7)
    timed_click('bluestacks_icon')
    # account_level()
    # run_job(db_next_job())
    # run_job(db_next_job())
    # run_job(db_next_job())
    while True:
    # for x in range(5):
        run_job(db_next_job())
        db_view()

    timed_click("pycharm")

def build2():
    account = 3
    # goto("main")
    if find_cv2("builder_zero", BUILDER_REGION)[0] > 0.8:
        print("All builders occupied")
        job_time = get_time_build()
        if job_time is None:
            db_update(account, "build", datetime.now() + timedelta(minutes=20))
        else:
            db_update(account, "build", job_time)
        return
    resources = current_resources()
    print(resources)
    if resources[0] > resources[1]:
        y_adj = 53
    else:
        y_adj = 100
    print(y_adj)
    click_cv2("main", BUILDER_REGION)
    val, loc, rect = find_cv2("suggested_upgrades", BUILDER_LIST_REGION)
    print("Build. Value of suggested upgrades", val, loc, rect)
    if val > 0.5:
        pag.click(loc[0] + 50, loc[1] + y_adj)

    wait_and_click("upgrade")
    pag.click((933,877))
    timed_click("red_cross", (0,0), 3)
    if find_cv2("builder_zero", BUILDER_REGION)[0] > 0.8:
        print("All builders occupied")
        job_time = get_time_build()
        print(job_time)
        if job_time is None:
            db_update(account, "build", datetime.now() + timedelta(minutes=20))
        else:
            db_update(account, "build", job_time)
        return



def test():
    timed_click('bluestacks_icon')
    time.sleep(.2)
    attack(2, GIANT240)
    # build2()
    # name = "super_barb_donate"
    # val, loc, rect = find_cv2(name, DONATE_AREA)
    # print(rect)
    # colour = check_colour_rect(rect)
    # print(colour)
    timed_click("pycharm")

mini()
# test()



# test_goto("main")
# test_next_step("attack_b")
# db_view()
# timed_click("pycharm")
