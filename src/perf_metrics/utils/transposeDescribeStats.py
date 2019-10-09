# transposeDescribeStats.py

# transposes the .describe() method's results into a row dataframe
# Adds skew and kurtosis stats as well
# Easier to concatenate results this way

import os, sys
import pandas as pd
import numpy as np

from decimal import Decimal

pd.set_option('precision',4)  # display precision

def transposeDescribeStats (result_series, header):

    result_series = result_series.dropna()
    
    stats_series = result_series.describe()

    stats_series = stats_series.rename (stats_series.name[:5])

    stats_df = pd.DataFrame(stats_series).transpose()

    stats_df['Header'] = header
    stats_df['count'] = int(stats_df['count'])

    cols = stats_df.columns

    # moves Header, Bin cols to beginning instead of end
    new_cols = list(cols[-1:]) + list(cols[:-1])
    stats_df = stats_df[new_cols]

    return stats_df
