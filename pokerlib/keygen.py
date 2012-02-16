#!/usr/bin/env python

import sys
from itertools import *

def checkSuitKeys(keys):
    sums = []
    for c in combinations_with_replacement(keys, 7):
        sums.append(sum(c))

    for s in sums:
        if sums.count(s) > 1:
            return False

    return True

def checkRankKeys(keys):
    sums = []
    for c in combinations_with_replacement(keys, 5):
        count = [c.count(i) for i in c]
        if max(count) < 5:
            sums.append(sum(c))

    for s in sums:
        if sums.count(s) > 1:
            return False

    return True

def generateRankKeys():
    keys = [0] * 2
    while len(keys) <= 13:
        accepted = False
        while not accepted:
            keys[-1] += 1
            accepted = checkRankKeys(keys)
            if accepted:
                print(keys)
                keys.append(keys[-1])


def generateSuitKeys():
    keys = [0] * 2
    while len(keys) <= 4:
        accepted = False
        while not accepted:
            keys[-1] += 1
            accepted = checkSuitKeys(keys)
            if accepted:
                print(keys)
                keys.append(keys[-1])

if __name__ == "__main__":
    generateSuitKeys()
