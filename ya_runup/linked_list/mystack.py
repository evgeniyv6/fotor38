#!/usr/bin/env python

from link_node import Node

# LIFO
class Stack:
    def __init__(self):
        self.first = None
        self.name = 'Stack'
        self.n = 0

    def is_empty(self):
        return self.first is None

    def push(self, item):
        self.first = Node(item, self.first)
        self.n += 1

    def pop(self):
        old = self.first.item
        self.first = self.first.next
        self.n -= 1
        return old

    def __len__(self):
        return self.n

    def _to_iter(self, a):
        cur = self.first
        while cur:
            a += [cur.item]
            cur = cur.next
        return a

    def __iter__(self):
        a = []
        self._to_iter(a)
        return iter(a)

    def __repr__(self):
        a = []
        self._to_iter(a)
        return f'{self.name} is {str(a)}'

if __name__ == '__main__':
    st = Stack()
    for i in (1,2,3): st.push(i)
    st.pop()
    print('simple print: ', end ='')
    print(st)
    print('iter print: ', end = '')
    for e in st: print(e, end = ' ')
