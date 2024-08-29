import pyautogui as pag
from enum import Enum
import grill as grl
import shopping as shop
import worker as worker
import time
import order as ord
import build as bld


class State(Enum):
    Title = 0
    Order = 1
    Grill = 2
    Build = 3
    Ordering = 4
    Serving = 5
    Results = 6
    Overnight = 7
    Shop = 8
    Morning = 9


gameState = State.Overnight

def GetCustomerNumber(day):
    if day <= 1:
        return 1
    elif day <= 3:
        return 4
    elif day <= 7:
        return 5
    elif day <= 11:
        return 6
    elif day <= 14:
        return 7
    else:
        return 8


def StartGame():
    print('starting game')
    pag.leftClick(960, 800)
    grl.wait(1)
    pag.leftClick(960, 730)
    grl.wait(0.5)
    pag.leftClick(750, 730)
    grl.wait(0.5)
    pag.leftClick(1140, 690)
    grl.wait(0.5)
    pag.leftClick(1500, 1000)
    tutorial()


def StartDay(day):
    shop.purchaseUpgrades(day)

    print('starting day')
    grl.wait(0.25)
    grl.checkPurchases()
    pag.leftClick(960, 960)
    gameState = State.Morning
    located = False
    while not located:
        pag.leftClick(1450, 980)
        grl.wait(0.1)
        if pag.locateOnScreen('./Graphics/open.jpg'):
            print('start confirmed')
            located = True

    if day >= 40:
        print('changing to Royal Crown')
    elif day >= 29: 
        print('changing to Viking Helmet')
    elif day >= 20:
        print('changing to Chef Hat')
    elif day >= 13:
        print('changing to Sombrero')
    else:
        print('Changing to Taco Hat')

    worker.scheduler.enterabs(time.time(), 1, ord.TakeOrderSchedule, [1, GetCustomerNumber(day)])
    print('start day finished')
    worker.runner = True


def WaitUntilOpen():
    print('waiting for open')
    located = False
    while not located:
        located = True
        if not pag.locateOnScreen('./Graphics/open.jpg'):
            located = False


def WaitUntilSign():
    print('waiting for sign')
    located = False
    while not located:
        if pag.locateOnScreen('./Graphics/open.jpg') or pag.locateOnScreen('./Graphics/Closed.jpg'):
            located = True


def WaitForShop():
    print('waiting for shop')
    located = False
    while not located:
        if pag.locateOnScreen('./Graphics/continue.png'):
            located = True


def WaitUntilServe():
    print('waiting for serve end')
    located = False
    while not located:
        if pag.locateOnScreen('./Graphics/Trashhandle.jpg', confidence=0.995):
            located = True
            return False
        if pag.locateOnScreen('./Graphics/serviceimage.jpg', confidence=0.995):
            located = True
            return True


def CheckOpen():
    print('checking for open')
    if pag.locateOnScreen('./Graphics/open.jpg'):
        return True
    else:
        return False


def EndDay():
    print('ending day')
    worker.runner = False
    grl.wait(15)
    pag.leftClick(960, 980)
    grl.wait(10)


def tutorial():
    print('playing tutorial')
    WaitUntilSign()
    pag.leftClick(grl.GRILL_STATION[0], grl.GRILL_STATION[1])
    grl.wait(1)
    pag.leftClick(bld.BUILD_STATION[0], bld.BUILD_STATION[1])
    grl.wait(1)
    pag.leftClick(ord.ORDER_STATION[0], ord.ORDER_STATION[1])
    gameState = State.Order
    WaitUntilSign()

    ord.TakeOrder(1, 1, 'tutorial')
    grl.wait(1)
    ord.TakeOrder(1, 1, 'tutorial')
    grl.wait(10)
    EndDay()