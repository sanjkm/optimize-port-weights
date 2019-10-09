# calcPerformanceMetrics.py
# Separate functions for each relevant performance metric

import os, sys
import pandas as pd
import matplotlib.pyplot as plt
import datetime


from utils.ReturnStreamStats import timePeriodStats, calcWorstNDays, hitRatioCalc
from utils.ReturnStreamStats import calcLeverageStats, calcMoAnnReturns
from utils.Drawdown import drawdownStats


def getMaxDrawdown (returns_df):

    drawdown_df = drawdownStats (returns_df)

    return drawdown_df.loc[drawdown_df.index[-1], 'Max Drawdown']

def getAnnualReturn (returns_df):

    time_stats_df = timePeriodStats (returns_df) # Daily,monthly, annual stats

    return time_stats_df.loc[time_stats_df['Header'] == 'Annual',
                             'mean'].values[0]

def getMonthlyAnnualReturns (returns_df):

    monthly_series, ann_series = calcMoAnnReturns (returns_df)

    return monthly_series, ann_series

def getWorstNDays (returns_df, num_days):

    return calcWorstNDays (returns_df, num_days)

def calcMonthlySharpe (returns_df):

    time_stats_df = timePeriodStats (returns_df) # Daily,monthly, annual stats

    monthly_ret = time_stats_df.loc[time_stats_df['Header'] == 'Monthly',
                             'mean'].values[0]

    monthly_stdev = time_stats_df.loc[time_stats_df['Header'] == 'Monthly',
                             'std'].values[0]
    
    return monthly_ret / monthly_stdev

def getLeverageStats (returns_df):

    open_dict, intra_dict = {}, {}
    
    long_col_name = 'Long Open Trade Size'
    short_col_name = 'Short Open Trade Size'
    
    max_net, min_net, max_total = calcLeverageStats (returns_df,
                                                     long_col_name=long_col_name,
                                                     short_col_name=short_col_name)

    open_dict['max net'], open_dict['min net'] = max_net, min_net
    open_dict['max total'] = max_total

    long_col_name = 'Long Intraday Trade Size'
    short_col_name = 'Short Intraday Trade Size'

    max_net, min_net, max_total = calcLeverageStats (returns_df,
                                                     long_col_name=long_col_name,
                                                     short_col_name=short_col_name)

    intra_dict['max net'], intra_dict['min net'] = max_net, min_net
    intra_dict['max total'] = max_total

    return (max(open_dict['max net'], intra_dict['max net']),
            min(open_dict['min net'], intra_dict['min net']),
            max(open_dict['max total'], intra_dict['max total']))

def getAllTimeStats (returns_df):

    time_stats_df = timePeriodStats (returns_df) # Daily,monthly, annual stats

    return time_stats_df


def plotReturns (returns_df, ret_field = 'Daily Return',
                 output_dir = 'results/'):

    plot_df = returns_df[['Date', ret_field]]

    min_date = plot_df['Date'].min()

    # add a start date with initial capital
    start_date = min_date - datetime.timedelta(days=1)
    init_cap, init_ret = 1000, 0.0

    init_df = pd.DataFrame()
    init_df['Date'], init_df[ret_field] = [start_date], [0.0]

    plot_df = pd.concat([init_df, plot_df])

    plot_df['1 + Ret'] = 1 + plot_df[ret_field]

    plot_df['Cumulative Return'] = plot_df['1 + Ret'].cumprod()

    plot_df['Capital'] = init_cap * plot_df['Cumulative Return']

    plot_df.index = plot_df['Date']

    plot_df = plot_df.filter(['Capital'])
    plot_df.plot()
    plt.show()
    plot_df.plot()
    plt.savefig(output_dir + 'ReturnsPlot.png')
    plt.close()
    

    

    
