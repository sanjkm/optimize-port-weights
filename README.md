Python utility that takes csv files with daily returns for assets/models as inputs,
calculates the optimal portfolio weighting using the chosen metric, 
and outputs return metrics as well as a time-series plot

Usage: 

1) In the 'parameters/input_models.csv' file, list the Name, File location, Header, Date column number, Returns column number, 
Minimum asset weight, and Maximum weight for each model/file. 
- Header column is y/n, if csv file has a header. Assumes yes if not filled in
- Date column is assumed to be 1, first column, if not entered
- Returns column is assumed to be 2, second column, if not entered

This file is filled in by default with data for the SPY,
TLT, HYG, and GLD ETFs included in the data/sample directory. 

2) Enter the simulation start date, model end date, actual end date, and minimum
annual return constraint in the 'parameters/data_params.csv' file.
Model end date is the final date for weight optimization, while returns will be 
calculated until actual end date, giving a 'training/test'
option to this program. 

3) Run the PortOpt.py program from the top folder. Results are all outputted
to the results directory. 

Note on optimization metric:

By default, returns are calculated to optimize the annual return divided maximum 
drawdown ratio. You may choose another metric, e.g. monthly sharpe ratio,
by editing the code. This can be implemented by changing the return value for
the function named maximizeFunction in the code file located at
'src/optimize/optimize.py'. I have listed 2 other possibilities within
this function, with both commented out currently. 



Requirements:
Python 2/3
Numpy
Scipy
Pandas
