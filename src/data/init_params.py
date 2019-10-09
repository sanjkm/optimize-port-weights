# init_params.py

import os, sys
import pandas as pd
from datetime import datetime


def fill_nan_vals (model_df):

    model_df['Header'] = model_df['Header'].fillna(True)

    model_df['Date Column'] = model_df['Date Column'].fillna(0)

    model_df['Returns Column'] = model_df['Returns Column'].fillna(1)

    return model_df

    

def get_model_dict (model_file):

    model_df = pd.read_csv(model_file)

    model_df = fill_nan_vals (model_df)

    dict_list = model_df.to_dict(orient='records')

    model_dict = {x['Model Name']:x for x in dict_list}
    
    return model_dict

def get_params_series (param_file):

    param_series = pd.read_csv(param_file, index_col=0,
                               header=None, squeeze=True)

    date_labels = ['Start Date', 'Model End Date', 'Actual End Date']

    for fname in date_labels:
        param_series[fname] = datetime.strptime(param_series[fname],
                                                '%Y-%m-%d')

    param_series['Min Annual Return'] = float(param_series['Min Annual Return'])

    return param_series

def get_file_names (file_dict_file):

    file_series = pd.read_csv(file_dict_file, index_col=0,
                               header=None, squeeze=True)

    return file_series
