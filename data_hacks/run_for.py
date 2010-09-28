#!/bin/env python
"""
Pass through data for a specified amount of time

created by Jehiah Czebotar 2010-09-27
Copyright (c) 2010 bit.ly. All rights reserved.

http://github.com/bitly/data_hacks
"""
import time
import sys

def getruntime(arg):
    if not arg:
        return
    suffix = arg[-1]
    base = int(arg[:-1])
    if suffix == "s":
        return base
    elif suffix == "h":
        return base * 60
    elif suffix == "d":
        return base * 60 * 24
    else:
        print >>sys.stderr, "invalid time suffix %r" % arg

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
    runtime = getruntime(sys.argv[-1])
    if not runtime:
        print >>sys.stderr, "usage: tail -f access.log | run_for.py 10s | wc -l"
        sys.exit(1)
    run(runtime)