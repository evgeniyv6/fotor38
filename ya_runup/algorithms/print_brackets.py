#!/usr/bin/env python

def brackets(num = 3, open = 0, close = 0, bracket = ''):
    if open + close == 2 * num: print(bracket)
    else:
        if open < num: brackets(num, open+1, close, bracket + '{')
        if close < open: brackets(num, open, close+1, bracket + '}')

if __name__ == '__main__':
    brackets()