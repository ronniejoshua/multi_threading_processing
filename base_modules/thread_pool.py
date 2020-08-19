#!/usr/bin/env python3
""" Chopping vegetables with a ThreadPool """

"""
Thread pool

After identifying the tasks in a program that can run asynchronously, one way to run those tasks in parallel is to 
create independent threads or processes for each of them. 

In some scenarios, rather than creating a new thread for every single task, it can be more efficient to use a thread  
pool, which creates and maintains a small collection of worker threads. As the program submits tasks to the thread pool, 
the thread pool reuses those existing worker threads to execute the tasks. Submitting tasks to a thread pool is 
like adding them to a to-do list for the worker threads.

Reusing threads with a thread pool addresses the overhead involved with creating new threads, and that becomes a 
real advantage when the time it takes to execute the task is less than the time required to create a new thread. 

Since our threads already exist, when a new task arrives, we eliminate the delay of thread creation, which can make 
our program more responsive.


To create a thread pool in Python, we'll be using the ThreadPoolExecutor Class which is part of the 
concurrent.futures module. It provides a high-level interface for asynchronously running tasks rather 
than working with individual threads directly. Under the hood, the ThreadPoolExecutor manages a pool of 
threads so that you don't have to manually create new threads for each task. You simply submit callable 
objects to the ThreadPoolExecutor, and it assigns them to existing threads in its thread pool to run 
asynchronously. 

By default, if you do not specify a value for max_workers, it gets set to none, which will make the ThreadPoolExecutor 
create up to five times as many threads as there are processors in the system. This is based on the assumption that 
thread pools are commonly used to overlap IO bound tasks rather than CPU intensive tasks, so the number of threads 
should exceed the number of processors.
 
 
Calling shutdown will free up any resource that the pool is using after all of its remaining submitted tasks have 
finished executing. You can't submit any more tasks after calling shutdown. By default, the wait parameter is set 
to True, which prevents the shutdown method from returning until all of the pending tasks have finished and the 
resources have been freed. 
"""

import threading
from concurrent.futures import ThreadPoolExecutor


def vegetable_chopper(vegetable_id):
    name = threading.current_thread().getName()
    print(f'{name} chopped vegetable {vegetable_id}\n')


if __name__ == '__main__':
    pool = ThreadPoolExecutor(max_workers=5)
    for vegetable in range(100):
        pool.submit(vegetable_chopper, vegetable)
    pool.shutdown()
