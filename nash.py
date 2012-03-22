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


SB: card 1 BB: card 1

  SB -- fold [SB -2 BB 2]
   | 
 raise
   |
  BB -- fold [SB 2 BB -2]
   | \
   |  call   [SB 0 BB 0]
 raise
   |
  SB -- fold [SB -3 BB 3]
   | \
   |  call   [SB 0 BB 0]
 raise
   |
  BB -- fold [SB 4 BB -4]
     \
      call   [SB 0 BB 0]

SB starts with the strategy of always raising.

Weights for Strategy ALWAYS_RAISE:
1: [0.0, 0.0, 0.0, 1.0]
2: [0.0, 0.0, 0.0, 1.0]
3: [0.0, 0.0, 0.0, 1.0]

We must find the BB strategy that gives the highest equity against
ALWAYS_RAISE. This means for each possible SB strategy (FOLD,
RAISE_FOLD, RAISE_CALL, RAISE_RAISE), for each possible card, we must
figure out the equity of BBs options (FOLD, CALL, RAISE_FOLD and
RAISE_CALL)

BB FOLD: (Pot contribution: 2 chips)
SB_OPTIONS = [FOLD, RAISE_FOLD, RAISE_CALL, RAISE_RAISE]
BB_OPTIONS = [FOLD, CALL, RAISE_FOLD, RAISE_CALL]

BB 1:

SB 1: [0.0, 0.0, 0.0, 1.0] dot [2, -2, -2, -2] -2
SB 2: [0.0, 0.0, 0.0, 1.0] dot [2, -2, -2, -2] -2 -2
SB 3: [0.0, 0.0, 0.0, 1.0] dot [2, -2, -2, -2] -2

BB 2:

SB 1: [0.0, 0.0, 0.0, 1.0] dot [2, -2, -2, -2] -2
SB 2: [0.0, 0.0, 0.0, 1.0] dot [2, -2, -2, -2] -2 -2
SB 3: [0.0, 0.0, 0.0, 1.0] dot [2, -2, -2, -2] -2

BB 3:

SB 1: [0.0, 0.0, 0.0, 1.0] dot [2, -2, -2, -2] -2
SB 2: [0.0, 0.0, 0.0, 1.0] dot [2, -2, -2, -2] -2 -2
SB 3: [0.0, 0.0, 0.0, 1.0] dot [2, -2, -2, -2] -2

BB CALL: (Pot contribution: 3 chips)
SB_OPTIONS = [FOLD, RAISE_FOLD, RAISE_CALL, RAISE_RAISE]

BB 1: 

SB 1: [0.0, 0.0, 0.0, 1.0] dot [2,  0,  0,  0]  0
SB 2: [0.0, 0.0, 0.0, 1.0] dot [2, -3, -3, -3] -3 -2
SB 3: [0.0, 0.0, 0.0, 1.0] dot [2, -3, -3, -3] -3

BB 2:

SB 1: [0.0, 0.0, 0.0, 1.0] dot [2,  3,  3,  3]  3
SB 2: [0.0, 0.0, 0.0, 1.0] dot [2,  0,  0,  0]  0  0
SB 3: [0.0, 0.0, 0.0, 1.0] dot [2, -3, -3, -3] -3

BB 3:

SB 1: [0.0, 0.0, 0.0, 1.0] dot [2,  3,  3,  3]  3
SB 2: [0.0, 0.0, 0.0, 1.0] dot [2,  3,  3,  3]  3  2
SB 3: [0.0, 0.0, 0.0, 1.0] dot [2,  0,  0,  0]  0

BB RAISE_FOLD: (Pot contribution: 4 chips)
SB_OPTIONS = [FOLD, RAISE_FOLD, RAISE_CALL, RAISE_RAISE]

BB 1:

SB 1: [0.0, 0.0, 0.0, 1.0] dot [2,  3,  0, -4] -4
SB 2: [0.0, 0.0, 0.0, 1.0] dot [2,  3, -4, -4] -4 -4
SB 3: [0.0, 0.0, 0.0, 1.0] dot [2,  3, -4, -4] -4

BB 2:

SB 1: [0.0, 0.0, 0.0, 1.0] dot [2,  3,  4, -4] -4
SB 2: [0.0, 0.0, 0.0, 1.0] dot [2,  3,  0, -4] -4 -4
SB 3: [0.0, 0.0, 0.0, 1.0] dot [2,  3, -4, -4] -4

BB 3:

SB 1: [0.0, 0.0, 0.0, 1.0] dot [2,  3,  4, -4] -4
SB 2: [0.0, 0.0, 0.0, 1.0] dot [2,  3,  4, -4] -4 -4
SB 3: [0.0, 0.0, 0.0, 1.0] dot [2,  3,  0, -4] -4

BB RAISE_CALL: (Pot contribution: 4 or 5 chips)
SB_OPTIONS = [FOLD, RAISE_FOLD, RAISE_CALL, RAISE_RAISE]

BB 1:

SB 1: [0.0, 0.0, 0.0, 1.0] dot [2,  3,  0,  0]  0
SB 2: [0.0, 0.0, 0.0, 1.0] dot [2,  3, -4, -5] -5 -3.33
SB 3: [0.0, 0.0, 0.0, 1.0] dot [2,  3, -4, -5] -5

BB 2:

SB 1: [0.0, 0.0, 0.0, 1.0] dot [2,  3,  4,  5]  5
SB 2: [0.0, 0.0, 0.0, 1.0] dot [2,  3,  0,  0]  0   0
SB 3: [0.0, 0.0, 0.0, 1.0] dot [2,  3, -4, -5] -5

BB 3:

SB 1: [0.0, 0.0, 0.0, 1.0] dot [2,  3,  4,  5]  5
SB 2: [0.0, 0.0, 0.0, 1.0] dot [2,  3,  4,  5]  5  3.33
SB 3: [0.0, 0.0, 0.0, 1.0] dot [2,  3,  0,  0]  0

So an optimal mixed strategy against ALWAYS RAISE is:

1: [0.5, 0.5, 0.0, 0.0]
2: [0.0, 0.5, 0.0, 0.5]
3: [0.0, 0.0, 0.0, 1.0]

If BB is holding a 1, he should fold half the time and call half the time
If BB is holding a 2, he should call half the time and raise-call half the time
If BB is holding a 3, he should raise-call every time

Game Tree Nodes:

Decision node:
 - type: SB or BB
 - fold, call, raise
 - children: 0 or 1 Decision nodes + Showdown nodes for call, fold

Showdown node:
  - compute equity for SB and BB

Traversal (Game) State:
 - pot: num chips contributed by each decision node type (SB or BB)
 - cards held by SB and BB
 - strategy options and weights for SB and BB
 
"""

BET = 1
ANTE = 2
DECK = [0, 1, 2]

SB_OPTIONS = [FOLD, RAISE_FOLD, RAISE_CALL, RAISE_RAISE]
BB_OPTIONS = [FOLD, CALL, RAISE_FOLD, RAISE_CALL]

""" initial strategy of always raising """
ALWAYS_RAISE = [[0, 0, 0, 1], [0, 0, 0, 1], [0, 0, 0, 1], [0, 0, 0, 1]]

if __name__ == "__main__":
    sys.exit(0)
