#!/usr/bin/env python
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

def median(values):
    length = len(values)
    if length%2:
        median_indeces = [length/2]
    else:
        median_indeces = [length/2-1, length/2]

    values = sorted(values)
    return sum([values[i] for i in median_indeces]) / len(median_indeces)

def test_median():
    assert 6 == median([8,7,9,1,2,6,3]) # odd-sized list
    assert 4 == median([4,5,2,1,9,10]) # even-sized int list. (4+5)/2 = 4
    assert "4.50" == "%.2f" % median([4.0,5,2,1,9,10]) #even-sized float list. (4.0+5)/2 = 4.5

#
# Inverse normal, taken lovingly from:
#     http://home.online.no/~pjacklam/notes/invnorm/impl/field/ltqnorm.txt
#
def ltqnorm( p ):
    """
    Modified from the author's original perl code (original comments follow below)
    by dfield@yahoo-inc.com.  May 3, 2004.

    Lower tail quantile for standard normal distribution function.

    This function returns an approximation of the inverse cumulative
    standard normal distribution function.  I.e., given P, it returns
    an approximation to the X satisfying P = Pr{Z <= X} where Z is a
    random variable from the standard normal distribution.

    The algorithm uses a minimax approximation by rational functions
    and the result has a relative error whose absolute value is less
    than 1.15e-9.

    Author:      Peter John Acklam
    Time-stamp:  2000-07-19 18:26:14
    E-mail:      pjacklam@online.no
    WWW URL:     http://home.online.no/~pjacklam
    """

    if p <= 0 or p >= 1:
        # The original perl code exits here, we'll throw an exception instead
        raise ValueError( "Argument to ltqnorm %f must be in open interval (0,1)" % p )

    # Coefficients in rational approximations.
    a = (-3.969683028665376e+01,  2.209460984245205e+02, \
         -2.759285104469687e+02,  1.383577518672690e+02, \
         -3.066479806614716e+01,  2.506628277459239e+00)
    b = (-5.447609879822406e+01,  1.615858368580409e+02, \
         -1.556989798598866e+02,  6.680131188771972e+01, \
         -1.328068155288572e+01 )
    c = (-7.784894002430293e-03, -3.223964580411365e-01, \
         -2.400758277161838e+00, -2.549732539343734e+00, \
          4.374664141464968e+00,  2.938163982698783e+00)
    d = ( 7.784695709041462e-03,  3.224671290700398e-01, \
          2.445134137142996e+00,  3.754408661907416e+00)

    # Define break-points.
    plow  = 0.02425
    phigh = 1 - plow

    # Rational approximation for lower region:
    if p < plow:
       q  = math.sqrt(-2*math.log(p))
       return (((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / \
               ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)

    # Rational approximation for upper region:
    if phigh < p:
       q  = math.sqrt(-2*math.log(1-p))
       return -(((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / \
                ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)

    # Rational approximation for central region:
    q = p - 0.5
    r = q*q
    return (((((a[0]*r+a[1])*r+a[2])*r+a[3])*r+a[4])*r+a[5])*q / \
           (((((b[0]*r+b[1])*r+b[2])*r+b[3])*r+b[4])*r+1)

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

    if not max_v > min_v:
        raise ValueError('max must be > min. max:%s min:%s' % (max_v, min_v))
    diff = max_v - min_v

    boundaries = []
    bucket_counts = []
    buckets = 0

    if options.custbuckets:
        bound = options.custbuckets.split(',')
        bound_sort = sorted(map(Decimal, bound))

        # if the last value is smaller than the maximum, replace it
        if bound_sort[-1] < max_v:
            bound_sort[-1] = max_v
        
        # iterate through the sorted list and append to boundaries
        for x in bound_sort:
            if x >= min_v and x <= max_v:
                boundaries.append(x)
            elif x >= max_v:
                boundaries.append(max_v)
                break

        # beware: the min_v is not included in the boundaries, so no need to do a -1!
        bucket_counts = [0 for x in range(len(boundaries))]
        buckets = len(boundaries)
    else:
        buckets = options.buckets and int(options.buckets) or 10
        if buckets <= 0:
            raise ValueError('# of buckets must be > 0')
        step = diff / buckets
        bucket_counts = [0 for x in range(buckets)]
        for x in range(buckets):
            boundaries.append(min_v + (step * (x + 1)))

    skipped = 0
    samples = 0
    mvsd = MVSD()
    accepted_data = []
    for value in data:
        samples +=1
        if options.mvsd:
            mvsd.add(value)
            accepted_data.append(value)
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
        mean_string = "%f" % mvsd.mean()
        if options.confidence and 0 < float(options.confidence) < 1:
            # Convert to float and adjust so it is the correct value for a half
            # interval.
            confidence = (float(options.confidence) + 1.0)/2
            if len(accepted_data) >= 30:
                interval_width = ltqnorm(confidence)
                interval_width *= mvsd.sd() / math.sqrt(samples)
            # TODO(awreece) Students t distribution if <30 samples.
            interval_width = Decimal(interval_width)
            mean_string = "%f (+/- %f)" % (mvsd.mean(), interval_width)

        print "# Mean = %s; Variance = %f; SD = %f; Median %f" % (mean_string, mvsd.var(), mvsd.sd(), median(accepted_data))
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
    parser.add_option("-B", "--custom-buckets", dest="custbuckets",
                        help="Comma seperated list of bucket edges for the histogram")
    parser.add_option("--no-mvsd", dest="mvsd", action="store_false", default=True,
                        help="Dissable the calculation of Mean, Vairance and SD. (improves performance)")
    parser.add_option("-c", "--confidence", dest="confidence",
                        help="Confidence interval width (set to 0 or don't specify for no interval). Requires msvd.")

    (options, args) = parser.parse_args()
    if sys.stdin.isatty():
        # if isatty() that means it's run without anything piped into it
        parser.print_usage()
        print "for more help use --help"
        sys.exit(1)
    histogram(load_stream(sys.stdin), options)

