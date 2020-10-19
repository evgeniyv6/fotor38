#!/usr/bin/env python

def find_needle(haystack, needle):
    for i in range(len(haystack) - len(needle) + 1):
        if haystack[i: i + len(needle)] == needle: return True
    return False

if __name__=='__main__':
    print(find_needle('hello', 'he'))