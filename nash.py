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

Terminal node:
  - compute equity for SB and BB

Traversal (Game) State:
 - pot: num chips contributed by each decision node type (SB or BB)
 - cards held by SB and BB
 - strategy options and weights for SB and BB
 
"""

DECK = [0, 1, 2]

class FictitiousPlay:
    def __init__(self, gametree):
        self.gametree = gametree

    def computeEquityByCard(self, player1, player2):
        equitybycard = [0, 0, 0]
        for player2.card in DECK:
            state = GameState([player1, player2])
            equity = [self.gametree.computeEquity(state) for player2.strategy in player2.strategies]
            equitybycard[player2.card] = dot(equity, player2.probabilities[player2.card]) / 3.0
        return equitybycard

    def computeBestResponse(self, player1, player2):
        for player1.card in DECK:
            response = [0] * 4
            equity_by_strategy = []
            for player1.strategy in player1.strategies:
                equity_by_card = self.computeEquityByCard(player1, player2)
                equity_by_strategy += [sum(equity_by_card)]
            max_equity = max(equity_by_strategy)
            response[equity_by_strategy.index(max_equity)] = 1
            player1.updateProbabilities(response)
        player1.n += 1
            

def dot(v1, v2):
    assert len(v1) == len(v2)
    return sum([v1[i] * v2[i] for i in range(len(v1))])

class Player:
    def __init__(self):
        self.n = 1.0
        self.bet = 2
        self.card = -1
        self.currentmove = -1
        self.strategy = None
        self.strategies = None
        self.probabilities = [[1, 0, 0, 0],
                              [1, 0, 0, 0],
                              [1, 0, 0, 0]]

    def updateProbabilities(self, response):
        probabilities = self.probabilities[self.card]
        for i in range(len(probabilities)):
            probabilities[i] *= (self.n / (self.n + 1))
            probabilities[i] += response[i] / (self.n + 1)

    def nextMove(self):
        self.currentmove += 1
        return self.strategy[self.currentmove]

class GameState:
    def __init__(self, players):
        self.players = players
        self.player = None
        self.reset()

    def reset(self):
        self.bet = 0
        for player in self.players:
            player.currentmove = -1
            player.bet = 2

class Decision:
    def __init__(self, player, children):
        self.player = player
        self.children = children

    def computeEquity(self, gamestate):
        gamestate.player = self.player
        return self.children[self.player.nextMove()].computeEquity(gamestate)

class Raise:
    def __init__(self, decision):
        self.decision = decision

    def computeEquity(self, gamestate):
        gamestate.bet += 1
        gamestate.player.bet += gamestate.bet
        return self.decision.computeEquity(gamestate)

class Fold:
    def __init__(self):
        self.equity = 0

    def computeEquity(self, state):
        if state.player == state.players[0]:
            self.equity = -state.player.bet
        else:
            self.equity = state.player.bet
        state.reset()
        return self.equity

class Call:
    def __init__(self):
        self.equity = 0

    def computeEquity(self, state):
        bet = state.player.bet + 1
        if state.players[0].card > state.players[1].card:
            self.equity = bet
        elif state.players[0].card < state.players[1].card:
            self.equity = -bet
        else:
            self.equity = 0
        state.reset()
        return self.equity


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

    player1.probabilities = [[0, 0, 0, 1],
                             [0, 0, 0, 1],
                             [0, 0, 0, 1]]


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
