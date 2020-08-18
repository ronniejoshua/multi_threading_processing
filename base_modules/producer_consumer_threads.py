#!/usr/bin/env python3


""" Producers serving soup for Consumers to eat """

"""
Producer-consumer
-----------------
A common design pattern in concurrent programming is the producer-consumer architecture where one or more threads, 
or processes, act as a producer, which adds elements to some shared data structure. And one or more other threads 
act as a consumer which removes items from that structure and does something with them. 

Queues operate on a principle called a First-In-First-Out or FIFO, which means items are removed in the same order 
that they're put into the queue. The first item that was added will be the first item to be removed. 

The bowls of soup represent elements of data for the consumer thread to process, or perhaps packaged tasks for the 
consumer to execute. Now when multiple threads are operating in the type of producer-consumer situation it poses 
several challenges for synchronization. 

First off, the queue is a shared resource, so we'll need something to enforce mutual exclusion and make sure that only 
one thread can use it at a time to add or remove items. We also need to make sure that the producer will not try to add 
data to the queue when it's full, and that the consumer won't try to remove data from an empty buffer. Some programming 
languages may include implementations of a queue that's considered thread-safe and handles all of these challenges under 
the hood so you don't have to, but if your language does not include that support, then you can use the combination of 
a mutex and condition variables to implement your own thread-safe synchronized queue. 


You may run into scenarios where the producer cannot be paused if the queue fills up. The producer might be an external
source of streaming data that you can't slow down. So it's important to consider the rate at which items are produced 
and consumed from the queue. 

If the consumer can't keep up with production then we face a buffer overflow and we'll lose data. Some programming 
languages offer implementations of unbounded queues which are implemented using linked lists to have an advertised 
unlimited capacity. But keep in mind even those will be limited by the amount of physical memory in the computer. 

The rate at which the producer is adding items may not always be consistent. For example, in network applications 
data might arrive in bursts of network brackets But if those bursts occur rather infrequently then consumer has time 
to catch up between bursts. You should consider the average rate at which items are produced and consumed. 

You want the average rate of production to be less than the average rate of consumption. 
 
A pipeline consists of a chain of processing elements arranged so that the output of each element is the input to 
the next one. It's basically a series of producer-consumer pairs connected together with some sort of buffer like a 
queue between each consecutive element. 

Now the issue of processing rates is still a concern, each element needs to be able to consume and process data faster 
than the elements upstream can produce it.
"""

import queue
import threading
import time

serving_line = queue.Queue(maxsize=5)


def soup_producer():
    # serve 20 bowls of soup
    for i in range(20):
        serving_line.put_nowait('Bowl #' + str(i))
        print('Served Bowl #', str(i), '- remaining capacity:', serving_line.maxsize - serving_line.qsize())

        # time to serve a bowl of soup
        time.sleep(0.2)

    # Because there are two consumers
    serving_line.put_nowait('no soup for you!')
    serving_line.put_nowait('no soup for you!')


def soup_consumer():
    # continuously take soup from the queue
    while True:
        bowl = serving_line.get()

        # Out Production Condition
        if bowl == 'no soup for you!':
            break
        print('Ate', bowl)

        # time to eat a bowl of soup
        time.sleep(0.3)


if __name__ == '__main__':

    # Two consumers threads to eat the soup
    # Adding two consumers avoided the buffer overflow problem
    for consumer in range(2):
        threading.Thread(target=soup_consumer).start()

    # Soup Production
    threading.Thread(target=soup_producer).start()
