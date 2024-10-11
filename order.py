import build as bld
import grill as grl
from enum import Enum
import cv2
import numpy as np
import pyautogui as pag
import os
import startup as start
import worker
import time
import easyocr
import json
import torch

class Section(Enum):
   Shell = 1
   Meat = 2
   Toppings = 3

SHELL_PATH = './Graphics/Shells'
MEAT_PATH = './Graphics/Meats'
TOPPING_PATH = './Graphics/Toppings'
ORDER_STATION = [740,980]
TAKE_ORDER = [650,410]

shellDict = {'hard.jpg':grl.Shell.Hard,'pita.jpg':grl.Shell.Pita,'soft.jpg':grl.Shell.Soft}
meatDict = {'chicken.jpg':grl.Meat.Chicken,'beef.jpg':grl.Meat.Beef,'steak.jpg':grl.Meat.Steak,'pork.jpg':grl.Meat.Pork}
toppingDict = {}

for newitem, count in zip(os.listdir(TOPPING_PATH), range(85)):
   if count < 5:
      toppingDict[newitem] = bld.Topping.BBeans
   elif count < 10:
      toppingDict[newitem] = bld.Topping.BRice
   elif count < 15:
      toppingDict[newitem] = bld.Topping.Cheese
   elif count < 20:
      toppingDict[newitem] = bld.Topping.Gaucamole
   elif count < 25:
      toppingDict[newitem] = bld.Sauce.Hot
   elif count < 30:
      toppingDict[newitem] = bld.Topping.Jalapenos
   elif count < 35:
      toppingDict[newitem] = bld.Topping.Lettuce
   elif count < 40:
      toppingDict[newitem] = bld.Sauce.Loco
   elif count < 45:
      toppingDict[newitem] = bld.Sauce.Mild
   elif count < 50:
      toppingDict[newitem] = bld.Sauce.Nacho
   elif count < 55:
      toppingDict[newitem] = bld.Topping.Onions
   elif count < 60:
      toppingDict[newitem] = bld.Topping.Peppers
   elif count < 65:
      toppingDict[newitem] = bld.Topping.PBeans
   elif count < 70:
      toppingDict[newitem] = bld.Sauce.Sour
   elif count < 75:
      toppingDict[newitem] = bld.Topping.Tomatoes
   elif count < 80:
      toppingDict[newitem] = bld.Sauce.Verde
   elif count < 85:
      toppingDict[newitem] = bld.Topping.WRice
   
customerStarDict = {}

def SaveDict():
    global customerStarDict
    with open('./temp/customerStarDict.json', 'w') as f:
        json.dump(customerStarDict, f)

def LoadDict():
    with open('./temp/customerStarDict.json', 'r') as f:
        return json.load(f)

def GetStarCount(star):
   starcount = 0
   if star == 0:
      threshold = 1 
      max = 5
   elif star == 1:
      threshold = 5
      max = 10
   elif star == 2:
      threshold = 10
      max = 15
   elif star == 3:
      threshold = 15
      
   global customerStarDict
   for customer, visits in zip(customerStarDict.keys(), customerStarDict.values()):
      if star == 3:
         if visits >= threshold:
            starcount += 1
      elif visits >= threshold and visits < max:
         starcount += 1
   
   return starcount


def GetOrder(orders,count,image):
   orders[count-1] = OrderParse(image, count)

