#!/usr/bin/env python

from itertools import *

card_ranks = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
card_suits = ['s', 'h', 'c', 'd']

# keys below obtained by running generateAllKeys() (takes hours so hard-coded here)
rank_keys5 = [79415, 43258, 19998, 12522, 5624, 2422, 992, 312, 94, 22, 5, 1, 0]
rank_keys6 = [436437, 206930, 90838, 37951, 14270, 5760, 1734, 422, 98, 22, 5, 1, 0]
rank_keys7 = [1479181, 636345, 262349, 83661, 22854, 8698, 2031, 453, 98, 22, 5, 1, 0]
suit_keys6 = [43, 7, 1, 0]
suit_keys7 = [57, 8, 1, 0]

flush_keys = [4096, 2048, 1024, 512, 256, 128, 64, 32, 16, 8, 4, 2, 1]

max_5_card_rank_key = 4 * 79415 + 3 * 43258
max_6_card_rank_key = 4 * 436437 + 3 * 206930
max_7_card_rank_key = 4 * 1479181 + 3 * 636345

max_5_card_flush_key = 4096 + 2048 + 1024 + 512 + 256
max_6_card_flush_key = 4096 + 2048 + 1024 + 512 + 256 + 128
max_7_card_flush_key = 4096 + 2048 + 1024 + 512 + 256 + 128 + 64

flush_bit_shift = 9
flush_bit_mask = 511

def uniqueSums(keys, k, r):
    """ 
    return true if all sums of keys with length k with at most r
    repetitions is unique among all such sums
    """
    sums = [sum(c) for c in combinations_with_replacement(keys, k) if max([c.count(i) for i in c]) <= r]
    return len(sums) == len(set(sums))

def generateKeys(n, k, r):
    """
    generates a list of n integers with the property that the sum of k
    integers with at most r repetitions is unique among all such sums
    """
    keys = [0]
    while len(keys) < n:
        keys.append(keys[-1] + 1)
        while not uniqueSums(keys, k, r): keys[-1] += 1
    return keys

def generateAllKeys():
    print("suit keys for 5-card hands:", generateKeys(4, 5, 13))
    print("suit keys for 6-card hands:", generateKeys(4, 6, 13))
    print("suit keys for 7-card hands:", generateKeys(4, 7, 13))
    print("rank keys for 5-card hands", generateKeys(13, 5, 4))
    print("rank keys for 6-card hands", generateKeys(13, 6, 4))
    print("rank keys for 7-card hands", generateKeys(13, 7, 4))

class FiveEval:
    """
    Generate all 7462 unique 5-card poker hands, ordered from highest
    value (royal flush) to lowest value (7-high), and assign them a
    rank from 7462 to 1. The non-flush hands are stored in the rank
    list, with an index computed by summing the card keys obtained
    from the keygen script. The flush hands are stored in the flushes
    array, with an index obtained by summing the corresponding flush
    keys.
    """
    def __init__(self):
        self.current_rank = 7462
        self.ranks = [0] * (max_5_card_rank_key + 1)
        self.flushes = [0] * (max_5_card_flush_key + 1)

        r = list(range(13)) + [0]
        straight        = [sorted(r[i:i+5]) for i in range(10)]
        four_of_a_kind  = [[i] * 4 + [j] for i in range(13) for j in range(13) if i != j]
        full_house      = [[i] * 3 + [j] * 2 for i in range(13) for j in range(13) if i != j]
        three_of_a_kind = [[i] * 3 + list(c) for i in range(13) for c in combinations(list(range(13)), 2) if i not in c]
        two_pair        = [[i] * 2 + [j] * 2 + [k] for i in range(13) for j in range(i+1, 13) for k in range(13) if (i != j and i != k and j != k)]
        one_pair        = [[i] * 2 + list(c) for i in range(13) for c in combinations(list(range(13)), 3) if i not in c]
        high_card       = [list(c) for c in combinations(list(range(13)), 5) if list(c) not in straight]

        self.assign_ranks(straight, True)
        self.assign_ranks(four_of_a_kind)
        self.assign_ranks(full_house)
        self.assign_ranks(high_card, True)
        self.assign_ranks(straight)
        self.assign_ranks(three_of_a_kind)
        self.assign_ranks(two_pair)
        self.assign_ranks(one_pair)
        self.assign_ranks(high_card)

        open("data/ranks_5.dat", "w+").writelines(["%i\n" % i for i in self.ranks])
        open("data/flushes_5.dat", "w+").writelines(["%i\n" % i for i in self.flushes])

    def assign_ranks(self, hands, is_flush = False):
        keys = flush_keys if is_flush else rank_keys5
        table = self.flushes if is_flush else self.ranks
        for hand in hands:
            # print(''.join([card_ranks[i] for i in hand]), self.current_rank) # debug
            index = sum([keys[i] for i in hand])
            table[index] = self.current_rank
            self.current_rank -= 1

    def getRankOfFive(self, c):
        is_flush = (c[0] & 3 == c[1] & 3 == c[2] & 3 == c[3] & 3 == c[4] & 3)
        keys = flush_keys if is_flush else rank_keys5
        index = sum(keys[i >> 2] for i in c)
        return self.flushes[index] if is_flush else self.ranks[index]

    def getRank(self, hand):
        return max([self.getRankOfFive(five) for five in combinations(hand, 5)])

