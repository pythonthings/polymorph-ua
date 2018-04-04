# Aggregated file for scoring advertisers on part-00000 data
# Variable portions marked by TODO

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math

# TODO
ADVERTISERS = pd.read_json("lookup/advertiser_id/map.json", lines=False)
SAMPLE = pd.read_json("./part-00000", lines=True)

# Standard scoring func
# Input score_func=lambda x: x to see un-modified results
def score_advertisers(table, score_func):
    click_counts = table[["advertiser_id", "c_cnt"]]
    clean_ccnt = click_counts.dropna()
    merged = pd.merge(clean_ccnt, ADVERTISERS)
    grouped = merged.groupby("advertiser_name")
    score_means = lambda x: score_func(np.mean(x))
    agg_scored = grouped.agg({'c_cnt': score_means})
    agg_scored = agg_scored.sort_values(by="c_cnt", ascending=False)
    return agg_scored


# Added wrapper option to add additional info to scoring_func without computing every time e.g. the mean
# See scoring_funcs.py for example wrapper functions
def score_advertisers_power(table, score_func=None, wrapper=None):
    if wrapper == None:
        wrapper = lambda t: lambda x: score_func(x, t)
    click_counts = table[["advertiser_id", "c_cnt"]]
    clean_ccnt = click_counts.dropna()
    merged = pd.merge(clean_ccnt, ADVERTISERS)
    grouped = merged.groupby("advertiser_name")
    new_score_func = wrapper(table)
    score_means = lambda x: new_score_func(np.mean(x))
    agg_scored = grouped.agg({'c_cnt': score_means})
    return agg_scored
