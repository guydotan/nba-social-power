'''
     File name: hw5a_nba_twitter_gd.py
     Author: Guy Dotan
     Date: 03/13/2019
     Course: UCLA Stats 404
     Description: HW #5a. Final model, I/O, and code styling.
'''

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier


def bin_retweet_count(retweets: float) -> str:
    """Fcn to bin retweet counts via if-else statements, rather than cut()
       function, to compare performance of computation in Class 5.

       Arguments:
           - retweets: number of retweets in millions

       Returns:
           - categorical variable grouping retweets into one of four buckets
    """
    if retweets < 10:
        retweet_cat_group = "<10"
    elif (retweets >= 10) & (retweets < 50):
        retweet_cat_group = "10-50"
    elif (retweets >= 50) & (retweets < 150):
        retweet_cat_group = "50-150"
    else:
        retweet_cat_group = "150+"

    return retweet_cat_group


def process_data(input_dat):
    """Fcn to process dataset, clean data and handle null values

       Arguments:
           - input_dat: dataframe that needs to be cleaned

       Returns:
           - cleaned dataframe
    """

    # remove rows with NULL value for outcome variable
    output_dat = input_dat[np.isfinite(input_dat['TWITTER_RETWEET_COUNT'])]

    # select relevant features for model
    relevant_vars = ['AGE', 'W', 'SALARY_MILLIONS', 'WINS_RPM',
                     'ORPM', 'DRPM', 'PIE', "TWEET_CAT"]

    output_dat = output_dat[relevant_vars]
    return output_dat


def train_test(dat, size, strat):
    """Fcn to bin retweet counts via if-else statements, rather than cut()
       function, to compare performance of computation in Class 5.

       Arguments:
           - dat: dataset that needs to be split
           - size: ratio for testing set (in decimal form)
           - strat: class weighting method

       Returns:
           - training set dataframe and testing set dataframe
    """
    train_set, test_set = train_test_split(dat,
                                           test_size=size,
                                           random_state=2019,
                                           stratify=dat[strat])
    return [train_set, test_set]


def rf_model_run(num_trees, features, outcome):
    """Fcn to build Random forest model that accepts params for number of
       trees, a dataset of feature inputs, and the output variable.2`

       Arguments:
           - num_trees: number of trees used in random forest
           - features: feature set utilized
           - outcome: target predictive variable

       Returns:
           - completed random forest model object type
    """
    rf_res = RandomForestClassifier(n_estimators=num_trees,
                                    min_samples_leaf=5,
                                    oob_score=True,
                                    random_state=2019,
                                    class_weight='balanced',
                                    verbose=0)
    rf_res.fit(features, outcome)
    return rf_res


def rf_pred_res(forest, features):
    """Fcn to create list of prediction result strings generated from rf model

       Arguments:
           - forest: random forest model
           - features: feature set inputs into model

       Returns:
           - list of prediction results for retweet count bucket (as strings)
    """
    results = forest.predict(features)
    res = [str(i) for i in results]
    return res


def testing_prompts():
    """Fcn to begin testing prompt where user inputs values for all necessary
       features for the model which are then inserted into the model.

       Returns:
           - series of prompts enter in necessary features to test model
    """
    print('Player AGE:')
    input_age = float(input())

    print('Player Teams Wins:')
    input_w = float(input())

    print('Player Salary (millions):')
    input_salary = float(input())

    print('Player Wins-RPM:')
    input_wins_rpm = float(input())

    print('Player ORPM:')
    input_orpm = float(input())

    print('Player DRPM:')
    input_drpm = float(input())

    print('Player PIE:')
    input_pie = float(input())

    return [[input_age], [input_w], [input_salary], [input_wins_rpm],
            [input_orpm], [input_drpm], [input_pie]]


def create_dataframe(col_names, values):
    """Fcn to turn inputs into dataframe to plug into the model

       Arugments:
           - inputs: array of inputs
       Returns:
           - dataframe ready to parse by model
    """
    # taken from https://www.tutorialspoint.com/How-to-create-
    # Python-dictionary-from-list-of-keys-and-values
    fnc_df_dict = dict(zip(col_names, values))
    fnc_df = pd.DataFrame(fnc_df_dict, index=[0])
    return fnc_df


if __name__ == '__main__':
    PATH = ('https://s3-us-west-1.amazonaws.com/uclastats404-project/'
            'nba_2017_players_with_salary_wiki_twitter.csv')
    DF = pd.read_csv(PATH)

    # prevent pandas warning message for SettingWithCopyWarning
    # taken from https://stackoverflow.com/questions/20625582/
        # how-to-deal-with-settingwithcopywarning-in-pandas
    pd.options.mode.chained_assignment = None

    # apply category label for our output variable
    DF['TWEET_CAT'] = DF['TWITTER_RETWEET_COUNT'].\
        apply(lambda x: bin_retweet_count(x))

    NBA = process_data(DF)

    # establish trainin and testing sets
    DF_TRAIN, DF_VALID = train_test(NBA, 0.25, 'TWEET_CAT')

    X = DF_TRAIN.drop(columns=['TWEET_CAT'])
    Y = DF_TRAIN['TWEET_CAT']

    # build rf model with desired num of trees
    RF_MODEL = rf_model_run(1500, X, Y)

    # establish training and testing sets
    X_VALID = DF_VALID.drop(columns=['TWEET_CAT'])
    Y_VALID = DF_VALID['TWEET_CAT']

    RF_PREDS = rf_pred_res(RF_MODEL, X_VALID)

    FEATURE_NAMES = ['AGE', 'W', 'SALARY_MILLIONS', 'WINS_RPM',
                     'ORPM', 'DRPM', 'PIE']
    # process inputs into array of feature values
    FEATURE_VALUES = testing_prompts()

    TEST_DF = create_dataframe(FEATURE_NAMES, FEATURE_VALUES)
    TEST_RES = rf_pred_res(RF_MODEL, TEST_DF)
    print('Player retweet count prediction is \"' + TEST_RES[0] + '\" million')
    