#!/usr/bin/env python

def binary_search(elements: list, target) -> bool:
    '''
    :param elements: collection of elements
    :param target: element to find
    :return: True or Falses
    '''
    begin, end = 0, len(elements) - 1
    while begin <= end:
        med = (begin + end) // 2
        if target < elements[med]: end = med - 1
        elif target > elements[med]: begin = med + 1
        else: return True
    return False

if __name__ == '__main__':
    print(binary_search([1, 2, 3], 2))
    print(binary_search([1, 2, 3], 1))
    print(binary_search([1, 2, 3], 3))
    print(binary_search([1, 2, 3], 4))