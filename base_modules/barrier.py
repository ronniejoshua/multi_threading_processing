#!/usr/bin/env python3
""" Deciding how many bags of chips to buy for the party """

"""
Barrier

To prevent our race condition from occurring, we need a way to synchronize our actions so we execute our 
respective multiplication and addition operations in the correct order. And we can do that with something 
called a barrier. 

A barrier is a stopping point for a group of threads that prevents them from proceeding until all or enough 
threads have reached the barrier. I like to think of threads waiting on a barrier like players on a sports 
team coming together for a huddle. Before they join the huddle, the players might be doing other things, 
putting on their equipment or getting a drink of water. As they finish those individual activities, they join 
their teammates at the huddle. Players in the huddle wait there until all of their fellow teammates arrive, then 
they all yell break, and then, they scatter about to continue playing their game. 

We can use a similar strategy here to solve our race condition. Huddling together to synchronize when we each 
execute our operations to add and multiply items on the shopping list. I should complete my operation of adding 
three bags of chips to the list before we huddle together. 
"""

import threading

# start with one on the list
bags_of_chips = 1
pencil = threading.Lock()

# Number of threads to wait on the Barrier before it releases
# 5 Each for Baron and Olivia, hence 10
fist_bump = threading.Barrier(10)


def cpu_work(work_units):
    """
    Simulating CPU intensive work
    """
    x = 0
    for work in range(work_units * 1_000_000):
        x += 1


def barron_shopper():
    global bags_of_chips

    # do a bit of work first
    cpu_work(1)
    fist_bump.wait()

    # With context manager acquires and releases the threading lock
    with pencil:
        bags_of_chips *= 2
        print("Barron DOUBLED the bags of chips.")


def olivia_shopper():
    global bags_of_chips

    # do a bit of work first
    cpu_work(1)

    # With context manager acquires and releases the threading lock
    with pencil:
        bags_of_chips += 3
        print("Olivia ADDED 3 bags of chips.")
    fist_bump.wait()


if __name__ == '__main__':
    shoppers = []
    for s in range(5):
        shoppers.append(threading.Thread(target=barron_shopper))
        shoppers.append(threading.Thread(target=olivia_shopper))
    for shopper in shoppers:
        shopper.start()
    for shopper in shoppers:
        shopper.join()
    print('We need to buy', bags_of_chips, 'bags of chips.')
