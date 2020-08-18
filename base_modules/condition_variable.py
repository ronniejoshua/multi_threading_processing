#!/usr/bin/env python3

""" Two hungry people, anxiously waiting for their turn to take soup """

"""
Barron and I just made a slow cooker full of delicious hot soup and I'm ready to dig in. - But we should take turns to 
make sure we each get our fair share of soup. In this scenario, we're two hungry threads, competing for access to a 
shared resource, the soup. And the slow cooker lid will act as a mutex to protect it. Only the thread that holds the 
lid can 

check to see how much soup is left, 
determine if it's their turn to take the next serving, 
and modify the amount of soup that's left by taking some. 


What is busy waiting, or spinning, repeatedly acquiring and releasing the lock to check for a certain condition 
to continue. It isn't very efficient, especially if it goes on for a long time. - This is one of the limitations of 
using just a mutex. Sure it restricts multiple threads from taking soup at the same time, a way to signal each other 
to synchronize our actions. 

To do that, we can use another mechanism called a condition variable, which serves as a queue or container for threads 
that are waiting for a certain condition to occur. Think of it as a place for threads to wait and be notified. The 
condition variable is associated with a mutex, and they work together to implement a higher level construct 
called a monitor. 

Monitors protect a critical section of code with mutual exclusion, and they provide the ability for threads to wait 
or block until a certain condition has become true along with a mechanism to signal those waiting threads when their 
condition has been met. Conceptually, you can think of a monitor like a room that contains the procedures and shared 
data that you want to protect. Only one thread can be in that room at a time to use those procedures and access the 
data. The mutex is a lock on the door, other threads that try to enter the protected section while it's occupied, will 
wait outside in a condition variable which is like a waiting room. They might all be waiting for the same condition to 
occur before they enter the monitor room, or there might be multiple condition variables, or multiple waiting rooms, 
waiting for different conditions to occur to acquire that same mutex. When the thread inside the monitor finishes its 
business in the critical section, it will signal one of the conditions that it's their turn to execute, then it releases
its lock on the door to exit the critical section. One of the threads waiting for that condition that was signaled, 
will wake up and take its turn in the monitor, locking the door behind it so it can execute the critical section. 

Now the condition variable has three main operations: Wait, signal, and broadcast. Before using a condition variable, 
I first need to acquire the mutex associated with it, check for my condition, I see that it's not my turn to take 
more soup, so I'll use the condition variables wait operation, which releases my lock on the mutex, and then puts my 
thread to sleep or a pause state, and places it into a queue waiting for another thread to signal that somebody else 
takes soup. - Since Barron releases his lock on the lid before going to sleep, now I can acquire it, see that it's my 
turn to take some soup, so I'll do that. Then I'll use the signal operation to wake up a single thread from the waiting 
queue, so it can acquire the lock. Depending on the language you're using, you'll also see this operation called notify 
or wake. Barron wake up, it's your turn to take some soup. Finally, I'll release my lock on the mutex. - Ah, my turn. 

The third condition variable operation, broadcast, is similar to the signal operation, except that it wakes up all of 
threads in the waiting queue. You might also see it called things like notify all or wake all. Now in this little 
scenario we only had two threads signaling each other on a single condition, that somebody took soup, which then 
changes who's turn it is to take the next serving. 

A more common use case that requires multiple condition variables is implementing a shared queue or buffer. If multiple 
threads will be putting items in a queue and taking them out, then it needs a mutex to ensure that only one thread can 
add or remove items from it at a time. And for that we can use two condition variables. If a thread tries to add an 
item to the queue, which is already full, then it can wait on a condition variable to indicate when the buffer is not 
full. 

And if a thread tries to take an item but the queue's empty then it can wait on another condition variable for 
BufferNotEmpty. These condition variables enable threads to signal each other when the state of the queue changes. 
"""

import threading

slowcooker_lid = threading.Lock()
soup_servings = 11

# Condition Variable
soup_taken = threading.Condition(lock=slowcooker_lid)


def hungry_person(person_id):
    global soup_servings
    while soup_servings > 0:

        # Acquiring/Releasing the the lock with context manager
        with slowcooker_lid:
            # check if it's your turn to take the soup.
            # if the its the right person's turn and there is soup left while evaluates to false
            while (person_id != (soup_servings % 5)) and (soup_servings > 0):
                print('Person', person_id, 'checked... then put the lid back.')
                soup_taken.wait()
            if soup_servings > 0:
                # it's your turn; take some soup!
                soup_servings -= 1
                print('Person', person_id, 'took soup! Servings left:', soup_servings)
                """
                 If you only need to signal one of the waiting threads, and you don't care which 
                 one it is, then the basic notify method will work fine. But in this example, 
                 since I want a specific thread, out of those five hungry_people to wake up and 
                 see that it's their turn. Relying on the signal notify method to wake up the right 
                 thread will not always work.
                """
                # soup_taken.notify()
                soup_taken.notify_all()


if __name__ == '__main__':
    for person in range(5):
        threading.Thread(target=hungry_person, args=(person,)).start()
