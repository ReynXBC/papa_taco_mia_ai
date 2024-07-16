import pyautogui as pag
import cv2
import numpy as np

x, y, width, height = 750, 60, 450, 75 # Specify the region to capture
screenshot = pag.screenshot(region=(x, y, width, height))
screenshot_cv = np.array(screenshot)
screenshot_cv = cv2.cvtColor(screenshot_cv, cv2.COLOR_RGB2BGR)
cv2.imshow('sample',screenshot_cv)
cv2.waitKey(0)
#cv2.imwrite('./Graphics/upgrade.png', screenshot_cv)