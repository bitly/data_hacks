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
Calculate the 95% time from a list of times given on stdin

http://github.com/bitly/data_hacks
"""

import sys
import os
from decimal import Decimal

def run():
    count = 0
    data = {}
    for line in sys.stdin:
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
    if sys.stdin.isatty() or '--help' in sys.argv or '-h' in sys.argv:
        print "Usage: cat data | %s" % os.path.basename(sys.argv[0])
        sys.exit(1)
    run()
