#!/usr/bin/env python

import sys
import getopt

def permutations(items, n):
    if n==0: yield []
    else:
        for i in xrange(len(items)):
            for cc in permutations(items[:i]+items[i+1:],n-1):
                yield [items[i]]+cc

def permutations_with_replacement(items, n):
    if n==0: yield []
    else:
        for i in xrange(len(items)):
            for ss in permutations_with_replacement(items, n-1):
                yield [items[i]]+ss

def combinations(items, n):
    if n==0: yield []
    else:
        for i in xrange(len(items)):
            for cc in combinations(items[i+1:],n-1):
                yield [items[i]]+cc
            
def combinations_with_replacement(items, n):
    indices = [0] * n
    yield [items[i] for i in indices]
    while True:
        for i in reversed(range(n)):
            if indices[i] != len(items) - 1:
                break
        else:
            return
        indices[i:] = [indices[i] + 1] * (n - i)
        yield [items[i] for i in indices]

def main(argv):

    print "permutations:"
    for c in permutations(argv, len(argv)):
        print c

    print "permutations with replacement:"
    for c in permutations_with_replacement(argv, len(argv)):
        print c

    print "combinations:"
    for c in combinations(argv, len(argv)):
        print c

    print "combinations with replacement:"
    for c in combinations_with_replacement(argv, len(argv)):
        print c

    sys.exit(1)

if __name__=="__main__":
    main(sys.argv[1:])
