"""Copyright (C) 2018-Present E. Allen, D. Veron - University of Delaware"""
#
# You may use, distribute and modify this code under the
# terms of the GNU Lesser General Public License v3.0 license.
#
# https://www.gnu.org/licenses/lgpl-3.0.en.html
#
# Imports
from __future__ import print_function
import sys
import numpy as np

def getmetrics(obs, pred, stat_list):
    """Get Metrics: 5-20-2020, Verified all statistics

    Sources for formulas and help:
    https://dtcenter.org/met/users/docs/presentations/WRF_Users_2012.pdf
    https://www.hindawi.com/journals/amete/2015/758250/
    http://www.australianweathernews.com/verify/intro.htm
    https://pdfs.semanticscholar.org/af71/3d815a7caba8dff7248ecea05a5956b2a487.pdf
    http://dkmathstats.com/mean-median-mode-variance-in-python/
    https://www.dummies.com/education/math/statistics/how-to-calculate-standard-deviation-in-a-statistical-data-set/
    https://machinelearningmastery.com/time-series-forecasting-performance-measures-with-python/
    Found this after the fact:
    http://www.statsmodels.org/devel/_modules/statsmodels/tools/eval_measures.html#mse

    Numerous email corrospondences and discussions with Dr. Legates regarding IoA and NSE
    """

    out_list = []
    #SKIP Var.
    for stat in stat_list[1:]:
        #pred[pred == 0] = np.nan
        #obs[obs == 0] = np.nan
        #obs_nonan = obs[np.logical_not(np.isnan(obs))]
        #pred_nonan = pred[np.logical_not(np.isnan(pred))]
        #nonan_error = pred_nonan - obs_nonan

        #ERROR (pred - obs)
        error = pred - obs

        if stat.upper() == "OBS":
            # Mean observed (VERIFIED)
            mobs = np.nanmean(obs)
            out_list.append(mobs)


        elif stat.upper() == "PRED":
            # Mean predicted (VERIFIED)
            mpred = np.nanmean(pred)
            out_list.append(mpred)

        elif stat.upper() == "MAE":
            # MEAN ABSOLUTE ERROR ( 1/n * ∑|error| )
            # ******** MAE *********
            mae = np.nanmean(np.abs(error))
            out_list.append(mae)

        elif stat.upper() == "MBE" or stat.upper() == "BIAS":
            #BIAS  ( 1/n * ∑ error )
            # ******** BIAS *********
            bias1 = np.nanmean(error)
            out_list.append(bias1)


        elif stat.upper() == "MSE":
            #MEAN SQUARE ERROR ( 1/n * ∑ error^2 )
            # ******** MSE *********
            mse = np.nanmean(error**2)
            out_list.append(mse)

        elif stat.upper() == "RMSE":
            #MEAN SQUARE ERROR ( 1/n * ∑ error^2 )
            # ******** MSE *********
            mse = np.nanmean(error**2)

            #ROOT MEAN SQUARE ERROR (  √ (1/n * ∑ error^2 )  )
            # ******** RMSE *********
            rmse = np.sqrt(mse)
            out_list.append(rmse)


        elif stat.upper() == "MAD":
            # ******** MAD *********
            med_err = np.nanmedian(error) #median error
            #average of absolute value of error - median error
            mad = np.nanmean(np.abs(error - med_err))
            out_list.append(mad)

        elif stat.upper() == "MAPE":
            # ******** MAPE *********
            absdiv = np.abs(error / obs)
            mape = np.nanmean(absdiv) * 100.
            #print(mape)
            out_list.append(mape)

        elif stat.upper() == "NSE" or stat.upper() == "NASH SUTCLIFFE EFFICIENCY" or\
                     stat.upper() == "NASH-SUTCLIFFE EFFICIENCY" or stat.upper() == "EFFICIENCY":
            #Nash and Sutcliffe 1970 (Ej = 2)
            #Legates and McCabe 2013 (Ej = 1) -- USE THIS. EMAIL CORROSPONDANCE WITH LEGATES
            # ******** Nash-Sutcliffe ********* (VERIFIED)
            # Line Continuation after division symbol
            #nse = 1 - (np.nansum((obs - pred), axis=0, dtype=np.float64)/\
            #           np.nansum((obs - np.nanmean(obs)), dtype=np.float64))#[0]
                    #FASTER
            Ej = 1
            nse = 1 - (np.nansum(np.abs(obs - pred) ** Ej, axis=0,\
                                 dtype=np.float64) /\
                        np.nansum(np.abs(obs - np.nanmean(obs)) ** Ej, dtype=np.float64))

            #SAME RESULT. SLOWER
            #nse = 1 - (np.nansum((obs - pred)**2)/np.nansum((obs - np.nanmean(obs))** 2))
                # Nash-Sutcliffe model eficiency coefficient
            out_list.append(nse)

        elif stat.upper() == "IOA" or stat.upper() == "INDEX OF AGREEMENT":
            #Refined IoA. Willmott et al. 2012 (verified)
            #Read: Legates and McCabe 2013
            mobs = np.nanmean(obs)
            # ******** Index of Agreement *********
            part1 = np.nansum(np.abs(pred-obs))
            part2 = 2 * np.nansum(np.abs(obs - mobs))
            if part1 <= part2:
                iagree = 1 - part1/part2
            else:
                iagree = part2/part1 - 1
            out_list.append(iagree)

        elif stat.upper() == "R" or stat.upper() == "PEARSON":
            #Legates and McCabe 1999 (verified)
            mobs = np.nanmean(obs)
            mpred = np.nanmean(pred)
            # ******** R *********
            pearson = np.nanmean((obs-mobs)*(pred-mpred))/\
                (np.sqrt(np.nanmean((obs-mobs)**2))*np.sqrt(np.nanmean((pred-mpred)**2)))
            out_list.append(pearson)


        elif stat.upper() == "R2" or stat.upper() == "RTWO":
            #Legates and McCabe 1999 (verified)
            mobs = np.nanmean(obs)
            mpred = np.nanmean(pred)
            # ******** R *********
            pearson = np.nanmean((obs-mobs)*(pred-mpred))/\
                (np.sqrt(np.nanmean((obs-mobs)**2))*np.sqrt(np.nanmean((pred-mpred)**2)))
            # ******** R2 *********
            rtwo = pearson*pearson
            out_list.append(rtwo)
        else:
            sys.exit("INVALID STAT IN STAT LIST OR MISSING FROM getmetrics")
    #return [mae, mse, rmse, bias1, mape, rtwo, nse, iagree, pearson]

    return out_list
