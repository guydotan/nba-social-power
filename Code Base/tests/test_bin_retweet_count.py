'''
     File name: test_bin_retweet_count.py
     Author: Guy Dotan
     Date: 03/13/2019
     Course: UCLA Stats 404
     Description: HW5b - Unit testing for HW5a.
'''


"""Module for unit testing of 'bin_retweet_count' functions."""

import pytest
from hw5a_nba_twitter_gd import bin_retweet_count

def test_bin_retweet_count():
    """Unit test to showcase functionality of binning retweet counts into one 
       of four larger buckets.
    """
    expected_bin = "50-150"
    output_bin = bin_retweet_count(146.6)
    assert output_bin == expected_bin, """Should show that bins are the same"""


def test_bin_retweet_count_edge():
    """Unit test to showcase edge behavior that a retweet count on the border
       of two buckes does not get assigned to the both.
    """
    expected_bin = "10-50"
    incorrect_bin = "<10"
    output_bin = bin_retweet_count(10.0)
    assert (output_bin == expected_bin) & (output_bin != incorrect_bin),\
    """Should show that edge case bins into larger bucket"""
    