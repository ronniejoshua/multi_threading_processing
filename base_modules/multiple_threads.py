#!/usr/bin/env python3
import os
import threading
import time

"""
Parallel processing can be achieved in Python in two different ways: 
multiprocessing and threading.

All the threads of a process live in the same memory space, whereas processes 
have their separate memory space.

Threads are more lightweight and have lower overhead compared to processes. 
Spawning processes is a bit slower than spawning threads.

Sharing objects between threads is easier, as they share the same memory space. 
To achieve the same between process, we have to use some kind of IPC (inter-process communication) 
model, typically provided by the OS.
"""


# a simple function that wastes CPU cycles forever
def cpu_waster():
    while True:
        time.sleep(60)
        break


# display information about this process
print('Currently Running Process ID: ', os.getpid())
print('Return the number of Thread objects currently alive.', threading.active_count())

# Return a list of all Thread objects currently alive.
for thread in threading.enumerate():
    print(thread)

print('*' * 50)


# Start the thread’s activity. using .start()
# The threading.Thread() class represents an activity that is run in a separate
# thread of control. There are two ways to specify the activity:
# by passing a callable object to the constructor


print('Starting 6 CPU Wasters...')
for i in range(6):
    threading.Thread(target=cpu_waster).start()
print('*' * 50)

# Again display information about this process

print('Currently Running Process ID: ', os.getpid())
print('Return the number of Thread objects currently alive.', threading.active_count())

for thread in threading.enumerate():
    # Outputs 6 thread + 1 Main Thread
    print(thread)
print('*' * 50)

