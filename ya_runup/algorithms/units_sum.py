#!/usr/bin/env python

def units_sum(l: list) -> int:
    units = max_val = 0
    for el in l:
        if el == 1:
            units +=1
            max_val = max(units, max_val)
        else:
            units = 0
    return max_val

if __name__ == '__main__':
    print(units_sum([1,1,1,0,1,1]))
