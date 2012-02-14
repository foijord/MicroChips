#!/usr/bin/env python

import sys
import os

import Constants
from itertools import *

card_ranks = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
card_suits = ['s', 'h', 'c', 'd']
rank_keys = [1479181, 636345, 262349, 83661, 22854, 8698, 2031, 453, 98, 22, 5, 1, 0]
flush_keys = [4016, 2016, 1012, 508, 255, 128, 64, 32, 16, 8, 4, 2, 1]
suit_keys = [57, 8, 1, 0]

class FiveEval:
    def __init__(self) :
                
        self.ranks = [0] * (Constants.MAX_SEVEN_NONFLUSH_KEY_INT + 1)
        self.flushes = [0] * (Constants.MAX_FIVE_FLUSH_KEY_INT + 1)
                
        equivalence_classes = open("equivalence_classes.dat", 'r')
        for line in equivalence_classes:
            columns = line.split('\t')

            if "Flush" in columns[2]:
                key = sum([flush_keys[c] for c in [card_ranks.index(c) for c in columns[0]]])
                self.flushes[key] = int(columns[1])
            else:
                key = sum([rank_keys[c] for c in [card_ranks.index(c) for c in columns[0]]])
                self.ranks[key] = int(columns[1])
                                
    def getRankOfFive(self, c1, c2, c3, c4, c5) :
        if (c1 & 3 == c2 & 3 == c3 & 3 == c4 & 3 == c5 & 3):
            return self.flushes[flush_keys[c1 >> 2] +
                                flush_keys[c2 >> 2] +
                                flush_keys[c3 >> 2] +
                                flush_keys[c4 >> 2] +
                                flush_keys[c5 >> 2]]
                
        else:
            return self.ranks[rank_keys[c1 >> 2] +
                              rank_keys[c2 >> 2] +
                              rank_keys[c3 >> 2] +
                              rank_keys[c4 >> 2] +
                              rank_keys[c5 >> 2]]

    def getRank(self, hand):
        best_rank = 0
        for five in combinations(hand, 5):
            rank = self.getRankOfFive(five[0], five[1], five[2], five[3], five[4])
            if rank > best_rank:
                best_rank = rank

        return best_rank


class SevenEval:
    def __init__(self):
        self.ranks = [0] * (Constants.MAX_SEVEN_NONFLUSH_KEY_INT + 1)
        self.flushes = [0] * (Constants.MAX_SEVEN_FLUSH_KEY_INT + 1)
        self.flushCheck = [-1] * (Constants.MAX_FLUSH_CHECK_SUM + 1)
        self.deck_keys = [(rank_keys[n >> 2] << Constants.NON_FLUSH_BIT_SHIFT) + suit_keys[n & 3] for n in range(52)]
        
        five_eval = FiveEval()

        # All combinations, except flushes
        for c in combinations_with_replacement([i for i in range(13)], 7):
            #peel off invalid hands
            card_count = [c.count(c[i]) for i in range(7)]
            if (max(card_count) < 5):
                key = sum([rank_keys[i] for i in c])
                self.ranks[key] = five_eval.getRank([c[0]*4, c[1]*4, c[2]*4, c[3]*4, c[4]*4+1, c[5]*4+1, c[6]*4+1])

        # Flush ranks.
        for n in [5, 6, 7]:
            for c in combinations([i for i in range(13)], n):
                key = sum([flush_keys[c[i]] for i in range(0, n)])
                self.flushes[key] = five_eval.getRank([i * 4 for i in c])
                                
     
        # 7-card flush.
        for c in combinations_with_replacement(suit_keys, 7):
            suit_count = [c.count(suit_keys[i]) for i in range(4)]
            max_count = max(suit_count)
            if max_count > 4:
                key = sum(c)
                suit_index = suit_count.index(max_count)
                self.flushCheck[key] = suit_keys[suit_index]

    def getRankOfSeven(self, c1, c2, c3, c4, c5, c6, c7):
        # Create a 7-card hand key by adding up each of the card keys.
        key = self.deck_keys[c1] + self.deck_keys[c2] + self.deck_keys[c3] + self.deck_keys[c4] + self.deck_keys[c5] + self.deck_keys[c6] + self.deck_keys[c7]

        # Tear off the flush check strip.
        flush_suit = self.flushCheck[key & Constants.SUIT_BIT_MASK]
                
        if flush_suit < 0:
            # Tear off the non-flush key strip, and look up the rank.
            return self.ranks[key >> Constants.NON_FLUSH_BIT_SHIFT] 
        else :
            # Generate a flush key, and look up the rank.
            key = (flush_keys[c1 >> 2] if suit_keys[c1 & 3] == flush_suit else 0) + \
                (flush_keys[c2 >> 2] if suit_keys[c2 & 3] == flush_suit else 0) + \
                (flush_keys[c3 >> 2] if suit_keys[c3 & 3] == flush_suit else 0) + \
                (flush_keys[c4 >> 2] if suit_keys[c4 & 3] == flush_suit else 0) + \
                (flush_keys[c5 >> 2] if suit_keys[c5 & 3] == flush_suit else 0) + \
                (flush_keys[c6 >> 2] if suit_keys[c6 & 3] == flush_suit else 0) + \
                (flush_keys[c7 >> 2] if suit_keys[c7 & 3] == flush_suit else 0)
                
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
