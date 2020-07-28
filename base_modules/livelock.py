#!/usr/bin/env python3
""" Three philosophers, thinking and eating sushi

A livelock looks similar to a deadlock in the sense that two threads are blocking each other
from making progress, but the difference is that the threads in a livelock are actively trying
to resolve the problem.

A livelock can occur when two or more threads are designed to respond to the actions of each other.
Both threads are busy doing something, but the combination of their efforts prevent them from actually
making progress and accomplishing anything useful.

The program will never reach the end. The ironic thing about livelocks is that they're often caused
by algorithms that are intended to detect and recover from deadlock.

If one or more process or thread takes action to resolve the deadlock, then those threads can end up
being overly polite and stuck in a livelock.

To avoid that, ensure that only one process takes action chosen by priority or some other mechanism,
like random selection.
"""

import threading
import time
from random import random

chopstick_a = threading.Lock()
chopstick_b = threading.Lock()
chopstick_c = threading.Lock()
sushi_stock = 500


def philosopher(thread_name, first_chopstick, second_chopstick):
    global sushi_stock
    while sushi_stock > 0:
        first_chopstick.acquire()
        # if the second_chopstick is not taken/blocking, release the first_chopstick
        if not second_chopstick.acquire(blocking=False):
            print(f'{thread_name}, released their first chopstick.\n')
            first_chopstick.release()
            time.sleep(random() / 10)
        else:
            try:
                if sushi_stock > 0:
                    sushi_stock -= 1
                    print(f'{thread_name}, took a piece! Sushi remaining: {sushi_stock}\n')
            finally:
                second_chopstick.release()
                first_chopstick.release()


if __name__ == '__main__':
    # Note without we are still running the priority strategy which results in a deadlock
    threading.Thread(target=philosopher, args=('Barron', chopstick_a, chopstick_b)).start()
    threading.Thread(target=philosopher, args=('Olivia', chopstick_b, chopstick_c)).start()
    threading.Thread(target=philosopher, args=('Steve', chopstick_c, chopstick_a)).start()
