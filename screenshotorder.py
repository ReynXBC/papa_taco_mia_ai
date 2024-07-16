import pyautogui as pag
import cv2
import numpy as np

x, y, width, height = 1310, 65, 290, 584  # Specify the region to capture
screenshot = pag.screenshot(region=(x, y, width, height))
screenshot_cv = np.array(screenshot)
screenshot_cv = cv2.cvtColor(screenshot_cv, cv2.COLOR_RGB2BGR)
cv2.imwrite('./orders/order17.png', screenshot_cv)