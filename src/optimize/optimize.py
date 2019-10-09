# optimize.py
# Functions that calculate optimal weightings based on maximizing
# and constraints

import os, sys
import pandas as pd
import numpy as np
import datetime
from scipy.optimize import minimize, Bounds

parent_dir = os.path.dirname(os.path.dirname (os.path.abspath (__file__)))

sys.path.append(parent_dir + '/perf_metrics')

from calcPerformanceMetrics import getMaxDrawdown, getAnnualReturn 
from calcPerformanceMetrics import getWorstNDays, calcMonthlySharpe
from calcPerformanceMetrics import getAllTimeStats

from assignWeights import assignWeights

# Value that we want to maximize (sign = -1 --> minimizing)
# Optimizer runs to minimize, so always set sign to -1
# Have included other potential choices for optimization in the comments below
def maximizeFunction (returns_df, sign=-1.0):

    # return sign * calcMonthlySharpe (returns_df)

    return sign * getAnnualReturn (returns_df) / getMaxDrawdown (returns_df)
    
    # n = 5
    # sign = 1.0
    # return sign * getAnnualReturn (returns_df) / getWorstNDays (returns_df, n)

# Inequality constraints on the optimization
# Using the min annual return constraint from parameters,
# could add others
def constraintsDict (model_ret_dict, ann_ret_constraint):

    MONTHS_IN_YEAR = 12
    
    ret_list = [model_ret_dict[model]
                for model in sorted(model_ret_dict)]

    ineq_cons = {'type': 'ineq',
                 'fun' : lambda x: (np.array(np.dot(x, ret_list) -
                                             ann_ret_constraint/
                                             MONTHS_IN_YEAR))}
    return ineq_cons


def callbackFunc(X):
    # print X
    pass

def calcTotalMonths (df):
    min_date, max_date = df['Date'].min().date(), df['Date'].max().date()

    num_years = (max_date.year - min_date.year)

    num_months = (max_date.month - min_date.month)

    months_in_year = 12

    return (months_in_year * num_years + num_months + 1)

# Outputs dictionary mapping model name to its average monthly return
# Used for the inequality constraint, compelling avg overall return
# across models greater than inputted parameter
def calcModelMonthlyReturn (returns_df, model_list):

    total_months = calcTotalMonths (returns_df)

    model_dict = {}

    for model in model_list:

        df = returns_df.loc[returns_df['Model'] == model]

        if len(df) == 0:
            model_dict[model] = 0.0
            continue

        time_stats_df = getAllTimeStats(df)

        num_mos = time_stats_df.loc[time_stats_df['Header']=='Monthly',
                                    'count'].values[0]

        mo_ret = time_stats_df.loc[time_stats_df['Header']=='Monthly',
                                    'mean'].values[0]
        
        model_dict[model] = mo_ret * num_mos / total_months

    return model_dict


# removes data past cutoff date from the dataframe
# this allows optimization over a 'test data set'
def holdBackData (df, cutoff_date):

    return df.loc[df['Date'] <= cutoff_date]


# this takes the min weights and max weight for each model,
# compiles them in a list, as well as avg of min and max
def weightBoundsList (model_dict):

    args_list = []

    avg_wt_list = []
    
    for model in sorted(model_dict):

        model_param_dict = model_dict[model]

        model_args = [model_param_dict['Min Weight'],
                      model_param_dict['Max Weight']]

        model_avg = sum(model_args) / len(model_args)

        args_list.append(model_args)

        avg_wt_list.append(model_avg)

    return args_list, avg_wt_list

def outputWeightsToFile (weight_array, models_list, output_file):
    
    wt_list = list(weight_array)
        
    weights_series = pd.Series({models_list[i]:wt_list[i]
                                for i in range(len(wt_list))})

    weights_series.to_csv (output_file, float_format='%.4f',
                           header=False)
    
def findOptimalWeights (model_dict, param_series, file_series):

    returns_df = pd.read_hdf(file_series['model return file'])
    
    num_models = len(model_dict)
    models_list = sorted(model_dict.keys())

    hold_back_returns_df = holdBackData (returns_df,
                                         param_series['Model End Date'])

    # Offers option to maximize function over a list of dataframes
    def avgMaximizeFunction (weights_array):

        weights_list = list(weights_array)

        weights_dict = {models_list[i]:weights_list[i]
                        for i in range(len(weights_list))}

        return maximizeFunction (assignWeights(hold_back_returns_df,
                                               weights_dict),
                                 sign=-1)

    
    model_ret_dict = calcModelMonthlyReturn (hold_back_returns_df, 
                                                models_list)
    
    ineq_cons = constraintsDict (model_ret_dict,
                                 param_series['Min Annual Return'])
    
    wt_bound_list, avg_wt_list = weightBoundsList (model_dict)
    
    args = tuple(wt_bound_list)

    x0 = np.array(avg_wt_list)
    
    res = minimize(avgMaximizeFunction, x0, method='SLSQP', 
                   constraints=(ineq_cons), callback=callbackFunc,
                   options={'ftol': 1e-9, 'disp': True,
                            'maxiter':100}, bounds=args)

    outputWeightsToFile (res.x, models_list,
                         file_series['output directory'] + 
                         file_series['optimal weights file'])

    



    
