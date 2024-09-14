import pyautogui as pag
from enum import Enum
import grill as grl
import shopping as shop
import worker as worker
import time
import order as ord
import build as bld
import numpy as np
import cv2
import pytesseract as pt
import re
from PIL import Image
import easyocr
import torch


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

currentCustomerPoints = 0

RANKMULTIPLIER = 150

'''
def GetCustomerNumber(rank):
    if rank >= len(numberOfCustomers):
        rank = (len(numberOfCustomers))
    return numberOfCustomers[rank-1]

def getRank():
    x, y, width, height = 820, 300, 280, 145  # Specify the region to capture
    screenshot = pag.screenshot(region=(x, y, width, height))
    screenshot_cv = np.array(screenshot)
    #cv2.imshow('image',screenshot_cv)
    #cv2.waitKey(0)
    cv2.imwrite('./orders/rank.png', screenshot_cv)
    rank = cv2.cvtColor(screenshot_cv, cv2.COLOR_BGR2GRAY)
    (h, w) = rank.shape[:2]
    rank = cv2.resize(rank, (w * 2, h * 2))
    rank = cv2.copyMakeBorder(rank, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value=255)
    rank = cv2.adaptiveThreshold(rank, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 81, 12)
    #cv2.imshow('image',rank)
    #cv2.waitKey(0)
    pt.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    rank = pt.image_to_string(rank, config="digits") 
    rank = pt.image_to_string(Image.open('./orders/rank.png'), config='--psm 7')
    rank = re.sub(r'[^\d.]', '', rank)
    try:
        rank = int(rank)
        return rank
    except:
        return 100000
'''    

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
    
    if day == 60 or day == 40 or day == 30 or day == 20 or day == 10 or day == 80:
        changeHat()

    worker.scheduler.enterabs(time.time(), 1, ord.TakeOrderSchedule, [1])
    print('start day finished')
    worker.runner = True


def WaitUntilOpen():
    print('waiting for open')
    located = False
    while not located:
        located = True
        if not pag.locateOnScreen('./Graphics/open.jpg'):
            located = False


def changeHat():
    time.sleep(0.5)
    pag.click(1510,985)
    time.sleep(0.5)
    pag.click(1075,315)
    time.sleep(0.5)
    pag.click(950,950)


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
    
def GetRank(customerPoints):
    rank = 1
    rankThreshold = 0
    
    while True:
        nextThreshold = rankThreshold + (rank + 1) * RANKMULTIPLIER
        if customerPoints < nextThreshold:
            break
        rank += 1
        rankThreshold = nextThreshold
    
    return rank

def GetCustomerPoints():
    return currentCustomerPoints

def GetCustomerPointsNow():
    x, y, width, height = 1150, 367, 350, 40  # Specify the region to capture
    screenshot = pag.screenshot(region=(x, y, width, height))
    screenshot_cv = np.array(screenshot)
    screenshot_cv = cv2.cvtColor(screenshot_cv, cv2.COLOR_RGB2GRAY)
    screenshot_cv = cv2.threshold(screenshot_cv,180,255,cv2.THRESH_BINARY)
    #cv2.imshow('sample',screenshot_cv[1])
    #cv2.waitKey(0)
    cv2.imwrite('./temp/points.png', screenshot_cv[1])
    #pt.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    #customerPoints = pt.image_to_string(Image.open('./temp/points.png'), config='--oem 1 --psm 7')
    reader = easyocr.Reader(['en'])
    customerPoints = reader.readtext('./temp/points.png')
    customerPoints = re.sub(r'[^\d..]', '', customerPoints[0][1])
    try:
        return int(customerPoints)
    except:
        return -1

def InitCustomerDict():
    ord.InitCustomerDict()

def GetMoney():
    return shop.getMoney()

def GetShopCount(day):
    return len(shop.getShop(day))

def EndDay():
    global currentCustomerPoints
    print('ending day')
    worker.runner = False
    grl.wait(15)
    currentCustomerPoints = GetCustomerPointsNow()
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

    ord.TakeOrder(1, 'tutorial')
    grl.wait(1)
    ord.TakeOrder(1, 'tutorial')
    grl.wait(10)
    EndDay()