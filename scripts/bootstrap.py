#!/usr/bin/env python

import sys
from constants import *

equivalence_class = 7462

ranks = [i for i in range(13)]

def table_key(cards):
    return sum([rank_keys5[i] for i in cards])

def debug_key(cards):
    return ''.join([card_ranks[i] for i in cards])

key = debug_key if sys.flags.debug else table_key

def print_straights():
    r = list(ranks) + [0]
    print([key(r[i:i+5]) for i in range(10)])

def print_four_of_a_kind():
    print([key([i] * 4 + [j]) for i in ranks for j in ranks if i != j])

def print_full_house():
    print([key([i] * 3 + [j] * 2) for i in ranks for j in ranks if i != j])

def print_two_pair():
    print([key([i] * 2 + [j] * 2 + [k]) for i in ranks for j in ranks for k in ranks if (i != j and i != k and j != k)])

if __name__ == "__main__":
    print_four_of_a_kind()
    print_full_house()
    print_straights()
    print_two_pair()
