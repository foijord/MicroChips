#!/usr/bin/env python

import sys

"""
SB (button) and BB each ante 2 chips. They are then each dealt a
card: 1, 2, or 3. Each of them has a 1/3 chance of getting any card,
and they can both be dealt the same card, in which case they obviously
chop at showdown. SB acts first and has the option to fold or bet 1
more chip (call this a 2-bet, even though it's the first bet, to keep
the analogy with HU limit HE). BB then has the option to fold, call,
or reraise to 2 chips (3-bet). SB can now fold, call, or reraise to 3
chips (4-bet). BB must now just call or fold, and the hands are
showdown. A 3 is the best hand.
"""

BET = 1
ANTE = 2
DECK = [1, 2, 3]

SB_STRATEGIES = [FOLD, RAISE_FOLD, RAISE_CALL, RAISE_RAISE]
BB_STRATEGIES = [FOLD, CALL, RAISE_FOLD, RAISE_CALL]

ALWAYS_RAISE = [[0, 0, 0, 1], [0, 0, 0, 1], [0, 0, 0, 1], [0, 0, 0, 1]]

def getBestResponse(strategy, villain_options):
    response = []
    for s in strategy:
        for weight in s:
            pass
    return response

if __name__ == "__main__":

    sbstrategy = ALWAYS_RAISE
    bbstrategy = getBestResponse(sbstrategy, BB_STRATEGIES)

    print(sbstrategy)
    print(bbstrategy)
    
    sys.exit(0)
