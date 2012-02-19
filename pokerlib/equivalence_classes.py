#!/usr/bin/env python

from itertools import *
from constants import *

equivalence_class = 7462
highcards = []
straights = []

def key(hand):
    return ''.join(sorted(list(hand), key = card_ranks.index))

def init_straights():
    r = list(card_ranks) + ['A']
    for i in range(10):
        straights.append(key(''.join(r[i:i+5])))

def init_highcards():
    for c in combinations(card_ranks, 5):
        hand = key(''.join(list(c)))
        if not hand in straights:
            highcards.append(hand)

def print_class(hand, name):
    global equivalence_class
    print(key(hand) + "\t" + str(equivalence_class) + "\t" + name)
    equivalence_class -= 1

def print_straights(flush):
    name = "Straight Flush" if flush else "Straight"
    for s in straights:
        print_class(s, name)

def print_filled_hands(m, n):
    name = "Four of a Kind" if m == 4 else "Full House"
    for i in range(13):
        for j in range(12):
            r = list(card_ranks)
            r.remove(card_ranks[i])
            print_class(card_ranks[i] * m + r[j] * n, name)

def print_high_cards(flush):
    name = "Flush" if flush else "High Card"
    for h in highcards:
        print_class(h, name)

def print_trips():
    for i in range(13):
        r = list(card_ranks)
        r.remove(card_ranks[i])
        for c in combinations(r, 2):
            print_class(card_ranks[i] * 3 + ''.join(list(c)), "Three of a Kind")

def print_two_pair():
    for i in range(13):
        for j in range(i+1, 13):
            r = list(card_ranks)
            r.remove(card_ranks[i])
            r.remove(card_ranks[j])
            for k in r:
                print_class(card_ranks[i] * 2 + card_ranks[j] * 2 + k, "Two Pair")

def print_pairs():
    for i in range(13):
        r = list(card_ranks)
        r.remove(card_ranks[i])
        for c in combinations(r, 3):
            print_class(card_ranks[i] * 2 + ''.join(list(c)), "Pair")

def main():
    init_straights()
    init_highcards()

    print_straights(True)
    print_filled_hands(4, 1)
    print_filled_hands(3, 2)
    print_high_cards(True)
    print_straights(False)
    print_trips()
    print_two_pair()
    print_pairs()
    print_high_cards(False)

if __name__ == "__main__":
    main()
