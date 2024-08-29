import cv2
import startup as start
import pyautogui as pag
import time
import numpy as np
import pytesseract as pt
from PIL import Image
import pandas as pd
import re
import grill as grl

itemSlotDict = {
    0: [825, 175],
    2: [825, 400],
    4: [825, 630],
    1: [1475, 175],
    3: [1475, 400],
    5: [1475, 630]
}

NEXT_BUTTON = [1085, 860]
PREV_BUTTON = [820, 860]
BACK_BUTTON = [960, 960]


def findItem(item):
    shop = getShop(3)
    if item in list(shop['Item']):
        return True
    else:
        return False


def getShop(count):
    if count > 2:
        Shop = pd.read_excel('./tacomia.xlsx', sheet_name='currentshop', header=0)
        # print(Shop)

        Shop.sort_values(by=['Priority', 'Cost'], inplace=True, ascending=True, ignore_index=True)
        # print(Shop)
        return Shop
    else:
        Shop = pd.read_excel('./tacomia.xlsx', sheet_name='Sheet1', header=0)

        Shop.sort_values(by=['Priority', 'Cost'], inplace=True, ascending=True, ignore_index=True)

        with pd.ExcelWriter('./tacomia.xlsx', mode="a", engine="openpyxl", if_sheet_exists="replace") as writer:
            Shop.to_excel(writer, sheet_name='currentshop', index=False, header=True, startrow=0)
        # print(Shop)
        return Shop


def getMoney():
    x, y, width, height = 820, 650, 290, 35  # Specify the region to capture
    screenshot = pag.screenshot(region=(x, y, width, height))
    screenshot_cv = np.array(screenshot)
    screenshot_cv = cv2.cvtColor(screenshot_cv, cv2.COLOR_RGB2BGR)
    # cv2.imshow('sample',screenshot_cv)
    # cv2.waitKey(0)
    cv2.imwrite('./Graphics/money.png', screenshot_cv)
    pt.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    money = pt.image_to_string(Image.open('./Graphics/money.png'), config='--psm 7')
    money = re.sub(r'[^\d.]', '', money)
    try:
        money = float(money)
    except:
        money = -1
    return money


def buy(purchases):
    if purchases:
        pag.leftClick(960, 875)
        time.sleep(1)
        located = False
        while not located:
            pag.leftClick(1450, 980)
            time.sleep(0.1)
            if pag.locateOnScreen('./Graphics/upgrade.png'):
                located = True
        for item in purchases:
            next = 0
            for x in range(item):
                if x % 6 == 0 and not x == 0:
                    # print('advancing page. x is currently', x)
                    pag.leftClick(NEXT_BUTTON)
                    next += 1
                    time.sleep(0.25)
                if x + 1 == item:
                    pag.leftClick(itemSlotDict[x % 6])
                    print('Clicking item slot', x % 6, 'item is', item)
                    time.sleep(0.25)
            for x in range(next):
                # print('returning to start', x+1)
                pag.leftClick(PREV_BUTTON)
                time.sleep(0.25)


def updateShop(purchases, shop):
    if purchases:
        # Sort purchases in descending order to avoid indexing issues
        sorted_purchases = sorted(purchases, reverse=True)
        
        for item in sorted_purchases:
            # Remove the purchased item
            shop.drop(shop[shop['Slot'] == item].index, inplace=True)
            
            # Update slots for remaining items
            shop.loc[shop['Slot'] > item, 'Slot'] -= 1

        # Reset index if needed
        shop.reset_index(drop=True, inplace=True)
    
    print(shop)
    return shop


def moneyTest():
    return 10000.00


def getPurchases(money, shop):
    purchases = []
    try:
        # Sort the shop by Priority (ascending) and Cost (ascending)
        sorted_shop = shop.sort_values(['Priority', 'Cost'])
        
        # Iterate through all priority levels
        for priority in sorted(shop['Priority'].unique()):
            priority_items = sorted_shop[sorted_shop['Priority'] == priority]
            
            # Try to purchase items of the current priority
            for _, row in priority_items.iterrows():
                if money >= row['Cost']:
                    purchases.append(row['Slot'])
                    money -= row['Cost']
        
        return purchases
    except Exception as e:
        print(f"An error occurred: {e}")
        return None



def purchaseUpgrades(count):
    shop = getShop(count)
    money = getMoney()
    # money = moneyTest()
    purchases = getPurchases(money, shop)
    print(purchases)
    buy(purchases)
    shop = updateShop(purchases, shop)

    with pd.ExcelWriter('./tacomia.xlsx', mode="a", engine="openpyxl", if_sheet_exists="replace") as writer:
        shop.to_excel(writer, sheet_name='currentshop', index=False, header=True, startrow=0)
