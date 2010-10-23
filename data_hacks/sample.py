#!/bin/env python
# 
# Copyright 2010 bit.ly
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""
Pass through a sampled percentage of data

http://github.com/bitly/data_hacks
"""

import sys
import random
from optparse import OptionParser
from decimal import Decimal

def run(sample_rate):
    input_stream = sys.stdin
    for line in input_stream:
        if random.randint(1,100) <= sample_rate:
            sys.stdout.write(line)

def get_sample_rate(rate_string):
    """ return a rate as a percentage"""
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
    parser = OptionParser(usage="cat data | %prog [options] [sample_rate]")
    parser.add_option("--verbose", dest="verbose", default=False, action="store_true")
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
