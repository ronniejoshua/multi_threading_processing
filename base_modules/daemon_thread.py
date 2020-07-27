#!/usr/bin/env python3
""" Barron finishes cooking while Olivia cleans """

import threading
import time


def garbage_collector():
    while True:
        print('daemon_thread collected the garbage.')
        time.sleep(1)


if __name__ == '__main__':
    daemon_thread = threading.Thread(target=garbage_collector)

    # Making a thread to be a daemon thread and starting it
    daemon_thread.daemon = True
    daemon_thread.start()

    print('Main_Thread is running...')
    time.sleep(0.6)

    print('Main_Thread is running...')
    time.sleep(0.6)

    print('Main_Thread is running...')
    time.sleep(0.6)

    print('Main_Thread is Done!!')
