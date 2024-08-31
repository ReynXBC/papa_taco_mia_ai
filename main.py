import threading
import startup as start
import worker
import time

DAY = 1
start.StartGame()
DAY = 2

#USE THIS ONE TO CHANGE THE DAY
#DAY = 7

while DAY <= 50:
    scheduler_thread = threading.Thread(target=worker.scheduler_worker, name='scheduler thread')
    scheduler_thread.daemon = True

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