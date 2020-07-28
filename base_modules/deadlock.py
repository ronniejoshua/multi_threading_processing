"""
What is a deadlock? When Each member of a group is waiting for some other member to take action
and as a result neither member is able to make progress.

Avoiding deadlock is a common challenge in concurrent programs that use mutual exclusion mechanisms to
protect critical sections of code.

We want our program to be free from deadlock to guarantee liveness which is a set of properties that
require concurrent programs to make progress.

Some processes or threads may have to take turns in a critical section but a well written program with
liveness guarantees that all processes will eventually make progress.
"""

import threading

chopstick_a = threading.Lock()
chopstick_b = threading.Lock()
chopstick_c = threading.Lock()
sushi_stock = 500


def philosopher(thread_name, first_chopstick, second_chopstick):
    global sushi_stock

    # eat sushi until it's all gone
    while sushi_stock > 0:
        first_chopstick.acquire()
        second_chopstick.acquire()

        if sushi_stock > 0:
            sushi_stock -= 1
            print(f'{thread_name}, took a piece! Sushi remaining: {sushi_stock}')

        second_chopstick.release()
        first_chopstick.release()


if __name__ == '__main__':
    """
    Solution of prioritizing the locks. We'll say that chopstick A has the highest priority, 
    B is second and C is third. And each philosopher should always acquire their highest 
    priority chopstick first.
    a > b > c
    
    Another technique for preventing deadlocks is to put a timeout on lock attempts. 
    If a thread is not able to successfully acquire all of the locks it needs within a 
    certain amount of time, it will back up, free all of the locks that it did take and 
    then wait for a random amount of time before trying again to give other threads a 
    chance to take the locks they need.
    """
    threading.Thread(target=philosopher, args=('Barron', chopstick_a, chopstick_b)).start()
    threading.Thread(target=philosopher, args=('Olivia', chopstick_b, chopstick_c)).start()
    threading.Thread(target=philosopher, args=('Steve', chopstick_a, chopstick_c)).start()
