#!/usr/bin/env python

import sys

"""
Simple "Poker" Game:

SB (button) and BB each ante 2 chips. They are then each dealt a card:
0, 1 or 2 where 2 is the highest card. Each of them has a 1/3 chance
of getting any card, and they can both be dealt the same card. SB acts
first and has the option to fold or bet 1 more chip. BB then has the
option to fold, call, or reraise to 2 chips. SB can now fold, call, or
reraise to 3 chips. BB must now call or fold.

SB initial strategy when holding a 
0: RAISE-FOLD
1: RAISE-CALL
2: RAISE-RAISE

BB 0 Game Tree:

  SB -- fold  ev: ( 2,  2,  2) * (0.0, 0.0, 0.0) = 0
   |
 raise  probability: (1.0, 1.0, 1.0), ev 0
   |
  BB -- fold  ev: (-2, -2, -2) * (1.0, 1.0, 1.0) = -6
   | \  
   |  call    ev: ( 0, -3, -3) * (1.0, 1.0, 1.0) = -6
   |
 raise
   | 
  SB -- fold  ev: ( 3,  3,  3) * (1.0, 0.0, 0.0) * (1.0, 1.0, 1.0) =  3
   | \
   |  call    ev: ( 0, -4, -4) * (0.0, 1.0, 0.0) * (1.0, 1.0, 1.0) = -4
   |
 raise  probability: (0.0, 0.0, 1.0) * (1.0, 1.0, 1.0) ev = 3 - 4 = -1
   |
  BB -- fold  ev: (-4, -4, -4) * (0.0, 0.0, 1.0) = -4 + -1 = -5
     \
      call    ev: ( 0, -5, -5) * (0.0, 0.0, 1.0) = -5 + -1 = -6

BB 1 Game Tree:

  SB -- fold  ev: ( 2,  2,  2) * (0.0, 0.0, 0.0) = 0
   |
 raise  probability: (1.0, 1.0, 1.0), ev 0
   |
  BB -- fold  ev: (-2, -2, -2) * (1.0, 1.0, 1.0) = -6
   | \  
   |  call    ev: ( 3,  0, -3) * (1.0, 1.0, 1.0) =  0
   |
 raise
   | 
  SB -- fold  ev: ( 3,  3,  3) * (1.0, 0.0, 0.0) * (1.0, 1.0, 1.0) =  3
   | \
   |  call    ev: ( 4,  0, -4) * (0.0, 1.0, 0.0) * (1.0, 1.0, 1.0) =  0
   |
 raise  probability: (0.0, 0.0, 1.0) * (1.0, 1.0, 1.0) ev = 3 + 0 = 3
   |
  BB -- fold  ev: (-4, -4, -4) * (0.0, 0.0, 1.0) = -4 + 3 = -1
     \
      call    ev: ( 5,  0, -5) * (0.0, 0.0, 1.0) = -5 + 3 = -2

BB 2 Game Tree:

  SB -- fold  ev: ( 2,  2,  2) * (0.0, 0.0, 0.0) = 0
   |
 raise  probability: (1.0, 1.0, 1.0), ev 0
   |
  BB -- fold  ev: (-2, -2, -2) * (1.0, 1.0, 1.0) = -6
   | \  
   |  call    ev: ( 3,  3,  0) * (1.0, 1.0, 1.0) =  6
   |
 raise
   | 
  SB -- fold  ev: ( 3,  3,  3) * (1.0, 0.0, 0.0) * (1.0, 1.0, 1.0) =  3
   | \
   |  call    ev: ( 4,  4,  0) * (0.0, 1.0, 0.0) * (1.0, 1.0, 1.0) =  4
   |
 raise  probability: (0.0, 0.0, 1.0) * (1.0, 1.0, 1.0) ev = 3 + 4 = 7
   |
  BB -- fold  ev: (-4, -4, -4) * (0.0, 0.0, 1.0) = -4 + 7 = 3
     \
      call    ev: ( 5,  5,  0) * (0.0, 0.0, 1.0) = 0 + 7 = 7

BB best response:
0: RAISE-FOLD (ev -6)
1: CALL       (ev  0)
2: RAISE-CALL (ev  7)

incorporate these probabilities in the game tree and find SBs best response:

SB 0 Game Tree:

  SB -- fold  ev: (-2, -2, -2) * (1.0, 1.0, 1.0) = -6
   |
 raise
   |
  BB -- fold  ev: ( 2,  2,  2) * (0.0, 0.0, 0.0) = 0
   | \  
   |  call    ev: ( 0, -3, -3) * (0.0, 1.0, 0.0) = -3
   |
 raise  probability: (1.0, 0.0, 1.0) ev -3
   | 
  SB -- fold  ev: (-3, -3, -3) * (1.0, 0.0, 1.0) = -3 -3 -3 = -9
   | \
   |  call    ev: ( 0, -4, -4) * (1.0, 0.0, 1.0) = -4 -3 = -7
   |
 raise  (ev -1)
   |
  BB -- fold  ev: ( 4,  4,  4) * (1.0, 0.0, 0.0) = 4 
     \
      call    ev: ( 0, -5, -5) * (0.0, 0.0, 1.0) = -5

SB 1 Game Tree:

  SB -- fold  ev: (-2, -2, -2) * (1.0, 1.0, 1.0) = -6
   |
 raise
   |
  BB -- fold  ev: ( 2,  2,  2) * (0.0, 0.0, 0.0) = 0
   | \  
   |  call    ev: ( 3,  0, -3) * (0.0, 1.0, 0.0) = 0
   |
 raise  probability: (1.0, 0.0, 1.0) ev = 0
   | 
  SB -- fold  ev: (-3, -3, -3) * (1.0, 0.0, 1.0) = -3 -3 = -6
   | \
   |  call    ev: ( 4,  0, -4) * (1.0, 0.0, 1.0) =  4 -4 = 0
   |
 raise        ev: -6
   |
  BB -- fold  ev: ( 4,  4,  4) * (0.0, 0.0, 0.0) = 0
     \
      call    ev: ( 5,  0, -5) * (0.0, 0.0, 1.0) = -5 + 2 = -3

SB 2 Game Tree:

  SB -- fold  ev: (-2, -2, -2) * (1.0, 1.0, 1.0) = -6
   |
 raise
   |
  BB -- fold  ev: ( 2,  2,  2) * (1.0, 0.0, 0.0) = 2
   | \  
   |  call    ev: ( 3,  3,  0) * (0.0, 1.0, 0.0) = 3
   |
 raise  probability: (0.0, 0.0, 1.0) ev = 5
   | 
  SB -- fold  ev: (-3, -3, -3) * (0.0, 0.0, 1.0) = -3 + 5 = 2
   | \
   |  call    ev: ( 4,  4,  0) * (0.0, 0.0, 1.0) = 0 + 5 = 5
   |
 raise        ev: 7
   |
  BB -- fold  ev: ( 4,  4,  4) * (0.0, 0.0, 0.0) = 0
     \
      call    ev: ( 5,  5,  0) * (0.0, 0.0, 1.0) = 0 + 7 = 7

SB best response:
0: RAISE-FOLD (ev -4)
1: RAISE-FOLD (ev -1)
2: RAISE-CALL (ev  7)


"""

