#!/usr/bin/env python3
"""
Anytime multiple threads are concurrently reading and writing a shared resource,
it creates the potential for incorrect behavior, like a data race, but we can defend
against that by identifying and protecting critical sections of code.

A critical section or critical region is part of a program that accesses a shared resource,
such as a data structured memory or an external device, and it may not operate correctly
if multiple threads concurrently access it. The critical section needs to be protected
so that it only allows one thread or process to execute in it at a time.

What is Mutex or Mutual Exclusion Or Lock?
Only one thread or process can have possession of the lock at a time so it can be used to
prevent multiple threads from simultaneously accessing a shared resource, forcing them to take turns.

1. acquire the lock
2. change the state of the data
3. release the lock


The operation to acquire the lock is an atomic operation, which means it's always executed as a single,
indivisible action. To the rest of the system, an atomic operation appears to happen instantaneously,
even if under the hood it really takes multiple steps. The key here is that the atomic operation
is un-interruptible. Acquiring the mutex is an atomic action that no other thread can interfere
with halfway through. Either you have the mutex, or you don't.

Threads that try to acquire a lock that's currently possessed by another thread, can pause and wait
until it's available. Since threads can get blocked and stuck waiting for a thread in the critical
section to finish executing, it's important to keep the section of code protected with the mutex as
short as possible.

"""

import threading
import time

counter = 0
mutex_lock = threading.Lock()


def data_race_counter():
    global counter
    for i in range(5):
        print(f'{threading.current_thread().getName()} is thinking.')
        time.sleep(0.5)
        mutex_lock.acquire()
        counter += 1
        mutex_lock.release()


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

    print(f'The Counter Variable is at {counter} ')
