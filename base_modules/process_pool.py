#!/usr/bin/env python3
""" Chopping vegetables with a ThreadPool """

"""
Process pool: Python demo

Python's ThreadPoolExecutor is great when you have a bunch of IO-dependent tasks to perform. However, if the tasks are 
primarily CPU intensive, then there isn't much benefit to running them all in concurrent threads due to the global 
interpreter lock. The workaround in Python is to use multiple processes. So, in addition to the ThreadPoolExecutor, 
the Python concurrent.futures module also has a ProcessPoolExecutor. 

Both the ThreadPoolExecutor and the ProcessPoolExecutor are designed to be used with a context manager.The context 
manager automatically shuts down the pool when it's done.
"""

from concurrent.futures import ProcessPoolExecutor
import os


def vegetable_chopper(vegetable_id):
    name = os.getpid()
    print(f'{name} chopped vegetable {vegetable_id}\n')


if __name__ == '__main__':
    with ProcessPoolExecutor(max_workers=5) as pool:
        for vegetable in range(100):
            pool.submit(vegetable_chopper, vegetable)
