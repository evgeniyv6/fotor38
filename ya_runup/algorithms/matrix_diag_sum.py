#!/usr/bin/env python

'''
1 2 3
4 5 6
7 8 9
'''

def matrix_sum_diag(l: list) -> int:
    '''
    :param l: list of lists
    :return: sum of main and opposite diagonals
    '''
    n = len(l)
    sum = 0
    for i in range(n):
        sum += l[i][i] + l[i][n-i-1]
    if n % 2 == 1:
        sum -= l[n // 2][n // 2]
    return sum

if __name__ == '__main__':
    print(matrix_sum_diag([[1,2,3],[4,5,6], [7,8,9]]))