DECK = [0, 1, 2]

class Player:
    def __init__(self, name):
        self.bet = 2
        self.card = -1
        self.name = name

class GameState:
    def __init__(self):
        self.path = []
        self.betsize = 0
        self.equity = 0.0
        self.player = None
        self.maxpath = None
        self.maxequity = -100
        self.probabilities = [1, 1, 1]

    def updateMaxEquity(self, node):
        if node.average_equity > self.maxequity:
            self.maxequity = node.average_equity
            self.maxpath = list(self.path + [node])

class Decision:
    def __init__(self, player, children):
        self.player = player
        self.children = children

    def computeEquity(self, state, player1, player2):
        state.player = self.player
        print(state.player.name)
        return sum([c.computeEquity(state, player1, player2) for c in self.children])
        
class Fold:
    def __init__(self, probabilities):
        self.average_equity = 0
        self.equity = [0.0, 0.0, 0.0]
        self.probabilities = probabilities

    def computeEquity(self, state, player1, player2):
        for player2.card in DECK:
            if state.player == player1: 
                self.equity[player2.card] = -state.player.bet 
            else: self.equity[player2.card] = state.player.bet

        p = state.probabilities
        if state.player == player2:
            p = self.probabilities

        self.average_equity = sum([i * j for i, j in zip(self.equity, p)])

        if state.player == player2:
            state.equity += self.average_equity
        else:
            self.average_equity += state.equity
            state.updateMaxEquity(self)

        e = self.equity
        print("Fold, ev: [%.2f %.2f %.2f] p: [%.2f, %.2f, %.2f] ev: %d" % (e[0], e[1], e[2], p[0], p[1], p[2], self.average_equity))
        return self.average_equity

