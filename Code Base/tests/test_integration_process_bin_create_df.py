'''
     File name: test_integration_process_bin_create_df.py
     Author: Guy Dotan
     Date: 03/13/2019
     Course: UCLA Stats 404
     Description: HW5b - Integration testing for HW5a.
'''

"""Module for unit testing of 'bin_retweet_count', 'process_data', and 
   'create_dataframe' functions.
"""

import pytest
from hw5a_nba_twitter_gd import bin_retweet_count, process_data, create_dataframe

def test_integration_process_data_bin_retweets_create_df():
    """Integration test to check the processes of determinig the correct bin 
       then processing the data and leaving only the relevant variables.
    """
    
    expected_bin = "150+"
    actual_retweets = 2893
    output_bin = bin_retweet_count(actual_retweets)
    column_list = ['AGE', 'W', 'SALARY_MILLIONS', 'WINS_RPM', 'ORPM',
                   'DRPM', 'PIE', 'TWITTER_RETWEET_COUNT', 'TWEET_CAT']
    input_array = [28, 65, 12.11, 18.8, 7.27, 0.14, 15.1, \
                   actual_retweets, output_bin]
    input_df = create_dataframe(column_list, input_array)
    output_df = process_data(input_df)
    assert (expected_bin == output_bin) & (len(output_df.columns) == 8)
    """Should confirm the following...
       (1) The retweets were binned into the correct bucket (150+)
       (2) A correcet dataframe was created with the columns and values
       (3) Dataframe was parsed correctly and only the 8 relevant columns remain
    """
