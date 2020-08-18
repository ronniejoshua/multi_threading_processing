#!/usr/bin/env python3
""" Producers serving soup for Consumers to eat """

"""
Producer-consumer processes: Python demo

We were able to resolve the buffer overflow problem in the previous producer consumer example by adding an additional 
consumer thread. That worked because we simulated the time it took for a producer to add items to the queue and 
for the consumer to process those items by using the sleep statements. 

When a thread is sleeping, it does not use CPU resources. So that scenario represents a situation where the consumers 
are performing an I/O bound task. Like downloading files over a network. 


But what would happen if the consumers task was CPU intensive instead. Perhaps the producer was streaming data that 
the consumer needed to process in real time. 

To simulate that scenario, I'll define a new helper function called CPU work and I'll pass it in argument representing 
the amount of CPU work to simulate. Within the function, I'll simply create a variable named X. And initialize it to 
zero. And then I'll use a for loop to increment X by the number of work units times one million. And within that loop, 
I'll simply do X plus equals one. 

This simulates a CPU intensive operation that will keep the processor busy for a period of time. 

Now down in the consumer function, I'll replace the 300 millisecond sleep statement on line 97 with a call to CPU work 
for four units of work. That should take roughly the same amount of time or 300 milliseconds. I'll leave the producer 
function alone for now so it will continue putting new elements into the queue at a steady rate of once every 200 
milliseconds. 


We can see down in the main, that the program will spawn two consumer threads and one producer thread. 
As you can see it fills up the queue and the producer error's out. 

The problem here is with Python. In particular the global interpreter lock. The global interpreter lock or GIL only 
allows one Python thread to execute at a time. So at any given moment, only one of the consumer threads will actually 
be executing the CPU work task. That's why creating more threads doesn't solve our problem. To get around this 
limitation in Python, we can restructure the program to use multiple processes instead. 

To do that, I'll replace the import threading statement to import the multi-processing package as mp. 

Then I'll replace the regular queue to use the queue class from the multi-processing module which is 
specifically designed to exchange data between processes. And it doesn't need the max size argument name there. 

Since we'll be spawning the producer and consumer as separate processes, in order for them to see the same serving 
line queue object, we'll need to pass it as an input argument to their functions. 

Finally, down in the main section, I'll replace the lines to create the consumer and producer threads with their 
counterparts to create processes instead. 

That was necessary in this scenario due to the CPU intensive work load but if the consumer tasks were I/O bound, 
then simply using threads will usually work just fine.
"""

from base_modules.my_queue import MyQueue
import multiprocessing as mp
import time

serving_line = MyQueue(5)


# Simulate CPU Intensive task
def cpu_work(work_units):
    x = 0
    for work in range(work_units * 1_000_000):
        x += 1


def soup_producer(serving_line):
    # serve 20 bowls of soup
    for i in range(20):
        serving_line.put_nowait('Bowl #' + str(i))
        print('Served Bowl #', str(i), '- remaining capacity:', serving_line._maxsize - serving_line.qsize())
        # time to serve a bowl of soup [200 milliseconds]
        time.sleep(0.2)

    serving_line.put_nowait('no soup for you!')
    serving_line.put_nowait('no soup for you!')


def soup_consumer(serving_line):
    # continuously take soup from the queue
    while True:
        bowl = serving_line.get()
        # Out Production Condition
        if bowl == 'no soup for you!':
            break
        print('Ate', bowl)
        # time to eat a bowl of soup
        cpu_work(4)


if __name__ == '__main__':
    for consumer in range(2):
        mp.Process(target=soup_consumer, args=(serving_line,)).start()
    mp.Process(target=soup_producer, args=(serving_line,)).start()
