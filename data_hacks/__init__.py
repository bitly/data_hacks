# -*- coding: utf-8 -*-
from __future__ import absolute_import
import sys
from data_hacks.bar_chart import run as bar_chart
from data_hacks import histogram as hist
from data_hacks.ninety_five_percent import run as ninety_five_percent
from data_hacks.sample import run as sample


class BarChartOpt(object):

    def __init__(
            self, agg_value_key=False, agg_key_value=False, sort_keys=True,
            sort_values=False, reverse_sort=False, numeric_sort=False,
            percentage=False, dot="∎"):
        self.agg_value_key = agg_value_key
        self.agg_key_value = agg_key_value
        self.sort_keys = sort_keys
        self.sort_values = sort_values
        self.reverse_sort = reverse_sort
        self.numeric_sort = numeric_sort
        self.percentage = percentage
        self.dot = dot


class HistogramOpt(object):

    def __init__(
            self, agg_value_key=False, agg_key_value=False, min=None,
            max=None, buckets=None, logscale=False, custbuckets=None,
            mvsd=True, format="%10.4f", percentage=False, dot="∎"):
        self.agg_value_key = agg_value_key
        self.agg_key_value = agg_key_value
        self.min = min
        self.max = max
        self.buckets = buckets
        self.logscale = logscale
        self.custbuckets = custbuckets
        self.mvsd = mvsd
        self.format = format
        self.percentage = percentage
        self.dot = dot


def histogram(stream, options, output=sys.stdout):
    hist.histogram(hist.load_stream(
        stream, options.agg_value_key, options.agg_key_value), options, output)
