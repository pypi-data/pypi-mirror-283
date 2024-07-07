#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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
from decimal import Decimal
import math
import sys


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

def median(values):
    length = len(values)
    if length%2:
        median_indeces = [length//2]
    else:
        median_indeces = [length//2-1, length//2]

    values = sorted(values)
    return sum([values[i] for i in median_indeces]) / len(median_indeces)

def test_median():
    assert 6 == median([8,7,9,1,2,6,3]) # odd-sized list
    assert 4 == median([4,5,2,1,9,10]) # even-sized int list. (4+5)/2 = 4
    assert "4.50" == "%.2f" % median([4.0,5,2,1,9,10]) #even-sized float list. (4.0+5)/2 = 4.5


DEFAULT_graph_char = u'\u2592'
DEFAULT_display_empty_buckets = True

def histogram(stream, minimum=None, maximum=None, buckets=None, custbuckets=None, calc_msvd=True, graph_char=None, display_empty_buckets=None):
    """
    Loop over the stream and add each entry to the dataset, printing out at the end


    minimum: minimum value for graph
    maximum: maximum value for graph
    buckets: Number of buckets to use for the histogram
    custbuckets: Comma seperated list of bucket edges for the histogram
    calc_msvd: Calculate and display Mean, Variance and SD.
    graph_char: Character to display for counts in histogram/bar.
    display_empty_buckets: if False, do not show empty buckets in display.
    """
    if not stream:
        raise NotImplementedError('No suport for empty data stream')
    graph_char = graph_char or DEFAULT_graph_char
    if display_empty_buckets is None:
        display_empty_buckets = DEFAULT_display_empty_buckets
    if not minimum or not maximum:
        # glob the iterator here so we can do min/max on it
        data = list(stream)
    else:
        data = stream
    bucket_scale = 1

    if minimum is not None:
        min_v = Decimal(minimum)
    else:
        min_v = Decimal(min(data))
    if maximum is not None:
        max_v = Decimal(maximum)
    else:
        max_v = Decimal(max(data))

    if not max_v >= min_v:
        raise ValueError('max must be > min. max:%s min:%s' % (max_v, min_v))
    diff = max_v - min_v

    boundaries = []
    bucket_counts = []

    if custbuckets:
        bound = custbuckets.split(',')
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
        buckets = buckets or 10
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
        if calc_msvd:
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

    print("# NumSamples = %d; Min = %0.2f; Max = %0.2f" % (samples, min_v, max_v))
    if skipped:
        print("# %d value%s outside of min/max" % (skipped, skipped > 1 and 's' or ''))
    if calc_msvd:
        print("# Mean = %f; Variance = %f; SD = %f; Median %f" % (mvsd.mean(), mvsd.var(), mvsd.sd(), median(accepted_data)))
    print("# each %s represents a count of %d" % (graph_char, bucket_scale))
    bucket_min = min_v
    bucket_max = min_v
    for bucket in range(buckets):
        bucket_min = bucket_max
        bucket_max = boundaries[bucket]
        bucket_count = bucket_counts[bucket]
        star_count = 0
        if bucket_count:
            star_count = int(bucket_count / bucket_scale)
        if display_empty_buckets or bucket_count:
            print('%11.4f - %11.4f [%6d]: %s' % (bucket_min, bucket_max, bucket_count, graph_char * star_count))  # TODO dynamically calc length of max value and generate string format on the fly

