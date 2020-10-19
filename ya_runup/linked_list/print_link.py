#!/usr/bin/env python

from link_node import Node

class print_link:
    def __init__(self, l: Node, res: list = None):
        self.l = l
        if res is None: self.res = []
        else:
            self.res = res

    @classmethod
    def printer(cls, l: Node, res = None):
        if res is None: res = []
        cur = l
        while cur:
            res.append(cur.item)
            cur = cur.next
        return cls(l, res)

    def __repr__(self):
        return f'Linked is {self.res}'


if __name__ == '__main__':
    link_list = Node(1, Node(2, Node(3,)))
    print(print_link.printer(link_list))