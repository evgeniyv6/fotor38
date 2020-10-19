#!/usr/bin/env python

import threading
import logging
import time

from binary_search import binary_search
from quick_sort_v1 import quick_sort as qs_v1
from buble_sort import buble_sort
from matrix_diag_sum import matrix_sum_diag
from digits import get_digits_sum, revers_digit
from one_diff_in_two_strings import is_one_diff_in_two_strings


logging.basicConfig(
    level = logging.DEBUG,
    format = '[%(levelname)s] (%(threadName)-41s) (%(message)s)'
)

def output(f, * args):
    logging.debug(f(*args))

if __name__ == '__main__':
    bin_search_worker = threading.Thread(name='binary search -> chk 2 in [1, 2, 3]', target = output, args=(binary_search, [1, 2, 3], 2,))
    bin_search_worker.start()

    quick_sort_worker = threading.Thread(target=output, args=(qs_v1, [9,7,8,9,9,7,6,5,4,3,2,4,5]))
    quick_sort_worker.setName('quick sort -> [9,7,8,9,9,7,6,5,4,3,2,4,5]')
    quick_sort_worker.start()

    buble_sort_worker = threading.Thread(name = 'buble sort -> [\'hi\', \'foo\', \'bar\']', target=output, args=(buble_sort, ['hi', 'foo', 'bar']))
    buble_sort_worker.start()

    matrix_sum_diag_worker = threading.Thread(name = 'matrix diagonals sum -> [[1,2],[4,5]]', target = output, args=(matrix_sum_diag, [[1,2],[4,5]],))
    matrix_sum_diag_worker.start()

    revers_digit_worker = threading.Thread(name = 'revers digit -> 123456789', target=output, args = (revers_digit, 123456789,))
    revers_digit_worker.start()

    is_one_diff_in_two_strings_worker = threading.Thread(name = 'two strings diff -> \'nine\', \'nin\'', target=output, args = (is_one_diff_in_two_strings, 'nine', 'nin',))
    is_one_diff_in_two_strings_worker.start()