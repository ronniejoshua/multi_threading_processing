#!/usr/bin/env python3
""" Three philosophers, thinking and eating sushi

Abandoned lock is another form of a deadlock through thread death. If one thread or process acquires a
lock and then terminates because of some unexpected reason it may not automatically release the lock
before it disappears. That leaves others tasks stuck waiting for a lock that will never be released.

It's good practice to always make sure locks will be released, if something goes wrong and unexpectedly
crashes a thread. And Python makes that especially easy, because lock objects support working with
context managers.

Using the with statement on a lock, is equivalent to using the try and finally blocks. Using a context
manager is the more pythonic way to program
"""
import threading
import time

chopstick_a = threading.Lock()
chopstick_b = threading.Lock()
chopstick_c = threading.Lock()
sushi_stock = 500


def philosopher_with(thread_name, first_chopstick, second_chopstick):
    global sushi_stock
    while sushi_stock > 0:
        # Using the Context Manager Construct
        with first_chopstick:
            with second_chopstick:
                if sushi_stock > 0:
                    sushi_stock -= 1
                    print(f'{thread_name}, took a piece! Sushi remaining: {sushi_stock}')

                if sushi_stock == 10:
                    print(1 / 0)


def philosopher_try(thread_name, first_chopstick, second_chopstick):
    global sushi_stock
    while sushi_stock > 0:
        first_chopstick.acquire()
        second_chopstick.acquire()
        # Using Try - finally Construct
        try:
            if sushi_stock > 0:
                sushi_stock -= 1
                print(f'{thread_name}, took a piece! Sushi remaining: {sushi_stock}')
            if sushi_stock == 10:
                print(1 / 0)
        except ZeroDivisionError as error:
            print('Division By Zero')
        finally:
            second_chopstick.release()
            first_chopstick.release()


if __name__ == '__main__':
    threading.Thread(target=philosopher_with, args=('Barron', chopstick_a, chopstick_b)).start()
    threading.Thread(target=philosopher_with, args=('Olivia', chopstick_b, chopstick_c)).start()
    threading.Thread(target=philosopher_with, args=('Steve', chopstick_a, chopstick_c)).start()
