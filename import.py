import scipy.io
import numpy as np
from math import ceil

def loadFromMat(filedir, Fs = 10e3, rFs = 256):
    """Loads folder of matlab data files and saves them in numpy format"""
    pts = [343*Fs+1, 643*Fs]

    electrodes = [
        21,31,41,51,61,71,12,22,32,42,52,62,72,82,13,23,33,43,53,63,73,83,14,
        24,34,44,54,64,74,84,15,25,35,45,55,65,75,85,16,26,36,46,56,66,76,86,
        17,27,37,47,57,67,77,87,28,38,48,58,68,78
    ]

    for ii in electrodes:
        mat = scipy.io.loadmat("{0}\Electrode_{1}_master.mat".format(filedir, ii))["dataheap"]
        data = mat[pts[0]:pts[1]]
        data = np.subtract(data, np.mean(data))
        np.save("{0}\Electrode_{1}_master".format(filedir,ii), mat)