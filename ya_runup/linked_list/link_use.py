#!/usr/bin/env python

from link_node import Node
from print_link import print_link


def merge_two_linked_lists(l1: Node, l2: Node) -> Node:
    res = Node()
    cur = res
    while l1 and l2:
        if l1.item < l2.item:
            cur.next = l1
            l1 = l1.next
        else:
            cur.next = l2
            l2 = l2.next
        cur = cur.next
    if not l1: cur.next = l2
    if not l2: cur.next = l1
    return print_link.printer(res.next)

def delete_duplicates(l: Node):
    cur = l
    prev = None
    s = set()
    while cur:
        if cur.item in s:
            prev.next = cur.next
            cur = cur.next
        else:
            s.add(cur.item)
            prev = cur
            cur = cur.next
    return print_link.printer(l)

if __name__ == '__main__':
    print(merge_two_linked_lists(Node(3, Node(4, Node(5))), Node(4, Node(10, Node(15)))))
    print(delete_duplicates(Node(1, Node(1, Node(2, Node(2, Node(3)))))))

