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

    $ cat /tmp/data | histogram.py --percentage --max=1000 --min=0
    # NumSamples = 60; Min = 0.00; Max = 1000.00
    # 1 value outside of min/max
    # Mean = 332.666667; Variance = 471056.055556; SD = 686.335236; Median 191.000000
    # each ∎ represents a count of 1
        0.0000 -   100.0000 [    28]: ∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎ (46.67%)
      100.0000 -   200.0000 [     2]: ∎∎ (3.33%)
      200.0000 -   300.0000 [     2]: ∎∎ (3.33%)
      300.0000 -   400.0000 [     8]: ∎∎∎∎∎∎∎∎ (13.33%)
      400.0000 -   500.0000 [     8]: ∎∎∎∎∎∎∎∎ (13.33%)
      500.0000 -   600.0000 [     7]: ∎∎∎∎∎∎∎ (11.67%)
      600.0000 -   700.0000 [     3]: ∎∎∎ (5.00%)
      700.0000 -   800.0000 [     0]:  (0.00%)
      800.0000 -   900.0000 [     1]: ∎ (1.67%)
      900.0000 -  1000.0000 [     0]:  (0.00%)

With logarithmic scale

    $ printf 'import random\nfor i in range(1000):\n print random.randint(0,10000)'|\
        python -|./data_hacks/histogram.py -l
    # NumSamples = 1000; Min = 2.00; Max = 9993.00
    # Mean = 4951.757000; Variance = 8279390.995951; SD = 2877.393090; Median 4828.000000
    # each ∎ represents a count of 6
        2.0000 -    11.7664 [     3]:
       11.7664 -    31.2991 [     0]:
       31.2991 -    70.3646 [     5]:
       70.3646 -   148.4956 [    11]: ∎
      148.4956 -   304.7576 [    15]: ∎∎
      304.7576 -   617.2815 [    35]: ∎∎∎∎∎
      617.2815 -  1242.3294 [    51]: ∎∎∎∎∎∎∎∎
     1242.3294 -  2492.4252 [   128]: ∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎
     2492.4252 -  4992.6168 [   269]: ∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎
     4992.6168 -  9993.0000 [   483]: ∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎

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

    $ cat data | bar_chart.py
    # each ∎ represents a count of 1. total 63
    14:40 [    49] ∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎
    14:41 [    14] ∎∎∎∎∎∎∎∎∎∎∎∎∎∎

`bar_chart.py` and `histogram.py` also support ingesting pre-aggregated values. Simply provide a two column input of `count<whitespace>value` for `-a` or `value<whitespace>count` for `-A`:

    $ cat data | uniq -c | bar_chart.py -a

This is very convenient if you pull data out, say Hadoop or MySQL already aggregated.
