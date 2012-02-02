#!/usr/bin/env python

import sys
import argparse
import itertools

ranks = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']

def main():
    parser = argparse.ArgumentParser(
        description = 'Generates permutations or combinations of the input, with or without replacement')

    parser.add_argument('-n', required = True, nargs = '+', help = 'collection to choose from')
    parser.add_argument('-r', required = True, type = int, help = 'choose R items from collection N')
    parser.add_argument('-t', required = False, default = False, action = 'store_true', help = 'generate with replacement')

    args = parser.parse_args()
    method = itertools.combinations_with_replacement if args.t else itertools.combinations
    for c in method(args.n, args.r): print(''.join(sorted(list(c), key = ranks.index)))

    sys.exit(1)

if __name__=="__main__":
    main()
