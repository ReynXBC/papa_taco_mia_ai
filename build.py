from enum import Enum
import pyautogui as pag
import grill as grl
import startup as start
import worker
import time


class Sauce(Enum):
    Mild = 1
    Sour = 2
    Hot = 3
    Nacho = 4
    Verde = 5
    Loco = 6


class Topping(Enum):
    Cheese = 1
    Gaucamole = 2
    Lettuce = 3
    Onions = 4
    PBeans = 5
    Tomatoes = 6
    WRice = 7
    Jalapenos = 8
    Peppers = 9
    BBeans = 10
    BRice = 11


TRASH_LOCATION = [1500, 790]
START_POUR = [590, 250]
END_POUR = [1020, 250]
BIG_TICKET = [1450, 140]
SERVE = [442, 524]
FINISH = [800, 680]

TICKET_SLOT = [[1150, 100], [1075, 100], [1000, 100], [925, 100], [850, 100], [775, 100], [700, 100], [625, 100]]
BUILD_STATION = [1180, 980]

SLOW_TIME = 3
FAST_TIME = 1.5

tut2 = False

toppingTypeDict = {Sauce.Verde: [350, 330, SLOW_TIME], Sauce.Sour: [435, 330, SLOW_TIME],
                   Sauce.Hot: [520, 330, SLOW_TIME], Sauce.Nacho: [1075, 330, SLOW_TIME],
                   Sauce.Mild: [1170, 330, SLOW_TIME],
                   Sauce.Loco: [1260, 330, SLOW_TIME], Topping.Jalapenos: [475, 780, SLOW_TIME],
                   Topping.Tomatoes: [660, 780, SLOW_TIME], Topping.WRice: [830, 780, FAST_TIME],
                   Topping.Lettuce: [1020, 780, SLOW_TIME], Topping.Peppers: [1200, 780, FAST_TIME],
                   Topping.BBeans: [380, 860, SLOW_TIME], Topping.Gaucamole: [560, 860, FAST_TIME],
                   Topping.Cheese: [740, 860, FAST_TIME], Topping.PBeans: [920, 860, SLOW_TIME],
                   Topping.Onions: [1105, 860, SLOW_TIME], Topping.BRice: [1285, 860, FAST_TIME]}


def BuildTopping(order, completionOrderNumber, tutorial=None):
    '''if not start.gameState == start.State.Build:
       print('changing gameState')
       grl.wait(1)
       pag.leftClick(BUILD_STATION[0],BUILD_STATION[1])
       grl.wait(0.25)
       start.gameState = start.State.Build'''
    if tutorial:
        build(order, completionOrderNumber, 'tutorial')
    else:
        build(order, completionOrderNumber)


def addTopping(item, tutorial=None):
    global tut2
    if item:
        if start.gameState != start.State.Build:
            print('changing gameState')
            pag.leftClick(1180, 980)
            start.gameState = start.State.Build
            grl.wait(0.25)

        print('adding topping', item)

        pag.moveTo(toppingTypeDict[item][0], toppingTypeDict[item][1])
        pag.dragTo(START_POUR[0], START_POUR[1], duration=0.5)

        if not tutorial:
            pag.moveTo(END_POUR[0], END_POUR[1], duration=toppingTypeDict[item][2])
        else:
            if tut2:
                print("IT WORKING")
                pag.moveTo(END_POUR[0], END_POUR[1],
                           duration=(toppingTypeDict[item][2] - 0.25) if toppingTypeDict[item][2] == FAST_TIME else (
                           toppingTypeDict[item][2]))
            else:
                pag.moveTo(END_POUR[0], END_POUR[1],
                           duration=(toppingTypeDict[item][2] + 2) if toppingTypeDict[item][2] == FAST_TIME else (
                           toppingTypeDict[item][2]))
        grl.wait(0.25)


def build(order, completionOrderNumber, tutorial=None):
    buffer = 0.1
    for item, count in zip(order, range(len(order))):
        if count > 2:
            if tutorial:
                addTopping(item, tutorial)
            else:
                if item:
                    #worker.scheduler.enterabs(time.time() + buffer, 0, addTopping, [item, tutorial])
                    worker.worker.append([completionOrderNumber + buffer + 2, addTopping, [item,None], order[0]])
                    buffer += 0.1

    if tutorial:
        Serve(order[0], 'tutorial')
    else:
        #worker.scheduler.enterabs(time.time() + buffer, 0, Serve, [order[0]])
        worker.worker.append([completionOrderNumber + 0.9 + 2, Serve, [order[0]], order[0]])

def Serve(orderNum, tutorial=None):
    if tutorial:
        global tut2
        tut2 = True
    print('serving order# ', orderNum)
    if not start.gameState == start.State.Build:
        print('changing gameState')
        pag.leftClick(1180, 980)
        start.gameState = start.State.Build
        grl.wait(1)
    if tutorial:
        grl.wait(0.25)
    grl.wait(1)
    pag.leftClick(800, 680)
    grl.wait(0.25)
    if tutorial:
        grl.wait(0.25)
        pag.moveTo(BIG_TICKET[0], BIG_TICKET[1])
        pag.dragTo(SERVE[0], SERVE[1])
    else:
        pag.moveTo(TICKET_SLOT[orderNum - 1][0], TICKET_SLOT[orderNum - 1][1])
        pag.dragTo(SERVE[0], SERVE[1])
    grl.wait(2)
    end = start.WaitUntilServe()
    if not tutorial:
        grl.wait(0.5)
        if end:
            start.EndDay()
