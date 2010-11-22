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
Generate an ascii bar chart for input data

http://github.com/bitly/data_hacks
"""
import sys
from collections import defaultdict
from optparse import OptionParser

def load_stream(input_stream):
    for line in input_stream:
        clean_line = line.strip()
        if not clean_line:
            # skip empty lines (ie: newlines)
            continue
        if clean_line[0] in ['"', "'"]:
            clean_line = clean_line.strip('"').strip("'")
        if clean_line:
            yield clean_line

def run(input_stream, options):
    data = defaultdict(lambda:0)
    for row in input_stream:
        data[row]+=1
    
    if not data:
        print "Error: no data"
        sys.exit(1)
    
    max_length = max([len(key) for key in data.keys()])
    max_length = min(max_length, 50)
    value_characters = 80 - max_length
    max_value = max(data.values())
    scale = int(float(max_value) / value_characters)
    scale = max(1, scale)
    
    print "# each * represents a count of %d" % scale
    
    if options.sort_values:
        # sort by values
        data = [[value,key] for key,value in data.items()]
        if options.reverse_sort:
            data.sort(reverse=True)
        else:
            data.sort()
    else:
        data = [[key,value] for key,value in data.items()]
        data.sort(reverse=options.reverse_sort)
        data = [[value, key] for key,value in data]
    format = "%" + str(max_length) + "s [%6d] %s"
    for value,key in data:
        print format % (key[:max_length], value, (value / scale) * "*")

if __name__ == "__main__":
    parser = OptionParser()
    parser.usage = "cat data | %prog [options]"
    parser.add_option("-k", "--sort-keys", dest="sort_keys", default=True, action="store_true",
                        help="sort by the key [default]")
    parser.add_option("-v", "--sort-values", dest="sort_values", default=False, action="store_true",
                        help="sort by the frequence")
    parser.add_option("-r", "--reverse-sort", dest="reverse_sort", default=False, action="store_true",
                        help="reverse the sort")
    
    (options, args) = parser.parse_args()
    
    if sys.stdin.isatty():
        parser.print_usage()
        print "for more help use --help"
        sys.exit(1)
    run(load_stream(sys.stdin), options)

