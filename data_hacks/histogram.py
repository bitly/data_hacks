#!/bin/env python
"""
Generate a text format histogram 

This is a loose port to python of the Perl version at
http://www.pandamatak.com/people/anand/xfer/histo

created by Jehiah Czebotar 2010-09-27
Copyright (c) 2010 bit.ly. All rights reserved.

http://github.com/bitly/data_hacks

"""

import sys
from decimal import Decimal
import math

class MVSD(object):
    """ A class that calculates a running Mean / Variance / Standard Deviation"""
    def __init__(self):
        self.is_started = False
        self.ss = Decimal(0) # (running) sum of square deviations from mean
        self.m = Decimal(0) # (running) mean
        self.total_w = Decimal(0) # weight of items seen
        
    def add(self, x, w=1):
        x = x * Decimal('1.0')
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
    while True:
        line = input_stream.readline()
        if not line:
            break
        line = line.strip()
        if not line:
            # skip empty lines (ie: newlines)
            continue
        try:
            yield Decimal(line)
        except:
            try:
                line = line.strip('"').strip("'")
                yield Decimal(line)
            except:
                print >>sys.stderr, "invalid line %r" % line

def histogram(stream):
    # we can't iterate on stream because we need to get min/max first and then put it into buckets
    data = list(stream)
    buckets = 10
    bucket_scale = 1
    
    min_v = min(data)
    max_v = max(data)
    diff = max_v - min_v
    step = diff / buckets
    bucket_counts = [0 for x in range(buckets)]
    boundaries = []
    for x in range(buckets):
        boundaries.append(min_v + (step * (x + 1)))
    
    mvsd = MVSD()
    for value in data:
        mvsd.add(value)
        # find the bucket this goes in
        for bucket_postion, boundary in enumerate(boundaries):
            if value <= boundary:
                bucket_counts[bucket_postion] +=1
                break
    
    # auto-pick the bucket size
    if max(bucket_counts) > 75:
        bucket_scale = int(max(bucket_counts) / 75)
    
    print "# NumSamples = %d; Max = %0.2f; Min = %0.2f" % (len(data), max_v, min_v)
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
    histogram(load_stream(sys.stdin))
