#!/usr/bin/env python3
""" Threads that waste CPU cycles """

import os
import threading
import multiprocessing as mp
import time


# a simple function that wastes CPU cycles forever
def cpu_waster():
    print('Process ID: ', os.getpid())
    while True:
        time.sleep(30)
        break


print(f"Python Module name is {__name__}")
if __name__ == '__main__':
    # display information about this process
    print('*' * 50)
    print('Process ID: ', os.getppid())
    print('Return the number of Thread objects currently alive.', threading.active_count())

    # Return a list of all Thread objects currently alive.
    for thread in threading.enumerate():
        print(thread)

    print('*' * 50)
    print('Starting 6 CPU Wasters...')
    for i in range(6):
        mp.Process(target=cpu_waster).start()
        time.sleep(1)

    # display information about this process
    print('*' * 50)
    print('Process ID: ', os.getppid())
    print('Return the number of Thread objects currently alive.', threading.active_count())
    # Return a list of all Thread objects currently alive.
    for thread in threading.enumerate():
        print(thread)
