#!/usr/bin/env python

def combinations(items, n):
    if n==0: yield []
    else:
        for i in xrange(len(items)):
            for cc in combinations(items[i+1:], n-1):
                yield [items[i]] + cc


