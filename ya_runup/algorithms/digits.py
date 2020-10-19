#!/usr/bin/env python

def get_digits_sum(num: int) -> int:
    '''
    :param num:
    :return:
    '''
    sum = 0
    while num:
        d, m = divmod(num, 10)
        sum += m
        num = d
    return sum

def revers_digit(num: int) -> int:
    rev = 0
    while num:
        d, m =divmod(num, 10)
        rev = rev * 10 + m
        num = d
    return rev

if __name__ == '__main__':
    print(get_digits_sum(1553))
    print(revers_digit(1553))