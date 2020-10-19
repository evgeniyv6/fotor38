#!/usr/bin/env python

def buble_sort(l: list):
    '''
    :param l: collection of elements
    :return: sorted collection
    '''
    n = len(l)
    counter = 1
    while counter < n:
        for i in range(n - counter):
            if l[i] > l[i+1]:
                l[i], l[i+1] = l[i+1], l[i]
        counter +=1
    return l

if __name__ == '__main__':
    print(buble_sort([9,8,7,5,6,7,8,9,6,4,3,2,4]))
    print(buble_sort(['hi', 'foo', 'bar']))