# PortOpt.py
# Gets data from the inputted model return files,
# optimizes weightings based on inputted constraints

import pandas as pd

from src.data.init_params import get_model_dict, get_params_series,get_file_names
from src.data.assembleReturnsData import assembleReturnsData
from src.optimize.optimize import findOptimalWeights
from src.results.overallMetrics import outputOverallMetrics

model_file = 'parameters/input_models.csv'
param_file = 'parameters/data_params.csv'
file_dict_file = 'parameters/file_names.csv'

if __name__ == '__main__':

    model_dict = get_model_dict (model_file)

    param_series = get_params_series (param_file)

    file_series = get_file_names (file_dict_file)

    assembleReturnsData(model_dict, param_series, file_series)

    findOptimalWeights (model_dict, param_series, file_series)

    outputOverallMetrics (file_series)
    
    
    
