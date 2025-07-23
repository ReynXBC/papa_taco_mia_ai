from PyQt5 import QtWidgets, QtGui, QtCore
import ctypes

class Overlay(QtWidgets.QWidget):
   update_signal = QtCore.pyqtSignal(list, list, str, str, str, str, str, str, str, str, str, str)  # Signal to update info

   def __init__(self):
      super().__init__()
      self.setWindowFlags(
         QtCore.Qt.FramelessWindowHint |
         QtCore.Qt.WindowStaysOnTopHint |
         QtCore.Qt.Tool
      )
      self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
      self.setAttribute(QtCore.Qt.WA_ShowWithoutActivating)
      self.resize(1920,1080)  # Set initial size
      self.move(0, 0)  # Position at the top-left corner of the screen
      self.info = [None, None, None, None, None, None, None, None, None, None, None, None]  # Store info to display
      self.update_signal.connect(self.set_info)
      self.show()
      self.set_click_through()

   def set_click_through(self):
    hwnd = int(self.winId())
    GWL_EXSTYLE = -20
    WS_EX_LAYERED = 0x80000
    WS_EX_TRANSPARENT = 0x2
    style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
    style |= WS_EX_LAYERED | WS_EX_TRANSPARENT
    ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)

   def set_info(self, worker="", scheduler="", day="0", money="0", shop = "0", points = "0", rank="0", star0="0", star1="0", star2="0", star3="0", customer_total="0"):
      self.info = [worker, scheduler, day, money, shop, points, rank, star0, star1, star2, star3, customer_total]
      self.update()  # Triggers paintEvent

   def paintEvent(self, event):
      #print("Overlay paintEvent called", self.info)
      painter = QtGui.QPainter(self)
      painter.setPen(QtGui.QPen(QtCore.Qt.white, 2))
      painter.setFont(QtGui.QFont("Arial", 16))
      # Draw info at specific locations
      painter.drawText(10, 525, "^^ Employee Queue ^^")
      painter.drawText(10, 1025, "^^ Manager Queue ^^")
      if self.info[0]:
         y = 500
         for x in self.info[0]:
            painter.drawText(10, y, str(x[1].__qualname__) + " #" + str(x[3]))
            y -= 25
            if y < 75:
               break
      if self.info[1]:
         y = 1000
         for x in self.info[1]:
            painter.drawText(10, y, str(x[1].__qualname__) + " #" + str(x[3]))
            y -= 25
            if y < 570:
               break
      painter.drawText(1640, 75, f"Day: {self.info[2]}")
      painter.drawText(1640, 100, f"Money: {self.info[3]}")
      painter.drawText(1640, 125, f"Shop Items: {self.info[4]}")
      painter.drawText(1640, 150, f"Customer Points: {self.info[5]}")
      painter.drawText(1640, 175, f"Rank: {self.info[6]}")
      painter.drawText(1640, 200, f"0-Star Customers: {self.info[7]}")
      painter.drawText(1640, 225, f"1-Star Customers: {self.info[8]}")
      painter.drawText(1640, 250, f"2-Star Customers: {self.info[9]}")
      painter.drawText(1640, 275, f"3-Star Customers: {self.info[10]}")
      painter.drawText(1640, 300, f"Customer Total: {self.info[11]}")