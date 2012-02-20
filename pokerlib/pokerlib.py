#!/usr/bin/env python

from itertools import *
from constants import *

class FiveEval:
    def __init__(self) :
        self.ranks = [int(rank) for rank in open("ranks_5.dat", "r")]
        self.flushes = [int(flush) for flush in open("flushes_5.dat", "r")]

                
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


class SevenEval:
    def __init__(self):
        self.ranks = [int(rank) for rank in open("ranks_7.dat", "r")]
        self.flushes = [int(flush) for flush in open("flushes_7.dat", "r")]
        self.flushcheck = [int(flushcheck) for flushcheck in open("flushcheck_7.dat", "r")]
        self.deck_keys = [(rank_keys7[n >> 2] << flush_bit_shift) + suit_keys7[n & 3] for n in range(52)]

    def getRankOfSeven(self, c1, c2, c3, c4, c5, c6, c7):
        # Create a 7-card hand key by adding up each of the card keys.
        key = self.deck_keys[c1] + \
            self.deck_keys[c2] + \
            self.deck_keys[c3] + \
            self.deck_keys[c4] + \
            self.deck_keys[c5] + \
            self.deck_keys[c6] + \
            self.deck_keys[c7]

        # Tear off the flush check strip.
        flush_suit = self.flushcheck[key & flush_bit_mask]
                
        if flush_suit < 0:
            # Tear off the non-flush key strip, and look up the rank.
            return self.ranks[key >> flush_bit_shift]
        else :
            # Generate a flush key, and look up the rank.
            key = (flush_keys[c1 >> 2] if suit_keys7[c1 & 3] == flush_suit else 0) + \
                (flush_keys[c2 >> 2] if suit_keys7[c2 & 3] == flush_suit else 0) + \
                (flush_keys[c3 >> 2] if suit_keys7[c3 & 3] == flush_suit else 0) + \
                (flush_keys[c4 >> 2] if suit_keys7[c4 & 3] == flush_suit else 0) + \
                (flush_keys[c5 >> 2] if suit_keys7[c5 & 3] == flush_suit else 0) + \
                (flush_keys[c6 >> 2] if suit_keys7[c6 & 3] == flush_suit else 0) + \
                (flush_keys[c7 >> 2] if suit_keys7[c7 & 3] == flush_suit else 0)
                
            return self.flushes[key]


def testFiveEval():
    deck = [i for i in range(52)]
    five_eval = FiveEval()
    counts = [0] * 7462

    for hand in combinations(deck, 5):
        rank = five_eval.getRankOfFive(hand[0], hand[1], hand[2], hand[3], hand[4])
        counts[rank - 1] += 1

    print(counts)

def testSevenEval():
    seven_eval = SevenEval()
    deck = [i for i in range(52)]
    """
    counts = [0] * 7462
    for c in combinations(deck, 7):
        rank = seven_eval.getRankOfSeven(c[0], c[1], c[2], c[3], c[4], c[5], c[6])
        counts[rank - 1] += 1

    print(counts)
    """
    face_deck = [rank + suit for rank in card_ranks for suit in card_suits]
    
    d = dict([(c, face_deck.index(c)) for c in face_deck])
    print(seven_eval.getRankOfSeven(d['As'], d['Kc'], d['Qs'], d['Js'], d['Ts'], d['2c'], d['2d']))
    print(seven_eval.getRankOfSeven(d['As'], d['Ks'], d['Qs'], d['Js'], d['Ts'], d['2s'], d['2h']))
    print(seven_eval.getRankOfSeven(d['As'], d['Ks'], d['Qs'], d['Js'], d['Ts'], d['3s'], d['2s']))

    
if __name__ == "__main__":
    testSevenEval()
