#!/usr/bin/env python

import sys
import os

import Constants
from combinations import *

card_ranks = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
card_suits = ['s', 'h', 'd', 'c']
face_deck = [rank + suit for rank in card_ranks for suit in card_suits]
rank_keys = [79415, 43258, 19998, 12522, 5624, 2422, 992, 312, 94, 22, 5, 1, 0]
flush_keys = [4016, 2016, 1012, 508, 255, 128, 64, 32, 16, 8, 4, 2, 1]

class FiveEval:
    def __init__(self) :
                
        self.ranks = [0] * (Constants.MAX_FIVE_NONFLUSH_KEY_INT + 1)
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
        if (c1 & 3 == c2 & 3 == c3 & 3 == c4 & 3 == c5 & 3) :
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

    def getRank(self, cards):                
        c = [face_deck.index(i) for i in cards]
        return self.getRankOfFive(c[0], c[1], c[2], c[3], c[4])
                
    def getRankOfSeven(self, c1, c2, c3, c4, c5, c6, c7) :
        seven_cards = [c1, c2, c3, c4, c5, c6, c7]
        five_temp = [0] * 5
        BEST_RANK_SO_FAR = 0
        CURRENT_RANK = 0
        m = 0
                
        for i in range(1, 7) :
            for j in range(0, i) :
                m = 0
                for k in range(0, 7) :
                    if k != i and k != j :
                        five_temp[m] = seven_cards[k]
                        m += 1
                        
                        CURRENT_RANK = self.getRankOfFive(five_temp[0], five_temp[1], five_temp[2], five_temp[3], five_temp[4])
                        if BEST_RANK_SO_FAR < CURRENT_RANK :
                            BEST_RANK_SO_FAR = CURRENT_RANK
				
        return BEST_RANK_SO_FAR

if __name__ == "__main__":

    deck = [i for i in range(52)]
    five_eval = FiveEval()

    counts = [0] * 7462
    
    for hand in combinations(deck, 5):
        rank = five_eval.getRankOfFive(hand[0], hand[1], hand[2], hand[3], hand[4])
        counts[rank - 1] += 1

    print(counts)


