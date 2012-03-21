#!/usr/bin/env python

import sys

"""
Simple "Poker" Game:

SB (button) and BB each ante 2 chips. They are then each dealt a card:
1, 2 or 3 where 3 is the highest card. Each of them has a 1/3 chance
of getting any card, and they can both be dealt the same card. SB acts
first and has the option to fold or bet 1 more chip. BB then has the
option to fold, call, or reraise to 2 chips. SB can now fold, call, or
reraise to 3 chips. BB must now call or fold.

Game Tree:

  SB -- fold
   | 
 raise
   |
  BB -- fold
   | \
   |  call
 raise
   |
  SB -- fold
   | \
   |  call
 raise
   |
  BB -- fold
     \
      call

SB starts with the strategy of always raising.

Strategy ALWAYS RAISE:
1: [0.0, 0.0, 0.0, 1.0]
2: [0.0, 0.0, 0.0, 1.0]
3: [0.0, 0.0, 0.0, 1.0]

We must find the BB strategy that gives the highest equity against
ALWAYS_RAISE. This means for each possible holding, we must figure out
the equity of FOLD, CALL, RAISE_FOLD and RAISE_CALL.

SB is holding a 1, 2, or 3 with equal probability

FOLD:
(Pot contribution: 2 chips)
         win tie lose ev
      1:  0   0   3   -2
Hand  2:  0   0   3   -2
      3:  0   0   3   -2

CALL:
(Pot contribution: 3 chips)
         win tie lose ev
      1:  0   1   2   -3
Hand  2:  1   1   1    0
      3:  2   1   0   +3

RAISE_FOLD:
(Pot contribution: 4 chips)
         win tie lose ev
      1:  0   0   3   -4
Hand  2:  0   0   3   -4
      3:  0   0   3   -4

RAISE_CALL:
(Pot contribution: 5 chips)
         win tie lose ev
      1:  0   1   2   -5
Hand  2:  1   1   1    0
      3:  2   1   0   +5


So the best strategy against ALWAYS RAISE is:

1: [1.0, 0.0, 0.0, 0.0]
2: [0.0, 0.5, 0.0, 0.5]
3: [0.0, 0.0, 0.0, 1.0]

If BB is holding a 1, he should always fold.
If BB is holding a 2, he should always call or raise, then call.
If BB is holding a 3, he should always raise, then call.

This strategy will win (5 + 0 -2) / 3 = 1 chip per hand

What's the best strategy against this counter-strategy?

FOLD:
(Pot contribution: 2 chips)
         win tie lose ev
      1:  0   0   3   -2
Hand  2:  0   0   3   -2
      3:  0   0   3   -2


RAISE_FOLD:

If SB is raising, BB will fold 1/3rd of the time, call 1/6th of the
time and raise half the time. If BB is raising, SB is losing, since
SB must then fold. SB puts 3 chips in the pot.

SB 1: BB 1: BB folds a 1            ev  2 * 1.0
SB 1: BB 2: BB calls with a 2.      ev -3 * 0.5
SB 1: BB 2: BB raises, SB folds.    ev -3 * 0.5
SB 1: BB 3: BB raises, SB folds.    ev -3 * 1.0

"""

BET = 1
ANTE = 2
DECK = [0, 1, 2]

SB_OPTIONS = [FOLD, RAISE_FOLD, RAISE_CALL, RAISE_RAISE]
BB_OPTIONS = [FOLD, CALL, RAISE_FOLD, RAISE_CALL]

""" initial strategy of always raising """
ALWAYS_RAISE = [[0, 0, 0, 1], [0, 0, 0, 1], [0, 0, 0, 1], [0, 0, 0, 1]]

"""

"""

def getEquityVersusStrategy(strategy):
    pass

def getBestResponse(strategy, options):
    response = []
    for s in strategy:
        for weight in s:
            pass
    return response

if __name__ == "__main__":
    sb_strategy = ALWAYS_RAISE
    bb_strategy = None

    bbstrategy = getBestResponse(sb_strategy, BB_OPTIONS)

    print(sbstrategy)
    print(bbstrategy)
    
    sys.exit(0)
