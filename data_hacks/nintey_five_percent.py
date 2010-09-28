#!/bin/env python
"""
Calculate the 95% time from a list of times given on stdin

created by Jehiah Czebotar 2010-09-27
Copyright (c) 2010 bit.ly. All rights reserved.

http://github.com/bitly/data_hacks
"""
import sys
from decimal import Decimal

def run():
    count = 0
    data = {}
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        line = line.strip()
        if not line:
            # skip empty lines (ie: newlines)
            continue
        try:
            t = Decimal(line)
        except:
            print >>sys.stderr, "invalid line %r" % line
        count +=1
        data[t] = data.get(t, 0) + 1
    print calc_95(data, count)
        
def calc_95(data, count):
    # find the time it took for x entry, where x is the threshold
    threshold = Decimal(count) * Decimal('.95')
    start = Decimal(0)
    times = data.keys()
    times.sort()
    for t in times:
        # increment our count by the # of items in this time bucket
        start += data[t]
        if start > threshold:
            return t

if __name__ == "__main__":
    run()
