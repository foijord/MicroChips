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
SB 2: [0.0, 0.0, 0.0, 1.0] dot [2,  3,  0,  0]  0  0
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

Terminal node:
  - compute equity for SB and BB

Traversal (Game) State:
 - pot: num chips contributed by each decision node type (SB or BB)
 - cards held by SB and BB
 - strategy options and weights for SB and BB
 
"""

DECK = list(range(10))

class FictitiousPlay:
    def __init__(self, gametree):
        self.gametree = gametree

    def computeEquityByStrategy(self, player1, player2):
        equitybycard = [0] * len(DECK)
        for player2.card in DECK:
            equity = [self.gametree.computeEquity(GameState(player1, player2)) for player2.strategy in player2.strategies]
            equitybycard[player2.card] = sum(ev * p for ev, p in zip(equity, player2.probabilities[player2.card]))
        return sum(equitybycard) / len(DECK)

    def computeBestResponse(self, player1, player2):
        for player1.card in DECK:
            equity = [self.computeEquityByStrategy(player1, player2) for player1.strategy in player1.strategies]
            player1.updateProbabilities(equity.index(max(equity)))
        player1.n += 1
            
class Player:
    def __init__(self):
        self.n = 1.0
        self.bet = 2
        self.card = -1
        self.action = -1
        self.strategy = None
        self.strategies = None
        self.probabilities = [[1, 0, 0, 0]] * len(DECK)

    def updateProbabilities(self, best_response):
        self.probabilities[self.card] = [p * (self.n / (self.n + 1)) for p in self.probabilities[self.card]]
        self.probabilities[self.card][best_response] += 1.0 / (self.n + 1)

    def nextAction(self):
        self.action += 1
        return self.strategy[self.action]

class GameState:
    def __init__(self, player1, player2):
        self.bet = 0
        self.player = None
        self.player1 = player1
        self.player2 = player2
        self.player1.bet = 2
        self.player2.bet = 2
        self.player1.action = -1
        self.player2.action = -1

class Decision:
    def __init__(self, player, children):
        self.player = player
        self.children = children

    def computeEquity(self, state):
        state.player = self.player
        return self.children[self.player.nextAction()].computeEquity(state)

class Raise:
    def __init__(self, decision):
        self.decision = decision

    def computeEquity(self, state):
        state.bet += 1
        state.player.bet += state.bet
        return self.decision.computeEquity(state)

class Fold:
    def computeEquity(self, state):
        equity = state.player.bet
        if state.player == state.player1: return -equity
        return equity

class Call:
    def computeEquity(self, state):
        equity = state.player.bet + 1
        if state.player1.card > state.player2.card: return equity
        if state.player1.card < state.player2.card: return -equity
        return 0


FOLD = 0
CALL = 1
RAISE = 2

SB_STRATEGIES = [[FOLD], [RAISE, FOLD], [RAISE, CALL], [RAISE, RAISE]]
BB_STRATEGIES = [[FOLD], [CALL], [RAISE, FOLD], [RAISE, CALL]]


if __name__ == "__main__":
    player1 = Player()
    player2 = Player()

    player1.strategies = SB_STRATEGIES
    player2.strategies = BB_STRATEGIES
    player1.probabilities = [[0, 0, 0, 1]] * len(DECK)

    gametree = Decision(player1, [Fold(), Call(), Raise(
                Decision(player2, [Fold(), Call(), Raise(
                            Decision(player1, [Fold(), Call(), Raise(
                                        Decision(player2, [Fold(), Call()]))]))]))])

    fp = FictitiousPlay(gametree)
    for i in range(1000):
        fp.computeBestResponse(player2, player1)
        fp.computeBestResponse(player1, player2)

    for p in player1.probabilities:
        for p2 in p:
            print("%.3f" % p2)

    for p in player2.probabilities:
        for p2 in p:
            print("%.3f" % p2)

    sys.exit(0)
