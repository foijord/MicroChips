#!/usr/bin/env python

import sys
from constants import *
from itertools import *

current_rank = 7462
ranks = [0] * (max_5_card_rank_key + 1)
flushes = [0] * (max_5_card_flush_key + 1)

def straight():
    r = list(range(13)) + [0]
    return [sorted(r[i:i+5]) for i in range(10)]

def four_of_a_kind():
    return [[i] * 4 + [j] for i in range(13) for j in range(13) if i != j]

def full_house():
    return [[i] * 3 + [j] * 2 for i in range(13) for j in range(13) if i != j]

def three_of_a_kind():
    return [[i] * 3 + list(c) for i in range(13) for c in combinations(list(range(13)), 2) if i not in c]

def two_pair():
    return [[i] * 2 + [j] * 2 + [k] for i in range(13) for j in range(i+1, 13) for k in range(13) if (i != j and i != k and j != k)]

def one_pair():
    return [[i] * 2 + list(c) for i in range(13) for c in combinations(list(range(13)), 3) if i not in c]

def high_card():
    return [list(c) for c in combinations(list(range(13)), 5) if list(c) not in straight()]

def save_ranks(hands, is_flush):
    global current_rank
    for hand in hands:
        if sys.flags.debug:
            print(''.join([card_ranks[i] for i in hand]), current_rank)
        if is_flush:
            key = sum([flush_keys[i] for i in hand])
            flushes[key] = current_rank
        else:
            key = sum([rank_keys5[i] for i in hand])
            ranks[key] = current_rank

        current_rank -= 1

if __name__ == "__main__":

    save_ranks(straight(), True)
    save_ranks(four_of_a_kind(), False)
    save_ranks(full_house(), False)
    save_ranks(high_card(), True)
    save_ranks(straight(), False)
    save_ranks(three_of_a_kind(), False)
    save_ranks(two_pair(), False)
    save_ranks(one_pair(), False)
    save_ranks(high_card(), False)

    if not sys.flags.debug:
        open("ranks.dat", "w+").writelines(["%i\n" % i for i in ranks])
        open("flushes.dat", "w+").writelines(["%i\n" % i for i in flushes])
