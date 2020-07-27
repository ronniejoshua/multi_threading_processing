#!/usr/bin/env python3
"""
A data race occurs when: two or more threads in a single process access
the same memory location concurrently, and. at least one of the accesses is
for writing, and. the threads are not using any exclusive locks to control
their accesses to that memory.

Since a data race only occurs when at least one of the concurrent threads is
modifying the value of a memory location, pay close attention to anywhere you
use an assignment operation, or an operator like the plus equal incrementor
that changes a variable's value. If there's a potential for two or more threads
to access that variable and make changes to it, then you'll almost certainly
need to use some sort of mechanism to protect it.

"""

import threading

counter = 0


def data_race_counter():
    global counter
    for i in range(10_000_000):
        counter += 1


if __name__ == '__main__':

    print(threading.main_thread())

    # Two threads which concurrently increments a shared variable
    # Initializing the Threads
    thread_one = threading.Thread(target=data_race_counter)
    thread_two = threading.Thread(target=data_race_counter)

    # Starting the Threads
    thread_one.start()
    thread_two.start()

    # Calling the join() to wait until they are both done
    thread_one.join()
    thread_two.join()

    print(f'The Counter Variable is at {counter} instead of 20_000_000')
