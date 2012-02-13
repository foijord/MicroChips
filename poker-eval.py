#!/usr/bin/env python

import sys
import os
import itertools

from FiveEval import *
import Constants

ranks = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
suits = ['s', 'h', 'd', 'c']
cards = [ r + s for r in ranks for s in suits ]
deck = dict([(c, cards.index(c)) for c in cards])

class SevenEval :
    def __init__(self) :
        self.rankArray = [0] * Constants.CIRCUMFERENCE_SEVEN
        self.flushRankArray = [0] * (Constants.MAX_SEVEN_FLUSH_KEY_INT + 1)
        self.deckcardsKey = [0] * Constants.DECK_SIZE
        self.deckcardsFlush = [0] * Constants.DECK_SIZE
        self.deckcardsSuit = [0] * Constants.DECK_SIZE      
        self.flushCheck = [0] * (Constants.MAX_FLUSH_CHECK_SUM + 1)
    
        face = [Constants.ACE, Constants.KING, Constants.QUEEN, Constants.JACK, Constants.TEN,
                Constants.NINE, Constants.EIGHT, Constants.SEVEN, Constants.SIX, Constants.FIVE,
                Constants.FOUR, Constants.THREE, Constants.TWO]

        faceFlush = [Constants.ACE_FLUSH, Constants.KING_FLUSH, Constants.QUEEN_FLUSH,
                     Constants.JACK_FLUSH, Constants.TEN_FLUSH, Constants.NINE_FLUSH,
                     Constants.EIGHT_FLUSH, Constants.SEVEN_FLUSH, Constants.SIX_FLUSH,
                     Constants.FIVE_FLUSH, Constants.FOUR_FLUSH, Constants.THREE_FLUSH,
                     Constants.TWO_FLUSH]

        for n in range(0, 13):
            self.deckcardsKey[4*n + 0] = (face[n] << Constants.NON_FLUSH_BIT_SHIFT) + Constants.SPADE
            self.deckcardsKey[4*n + 1] = (face[n] << Constants.NON_FLUSH_BIT_SHIFT) + Constants.HEART
            self.deckcardsKey[4*n + 2] = (face[n] << Constants.NON_FLUSH_BIT_SHIFT) + Constants.DIAMOND
            self.deckcardsKey[4*n + 3] = (face[n] << Constants.NON_FLUSH_BIT_SHIFT) + Constants.CLUB
            
            self.deckcardsFlush[4*n + 0] = faceFlush[n]
            self.deckcardsFlush[4*n + 1] = faceFlush[n]
            self.deckcardsFlush[4*n + 2] = faceFlush[n]
            self.deckcardsFlush[4*n + 3] = faceFlush[n]
            
            self.deckcardsSuit[4*n + 0] = Constants.SPADE
            self.deckcardsSuit[4*n + 1] = Constants.HEART
            self.deckcardsSuit[4*n + 2] = Constants.DIAMOND
            self.deckcardsSuit[4*n + 3] = Constants.CLUB
        
        fiveCardEvaluator = FiveEval()
                
        # High card.
        for i in range(1, len(ranks)):
            for j in range(1, i+1) :
                for k in range(1, j+1) :
                    for l in range(0, k+1) :
                        for m in range(0, l+1) :
                            for n in range(0, m+1) :
                                for p in range(0, n+1) :
                                    if i != m and j != n and k != p :
                                        key = face[i] + face[j] + face[k] + face[l] + face[m] + face[n] + face[p]
                                        # The 4*i+0 and 4*m+1 trick prevents flushes.
                                        rank = fiveCardEvaluator.getRankOfSeven(4*i, 4*j, 4*k, 4*l, 4*m+1, 4*n+1, 4*p+1)
                                        self.rankArray[key % Constants.CIRCUMFERENCE_SEVEN] = rank



        # Flush ranks.
        # All 7 same suit.
        for c in itertools.combinations([i for i in range(0, Constants.NUMBER_OF_FACES)], 7):
            key = sum([faceFlush[c[i]] for i in range(0, 7)])
            self.flushRankArray[key] = fiveCardEvaluator.getRankOfSeven(4*c[0], 4*c[1], 4*c[2], 4*c[3], 4*c[4], 4*c[5], 4*c[6])
            
        # Only 6 same suit.
        for c in itertools.combinations([i for i in range(0, Constants.NUMBER_OF_FACES)], 6):
            key = sum([faceFlush[c[i]] for i in range(0, 6)])
            # The Two of clubs is the card at index 51; the other six
            # cards all have the spade suit.
            self.flushRankArray[key] = fiveCardEvaluator.getRankOfSeven(4*c[0], 4*c[1], 4*c[2], 4*c[3], 4*c[4], 4*c[5], 51)
                                
        # Only 5 same suit.
        for c in itertools.combinations([i for i in range(0, Constants.NUMBER_OF_FACES)], 5):
            key = sum([faceFlush[c[i]] for i in range(0, 5)])
            self.flushRankArray[key] = fiveCardEvaluator.getRankOfFive(4*c[0], 4*c[1], 4*c[2], 4*c[3], 4*c[4]);
                        
        # Initialise flush checks.
        suits = [Constants.SPADE, Constants.HEART, Constants.DIAMOND, Constants.CLUB]
        # Initialise all entries of flushCheck[] to UNVERIFIED, as yet unchecked.       
        self.flushCheck = [Constants.UNVERIFIED] * (Constants.MAX_FLUSH_CHECK_SUM + 1)
        
        # 7-card flush.
        for card_1 in range(0, Constants.NUMBER_OF_SUITS) :
            for card_2 in range(0, card_1 + 1) :
                for card_3 in range(0, card_2 + 1) :
                    for card_4 in range(0, card_3 + 1) :
                        for card_5 in range(0, card_4 + 1) :
                            for card_6 in range(0, card_5 + 1) :
                                for card_7 in range(0, card_6 + 1) :
                                    FLUSH_SUIT_INDEX = -1
                                    CARDS_MATCHED_SO_FAR = 0
                                    SUIT_KEY = suits[card_1] + suits[card_2] + suits[card_3] + \
                                        suits[card_4] + suits[card_5] + suits[card_6] + \
                                        suits[card_7]
                                                                        
                                    if self.flushCheck[SUIT_KEY] == Constants.UNVERIFIED :
                                        while CARDS_MATCHED_SO_FAR < 3 and FLUSH_SUIT_INDEX < 4 :
                                            FLUSH_SUIT_INDEX += 1
                                            SUIT_COUNT = (suits[card_1] == suits[FLUSH_SUIT_INDEX]) + \
                                                (suits[card_2] == suits[FLUSH_SUIT_INDEX]) + \
                                                (suits[card_3] == suits[FLUSH_SUIT_INDEX]) + \
                                                (suits[card_4] == suits[FLUSH_SUIT_INDEX]) + \
                                                (suits[card_5] == suits[FLUSH_SUIT_INDEX]) + \
                                                (suits[card_6] == suits[FLUSH_SUIT_INDEX]) + \
                                                (suits[card_7] == suits[FLUSH_SUIT_INDEX])
                                            CARDS_MATCHED_SO_FAR += SUIT_COUNT

                                    self.flushCheck[SUIT_KEY] = suits[FLUSH_SUIT_INDEX] if SUIT_COUNT > 4 else Constants.NOT_A_FLUSH
                
        
    def getRank(self, hand):
        # Create a 7-card hand key by adding up each of the card keys.
        KEY = sum([self.deckcardsKey[card] for card in hand])

        # Tear off the flush check strip.
        FLUSH_SUIT = self.flushCheck[KEY & Constants.SUIT_BIT_MASK]
                
        if FLUSH_SUIT == Constants.NOT_A_FLUSH :
            # Tear off the non-flush key strip, and look up the rank.
            KEY = ( KEY >> Constants.NON_FLUSH_BIT_SHIFT )
            
            # Take key modulo the circumference. A dichotomy is faster than using
            # the usual modulus operation. This is fine for us because the circumference
            # is more than half the largest face key we come across.
            rank = self.rankArray[KEY] if KEY < Constants.CIRCUMFERENCE_SEVEN else self.rankArray[KEY - Constants.CIRCUMFERENCE_SEVEN]
            return rank
                
        else :
            # Generate a flush key, and look up the rank.
            flushkeys = [self.deckcardsFlush[card] if self.deckcardsSuit[card] == FLUSH_SUIT else 0 for card in hand]
            return self.flushRankArray[sum(flushkeys)]
        
    def eval7(self, cards):
        return self.getRankOfSeven(deck[cards[0]], deck[cards[1]], deck[cards[2]], deck[cards[3]], deck[cards[4]], deck[cards[5]], deck[cards[6]])

"""                
0 = Ace of Spades
1 = Ace of Hearts
2 = Ace of Diamonds
3 = Ace of Clubs

4 = King of Spades
5 = King of Hearts
6 = King of Diamonds
7 = King of Clubs
"""

def main():
    seven_eval = SevenEval()

    # evaluate all 7-card hands:
    deck = [i for i in range(52)]

    counts = [0] * 7462
    for hand in itertools.combinations(deck, 7):
        rank = seven_eval.getRank(hand)
        counts[rank - 1] += 1

    print(counts)

if __name__ == "__main__":
    main()
