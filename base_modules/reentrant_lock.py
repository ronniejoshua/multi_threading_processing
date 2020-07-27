#!/usr/bin/env python3
"""
If a thread tries to lock a mutex that it's already locked, it'll enter into a waiting list
for that mutex, which results in something called a deadlock, because no other thread can unlock
that mutex. - There may be times when a program needs to lock a mutex multiple times before unlocking it.

In that case, you should use a reentrant mutex to prevent this type of problem. A reentrant mutex is a
particular type of mutex that can be locked multiple times by the same process or thread.
Internally, the reentrant mutex keeps track of how many times it's been locked by the owning thread,
and it has to be unlocked an equal number of times before another thread can lock it.

One interesting difference between the regular lock and Rlock in Python is that the regular lock can be
released by different threads than the one that acquired it, but the reentrant lock must be released by
the same thread that acquired it. And of course, it must be released by that thread as many times as it
was acquired before it will be available for another thread to take. This is just the difference between
how lock and Rlock are implemented in Python.
"""

import threading

counter_one, counter_two = (0, 0)
reentrant_mutex = threading.RLock()


def counter_one_increment():
    global counter_one
    reentrant_mutex.acquire()
    counter_one += 1
    reentrant_mutex.release()


def counter_two_increment():
    global counter_two
    reentrant_mutex.acquire()
    counter_two += 1
    # Case where we try to re-acquire the mutex
    counter_one_increment()
    reentrant_mutex.release()


def shopper():
    for i in range(10_000):
        counter_one_increment()
        counter_two_increment()


if __name__ == '__main__':
    print(threading.main_thread())

    # Two threads which concurrently increments a shared variable
    # Initializing the Threads
    thread_one = threading.Thread(target=shopper)
    thread_two = threading.Thread(target=shopper)

    # Starting the Threads
    thread_one.start()
    thread_two.start()

    # Calling the join() to wait until they are both done
    thread_one.join()
    thread_two.join()

    print(f'The Counter One Variable is at {counter_one} ')
    print(f'The Counter Two Variable is at {counter_two} ')
