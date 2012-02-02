#!/usr/bin/env python3

import sys

handdict = {}

def main():
    ec = open('ec.dat', 'r')
    for line in ec:
        line = line.replace('\n', '') # better way of removing newline?
        elements = line.split('\t')
        handdict[elements[0]] = (elements[1], elements[2])

    level5 = open('level5.dat', 'r')
    for line in level5:
        line = line.replace('\n', '')
        if not line in handdict:
            print("key not found:", line)

if __name__ == "__main__":
    main()
