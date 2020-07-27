#!/usr/bin/env python3
import threading
import time


# Spawned  and terminated


# JARVIS is the Child Thread
class JarvisProcess(threading.Thread):

    def __init__(self):
        # initializes the Super Class: threading.Thread
        super().__init__()

    def run(self):
        """
        Method representing the thread’s activity.
        The standard run() method invokes the callable object passed to the object’s
        constructor as the target argument, if any, with positional and keyword arguments
        taken from the args and kwargs arguments, respectively.
        """
        print('Jarvis started & waiting for job to be done...')
        time.sleep(3)
        print('Jarvis finished the job.')


# SKYNET is the main thread
if __name__ == '__main__':
    print("Skynet(Main Thread) started & requesting Jarvis's help.")
    # Child Thread initialized but not started
    jarvis = JarvisProcess()
    print('  Jarvis alive?:', jarvis.is_alive())

    print('Skynet tells jarvis to start.')
    # Child Thread started
    jarvis.start()
    print('  Jarvis alive?:', jarvis.is_alive())

    print('Skynet continues doing the job.')
    time.sleep(0.5)
    print('  Jarvis alive?:', jarvis.is_alive())

    print('Skynet patiently waits for Jarvis to finish and join...')
    # Main thread waits for the Child thread to finish the job and join
    jarvis.join()
    print('  Jarvis alive?:', jarvis.is_alive())

    print('Skynet and Jarvis are both done!')
