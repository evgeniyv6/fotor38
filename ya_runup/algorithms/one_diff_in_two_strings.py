#!/usr/bin/env python

def is_one_diff_in_two_strings(s1: str, s2: str) -> bool:
    l1 = len(s1); l2 = len(s2)
    if abs(l1-l2) > 1: return False
    i = j = count = 0
    while i < l1 and j < l2:
        if s1[i] != s2[j]:
            if count == 1: return False
            if l1 > l2: i += 1
            elif l1 < l2: j += 1
            else:
                i+=1
                j+=1
            count += 1
        else:
            i+=1
            j+=1
    if i < l1 or j < l2: count += 1
    return count == 1

if __name__ == '__main__':
    print(is_one_diff_in_two_strings('nine', 'nin'))