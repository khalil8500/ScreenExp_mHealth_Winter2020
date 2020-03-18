#!/usr/bin/python

import pyphysio as ph
import sys
from sklearn.preprocessing import minmax_scale
import csv
import numpy as np
import matplotlib.pyplot as plt


def getMoments(arr, std):
    num_arousing = 0
    level_5 = 0
    arousing_moments = np.array([])
    level_5_moments = np.array([])

    for i in range(0, arr.shape[0]):
        if i == arr.shape[0] - 1:
            if arr[i] / .2 >= 4:
                level_5 += 1
            continue

        p1 = np.floor(arr[i] / .2)

        # print(p2-p1)
        # print(p2)

        if np.abs(arr[i + 1] - arr[i]) >= std * 0.25:
            num_arousing += 1
            arousing_moments = np.append(arousing_moments, i)
        if p1 == 4:
            level_5 += 1
            level_5_moments = np.append(level_5_moments, i)

    #print(arousing_moments * 5)
    #print(level_5_moments)

    return arousing_moments, level_5_moments,num_arousing, level_5


if __name__ == '__main__':
    sample_freq = 0
    start_time = 0
    vals = np.array([])

    base = "novideo"

    loc = base+"/empatica_data/EDA.csv"

    seg_dict={
        "video2": np.array([240, 384, 480, 720]),
        "video3": np.array([-1224,-816,-552,-240]),
        "novideo": np.array([1200, 1500])
    }

    offset = 0
    segements = seg_dict[base]     #-video2 -video3 -no video

    with open(loc, newline='') as csvfile:
        csv_data = csv.reader(csvfile, delimiter=',')
        i = 0
        for row in csv_data:
            if i == 0:
                start_time = float(row[0])
            elif i == 1:
                sample_freq = int(float(row[0]))
            else:
                vals = np.append(vals, float(row[0]))
            i += 1

    #print(vals)
    #print(sample_freq)

    eda = ph.EvenlySignal(values=vals, sampling_freq=sample_freq, signal_type='eda')
    eda.plot()
    plt.show()

    #eda_filt = ph.IIRFilter(fp=0.8, fs=1.1, ftype='ellip')(eda)
    eda_filt = ph.DenoiseEDA(threshold=0.1, win_len=5.0)(eda)
    eda_filt.plot()
    plt.show()

    eda = eda_filt
    eda = ph.Normalize(norm_method='maxmin')(eda)
    #eda.plot()
    #plt.show()

    driver = ph.DriverEstim()(eda)
    # driver.plot()
    # plt.show()

    phasic, tonic, _ = ph.PhasicEstim(delta=0.02)(driver)
    # phasic.plot()
    # tonic.plot()
    # plt.show()

    #print(eda.shape)
    M = 20
    splitArr = np.array_split(eda, eda.shape[0] / M)
    res = np.array([item.mean() for item in splitArr])

    res = minmax_scale(res)
    #print(res)
    #print(res.shape[0])

    #aM, l5, numAM, numL5 = getMoments(res)

    segs = np.array_split(res, segements)
    std = np.std(res)
    #print(segs)

    file = open(base+".txt", "w+")

    plt.plot(res)
    plt.plot(segs[0],'r')
    plt.show()

    i = 1
    file.write("Segment, Number of arousing moments, Number of level 5 arousal\n")
    for arr in segs:
        aM, l5, numAM, numL5 = getMoments(arr, std)
        file.write(str(i) + "," + str(numAM) + "," + str(numL5) + "\n")
        i += 1
