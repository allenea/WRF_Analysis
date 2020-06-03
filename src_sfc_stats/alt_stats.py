"""Copyright (C) 2018-Present E. Allen, D. Veron - University of Delaware"""
#
# You may use, distribute and modify this code under the
# terms of the GNU Lesser General Public License v3.0 license.
#
# https://www.gnu.org/licenses/lgpl-3.0.en.html
#
# Imports
from __future__ import print_function
import numpy as np

#Absolute Error
def absolute_error(forecast, actual):
    """
    Absolute Error: measures absolute difference from the forecasted value
                    and the observed value
    Input - A single actual observed value (float)
    Input - A single model forecasted value (float)
    Output - abs_err (absolute error)
    """
    absolute_error_out = abs(float(forecast) - float(actual))
    return absolute_error_out

#Relative Error
def relative_error(forecast, actual):
    """
    Relative Error: measures absolute error divided by the observed value f
    Calls function absolute_error to calculate absolute_error for the numerator
    If actual is 0 then np.nan is returned.
    Input - A single actual observed value (float)
    Input - A single model forecasted value (float)
    Output - RelativeError (relative error)
    """
    if actual == 0:
        actual = np.nan
    abs_err = absolute_error(float(forecast), float(actual))
    relative_error_out = abs_err / float(actual)
    return relative_error_out

#Percent Error
def percent_error(forecast, actual):
    """
    Percent Error: measures relative error as a percentage
    Calls function relative_error to get relative error which calls absolute error.
    If actual is 0 then np.nan is returned.
    Input - A single actual observed value  (float)
    Input - A single model forecasted value (float)
    Output - PercentError
    """
    percent_error_out = (relative_error(float(forecast), float(actual))) * 100
    return percent_error_out

#Forecast Error
def forecast_error(forecast, actual):
    """
    Forecast Error: Difference between forecast and observed
    Input - A single actual observed value  (float)
    Input - A single model forecasted value (float)
    Output - forecast_error
    """
    forecast_error_out = float(forecast) - float(actual)
    return forecast_error_out

#Mean Square Error
def mean_square_error(forecast, actual):
    """
    Mean Square Error: Average of the squares of the difference between the forecast
                        and observed observations.
                        -  Continuous Scores
                        - Does not indicate direction of error
                        - Quadratic rule, therefore large weight on large errors
                        - Good if you wihs to penalize large error BUT SENSITIVE
    Input  - A list actual observed values  (float)
    Input  - A list model forecasted values (float)
    Output - MSE (single value)
    """
    nlength = 0.0
    sfe = 0.0
    if len(actual) == len(forecast):
        nlength = len(forecast)
    else:
        print("MSE - Not Same Size")
    #http://www.australianweathernews.com/verify/intro.htm
    for idx in range(nlength):
        sfe += forecast_error(float(forecast[idx]), float(actual[idx])) ** 2
    mse = (1./nlength) * sfe
    return mse

#Mean Absolute Error
def mean_absolute_error(forecast, actual):
    """
    Mean absolute error: measures the mean amplitude/magnitude of the absolute error
            with respect to the observation.
            - Linear score = each error has the same weight
            - Does not indicate the direction of the error, just the magnitude
    Input  - list of actual observed values (floats)
    Input  - list of model forecasted values (floats)
    Output - MAE
    """
    #MEASURES ACCURACY
    nlength = 0.0
    sae = 0.0
    if len(actual) == len(forecast):
        nlength = len(forecast)
    else:
        print("MSE - Not Same Size")
    #http://www.australianweathernews.com/verify/intro.htm
    for idx in range(nlength):
        #Sum Absolute Error
        sae += absolute_error(float(forecast[idx]), float(actual[idx]))
    mae = (1./nlength) * sae
    return mae

#Root Mean Square Error
def root_mean_square_error(forecast, actual):
    """
    Root mean square error (RMSE): measures the mean square gap between observed
                                   and modelled data.
                        - Does not indicate direction of the error
                        - defined with quadratic rule = sensitive to errors
                        - RMSE IS ALWAYS LARGER OR EQUAL THAN THE MAE
    Calls mean_square_error and takes the square root of MSE
    Input - A list actual observed values  (float)
    Input - A list model forecasted values (float)
    Output - RMSE
    """
    if len(actual) != len(forecast):
        print("ERROR RMSE - Not Same Size")
    #http://www.australianweathernews.com/verify/intro.htm
    rmse = mean_square_error(forecast, actual) ** 0.5
    return rmse

#Bias
def bias(forecast, actual):
    """
    Bias: Measures the mean difference between simulation and observation
    Input - list of actual observed values
    Input - list of model forecasted values
    Output - Single Bias Value
    """
    num_actual = len(actual)
    num_forecast = len(forecast)
    num = 0.0
    sum_diff = 0.0
    if num_actual == num_forecast:
        num = num_actual
    else:
        print("BIAS - Not Same Size")
    for idx in range(num_actual):
        sum_diff += forecast_error(float(forecast[idx]), float(actual[idx]))

    #http://www.australianweathernews.com/verify/intro.htm
    bias_calc = (1./num) * sum_diff
    return bias_calc

#Median Absolute Deviation
def median_absolute_deviation(lst_absolute_error):
    """
    Median Absolute Deviation (MAD): Median of the magnitude of the errors. Very Robust
                                     - Measures accuracy
    Input - list of absolute errors
    Output - Single Median Absolute Error Value
    """
    return median(lst_absolute_error)

# Mean, Variance, STD


#Mean
def mean(lst):
    """
    Mean - Calculates the average or mean value from a list of numbers
    Input - List
    Output - Mean
    """
    return sum(lst)/float(len(lst))

#Median
def median(lst):
    """
    Median - Takes a list, sorts it, and find the median value
    For Python-2.X
    Input - List
    Output - Median Value
    for Python-3.X use below
        from statistics import median
        median([5, 2, 3, 8, 9, -2])
    """
    nlength = len(lst)
    if nlength < 1:
        return None
    if nlength % 2 == 1:
        return sorted(lst)[nlength//2]
    return sum(sorted(lst)[nlength//2-1:nlength//2+1])/2.0

#Mode
def mode(lst):
    """
    Mode - Finds the most common element in a list
    Allows for multiple modes
    Input - List
    Output - Most Common Element if 1; List of Most Common Elements >1
    """
    most = max(list(map(lst.count, lst)))
    return list(set(filter(lambda x: lst.count(x) == most, lst)))

#Variance
def variance(lst):
    """
    Variance - average of the squared differences from the Mean to individal observation.
    Input - List
    Output - Variance
    """
    average = mean(lst)
    variance_out = 0.0
    for item in lst:
        variance_out += (float(average) - float(item)) ** 2.0
    return variance_out/len(lst)

#Standard Deviation
def standard_deviation(lst):
    """
    Standard Deviation - Measures the spread of the numbers.
                       - Square root of variance
    Input - List
    Output - Standard Deviation
    """
    return variance(lst) ** 0.5
