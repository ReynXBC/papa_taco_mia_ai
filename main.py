import startup as start
import worker
import threading

#day = 1
#start.StartGame()
day = 23

while day <= 30:
   scheduler_thread = threading.Thread(target=worker.scheduler_worker,name='scheduler thread')
   scheduler_thread.daemon = True

   start.StartDay(day)
   day += 1
   scheduler_thread.start()

   scheduler_thread.join()

   print('next day is',day)