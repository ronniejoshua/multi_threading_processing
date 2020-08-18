#!/usr/bin/env python3
""" Connecting cell phones to a charger """

"""
A semaphore is another synchronization mechanism that can be used to control access to shared resources, sort of like 
a mutex. But unlike a mutex, a semaphore can allow multiple threads to access the resource at the same time. And it 
includes a counter to track how many times it's been acquired or released. As long as the semaphore's count value is 
positive any thread can acquire the semaphore, which then decrements that counter value. 

If the counter reaches zero, then threads trying to acquire the semaphore will be blocked and placed in a queue to 
wait until it's available. When a thread is done using the resource it releases the semaphore, which increments 
that counter value. And if there are any other threads waiting to acquire the semaphore, they'll be signaled to wake 
up and do so. 

This type of semaphore that we're using here is called a counting semaphore because it can have a value of zero, one, 
two, three, and so on to represent the number of resources we have. In Software, a counting semaphore might be used to 
manage access among multiple threads to a limited pool of connections for something like a server or a database, or a 
counting semaphore could be used to track how many items are in a queue. 

Now, it's also common to restrict the possible values of a semaphore to only being either zero or one, with zero 
representing a locked state and one representing unlocked. This is called a binary semaphore and at first glance it 
looks a lot like a mutex. In fact, it can be used just like a mutex with a thread acquiring and releasing the semaphore 
to lock and unlock it. 

However, there is a key difference. A mutex can only be unlocked by the same thread that originally locked it. A 
semaphore on the other hand can be acquired and released by different threads. Any thread can increment the semaphore's 
value by releasing it or attempt to decrement the value by acquiring it. That may sound like a recipe for trouble and 
it certainly can be if you're not careful but the ability for different threads to increment and decrement a 
semaphore's value and for threads to wait and be signaled by the semaphore is what enables it to be used as a 
signaling mechanism to synchronize the action between threads. 

For example, a pair of semaphores can be used in a similar way to condition variables to synchronize producer and 
consumer threads, adding and removing elements from a shared finite cue or buffer. One semaphore tracks the number of 
items in the buffer, shown here as fill count, and the other one tracks the number of free spaces, which I'll call 
empty count. To add an element to the buffer, the producer will first acquire the empty count, which decrements its 
value, then it pushes the item into the buffer, and finally it releases the fill count semaphore to increment its value.

Now, on the other side of the buffer, when the consumer wants to take an item, it first acquires fill count to 
decrement its value, then it removes an item from the buffer, and finally increments the empty count by releasing it. 

Notice that the producer and consumer each acquire a different semaphore as the first operation in their respective 
sequences. If the consumer tries to take an item when the buffer is empty, then when it tries to acquire that fill 
count semaphore, it'll block and wait until a producer adds an item and releases fill count, which will then signal 
the consumer to continue. 

Likewise, if the producer tries to add an item to the full buffer, then it goes to acquire the empty count semaphore, 
it'll block and wait until a consumer removes an item and releases the empty count.
"""

import random
import threading
import time

# Counting Semaphore
charger = threading.Semaphore(4)

# Binary Semaphore/Mutex
# charger = threading.Semaphore(1)


def cellphone():
    name = threading.current_thread().getName()
    # The context manager does the following job
    # charger.acquire()
    # charger.release()
    with charger:
        print(name, 'is charging...')
        time.sleep(random.uniform(1, 2))
        print(name, 'is DONE charging!')


if __name__ == '__main__':
    # starting 10 cellphone threads
    for phone in range(10):
        threading.Thread(target=cellphone, name='Phone-' + str(phone)).start()