class SevenEval:
    def __init__(self, five_eval):
        self.ranks = [0] * (max_7_card_rank_key + 1)
        self.flushes = [0] * (max_7_card_flush_key + 1)
        self.flushcheck = [-1] * (7 * max(suit_keys7) + 1)

        self.five_eval = five_eval
        self.spades = [i * 4 + 0 for i in range(13)]
        self.hearts = [i * 4 + 1 for i in range(13)]

        self.rank_all_non_flush_hands()
        self.rank_all_flush_hands()
        self.init_flush_check()

        self.deck = [(rank_keys7[i >> 2] << flush_bit_shift) + suit_keys7[i & 3] for i in range(52)]

        open("data/ranks_7.dat", "w+").writelines(["%i\n" % i for i in self.ranks])
        open("data/flushes_7.dat", "w+").writelines(["%i\n" % i for i in self.flushes])
        open("data/flushcheck_7.dat", "w+").writelines(["%i\n" % i for i in self.flushcheck])

    def rank_all_non_flush_hands(self):
        for c in combinations_with_replacement(list(range(13)), 7):
            if (max([c.count(i) for i in c]) < 5):
                key = sum([rank_keys7[i] for i in c])
                non_flush = [self.spades[c[0]], self.spades[c[1]], self.spades[c[2]], self.spades[c[3]], self.hearts[c[4]], self.hearts[c[5]], self.hearts[c[6]]]
                self.ranks[key] = five_eval.getRank(non_flush)

    def rank_all_flush_hands(self):
        for n in [5, 6, 7]:
            for c in combinations(self.spades, n):
                key = sum([flush_keys[i >> 2] for i in c])
                self.flushes[key] = self.five_eval.getRank(c)

    def init_flush_check(self):
        for c in combinations_with_replacement(suit_keys7, 7):
            suit_count = [c.count(i) for i in suit_keys7]
            max_count = max(suit_count)
            if max_count >= 5:
                suit_index = suit_count.index(max_count) 
                self.flushcheck[sum(c)] = suit_keys7[suit_index]

    def getRank(self, hand):
        key = sum([self.deck[card] for card in hand])
        flush_suit = self.flushcheck[key & flush_bit_mask]

        if (flush_suit < 0):
            return self.ranks[key >> flush_bit_shift]

        keys = [flush_keys[i >> 2] for i in c if suit_keys7[i & 3] == flush_suit]
        return self.flushes[sum(keys)]

if __name__ == "__main__":
    five_eval = FiveEval()
    seven_eval = SevenEval(five_eval)

    ranks = []
    deck = list(range(52))
    for c in combinations(deck, 5):
        ranks.append(five_eval.getRankOfFive(c))
        
    ranks = set(ranks)
    if len(ranks) != 7462: print("five card evaluator invalid")
