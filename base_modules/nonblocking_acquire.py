#!/usr/bin/env python3
"""
Rather than using the standard locking method to acquire the mutex, Use what's called Try Lock, or Try Enter,
which is a non-blocking version of the lock or acquire method.

It returns immediately and one of two things will happen. If the mutex you're trying to lock is available,
it will get locked and the method will return true.

Otherwise, if the mutex is already possessed by another thread, the Try Lock method will immediately return false.
That return value of true or false lets the thread know whether or not it was successful in acquiring the lock.
"""

import threading
import time

hits_counter = 0
non_blocking_mutex = threading.Lock()


def web_visits():
    global hits_counter
    thread_name = threading.current_thread().getName()
    website_hits = 0
    while hits_counter <= 20:
        # if the website hits (0 = False) and mutex is non blocking
        # setting acquire(blocking=False) returns True
        # False and True = False
        if website_hits and non_blocking_mutex.acquire(blocking=False):
            hits_counter += website_hits
            print(thread_name, 'added', website_hits, 'item(s) to hits counter.')
            website_hits = 0
            # time spent writing
            time.sleep(0.3)
            non_blocking_mutex.release()
        # the continue looking for other things
        else:
            time.sleep(0.1)  # time spent searching
            website_hits += 1
            print(thread_name, 'found something else to buy.')


if __name__ == '__main__':
    print(threading.main_thread())
    thread_one = threading.Thread(target=web_visits, name='thread_one')
    thread_two = threading.Thread(target=web_visits, name='thread_two')

    start_time = time.perf_counter()

    # Starting the Threads
    thread_one.start()
    thread_two.start()

    # Calling the join() to wait until they are both done
    thread_one.join()
    thread_two.join()

    elapsed_time = time.perf_counter() - start_time
    print('Elapsed Time: {:.2f} seconds'.format(elapsed_time))
