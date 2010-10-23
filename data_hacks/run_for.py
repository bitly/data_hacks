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
Pass through data for a specified amount of time

http://github.com/bitly/data_hacks
"""

import time
import sys
import os

def getruntime(arg):
    if not arg:
        return
    suffix = arg[-1]
    base = int(arg[:-1])
    if suffix == "s":
        return base
    elif suffix == "m":
        return base * 60
    elif suffix == "h":
        return base * 60 * 60
    elif suffix == "d":
        return base * 60 * 60 * 24
    else:
        print >>sys.stderr, "invalid time suffix %r. must be one of s,m,h,d" % arg

def run(runtime):
    end = time.time() + runtime
    for line in sys.stdin:
        sys.stdout.write(line)
        if time.time() > end:
            return

if __name__ == "__main__":
    usage = "Usage: tail -f access.log | %s [time] | ..." % os.path.basename(sys.argv[0])
    help = "time can be in the format 10s, 10m, 10h, etc"
    if sys.stdin.isatty():
        print usage
        print help
        sys.exit(1)

    runtime = getruntime(sys.argv[-1])
    if not runtime:
        print usage
        sys.exit(1)
    run(runtime)
