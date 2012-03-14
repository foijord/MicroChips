#!/usr/bin/env python

from itertools import combinations_with_replacement as cwr

def uniqueSums(keys, k, r):
    """ 
    return true if all sums of keys with length k with at most r
    repetitions is unique among all such sums
    """
    sums = [sum(c) for c in cwr(keys, k) if max([c.count(i) for i in c]) <= r]
    return len(sums) == len(set(sums))

def generateKeys(n, k, r):
    """
    generates a list of n integers with the property that the sum of k
    integers with at most r repetitions is unique among all such sums
    """
    keys = [0]
    while len(keys) < n:
        keys.append(keys[-1] + 1)
        while not uniqueSums(keys, k, r): keys[-1] += 1
    return keys

if __name__ == "__main__":
    print("suit keys for 5-card hands:", generateKeys(4, 5, 13))
    print("suit keys for 6-card hands:", generateKeys(4, 6, 13))
    print("suit keys for 7-card hands:", generateKeys(4, 7, 13))
    print("rank keys for 5-card hands", generateKeys(13, 5, 4))
    print("rank keys for 6-card hands", generateKeys(13, 6, 4))
    print("rank keys for 7-card hands", generateKeys(13, 7, 4))

 
