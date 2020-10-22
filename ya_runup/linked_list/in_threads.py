#!/usr/bin/env python

import logging
from threading import Thread
import time
import random

from mystack import Stack
from myqueue import Queue

logging.basicConfig(
    level = logging.DEBUG,
    format='[%(levelname)s] (%(threadName)-10s) (%(message)-60s)'
)

class customThread(Thread):
    def __init__(self, name = 'custom thread', target = None, args = (), kwargs = None, group = None, daemon = None):
        super().__init__(name = name, target = target, group = group, daemon = daemon)
        self.args = args
        self.kwargs = kwargs

    def run(self):
        if self._target not in ('queue', 'stack'):
            logging.debug('cannot thread')
        elif self._target == 'stack':
            time.sleep(random.random())
            st = Stack()
            for e in self.args: st.push(e)
            st.pop()
            logging.debug(f'LIFO. Put {self.args}, one - pop => Output: {st}')
        elif self._target == 'queue':
            time.sleep(random.random())
            q = Queue()
            for e in self.args: q.enqueue(e)
            q.dequeue()
            logging.debug(f'FIFO. Put {self.args}, one - delete => Output: {q}')


if __name__ == '__main__':
    stack_worker = customThread(target='stack', args=(1,2,3,))
    stack_worker.setName('stack worker')
    stack_worker.start()

    queue_worker = customThread(name='queue worker', target='queue',args = (1,2,3,),)
    queue_worker.start()

