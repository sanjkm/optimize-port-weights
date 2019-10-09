# assignWeights.py
# Assign portfolio weights to each model in the portfolio
# Prepare dataset such that return stream stats can be calculated
# Output the prepared dataset

import pandas as pd
from pandas.api.types import is_numeric_dtype

# Assumes weights_list assigns weights to models alphabetically
# if weights_list = [], then equal weights assigned to each model
def assignWeights (returns_df, weights_dict):

    model_list = sorted(list((weights_dict.keys())))

    weights_list = []

    for k in sorted(weights_dict):
        weights_list.append(weights_dict[k])
    
    if len(weights_list) != len(model_list):
        print ('Weights and model list not of same length. Exiting')
        exit(0)

    dict_list = []
    for i in range(len(weights_list)):
        dict_list.append({'Model': model_list[i],
                          'Weight': weights_list[i]})

    weights_df = pd.DataFrame(dict_list)

    ret_weights_df = returns_df.merge(weights_df, on='Model')

    col_list = returns_df.columns

    for col in col_list:
        if is_numeric_dtype(ret_weights_df[col]) == False:
            continue
        
        ret_weights_df['Weighted ' + col] = ret_weights_df['Weight'] * ret_weights_df[col]

        ret_weights_df[col] = ret_weights_df['Weighted ' + col]

    ret_weights_df = ret_weights_df.filter (col_list, axis=1)

    col_count = 0
    aggregate_df = pd.DataFrame()
    
    for col in col_list:
        if is_numeric_dtype(ret_weights_df[col]) == False:
            continue

        mini_weights_df = pd.DataFrame(ret_weights_df.groupby('Date')[col].sum())
        
        mini_weights_df['Date'] = mini_weights_df.index
        mini_weights_df.index.names = ['IndexDate']

        if col_count == 0:
            aggregate_df = mini_weights_df[:]
        else:
            aggregate_df = aggregate_df.merge(mini_weights_df, on='Date')

        col_count += 1
        
    aggregate_df = aggregate_df.sort_values(by='Date')
        
    return aggregate_df
    

    

    

    

    
