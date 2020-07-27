#!/usr/bin/env python3
""" Two threads chopping vegetables """

import threading
import time

loop_condition = True


def counter_using_threads():
    # Get the name of the current tread
    thread_name = threading.current_thread().getName()
    intial_count_val = 0
    while loop_condition:
        print(f'{thread_name} Performed an Operation!\n')
        intial_count_val += 1
    print(f'{thread_name} Performed an Operation {intial_count_val} times.\n')


if __name__ == '__main__':
    threading.Thread(target=counter_using_threads, name='A').start()
    threading.Thread(target=counter_using_threads, name='B').start()

    # Count for 1 Second
    time.sleep(1)

    # Change the Looping Condition / Stops Counting
    loop_condition = False
