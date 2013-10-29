import scipy.io
import array
import numpy as np
from math import ceil
import os


electrodes = [
    21, 31, 41, 51, 61, 71, 12, 22, 32, 42, 52, 62, 72, 82, 13, 23, 33,
    43, 53, 63, 73, 83, 14, 24, 34, 44, 54, 64, 74, 84, 15, 25, 35, 45,
    55, 65, 75, 85, 16, 26, 36, 46, 56, 66, 76, 86, 17, 27, 37, 47, 57,
    67, 77, 87, 28, 38, 48, 58, 68, 78
]

def smash2(filedir, type, fileNum):
    #TODO use correct OS separators
    savedir = filedir + '\\' + type
    filename = savedir+"%03d"%(filenum-1)+".raw"
    fid = file(filename)
    fileSize = os.stat(filename)
    data = array.array("H")
    data.fromfile(fid, fileSize.st_size/2)
    data[:] = [(x-32768)*0.0104 for x in data]
    
    numelec = 60
    out = []
    for i in range(numelec):
        out.append(data[i:fileSize.st_size/2:numelec])
    
    return out

def loadFromMat(filedir, Fs=10e3, rFs=256):
    """Loads folder of matlab data files and saves them in numpy format.

    Args:
        filedir: the root folder to import
        Fs: sampling frequency rate
        rFS: resampling frequency rate

    """
    pts = [343*Fs+1, 643*Fs]

    for ii in electrodes:
        mat = scipy.io.loadmat(
            "{0}{2}Electrode_{1}_master.mat".format(filedir, ii, os.sep)
        )["dataheap"]
        data = np.array(mat[pts[0]:pts[1]], order='C', dtype=np.float32)
        data = np.subtract(data, np.mean(data))
        np.save("{0}{2}Electrode_{1}_master".format(filedir, ii, os.sep), data)

    return filedir

def loadFromRaw(filedir, numFiles=6, type='slice2_', Fs=20e3):
    for i in range(numFiles):
        smash2(filedir, type, i)
        
    