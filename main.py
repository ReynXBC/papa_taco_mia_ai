import threading
import startup as start
import worker
import time
import pandas as pd

log = pd.DataFrame(columns=['Day','Money','Shop Items Remaining','Customer Points', 'Rank', '0-Star', '1-Star', '2-Star', '3-Star', 'Total Customers'])

DAY = 1
start.StartGame()
DAY = 2

daylog = [DAY-1, start.GetMoney(), start.GetShopCount(DAY-1), start.GetCustomerPoints(), 
              start.GetRank(start.GetCustomerPoints()), start.ord.GetStarCount(0), 
              start.ord.GetStarCount(1), start.ord.GetStarCount(2), start.ord.GetStarCount(3),
              start.ord.GetStarCount(-1)]
print(daylog)
log.loc[len(log)] = daylog

#USE THIS ONE TO CHANGE THE DAY
#DAY = 16

if DAY > 2:
    start.ord.LoadDict()

while DAY <= 30:
    daylog = []

    scheduler_thread = threading.Thread(target=worker.scheduler_worker, name='scheduler thread')
    scheduler_thread.daemon = True
    
    currentDay = DAY

    start.StartDay(DAY)
    DAY += 1
    scheduler_thread.start()

    while worker.runner:
        if worker.worker:
            worker.worker.sort(key=lambda x: x[0])
            task = worker.worker.pop(0)
            print(task[1])
            task[1](*task[2])
        time.sleep(0.1)

    scheduler_thread.join()

    print('next day is', DAY)
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