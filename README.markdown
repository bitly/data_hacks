data_hacks
==========

Command line utilities for data analysis

Installing: `pip install data_hacks`

Installing from github `pip install -e git://github.com/bitly/data_hacks.git#egg=data_hacks`

Installing from source `python setup.py install`

data_hacks are friendly. Ask them for usage information with `--help`

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

ninety_five_percent.py
----------------------

A utility script that takes a stream of decimal values and outputs the 95% time.

This is useful for finding the 95% response time from access logs.

Example (assuming response time is the last column in your access log):

    $ cat access.log | awk '{print $NF}' | ninety_five_percent.py
    
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

bar_chart.py
------------

Generate an ascii bar chart for input data (this is like a visualization of `uniq -c`)

    $ cat data | bar_chart.py --sort-keys
    # each * represents a count of 2
    19:0 [     1] 
    19:1 [    24] ************
    19:2 [     3] *
    19:3 [     9] ****
    19:4 [     5] **
    19:5 [    41] ********************
    20:0 [   115] *********************************************************
    20:1 [   181] ******************************************************************************************
    20:2 [   136] ********************************************************************
    20:3 [   155] *****************************************************************************
    20:4 [   150] ***************************************************************************
    20:5 [    79] ***************************************
    21:0 [    64] ********************************
    21:1 [     8] ****

bar_chart.py also supports aggregated values. Simply provide a two column text file, space seperated and run like so:

    $ cat ./data 
    1 1
    2 1
    3 11
    3 5
    4 5
    5 7
    5 8
    6 5
    6 1
    $ cat ./data | bar_chart.py -a
    # each * represents a count of 1
    1 [     1] *
    2 [     1] *
    3 [    16] ****************
    4 [     5] *****
    5 [    15] ***************
    6 [     6] ******

This is very convenient if you pull data out, say Hadoop or MySQL already aggregated.