def ImgMatch(image, section):
   match = None

   if section == Section.Shell:
      tempDict = {}

      for ref in os.listdir(SHELL_PATH):
         refimage = cv2.imread(SHELL_PATH + '/' + ref)
         #image = cv2.resize(image, (300,100))
         #refimage = cv2.resize(refimage, (300,100))
         mse = np.sum((image - refimage) ** 2) / float(image.shape[0] * refimage.shape[1])
         tempDict[mse] = ref
         #print(ref,mse)

      lowest = 200000000000000000000000
      for pair in tempDict.items():
         if pair[0] < lowest:
            lowest = pair[0]
            match = shellDict[pair[1]]
      lowest = -1

   if section == Section.Meat:
      tempDict = {}

      for ref in os.listdir(MEAT_PATH):
         refimage = cv2.imread(MEAT_PATH + '/' + ref)
         #image = cv2.resize(image, (300,100))
         #refimage = cv2.resize(refimage, (300,100))
         mse = np.sum((image - refimage) ** 2) / float(image.shape[0] * refimage.shape[1])
         tempDict[mse] = ref
         #print(ref,mse)

      lowest = 200000000000000000000000
      for pair in tempDict.items():
         if pair[0] < lowest:
            lowest = pair[0]
            match = meatDict[pair[1]]
      lowest = -1
   
   if section == Section.Toppings: #Might consider a different type of id for this
      tempDict = {}

      for ref in os.listdir(TOPPING_PATH):
         refimage = cv2.imread(TOPPING_PATH + '/' + ref)
         #image = cv2.resize(image, (300,100))
         #refimage = cv2.resize(refimage, (300,100))
         mse = np.sum((image - refimage) ** 2) / float(image.shape[0] * refimage.shape[1])
         tempDict[mse] = ref
         #print(ref,mse)

      lowest = 200000000000000000000000
      for pair in tempDict.items():
         if pair[0] < lowest:
            lowest = pair[0]
            match = toppingDict[pair[1]]
   
   return match if lowest < 50 else None

def OrderParse(count):
   
   #LARGE VERSION
   orderimage = cv2.imread('./orders/order' + str(count) + '.png')
   x, y, width, height = 2, 484, 280, 95
   shellimage = orderimage[y:y+height, x:x+width]
   x, y, width, height = 2, 384, 280, 95
   meatimage = orderimage[y:y+height, x:x+width]
   x, y, width, height = 90, 324, 100, 50
   toppingimage1 = orderimage[y:y+height, x:x+width]
   x, y, width, height = 90, 272, 100, 50
   toppingimage2 = orderimage[y:y+height, x:x+width]
   x, y, width, height = 90, 220, 100, 50
   toppingimage3 = orderimage[y:y+height, x:x+width]
   x, y, width, height = 90, 168, 100, 50
   toppingimage4 = orderimage[y:y+height, x:x+width]
   x, y, width, height = 90, 116, 100, 50
   toppingimage5 = orderimage[y:y+height, x:x+width]


   '''
   #cv2.imwrite('./Testing/order'+str(count)+'shell'+str(toppingcount)+ '.jpg', shellimage)
   #toppingcount += 1
   #cv2.imwrite('./Testing/order'+str(count)+'meat'+str(toppingcount)+'.jpg', meatimage)
   #toppingcount += 1
   '''
   #toppingcount = 0
   #cv2.imwrite('./Testing/order'+str(count)+'topping'+str(toppingcount)+'.png', toppingimage1)
   #toppingcount += 1
   #cv2.imwrite('./Testing/order'+str(count)+'topping'+str(toppingcount)+'.png', toppingimage2)
   #toppingcount += 1
   #cv2.imwrite('./Testing/order'+str(count)+'topping'+str(toppingcount)+'.png', toppingimage3)
   #toppingcount += 1
   #cv2.imwrite('./Testing/order'+str(count)+'topping'+str(toppingcount)+'.png', toppingimage4)
   #toppingcount += 1
   #cv2.imwrite('./Testing/order'+str(count)+'topping'+str(toppingcount)+'.png', toppingimage5)
   #toppingcount += 1
   
   #cv2.imshow('sample',toppingimage5)
   #cv2.waitKey(0)
   


   order = [count, ImgMatch(shellimage,Section.Shell), ImgMatch(meatimage,Section.Meat), 
            #currentToppings[0],currentToppings[1],currentToppings[2],currentToppings[3],currentToppings[4]]
            ImgMatch(toppingimage1,Section.Toppings),ImgMatch(toppingimage2,Section.Toppings),ImgMatch(toppingimage3,Section.Toppings),ImgMatch(toppingimage4,Section.Toppings),ImgMatch(toppingimage5,Section.Toppings)]

   return order

