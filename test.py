import shopping as shop
import pandas as pd
import startup as start
import cv2
import pyautogui as pag
import numpy as np
import time

'''NextPurchase = pd.read_excel('./tacomia.xlsx',sheet_name='Sheet1',header=0)

NextPurchase.sort_values(by='Priority',inplace=True,ascending=True,ignore_index=True)

print(NextPurchase)'''

#x, y, width, height = 580, 380, 140, 60  # Specify the region to capture
#screenshot = pag.screenshot(region=(x, y, width, height))
#screenshot_cv = np.array(screenshot)
#screenshot_cv = cv2.cvtColor(screenshot_cv, cv2.COLOR_RGB2BGR)
#cv2.imshow('sample',screenshot_cv)
#cv2.waitKey(0)
#cv2.imwrite('./Graphics/orderButton.png', screenshot_cv)


customer = False
for x in range(10):
   if pag.locateOnScreen('./Graphics/orderButton.png',confidence=0.9):
      customer = True
print(customer)

