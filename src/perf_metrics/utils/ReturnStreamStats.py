# ReturnStreamStats.py
# Takes as input dataframe of dates, daily returns, and leverage
# Outputs multiple metrics describing the performance of the return stream

import os, sys
import pandas as pd

from .Drawdown import drawdownStats

from .transposeDescribeStats import transposeDescribeStats

def calcMoAnnReturns (returns_df):

    returns_df.index = returns_df['Date']

    ret_series = returns_df['Daily Return']

    tframe_dict = {'M':'Monthly', 'Y':'Annual'}

    series_dict = {}

    for tframe in tframe_dict:
         series_dict[tframe_dict[tframe]] = ret_series.groupby(pd.Grouper(freq=tframe)).sum()

    return series_dict['Monthly'], series_dict['Annual']

    

# Daily, monthly, annual return streams
def timePeriodStats (returns_df):
    returns_df.index = returns_df['Date']

    ret_series = returns_df['Daily Return']

    tframe_dict = {'D':'Daily', 'M':'Monthly', 'Y':'Annual'}

    time_df_list = []

    for tframe in tframe_dict:
        time_df = transposeDescribeStats(ret_series.groupby
                                         (pd.Grouper(freq=tframe)).sum(),
                                              tframe_dict[tframe])
        time_df_list.append(time_df)
    
    time_stats_df = pd.concat(time_df_list, axis=0)

    return time_stats_df



def hitRatioCalc (returns_df):

    returns_df.index = returns_df['Date']

    ret_series = returns_df['Daily Return']

    daily_series = ret_series.groupby (pd.Grouper(freq='D')).sum()

    daily_series = daily_series.sort_values()

    best_ret_avg, worst_ret_avg = daily_series.tail().mean(), daily_series.head().mean()

    pos_days = daily_series[daily_series > 0].count()
    neg_days = daily_series[daily_series < 0].count()

    hit_ratio = best_ret_avg / worst_ret_avg * -1 * pos_days / neg_days

    return hit_ratio

def calcWorstNDays (returns_df, worst_num_days):

    worst_n_days_ret = 0.0
    for i in range(1, worst_num_days + 1):
        worst_i_days_ret = (returns_df['Daily Return'].rolling(i).sum()).min()
        worst_n_days_ret = min([worst_i_days_ret, worst_n_days_ret])

    return worst_n_days_ret

def calcLeverageStats (returns_df, long_col_name = 'Long Trade Size',
                       short_col_name = 'Short Trade Size'):
    max_long = returns_df[long_col_name].max()

    max_short = returns_df[short_col_name].min()

    returns_df['Net Leverage'] = (returns_df[long_col_name] +
                                  returns_df[short_col_name])

    returns_df['Total Leverage'] = (returns_df[long_col_name] -
                                  returns_df[short_col_name])

    max_net, min_net = returns_df['Net Leverage'].max(), returns_df['Net Leverage'].min()

    max_total = returns_df['Total Leverage'].max()

    return max_net, min_net, max_total    

def returnStreamStats (returns_df, worst_num_days=10):
    col_list = ['Date', 'Daily Return', 'Long Trade Size',
                'Short Trade Size']

    for col in col_list:
        if col not in returns_df.columns:
            print (col + " not in dataframe - cannot compute")
            exit()

    time_stats_df = timePeriodStats (returns_df) # Daily,monthly, annual stats

    drawdown_df = drawdownStats (returns_df)

    hit_ratio = hitRatioCalc (returns_df)

    worst_n_days_ret = calcWorstNDays (returns_df, worst_num_days)

    return time_stats_df, drawdown_df, hit_ratio, worst_n_days_ret

'''    
datafile = 'TestData/Test2.h5'
df = pd.read_hdf(datafile)
returnStreamStats(df)
'''
