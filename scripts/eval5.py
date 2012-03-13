#!/usr/bin/env python

from itertools import *
from constants import *

class FiveEval:
    def __init__(self) :
        self.ranks = [int(rank) for rank in open("../data/ranks_5.dat", "r")]
        self.flushes = [int(flush) for flush in open("../data/flushes_5.dat", "r")]

                
    def getRankOfFive(self, c1, c2, c3, c4, c5) :
        if (c1 & 3 == c2 & 3 == c3 & 3 == c4 & 3 == c5 & 3):
            return self.flushes[flush_keys[c1 >> 2] +
                                flush_keys[c2 >> 2] +
                                flush_keys[c3 >> 2] +
                                flush_keys[c4 >> 2] +
                                flush_keys[c5 >> 2]]
                
        else:
            return self.ranks[rank_keys5[c1 >> 2] +
                              rank_keys5[c2 >> 2] +
                              rank_keys5[c3 >> 2] +
                              rank_keys5[c4 >> 2] +
                              rank_keys5[c5 >> 2]]

    def getRank(self, hand):
        best_rank = 0
        for five in combinations(hand, 5):
            rank = self.getRankOfFive(five[0], five[1], five[2], five[3], five[4])
            if rank > best_rank:
                best_rank = rank

        return best_rank
