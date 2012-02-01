#!/usr/bin/env python3

import sys
import itertools

ranks = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']

equivalence_class = 1

def print_straight_flushes():
    global equivalence_class
    r = list(ranks) # copy
    r += ['A'] # wrap
    for i in range(10):
        print(equivalence_class, r[i:i+5])
        equivalence_class += 1

def print_quads():
    global equivalence_class

    for i in range(13):
        for j in range(12):
            r = list(ranks) # copy
            r.remove(ranks[i])
            print(equivalence_class, list(ranks[i] * 4) + list(r[j] * 1))
            equivalence_class += 1

def print_full_houses():
    global equivalence_class

    for i in range(13):
        for j in range(12):
            r = list(ranks) # copy
            r.remove(ranks[i])
            print(equivalence_class, list(ranks[i] * 3) + list(r[j] * 2))
            equivalence_class += 1

# remove the 10 straight-flushes!
def print_flushes():
    global equivalence_class
    r = list(ranks) # copy
    for i in range(13):
        r.remove(ranks[i])
        for c in itertools.combinations(r, 4):
            print(equivalence_class, list(ranks[i]) + list(c))
            equivalence_class += 1

def main():
    print_straight_flushes()
    print_quads()
    print_full_houses()
    print_flushes()

if __name__ == "__main__":
    main()
