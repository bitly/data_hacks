data_hacks
==========

Command line utilities for data analysis

Installing: `pip install data_hacks`

Installing form github `pip install -e git://github.com/bitly/data_hacks.git#egg=data_hacks`

Installing from source `python setup.py install`

histogram.py
------------

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

nintey_five_percent.py
----------------------

A utility script that takes a stream of decimal values and outputs the 95% time.

This is useful for finding the 95% response time from access logs.

Example (assuming response time is the last column in your access log):

    $ cat access.log | awk '{print $NF}' | nintey_five_percent.py
    
sample.py
---------

Filter a stream to a random sub-sample of the stream

Example:

    $ cat access.log | sample.py 10% | post_process.py

run_for.py
----------

Pass through data for a specified amount of time

Example:

    $ tail -f access.log | run_for.py 10s | post_process.py
