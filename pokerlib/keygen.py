#!/usr/bin/env python

import sys
from itertools import *

def checkSuitKeys(keys):
    sums = [sum(c) for c in combinations_with_replacement(keys, 7)]
    return len(sums) == len(set(sums))

def checkRankKeys(keys):
    sums = [sum(c) for c in combinations_with_replacement(keys, 7) if max([c.count(i) for i in c]) < 5]
    return len(sums) == len(set(sums))

def generateKeys(n, keycheck):
    keys = [0] * 2
    while len(keys) <= n:
        while True:
            keys[-1] += 1
            if keycheck(keys):
                print(keys)
                keys.append(keys[-1])
                break

if __name__ == "__main__":
    generateKeys(8, checkRankKeys)
