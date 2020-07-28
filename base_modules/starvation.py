#!/usr/bin/env python3
""" Three philosophers, thinking and eating sushi

The operating system decides when each of the threads gets scheduled to execute and depending on the
timing of that, it can lead to problems.

If that happens occasionally, it's probably not a big deal, but if it happens regularly. - Too slow. -
Then then the thread's going to starve.

Another thing that can lead to starvation is having too many concurrent threads.
"""

import threading
import time

chopstick_a = threading.Lock()
chopstick_b = threading.Lock()
chopstick_c = threading.Lock()
sushi_stock = 500000


def philosopher(thread_name, first_chopstick, second_chopstick):
    global sushi_stock
    sushi_eaten = 0
    while sushi_stock > 0:
        with first_chopstick:
            with second_chopstick:
                if sushi_stock > 0:
                    sushi_stock -= 1
                    sushi_eaten += 1
                    # print(f'{thread_name}, took a piece! Sushi remaining: {sushi_stock}\n')
    print(f'{thread_name}, took {sushi_eaten}, pieces\n')


if __name__ == '__main__':
    for thread in range(3):
        threading.Thread(target=philosopher, args=('Barron', chopstick_a, chopstick_b)).start()
        threading.Thread(target=philosopher, args=('Olivia', chopstick_a, chopstick_b)).start()
        threading.Thread(target=philosopher, args=('Steve', chopstick_a, chopstick_b)).start()
        time.sleep(1)
        print("*" * 50)
