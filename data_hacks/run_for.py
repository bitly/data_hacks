#!/bin/env python
"""
Pass through data for a specified amount of time

created by Jehiah Czebotar 2010-09-27
Copyright (c) 2010 bit.ly. All rights reserved.

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
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        sys.stdout.write(line)
        if time.time() > end:
            return

if __name__ == "__main__":
    usage = "Usage: tail -f access.log | %(prog)s [time] | ..." % os.path.basename(sys.argv[0])
    help = "time can be in the format 10s 10m 10h etc"
    if sys.stdin.isatty():
        print usage
        print help
        sys.exit(1)

    runtime = getruntime(sys.argv[-1])
    if not runtime:
        print usage
        sys.exit(1)
    run(runtime)