import pyautogui as pag
import cv2
import numpy as np

x, y, width, height = 1380, 780, 180, 50  # Specify the region to capture
screenshot = pag.screenshot(region=(x, y, width, height))
screenshot_cv = np.array(screenshot)
screenshot_cv = cv2.cvtColor(screenshot_cv, cv2.COLOR_RGB2BGR)
cv2.imshow('sample',screenshot_cv)
cv2.waitKey(0)
cv2.imwrite('./Testing/ordertest.jpg', screenshot_cv)


##Storage
#this.customerOrder = [["pita"],["pork"],["onions"],["pintobeans"],["onions"],["special"],["sourcream"]];