def TakeScreenshot(count):
   x, y, width, height = 1310, 65, 290, 584  # Specify the region to capture
   screenshot = pag.screenshot(region=(x, y, width, height))
   screenshot_cv = np.array(screenshot)
   screenshot_cv = cv2.cvtColor(screenshot_cv, cv2.COLOR_RGB2BGR)
   cv2.imwrite('./orders/order'+ str(count) + '.png', screenshot_cv)
   order = OrderParse(count)
   print(order)
   return order

def InitCustomerDict():
   pass

def TakeNameScreenShot():
   x, y, width, height = 845, 710, 400, 55  # Specify the region to capture
   screenshot = pag.screenshot(region=(x, y, width, height))
   screenshot_cv = np.array(screenshot)
   screenshot_cv = cv2.cvtColor(screenshot_cv, cv2.COLOR_RGB2GRAY)
   screenshot_cv = cv2.threshold(screenshot_cv,180,255,cv2.THRESH_BINARY)
   #cv2.imshow('sample',screenshot_cv[1])
   #cv2.waitKey(0)
   cv2.imwrite('./temp/name.png', screenshot_cv[1])

   reader = easyocr.Reader(['en'])
   name = reader.readtext('./temp/name.png')

   #pt.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
   #name = pt.image_to_string(Image.open('./temp/name.png'), config='--psm 7')
   if name[0][1] == "DORDU":
      name = "RoBBY"
   else:
      name = name[0][1]

   try:
      return name
   except:
      return None

def GetCustomer():
   global customerStarDict
   name = TakeNameScreenShot()
   if name != 1:
      try:
         customerStarDict[name] = customerStarDict[name] + 1
      except:
         customerStarDict[name] = 1

def TakeOrderSchedule(count,tutorial = None):
   worker.worker.append([2,TakeOrder,[count,tutorial]])

def TakeOrder(count,tutorial = None):
   
   if not start.gameState == start.State.Order:
      pag.leftClick(ORDER_STATION[0],ORDER_STATION[1])
      start.gameState = start.State.Order
      grl.wait(0.25)
   
   start.WaitUntilSign()
   if count == 1:
      print('ORDER WAIT CHECK')
      if tutorial:
         grl.wait(4.25)
      else:
         grl.wait(3.75)
      pag.leftClick(ORDER_STATION[0],ORDER_STATION[1])
      grl.wait(0.25)
   
   customer = False
   for x in range(10):
      if pag.locateOnScreen('./Graphics/orderButton.png',confidence=0.9):
         customer = True

   if customer:
      pag.leftClick(TAKE_ORDER[0],TAKE_ORDER[1])
      start.gameState = start.State.Ordering

   if count <= 8 and not tutorial:
     if customer:
         if count != 8:
             worker.scheduler.append([time.time() + 10, TakeOrderSchedule,[count+1]])
     else:
         worker.scheduler.append([time.time() + 10, TakeOrderSchedule,[count]])

   if customer:
      grl.wait(1)
      GetCustomer()
      #grl.wait(1)
      start.WaitUntilSign()
      start.gameState = start.State.Order

      if not tutorial:
         order = TakeScreenshot(count)

      pag.moveTo(bld.BIG_TICKET[0],bld.BIG_TICKET[1])
      pag.dragTo(bld.TICKET_SLOT[count-1][0],bld.TICKET_SLOT[count-1][1])

      if tutorial:
         pag.leftClick(grl.GRILL_STATION[0],grl.GRILL_STATION[1])
         grl.wait(0.25)
         pag.moveTo(bld.TICKET_SLOT[count-1][0],bld.TICKET_SLOT[count-1][1])
         pag.dragTo(bld.BIG_TICKET[0],bld.BIG_TICKET[1])
         grl.wait(0.25)
         order = TakeScreenshot(count)
         grl.prepcook(order,grillSlot=5,tutorial=tutorial)
      else:
         #worker.scheduler.enterabs(time.time(),1,grl.prepcookSchedule,[order,grl.GetOpenGrillSlot()])
         worker.worker.append([2,grl.prepcook,[order,grl.GetOpenGrillSlot()]])
      