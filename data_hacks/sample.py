#!/bin/env python
"""
Pass through a sampled percentage of data

created by Jehiah Czebotar 2010-09-27
Copyright (c) 2010 bit.ly. All rights reserved.

http://github.com/bitly/data_hacks
"""

import sys
import random
from optparse import OptionParser
from decimal import Decimal

def usage():
    print """
    usage:
        cat data | sample.py 10% | sort | uniq -c
        cat data | sample.py 1/50 | sort | uniq -c
"""

def run(sample_rate):
    input_stream = sys.stdin
    while True:
        line = input_stream.readline()
        if not line:
            break
        if random.randint(1,100) < sample_rate:
            sys.stdout.write(line)

def get_sample_rate(rate_string):
    """ return a rate as a percewntage"""
    if rate_string.endswith("%"):
        rate = int(rate_string[:-1])
    elif '/' in rate_string:
        x, y  = rate_string.split('/')
        rate = Decimal(x) / (Decimal(y) * Decimal('1.0'))
        rate = int(rate * 100)
    else:
        raise ValueError("rate %r is invalid rate format must be '10%%' or '1/10'" % rate_string)
    if rate < 1 or rate > 100:
        raise ValueError('rate %r must be 1%% <= rate <= 100%% ' % rate_string)
    return rate

if __name__ == "__main__":
    parser = OptionParser()
    parser.usage = "cat data | %prog [options] [sample_rate]"
    parser.add_option("-v", "--verbose", dest="verbose", default=False, action="store_true")
    (options, args) = parser.parse_args()
    
    if not args or sys.stdin.isatty():
        parser.print_usage()
        sys.exit(1)
    
    try:
        sample_rate = get_sample_rate(sys.argv[-1])
    except ValueError, e:
        print >>sys.stderr, e
        parser.print_usage()
        sys.exit(1)
    if options.verbose:
        print >>sys.stderr, "Sample rate is %d%%" % sample_rate 
    run(sample_rate)
