#!/usr/bin/env python

from collections import defaultdict

def concat_and_sort_lists(l1: list, l2: list) -> list:
    dd = defaultdict(int)
    res = []
    for l in (l1,l2):
        for el in l: dd[el] +=1
    for k, v in sorted(dd.items()):
        for _ in range(v): res.append(k)
    return res

if __name__ == '__main__':
    print(concat_and_sort_lists(['foo', 'bar'], ['bar', 'foo']))