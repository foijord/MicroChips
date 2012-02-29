#!/usr/bin/env python

from itertools import *

def checkSuitKeys(keys):
    sums = [sum(c) for c in combinations_with_replacement(keys, 6)]
    return len(sums) == len(set(sums))

def checkRankKeys(keys):
    sums = [sum(c) for c in combinations_with_replacement(keys, 5) if max([c.count(i) for i in c]) < 5]
    return len(sums) == len(set(sums))

def generateKeys(n, keycheck):
    keys = [0]
    while len(keys) < n:
        keys.append(keys[-1])
        while True:
            keys[-1] += 1
            if keycheck(keys):
                print(keys)
                break


if __name__ == "__main__":
    generateKeys(4, checkSuitKeys)
 