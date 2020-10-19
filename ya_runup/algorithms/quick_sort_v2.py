#!/usr/bin/env python

import random

def swap(l: list, i: int, j: int):
    l[i], l[j] = l[j], l[i]

def quick_sort(l: list, begin: int, end: int) -> list:
    '''
    :param l: collection of elements
    :param begin: begin index
    :param end: last index
    :return: sorted collection
    '''
    if begin > end: return
    i, j, pivot = begin, end, l[random.randint(begin, end)]
    while i <= j:
        while l[i] < pivot: i += 1
        while l[j] > pivot: j -= 1
        if i <= j:
            swap(l, i, j)
            i += 1
            j -= 1
    quick_sort(l,begin,j); quick_sort(l,i,end)

if __name__ == '__main__':
    ldigits = [9,6,57,8,5,4,3,4,5,6,7]
    quick_sort(ldigits, 0, len(ldigits)-1)
    print(ldigits)

    lwords = ['hello', 'foo', 'bar']
    quick_sort(lwords, 0, len(lwords)-1)
    print(lwords)


