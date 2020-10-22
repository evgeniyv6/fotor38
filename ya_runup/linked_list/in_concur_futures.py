#!/usr/bin/env python

import time
import random
from concurrent import futures

from mystack import Stack
from myqueue import Queue

def stack_task(*args):
    time.sleep(random.random())
    st = Stack()
    for e in args:
        st.push(e)
    st.pop()
    return st

def queue_task(*args):
    q = Queue()
    for e in args:
        q.enqueue(e)
    q.dequeue()
    return q

def main():
    ex = futures.ProcessPoolExecutor(max_workers = 2)
    print('main: starting')

    wait_for = [ex.submit(stack_task, 1,2, 3,), ex.submit(queue_task, 1, 2, 3,)]

    for f in futures.as_completed(wait_for):
        print(f'main result is: {f.result()}')

if __name__ == '__main__':
    main()