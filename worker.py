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
scheduler = sched.scheduler(time.time, time.sleep)

# scheduler which adds the functions to the worker task Queue
def scheduler_worker():
    while runner == True:
        scheduler.run()