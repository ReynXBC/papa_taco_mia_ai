import time

runner = None

worker = []

scheduler = []

def scheduler_worker():
    while runner:
      if scheduler:
         scheduler.sort(key=lambda x: x[0])
         #print(scheduler[0][0],time.time())
         if scheduler[0][0] <= time.time():
            task = scheduler.pop(0)
            task[1](*task[2])
      time.sleep(0.1)
