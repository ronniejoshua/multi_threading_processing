#!/usr/bin/env python3
"""
Several users reading a calendar, but only a few users updating it
-------------------------------------------------------------------
We use a lock or mutex to protect a critical section of code to defend against data races,
which can occur when multiple threads are concurrently accessing the same location in memory 
and at least one of those threads is writing to that location. 

That second part is key, because if we have a bunch of threads and none of them are writing, 
they all just want to read from the same location, that's fine. It's okay to let multiple threads 
read the same shared value as long as no one else can change it. They'll all safely see the same thing. 

Danger only exists when you add a thread that's writing to the mix. When we use a basic lock or mutex 
to protect the shared resource, we limit access so that only one of the threads can use it at a time, 
regardless of whether that thread is reading or writing or both. - That works, but it's not necessarily 
the most efficient way to do things, especially when there are lots of threads that only need to read. 

This is where reader-writer locks can be useful. A reader-writer lock, or shared mutex, can be locked in 
one of two ways. 
    
    It can be locked in a shared read mode that allows multiple threads that only need to read  simultaneously 
    to lock it. 
    
    Or it can be locked in an exclusive write mode that limits access to only one thread at a time, allowing 
    that thread to safely write to the shared resource.

A thread trying to acquire the lock in write mode can't do so as long as it's still being held by any other 
threads in the read mode.
 
Only one thread can have the write lock at a time, all other threads wanting to read or write will have to wait 
until the lock becomes available again.

Now recognizing when to use a read-write lock is just as important as knowing how to use it. In certain scenarios, 
read-write locks can improve a program's performance versus  using a standard mutex. 

But they are more complicated to implement, and they typically use more resources  under the hood to keep track 
of the number of readers. Deciding which type of mutex to use is a complicated decision, but as a general rule 
of thumb, it makes sense to use a shared reader-writer lock when you have a lot more threads that will 
be reading from the shared data than the number of threads that will be writing to it, such as certain 
types of database applications. If the majority of your threads are writing, then there's not much, if any, 
advantage to using a read-write lock.
"""


import threading
from readerwriterlock import rwlock

WEEKDAYS = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
today = 0
# Gives Fair and Equal Priority to Reader and Writers
marker = rwlock.RWLockFair()


def calendar_reader(id_number):
    global today
    # Generates Reader Lock Object
    read_marker = marker.gen_rlock()
    name = 'Reader-' + str(id_number)
    while today < len(WEEKDAYS) - 1:
        read_marker.acquire()
        print(name, 'sees that today is', WEEKDAYS[today], '-read count:', read_marker.c_rw_lock.v_read_count)
        read_marker.release()


def calendar_writer(id_number):
    global today
    # Generates Writer Lock Object
    write_marker = marker.gen_wlock()
    name = 'Writer-' + str(id_number)
    while today < len(WEEKDAYS) - 1:
        write_marker.acquire()
        today = (today + 1) % 7
        print(name, 'updated date to ', WEEKDAYS[today])
        write_marker.release()


if __name__ == '__main__':
    # create ten reader threads
    for i in range(10):
        threading.Thread(target=calendar_reader, args=(i,)).start()
    # ...but only two writer threads
    for i in range(2):
        threading.Thread(target=calendar_writer, args=(i,)).start()
