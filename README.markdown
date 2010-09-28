data_hacks
========

Command line utilities for data analysis

histogram
=========

A utility that parses input data points and outputs a text histogram

Example:

    $ cat /tmp/data | histogram.py
    # NumSamples = 29; Max = 10.00; Min = 1.00
    # Mean = 4.379310; Variance = 5.131986; SD = 2.265389
    # each * represents a count of 1
        1.0000 -     1.9000 [     1]: *
        1.9000 -     2.8000 [     5]: *****
        2.8000 -     3.7000 [     8]: ********
        3.7000 -     4.6000 [     3]: ***
        4.6000 -     5.5000 [     4]: ****
        5.5000 -     6.4000 [     2]: **
        6.4000 -     7.3000 [     3]: ***
        7.3000 -     8.2000 [     1]: *
        8.2000 -     9.1000 [     1]: *
        9.1000 -    10.0000 [     1]: *

nintey_five_percent
===================

A utility script that takes a stream of decimal values and outputs the 95% time.

This is useful for finding the 95% response time from access logs.

Example:

    $ cat access.log | awk '{print $NF}' | nintey_five_percent.py
    
Installation
============

Installing from source:

pip install -e git://github.com/bitly/data_hacks.git#egg=data_hacks
