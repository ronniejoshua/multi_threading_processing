#!/usr/bin/env python3
""" Check how many vegetables are in the pantry """

"""
Future

Launching asynchronous tasks is a great way to accomplish multiple things at once. A Future acts as a placeholder 
for a result that's initially unknown, but will be available at some point in the future. It provides a mechanism 
to access the result of an asynchronous operation. Future is like an IOU note for the result. 

When you submit a task to an executor in Python, the submit method returns an instance of the future class, 
which encapsulates the asynchronous execution of the callable task. The future class has several methods that 
can be used to check the status of the task's execution. Cancel it if needed. 

And most importantly, it has a method named result() which is used to retrieve the return value after the call 
has completed. 

Calling the future object's result method will give me the return value from that function. However, if the future 
has not completed execution yet, then invoking the result method will block and wait until it's ready. 
"""


from concurrent.futures import ThreadPoolExecutor
import time


def how_many_vegetables():
    print('Olivia is counting vegetables...')
    time.sleep(3)
    return 42


if __name__ == '__main__':
    print('Barron asks Olivia how many vegetables are in the pantry.')
    with ThreadPoolExecutor() as pool:
        future = pool.submit(how_many_vegetables)
        print('Barron can do others things while he waits for the result...')
        print('Olivia responded with', future.result())
