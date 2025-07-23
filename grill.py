import threading
from enum import Enum
import time
import pyautogui as pag
import startup as start
import worker
import build as bld
import shopping as shop


class Meat(Enum):
    Steak = 1
    Beef = 2
    Chicken = 3
    Pork = 4


class Shell(Enum):
    Hard = 1
    Soft = 2
    Pita = 3


SPATULA_LOCATION = [445, 550]
KNIFE_LOCATION = [350, 550]
GRILL_STATION = [960, 980]

lock = threading.Lock()

grillSlots = [None, None, 'Locked', None, None, 'Locked']

goldSpatula = False
goldKnife = False

grillSlotDict = {1: [665, 445], 2: [905, 445], 3: [1145, 445], 4: [665, 650], 5: [905, 650], 6: [1145, 650]}
meatTypeDict = {Meat.Beef: [662, 270], Meat.Steak: [418, 270], Meat.Chicken: [906, 270], Meat.Pork: [1146, 270]}
shellTypeDict = {Shell.Hard: [830, 810], Shell.Soft: [1160, 810], Shell.Pita: [470, 810]}

completionOrderNumber = 0

def checkPurchases():
    global goldSpatula
    global goldKnife
    if grillSlots[2] != None:
        if not shop.findItem('Extra Burner'):
            grillSlots[2] = None
    if grillSlots[5] != None:
        if not shop.findItem('Extra Burner 2'):
            grillSlots[5] = None
    if not goldSpatula:
        if not shop.findItem('Gold Spatula'):
            goldSpatula = True
    if not goldKnife:
        if not shop.findItem('Gold Knife'):
            goldKnife = True


def wait(num):
    # print('waiting for ',num,' seconds')
    time.sleep(num)

def flipSchedule(grillSlot, order):
    worker.worker.append([1,flip,[grillSlot], order[0]])

def flip(grillSlot):
    wait(0.5)
    pag.leftClick(GRILL_STATION[0], GRILL_STATION[1])
    start.gameState = start.State.Grill
    if goldSpatula:
        wait(0.5)
    else:
        wait(1)
    pag.moveTo(SPATULA_LOCATION[0], SPATULA_LOCATION[1])
    pag.dragTo(grillSlotDict[grillSlot][0], grillSlotDict[grillSlot][1])
    print("Flipping Grill Slot", grillSlot)
    wait(0.1)

def chopSchedule(grillSlot, order):
    worker.worker.append([1,chop,[grillSlot], order[0]])

def chop(grillSlot):
    wait(0.5)
    print('changing gameState')
    pag.leftClick(GRILL_STATION[0], GRILL_STATION[1])
    start.gameState = start.State.Grill
    if goldKnife:
        wait(0.5)
    else:
        wait(1)
    pag.moveTo(KNIFE_LOCATION[0], KNIFE_LOCATION[1])
    pag.dragTo(grillSlotDict[grillSlot][0], grillSlotDict[grillSlot][1])
    print("Chopping Grill Slot", grillSlot)
    wait(0.1)

def sendToBuildSchedule(grillSlot, shellType, order, tutorial=None):
    worker.worker.append([1,sendToBuild,[grillSlot,shellType,order,tutorial], order[0]])

def sendToBuild(grillSlot, shellType, order, tutorial=None):
    #with lock:
    global completionOrderNumber
    print('changing gameState')
    pag.leftClick(GRILL_STATION[0], GRILL_STATION[1])
    start.gameState = start.State.Grill
    wait(0.5)
    pag.moveTo(grillSlotDict[grillSlot][0], grillSlotDict[grillSlot][1])
    pag.dragTo(shellTypeDict[shellType][0], shellTypeDict[shellType][1])
    grillSlots[grillSlot - 1] = None

    wait(1)
    start.gameState
    wait(1)
    
    print("Sending GrillSlot", grillSlot, "to Build")
    wait(0.25)
    print(order)
    print(completionOrderNumber)
    completionOrderNumber += 1
    if tutorial:
        bld.BuildTopping(order, completionOrderNumber, tutorial)
    else:
        bld.BuildTopping(order, completionOrderNumber)


def GetOpenGrillSlot():
    if not grillSlots[0]:
        return 1
    if not grillSlots[1]:
        return 2
    if not grillSlots[2]:
        return 3
    if not grillSlots[3]:
        return 4
    if not grillSlots[4]:
        return 5
    if not grillSlots[5]:
        return 6


def placeMeat(order, grillSlot, tutorial=None):
    with lock:
        wait(0.5)
        print('changing gameState')
        pag.leftClick(GRILL_STATION[0], GRILL_STATION[1])
        start.gameState = start.State.Grill
        wait(0.5)
        meatType = order[2]
        pag.moveTo(meatTypeDict[meatType])
        pag.dragTo(grillSlotDict[grillSlot])
        print('placing', meatType, 'in grillslot', grillSlot)
        wait(0.5)

    if tutorial:
        cook(order, grillSlot, tutorial)
    else:
        cook(order, grillSlot)

def prepcookSchedule(order, grillSlot, tutorial=None):
    worker.worker.append([1,prepcook, [order, grillSlot, tutorial], order[0]])

def prepcook(order, grillSlot, tutorial=None):
    if not start.gameState == start.State.Grill:
        pag.leftClick(GRILL_STATION[0], GRILL_STATION[1])
        start.gameState = start.State.Grill
    wait(0.25)

    if tutorial:
        placeMeat(order, grillSlot, tutorial)
    else:
        placeMeat(order, grillSlot)


def cook(order, grillSlot, tutorial=None):
    grillSlots[grillSlot - 1] = "in use"
    meatType = order[2]
    shellType = order[1]

    if tutorial:
        meatType = None
    if meatType == Meat.Beef:
        worker.scheduler.append([time.time() + 30, flipSchedule, [grillSlot, order], order[0]])
        worker.scheduler.append([time.time() + 60, sendToBuildSchedule, [grillSlot, shellType, order, None], order[0]])
    elif meatType == Meat.Chicken:
        worker.scheduler.append([time.time() + 27, chopSchedule, [grillSlot, order], order[0]])
        worker.scheduler.append([time.time() + 54, flipSchedule, [grillSlot, order], order[0]])
        worker.scheduler.append([time.time() + 80, sendToBuildSchedule, [grillSlot, shellType, order, None], order[0]])
    elif meatType == Meat.Pork:
        worker.scheduler.append([time.time() + 27, flipSchedule, [grillSlot, order], order[0]])
        worker.scheduler.append([time.time() + 54, chopSchedule, [grillSlot, order], order[0]])
        worker.scheduler.append([time.time() + 80, sendToBuildSchedule, [grillSlot, shellType, order, None], order[0]])
    elif meatType == Meat.Steak:
        worker.scheduler.append([time.time() + 30, chopSchedule, [grillSlot, order], order[0]])
        worker.scheduler.append([time.time() + 60, chopSchedule, [grillSlot, order], order[0]])
        worker.scheduler.append([time.time() + 90, sendToBuildSchedule, [grillSlot, shellType, order, None], order[0]])
    else:
        wait(15)
        flip(grillSlot)
        wait(15)
        sendToBuild(grillSlot, shellType, order, tutorial)
