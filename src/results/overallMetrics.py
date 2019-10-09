# overallMetrics.py
# Functions that calculate optimal weightings based on maximizing
# and constraints

import os, sys
import pandas as pd
import datetime
import math

parent_dir = os.path.dirname(os.path.dirname (os.path.abspath (__file__)))

sys.path.append(parent_dir + '/perf_metrics')

from calcPerformanceMetrics import getMaxDrawdown, getAnnualReturn 
from calcPerformanceMetrics import getWorstNDays, calcMonthlySharpe
from calcPerformanceMetrics import getAllTimeStats
from calcPerformanceMetrics import getMonthlyAnnualReturns
from calcPerformanceMetrics import plotReturns

from assignWeights import assignWeights


def getWeightsDict (file_series):

    outfile_dir = file_series['output directory']
    
    weights_file = outfile_dir + file_series['optimal weights file']

    weights_series = pd.read_csv(weights_file, index_col=0,
                                 header=None, squeeze=True)

    weights_dict = weights_series.to_dict()

    return weights_dict


def calcWeightedReturnsDF (returns_df, weights_dict):

    weighted_df = assignWeights(returns_df, weights_dict)

    cols = weighted_df.columns.tolist()

    # make Date the first column
    if cols[0] != 'Date':
        date_index = cols.index('Date')
        if date_index < 0:
            print ("No date in returns file - exiting")
            exit()
        cols = ['Date'] + cols
        cols.pop(date_index+1)
        
    weighted_df = weighted_df[cols]

    return weighted_df

# Summary stats for the returns
def outputStatsDict(weighted_df, file_series):

    stats_dict = {}

    n = 5  # worst n days

    max_DD, ann_ret = getMaxDrawdown(weighted_df), getAnnualReturn (weighted_df)
    worst_n = getWorstNDays(weighted_df, n)

    mo_sharpe = calcMonthlySharpe(weighted_df)

    stats_dict['Annual Return'] = float(ann_ret)
    stats_dict['Max Drawdown'] = float(max_DD)
    stats_dict['Worst Day'] = float(getWorstNDays(weighted_df, 1))
    stats_dict['Worst ' + str(n) + ' Days'] = float(worst_n)
    stats_dict['Monthly Sharpe'] = float(mo_sharpe)
    stats_dict['Annual Sharpe'] = math.sqrt(12) * mo_sharpe

    outfile_dir = file_series['output directory']

    outfile_name = file_series['summary file']

    stats_series = pd.Series(stats_dict)

    stats_series.to_csv (outfile_dir + outfile_name, sep='\t',
                         float_format = '%.4f', header=False)


def printOverallMetrics (returns_df, weights_dict, file_series):

    outfile_dir = file_series['output directory']

    outfile_suffix = file_series['returns file suffix']

    weighted_df = calcWeightedReturnsDF (returns_df, weights_dict)
    
    weighted_df.to_csv (outfile_dir + 'Daily' + outfile_suffix, index=False,
                        float_format = '%.4f')

    outputStatsDict(weighted_df, file_series)
    
    month_series, ann_series = getMonthlyAnnualReturns (weighted_df)

    month_series.to_csv (outfile_dir + 'Monthly' + outfile_suffix,
                         float_format = '%.4f', header=False)
    
    ann_series.to_csv (outfile_dir + 'Annual' + outfile_suffix,
                       float_format = '%.4f', header=False)

    plotReturns (weighted_df, ret_field = 'Daily Return',
                 output_dir = outfile_dir)

    
def outputOverallMetrics (file_series):

    weights_dict = getWeightsDict(file_series)

    returns_df = pd.read_hdf(file_series['model return file'])
    
    printOverallMetrics (returns_df, weights_dict, file_series)

    



    
