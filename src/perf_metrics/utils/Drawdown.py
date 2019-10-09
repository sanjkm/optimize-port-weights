# Drawdown.py
# Look for the biggest drawdowns in a return stream, determine
# their characteristics

import datetime
import pandas as pd
import numpy as np

# Characterizes each drawdown by start date, max DD, number of days
# until max DD, number of days until total recovery
def calcDrawdownList (df):

    df.index = df['Date']

    df_dict = df.to_dict('index')

    drawdown_dict, drawdown_dict_list = {}, []
    
    for k in sorted(df_dict):
        if (df_dict[k]['Drawdown'] == 0) and (drawdown_dict == {}):
            continue

        # first day of DD
        if drawdown_dict == {}:
            drawdown_dict['Start Date'] = df_dict[k]['Date']
            drawdown_dict['Drawdown Length'] = 1
            drawdown_dict['Max Drawdown'] = df_dict[k]['Drawdown']
            drawdown_dict['Time to Max Drawdown'] = 1
        else:
            drawdown_dict['Drawdown Length'] += 1
            
            if drawdown_dict['Max Drawdown'] < df_dict[k]['Drawdown']:
                
                drawdown_dict['Max Drawdown'] = df_dict[k]['Drawdown']
                drawdown_dict['Time to Max Drawdown'] = drawdown_dict['Drawdown Length']
                
        # End of DD
        if df_dict[k]['Drawdown'] == 0:
            drawdown_dict_list.append (drawdown_dict)
            drawdown_dict = {}

    drawdown_df = pd.DataFrame (drawdown_dict_list)

    drawdown_df = drawdown_df.sort_values(by='Max Drawdown')

    return drawdown_df
                
        
# Creates a column that contains the current drawdown amount of the
# portfolio
def drawdownStats (returns_df):

    dd_df = returns_df[['Date', 'Daily Return']]
    dd_df.index.names = ['IndexDate']
    dd_df = dd_df.sort_values(by='Date')

    dd_df['Principal Return'] = dd_df['Daily Return']  # constant capital

    dd_df['Cumulative Return'] = dd_df['Principal Return'].cumsum()

    dd_df['Cumulative Max Return'] = dd_df['Cumulative Return'].cummax()

    dd_df['Cumulative Max Return'] = np.maximum(dd_df['Cumulative Max Return'],
                                                0)

    dd_df['Drawdown'] = ((dd_df['Cumulative Max Return'] -
                         dd_df['Cumulative Return']))

    drawdown_df = calcDrawdownList (dd_df)

    return drawdown_df
    

