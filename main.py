import threading
import startup as start
import worker
import time
import pandas as pd
from PyQt5 import QtWidgets
from overlay import Overlay
import sys

log = pd.DataFrame(columns=['Day','Money','Shop Items Remaining','Customer Points', 'Rank', '0-Star', '1-Star', '2-Star', '3-Star', 'Total Customers'])

day = 1
start.StartGame()
day = 2

daylog = [day-1, start.GetMoney(), start.GetShopCount(day-1), start.GetCustomerPoints(), 
              start.GetRank(start.GetCustomerPoints()), start.ord.GetStarCount(0), 
              start.ord.GetStarCount(1), start.ord.GetStarCount(2), start.ord.GetStarCount(3),
              start.ord.GetStarCount(-1)]
print(daylog)
log.loc[len(log)] = daylog

#USE THIS ONE TO CHANGE THE DAY
#day = 16

if day > 2:
    start.ord.LoadDict()

def main():
    global day
    global log
    global screenoverlay
    global currentDay

    while day <= 5:
        daylog = []

        scheduler_thread = threading.Thread(target=worker.scheduler_worker, name='scheduler thread')
        scheduler_thread.daemon = True

        currentDay = day

        start.StartDay(day)
        day += 1
        scheduler_thread.start()

        screenoverlay.update_signal.emit(worker.worker, worker.scheduler, 
                                         str(day-1), str(start.GetMoneyNow()), 
                                         str(start.GetShopCount(day-1)), str(start.GetCustomerPoints()),
                                         str(start.GetRank(start.GetCustomerPoints())), 
                                         str(start.ord.GetStarCount(0)), str(start.ord.GetStarCount(1)), 
                                         str(start.ord.GetStarCount(2)), str(start.ord.GetStarCount(3)),
                                         str(start.ord.GetStarCount(-1)))

        while worker.runner:
            if worker.worker:
                worker.worker.sort(key=lambda x: x[0])
                screenoverlay.update_signal.emit(worker.worker, worker.scheduler, str(day-1), str(start.GetMoneyNow()), 
                                         str(start.GetShopCount(day-1)), str(start.GetCustomerPoints()),
                                         str(start.GetRank(start.GetCustomerPoints())), 
                                         str(start.ord.GetStarCount(0)), str(start.ord.GetStarCount(1)), 
                                         str(start.ord.GetStarCount(2)), str(start.ord.GetStarCount(3)),
                                         str(start.ord.GetStarCount(-1)))
        
                task = worker.worker.pop(0)
                #print(task[1])
                task[1](*task[2])
            time.sleep(0.1)

        scheduler_thread.join()

        print('next day is', day)
        daylog = [currentDay, start.GetMoney(), start.GetShopCount(currentDay), start.GetCustomerPoints(), 
                  start.GetRank(start.GetCustomerPoints()), start.ord.GetStarCount(0), 
                  start.ord.GetStarCount(1), start.ord.GetStarCount(2), start.ord.GetStarCount(3),
                  start.ord.GetStarCount(-1)]
        print(daylog)
        log.loc[len(log)] = daylog

        start.ord.SaveDict()

    print(log)

    with pd.ExcelWriter('./data.xlsx', mode="a", engine="openpyxl", if_sheet_exists="replace") as writer:
        log.to_excel(writer, sheet_name=str(currentDay), index=False, header=True, startrow=0)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    screenoverlay = Overlay()

    # Start your main logic in a background thread
    logic_thread = threading.Thread(target=main, args=())
    logic_thread.daemon = True
    logic_thread.start()

    # Start the Qt event loop in the main thread
    sys.exit(app.exec_())

    logic_thread.join()