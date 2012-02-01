#!/usr/bin/env python

import sys
import argparse

def permutations(items, n):
    if n==0: yield []
    else:
        for i in range(len(items)):
            for cc in permutations(items[:i]+items[i+1:],n-1):
                yield [items[i]]+cc

def permutations_with_replacement(items, n):
    if n==0: yield []
    else:
        for i in range(len(items)):
            for ss in permutations_with_replacement(items, n-1):
                yield [items[i]]+ss

def combinations(items, n):
    if n==0: yield []
    else:
        for i in range(len(items)):
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


def main():
    parser = argparse.ArgumentParser(
        description = 'Generates permutations or combinations of the input, with or without replacement')

    group = parser.add_mutually_exclusive_group()
    
    parser.add_argument('-n', required = True, nargs = '+', help = 'collection to choose from')
    parser.add_argument('-r', required = True, type = int, help = 'choose R items from collection N')
    parser.add_argument('-t', required = False, default = False, action = 'store_true', help = 'generate with replacement')
    group.add_argument('-c', required = False, default = False, action = 'store_true', help = 'generate combinations')
    group.add_argument('-p', required = False, default = False, action = 'store_true', help = 'generate permutations')

    args = parser.parse_args()
    method = combinations_with_replacement if args.t else combinations
    if (args.p): method = permutations_with_replacement if args.t else permutations
    for c in method(args.n, args.r): print(c)

    sys.exit(1)

if __name__=="__main__":
    main()
