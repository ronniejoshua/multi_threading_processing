#!/usr/bin/env python3

"""
Race condition

Data races and race conditions are two different potential problems in concurrent programs that people often confuse
with each other probably because they have similar sounding names with the word race in them.

Data races can occur when two or more threads concurrently access the same memory location. If at least one of those
threads is writing to, or changing that memory value, that can cause the threads to overwrite each other or read
wrong values.

That's a pretty straightforward definition, which makes it possible to create automated tools to identify potential
data races in code. And to prevent those data races, you need to ensure mutual exclusion for the shared resource.

A race condition, on the other hand, is a flaw in the timing or ordering of a program's execution that causes
incorrect behavior. In practice, many race conditions are caused by data races, and many data races lead to race
conditions. But those two problems are not dependent on each other. - It's possible to have data races without a
race condition and race conditions without a data race.

Race conditions can be really hard to discover and that's because a program might run correctly for millions of
times while you're building and testing it, so you think everything's fine. You release the finished program,
and then one time, things happen to execute in a different order and that causes an incorrect result.

Unfortunately, there's not a single catchall way to detect race conditions. Sometimes putting sleep statements at
different places throughout your code can help to uncover potential race conditions by changing the timing and,
therefore, order in which threads get executed.

That said, race conditions are often a type of heisenbug, which is a software bug that seems to disappear, or
alter its behavior, when you try to study it. Running debuggers and doing things to affect the timing of your code
in search of a race condition may actually prevent the race condition from occurring.
"""

""" Deciding how many bags of chips to buy for the party """

import threading

# start with one on the list
bags_of_chips = 1
pencil = threading.Lock()


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


if __name__ == "__main__":

    shoppers = list()

    for i in range(5):
        shoppers.append(threading.Thread(target=barron_shopper))
        shoppers.append(threading.Thread(target=olivia_shopper))

    for shopper in shoppers:
        shopper.start()

    for shopper in shoppers:
        shopper.join()

    print("We need to buy", bags_of_chips, "bags of chips.")
