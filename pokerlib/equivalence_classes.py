#!/usr/bin/env python

import sys
from combinations import *

ranks = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']

equivalence_class = 7462
highcards = []
straights = []

def key(hand):
    return ''.join(sorted(list(hand), key = ranks.index))

def init_straights():
    r = list(ranks) + ['A']
    for i in range(10):
        straights.append(key(''.join(r[i:i+5])))

def init_highcards():
    r = list(ranks)
    for i in range(13):
        r.remove(ranks[i])
        for c in combinations(r, 4):
            hand = key(ranks[i] + ''.join(list(c)))
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
            r = list(ranks)
            r.remove(ranks[i])
            print_class(ranks[i] * m + r[j] * n, name)

def print_high_cards(flush):
    name = "Flush" if flush else "High Card"
    for h in highcards:
        print_class(h, name)

def print_trips():
    for i in range(13):
        r = list(ranks)
        r.remove(ranks[i])
        for c in combinations(r, 2):
            print_class(ranks[i] * 3 + ''.join(list(c)), "Three of a Kind")

def print_two_pair():
    for i in range(13):
        for j in range(i+1, 13):
            r = list(ranks)
            r.remove(ranks[i])
            r.remove(ranks[j])
            for k in r:
                print_class(ranks[i] * 2 + ranks[j] * 2 + k, "Two Pair")

def print_pairs():
    for i in range(13):
        r = list(ranks)
        r.remove(ranks[i])
        for c in combinations(r, 3):
            print_class(ranks[i] * 2 + ''.join(list(c)), "Pair")

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
