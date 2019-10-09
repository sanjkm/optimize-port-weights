# assembleReturnsData.py
# Gets the returns data from all inputted model directories
# Concatenates into a single data frame and outputs to h5 file
# Performs this for both Training and Test data

import os, sys
import pandas as pd
import datetime

def applyColumnNames (model_returns_df, model_name_dict):

    date_col = int(model_name_dict['Date Column'])

    return_col = int(model_name_dict['Returns Column'])

    col_list = model_returns_df.columns
    
    rename_dict = {col_list[date_col]:'Date',
                   col_list[return_col]:'Daily Return'}

    model_returns_df = model_returns_df.rename(rename_dict, axis=1)

    return model_returns_df
    


def concatModelReturns (model_dict):

    overall_returns_df = pd.DataFrame()
    
    for model_name in model_dict:

        model_name_dict = model_dict[model_name]

        model_ret_file = model_name_dict['Returns File']

        if os.path.isfile(model_ret_file) == False:
            continue

        model_returns_df = pd.read_csv (model_ret_file)

        if len(model_returns_df) > 0:

            model_returns_df = applyColumnNames (model_returns_df,
                                                 model_name_dict)
            model_returns_df.loc[:, 'Model'] = model_name

        if len(overall_returns_df) == 0:
            overall_returns_df = model_returns_df
        else:
            overall_returns_df = pd.concat ([overall_returns_df,
                                             model_returns_df],
                                            axis=0, sort=False)

    return overall_returns_df

def applyParamConstraints (returns_df, param_series, file_series):

    returns_df['Date'] = pd.to_datetime(returns_df['Date'],
                                        errors='coerce')

    min_date = param_series['Start Date']

    returns_df = returns_df.loc[returns_df['Date'] >= min_date]

    returns_df = returns_df.sort_values(by='Date')

    model_ret_file = file_series['model return file']

    returns_df.to_hdf (model_ret_file, 'returns', mode='w',
                       format='table')

    return returns_df


def assembleReturnsData (model_dict, param_series, file_series):

    returns_df = concatModelReturns (model_dict)

    returns_df = applyParamConstraints (returns_df, param_series, file_series)
    
    return returns_df
