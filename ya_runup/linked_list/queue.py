#!/usr/bin/env python

from link_node import Node
from stack import Stack

# FIFO
class Queue(Stack):
    def __init__(self):
        super().__init__()
        self.name = 'Queue'
        self.last = None

    def dequeue(self):
        old = self.first.item
        self.first = self.first.next
        if self.is_empty(): self.last = None
        self.n -= 1
        return old

    def enqueue(self, item):
        prev_last = self.last
        self.last = Node(item)
        if self.is_empty():
            self.first = self.last
        else:
            prev_last.next = self.last
        self.n += 1

if __name__ == '__main__':
    q = Queue()
    for i in (1,2,3): q.enqueue(i)
    q.dequeue()
    print('simple print: ', end='')
    print(q)
    print('iter queue: ', end = '')
    for e in q: print(e, end = ' ')