#!/usr/bin/env python

from itertools import *
from constants import *
from pokerlib import *

def generate_5_card_ranks():
    ranks = [0] * (max_5_card_rank_key + 1)
    flushes = [0] * (max_5_card_flush_key + 1)

    for line in open("equivalence_classes.dat", 'r'):
        columns = line.split('\t')
        
        if "Flush" in columns[2]:
            key = sum([flush_keys[c] for c in [card_ranks.index(c) for c in columns[0]]])
            flushes[key] = int(columns[1])
        else:
            key = sum([rank_keys5[c] for c in [card_ranks.index(c) for c in columns[0]]])
            ranks[key] = int(columns[1])

    open("ranks_5.dat", "w+").writelines(["%i\n" % i for i in ranks])
    open("flushes_5.dat", "w+").writelines(["%i\n" % i for i in flushes])

def generate_7_card_ranks():
    ranks = [0] * (max_7_card_rank_key + 1)
    flushes = [0] * (max_7_card_flush_key + 1)
    flushcheck = [-1] * (7 * max(suit_keys7) + 1)
        
    five_eval = FiveEval()
    spades = [i * 4 for i in range(13)]

    # All combinations, except flushes
    for c in combinations_with_replacement(spades, 7):
        card_count = [c.count(i) for i in c]
        if (max(card_count) < 5):
            key = sum([rank_keys7[i >> 2] for i in c])
            ranks[key] = five_eval.getRank([c[0], c[1], c[2], c[3], c[4] + 1, c[5] + 1, c[6] + 1])

    # All flushes
    for n in [5, 6, 7]:
        for c in combinations(spades, n):
            key = sum([flush_keys[i >> 2] for i in c])
            flushes[key] = five_eval.getRank(c)

    # Flush checks
    for c in combinations_with_replacement(suit_keys7, 7):
        suit_count = [c.count(i) for i in suit_keys7]
        max_count = max(suit_count)
        if max_count >= 5:
            suit_index = suit_count.index(max_count) 
            flushcheck[sum(c)] = suit_keys7[suit_index]

    open("ranks_7.dat", "w+").writelines(["%i\n" % i for i in ranks])
    open("flushes_7.dat", "w+").writelines(["%i\n" % i for i in flushes])
    open("flushcheck_7.dat", "w+").writelines(["%i\n" % i for i in flushcheck])


if __name__ == "__main__":
    generate_5_card_ranks()
    generate_7_card_ranks()
