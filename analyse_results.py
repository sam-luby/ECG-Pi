import os

# results are for a male 18-25 (me)
normal_results = {'BPM_HIGH': 120, 'BPM_LOW' : 40,
                  'RMSSD_HIGH': 100, 'RMSSD_LOW': 70,
                  'SDNN_HIGH': 140, 'SDNN_LOW': 65,
                  'pNN50_HIGH': 0.25, 'pNN50_LOW': 0.10}


# compare measured results with normal results
def keep_or_delete_data(filename, results):
    alert_flag = False

    # check bpm falls within normal range
    if results['bpm'] > normal_results['BPM_HIGH'] or results['bpm'] < normal_results['BPM_LOW']:
        alert_flag = True

    # check rmssd falls within normal range
    if results['rmssd'] > normal_results['RMSSD_HIGH'] or results['rmssd'] < normal_results['RMSSD_LOW']:
        alert_flag = True

    # check sdnn falls withing normal range
    if  results['sdnn'] > normal_results['SDNN_HIGH'] or results['sdnn'] < normal_results['SDNN_LOW']:
        alert_flag = True


    # check delete flag
    if not alert_flag:
        os.remove(filename)
        print("Results are normal, data removed")
    else:
        print("Abnormal results, additional analysis required.")


