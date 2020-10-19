#!/usr/bin/env python

import random

def quick_sort(l: list) -> list: # slow ver
    '''
    :param l: collection of elements
    :return: sorted collection
    '''
    if len(l) <=1: return l
    else:
        pivot = random.choice(l)
        return quick_sort([el for el in l if el < pivot]) + [pivot]* l.count(pivot) + quick_sort([el for el in l if el > pivot])

if __name__ == '__main__':
    ldigits = [9,6,57,8,5,4,3,4,5,6,7]
    print(quick_sort(ldigits))
    lwords = ['hello', 'foo', 'bar']
    print(quick_sort(lwords))

