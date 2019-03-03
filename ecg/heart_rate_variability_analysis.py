# heart rate variability (HRV) analysis of ECG data

import numpy as np
import math


# calculate RMSSD (root mean square of successive differences)
def _calculate_RMSSD(results):
    RR_list = results['RR_list']
    print(RR_list)
    x = 0
    for i in range(len(RR_list)-1):
        x += (RR_list[i+1] - RR_list[i])**2
    x = x * (1 / (len(RR_list) - 1))
    rmssd = math.sqrt(x)
    print(rmssd)
    return rmssd


# calculate SDNN (standard deviation of RR intervals)
def _calculate_SDNN(results):
    RR_list = results['RR_list']
    avg = np.mean(RR_list)
    x = 0
    for i in range(len(RR_list)):
        x += (RR_list[i] - avg)**2
    x = x * (1 / (len(RR_list) - 1))
    sdnn = math.sqrt(x)
    print(sdnn)
    return sdnn


# get NNx and calculate pNNx (proportion of successive NN intervals that differ by > 50m)s
def _calculate_pNNx(results, x=50):
    RR_list = results['RR_list']
    NNx = 0
    for i in range(len(RR_list)-1):
        if (RR_list[i+1] - RR_list[i]) > x:
            NNx+=1
    pNNx = NNx/len(RR_list)
    print(pNNx)
    return pNNx

# main function
def run_hrv_analysis(results):
    results['rmssd'] =_calculate_RMSSD(results)
    results['sdnn'] = _calculate_SDNN(results)
    results['pNNx'] = _calculate_pNNx(results)
    return results