class Call:
    def __init__(self, probabilities):
        self.equity = [0.0, 0.0, 0.0]
        self.average_equity = 0
        self.probabilities = probabilities

    def computeEquity(self, state, player1, player2):
        bet = state.player.bet + 1
        for player2.card in DECK:
            if player1.card >  player2.card: self.equity[player2.card] =  bet
            if player1.card <  player2.card: self.equity[player2.card] = -bet
            if player1.card == player2.card: self.equity[player2.card] =  0.0

        p = state.probabilities
        if state.player == player2:
            p = self.probabilities

        self.average_equity = sum([i * j for i, j in zip(self.equity, p)])

        if state.player == player2:
            state.equity += self.average_equity
        else:
            self.average_equity += state.equity
            state.updateMaxEquity(self)

        e = self.equity
        print("Call, ev: [%.2f %.2f %.2f] p: [%.2f, %.2f, %.2f] ev: %i" % (e[0], e[1], e[2], p[0], p[1], p[2], self.average_equity))
        return self.average_equity

class Raise:
    def __init__(self, probabilities, isleaf, decision):
        self.isleaf = isleaf
        self.average_equity = 0
        self.probabilities = probabilities
        self.decision = decision

    def computeEquity(self, state, player1, player2):
        print("Raise")
        if state.player == player2:
            print("p: [%.2f, %.2f, %.2f]" % (self.probabilities[0], self.probabilities[1], self.probabilities[2]))
            print("State ev: %d" % state.equity)

        state.betsize += 1
        state.player.bet += state.betsize

        if state.player == player2: 
            for i in range(3): state.probabilities[i] *= self.probabilities[i]
        else:
            if not self.isleaf:
                state.path.append(self)

        self.average_equity = self.decision.computeEquity(state, player1, player2)

        if self.isleaf and state.player == player2:
            print("updating max equity for raise")
            state.updateMaxEquity(self)

        return self.average_equity


def computeBestResponse(player1, player2):
    player1.bet = 2
    player2.bet = 2
    state = GameState()
    gametree.computeEquity(state, player1, player2)
    print("max equity: %d" % state.maxequity)
    for node in state.maxpath:
        print(node.__class__)

if __name__ == "__main__":
    player1 = Player("Player1")
    player2 = Player("Player2")

    gametree = Decision(player1, [Fold([0, 0, 0]), Raise([1, 1, 1], False,
                Decision(player2, [Fold([0, 0, 0]), Call([0, 1, 0]), Raise([1, 0, 1], False,
                            Decision(player1, [Fold([1, 0, 0]), Call([0, 1, 0]), Raise([0, 0, 1], True,
                                        Decision(player2, [Fold([1, 0, 0]), Call([0, 0, 1])]))]))]))])


    player1.card = 0
    player2.card = 0
    computeBestResponse(player1, player2)
