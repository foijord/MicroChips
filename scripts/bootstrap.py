#!/usr/bin/env python

from constants import *

equivalence_class = 7462

def print_straights():
    r = list(rank_keys5) + [rank_keys5[0]]
    print([sum(r[i:i+5]) for i in range(10)])

if __name__ == "__main__":
    print_straights()
