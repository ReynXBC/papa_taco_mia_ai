import threading
import startup as start
import worker

# day = 1
# start.StartGame()
DAY = 23

while DAY <= 30:
    scheduler_thread = threading.Thread(target=worker.scheduler_worker, name='scheduler thread')
    scheduler_thread.daemon = True

    start.StartDay(DAY)
    DAY += 1
    scheduler_thread.start()

    if worker.runner:
        worker.sort(key=lambda x: x[0])
        task = worker.pop(0)
        task[1](*task[2])

    scheduler_thread.join()

    print('next day is', DAY)
