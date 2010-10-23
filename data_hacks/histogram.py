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
Generate a text format histogram

This is a loose port to python of the Perl version at
http://www.pandamatak.com/people/anand/xfer/histo

http://github.com/bitly/data_hacks
"""

import sys
from decimal import Decimal
import math
from optparse import OptionParser

class MVSD(object):
    """ A class that calculates a running Mean / Variance / Standard Deviation"""
    def __init__(self):
        self.is_started = False
        self.ss = Decimal(0) # (running) sum of square deviations from mean
        self.m = Decimal(0) # (running) mean
        self.total_w = Decimal(0) # weight of items seen
        
    def add(self, x, w=1):
        """ add another datapoint to the Mean / Variance / Standard Deviation"""
        if not isinstance(x, Decimal):
            x = Decimal(x)
        if not self.is_started:
            self.m = x
            self.ss = Decimal(0)
            self.total_w = w
            self.is_started = True
        else:
            temp_w = self.total_w + w
            self.ss += (self.total_w * w * (x - self.m) * (x - self.m )) / temp_w
            self.m += (x - self.m) / temp_w 
            self.total_w = temp_w
        
        # print "added %-2d mean=%0.2f var=%0.2f std=%0.2f" % (x, self.mean(), self.var(), self.sd())
        
    def var(self):
        return self.ss / self.total_w
    
    def sd(self):
        return math.sqrt(self.var())
    
    def mean(self):
        return self.m

def test_mvsd():
    mvsd = MVSD()
    for x in range(10):
        mvsd.add(x)
    
    assert '%.2f' % mvsd.mean() == "4.50"
    assert '%.2f' % mvsd.var() == "8.25"
    assert '%.14f' % mvsd.sd() == "2.87228132326901"


def load_stream(input_stream):
    for line in input_stream:
        clean_line = line.strip()
        if not clean_line:
            # skip empty lines (ie: newlines)
            continue
        if clean_line[0] in ['"', "'"]:
            clean_line = clean_line.strip('"').strip("'")
        try:
            yield Decimal(clean_line)
        except:
            print >>sys.stderr, "invalid line %r" % line

def histogram(stream, options):
    """
    Loop over the stream and add each entry to the dataset, printing out at the end
    
    stream yields Decimal() 
    """
    if not options.min or not options.max:
        # glob the iterator here so we can do min/max on it
        data = list(stream)
    else:
        data = stream
    bucket_scale = 1
    
    if options.min:
        min_v = Decimal(options.min)
    else:
        min_v = min(data)
    if options.max:
        max_v = Decimal(options.max)
    else:
        max_v = max(data)
    buckets = options.buckets and int(options.buckets) or 10
    if buckets <= 0:
        raise ValueError('# of buckets must be > 0')
    if not max_v > min_v:
        raise ValueError('max must be > min. max:%s min:%s' % (max_v, min_v))
        
    diff = max_v - min_v
    step = diff / buckets
    bucket_counts = [0 for x in range(buckets)]
    boundaries = []
    for x in range(buckets):
        boundaries.append(min_v + (step * (x + 1)))
    
    skipped = 0
    samples = 0
    mvsd = MVSD()
    for value in data:
        samples +=1
        if options.mvsd:
            mvsd.add(value)
        # find the bucket this goes in
        if value < min_v or value > max_v:
            skipped +=1
            continue
        for bucket_postion, boundary in enumerate(boundaries):
            if value <= boundary:
                bucket_counts[bucket_postion] +=1
                break
    
    # auto-pick the hash scale
    if max(bucket_counts) > 75:
        bucket_scale = int(max(bucket_counts) / 75)
    
    print "# NumSamples = %d; Min = %0.2f; Max = %0.2f" % (samples, min_v, max_v)
    if skipped:
        print "# %d value%s outside of min/max" % (skipped, skipped > 1 and 's' or '')
    if options.mvsd:
        print "# Mean = %f; Variance = %f; SD = %f" % (mvsd.mean(), mvsd.var(), mvsd.sd())
    print "# each * represents a count of %d" % bucket_scale
    bucket_min = min_v
    bucket_max = min_v
    for bucket in range(buckets):
        bucket_min = bucket_max
        bucket_max = boundaries[bucket]
        bucket_count = bucket_counts[bucket]
        star_count = 0
        if bucket_count:
            star_count = bucket_count / bucket_scale
        print '%10.4f - %10.4f [%6d]: %s' % (bucket_min, bucket_max, bucket_count, '*' * star_count)
        

if __name__ == "__main__":
    parser = OptionParser()
    parser.usage = "cat data | %prog [options]"
    parser.add_option("-m", "--min", dest="min",
                        help="minimum value for graph")
    parser.add_option("-x", "--max", dest="max",
                        help="maximum value for graph")
    parser.add_option("-b", "--buckets", dest="buckets",
                        help="Number of buckets to use for the histogram")
    parser.add_option("--no-mvsd", dest="mvsd", action="store_false", default=True,
                        help="Dissable the calculation of Mean, Vairance and SD. (improves performance)")

    (options, args) = parser.parse_args()
    if sys.stdin.isatty():
        # if isatty() that means it's run without anything piped into it
        parser.print_usage()
        print "for more help use --help"
        sys.exit(1)
    histogram(load_stream(sys.stdin), options)

