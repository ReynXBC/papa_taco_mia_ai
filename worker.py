import threading
import sched
import time

# Lock and condition variable to synchronize access to the shared resource
lock = threading.Lock()

# Scheduler for managing task execution times
#scheduler = sched.scheduler(time.time, time.sleep)

# Event object to signal when the scheduler is allowed to stop
runner = None

# Scheduler for managing task execution times
scheduler = []

# List of Priority and Function for a task in format [Priority, Task, Arguements] or in type [float, function, list]
worker = []

# scheduler which adds the functions to the worker task Queue
def scheduler_worker():
    while runner:
      if scheduler:
         scheduler.sort(key=lambda x: x[0])
         #print(scheduler[0][0],time.time())
         if scheduler[0][0] <= time.time():
            task = scheduler.pop(0)
            task[1](*task[2])
      time.sleep(0.1)
