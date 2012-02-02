#!/usr/bin/env python

import sys
import itertools

ranks = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
straights = ['AKQJT', 'KQJT9', 'QJT98', 'JT987', 'T9876', '98765', '87654', '76543', '65432', 'A5432']

equivalence_class = 1
highcards = []

def init_highcards():
    r = list(ranks)
    for i in range(13):
        r.remove(ranks[i])
        for c in itertools.combinations(r, 4):
            hand = ranks[i] + ''.join(list(c))
            if not hand in straights:
                highcards.append(hand)

def print_class(cards):
    global equivalence_class
    print(str(cards), equivalence_class)
    equivalence_class += 1

def print_straights(flush):
    for s in straights:
        if flush: s += '*'
        print_class(s)

def print_filled_hands(m, n):
    for i in range(13):
        for j in range(12):
            r = list(ranks)
            r.remove(ranks[i])
            print_class(ranks[i] * m + r[j] * n)

def print_high_cards(flush):
    for h in highcards:
        if flush: h += '*'
        print_class(h)

def print_trips():
    for i in range(13):
        r = list(ranks)
        r.remove(ranks[i])
        for c in itertools.combinations(r, 2):
            print_class(ranks[i] * 3 + ''.join(list(c)))

def print_two_pair():
    for i in range(13):
        for j in range(i+1, 13):
            r = list(ranks)
            r.remove(ranks[i])
            r.remove(ranks[j])
            for k in r:
                print_class(ranks[i] * 2 + ranks[j] * 2 + k)

def print_pairs():
    for i in range(13):
        r = list(ranks)
        r.remove(ranks[i])
        for c in itertools.combinations(r, 3):
            print_class(ranks[i] * 2 + ''.join(list(c)))

def main():
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
