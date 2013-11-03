import scipy.io
import array
import numpy as np
from math import ceil
import os
import tempfile


electrodes = [
    21, 31, 41, 51, 61, 71, 12, 22, 32, 42, 52, 62, 72, 82, 13, 23, 33,
    43, 53, 63, 73, 83, 14, 24, 34, 44, 54, 64, 74, 84, 15, 25, 35, 45,
    55, 65, 75, 85, 16, 26, 36, 46, 56, 66, 76, 86, 17, 27, 37, 47, 57,
    67, 77, 87, 28, 38, 48, 58, 68, 78
]

def smash2(filedir, workingdir, type, fileNum):
    savedir = filedir + os.sep + type
    filename = savedir+"%04d"%(fileNum)+".raw"
    print filename
    fid = file(filename)
    #fileSize = os.stat(filename).st_size
    #data = array.array("H")
    #data.fromfile(fid, fileSize/2)
    data = np.fromfile(fid, dtype=np.uint16)
    
    #convertedData = [(x-32768)*0.0104 for x in data]
    data -= 32768
    data *= 0.0104
    
    numelec = 60
    out = []
    for i in range(numelec):
        #out.append(data[i:data.size:numelec])
        np.save(workingdir + os.sep + "Electrode_"+str(electrodes[i])+"_"+str(fileNum), data[i:data.size:numelec])
    return

def mergemat(filename, numFiles, Fs):
    datatemp = np.load(filename+"0.npy")
    
    L = (2*60)*Fs
    
    data = np.zeros((L,numFiles-2))
    
    for i in range(numFiles-2):
        data[:,i+1] = np.load(filename + i+1)
    
    L2 = (numFiles-2)*L
    dataheap = np.reshape(data, (L2,1))
    
    data = np.load(filename + str(numFiles-1) + ".npy")
    dataheap = np.array([[datatemp],[dataheap],[data]])
    
    holder = {}
    holder['dataheap'] = dataheap
    return holder

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
    workingdir = tempfile.mkdtemp()
    for i in xrange(numFiles):
        smash2(filedir, workingdir, type, i)
    
    for i in range(60):
        file = workingdir + os.sep + "Electrode_" + str(electrodes[i]) + "_"
        holder = mergemat(file, numFiles, Fs)
        #f = open("{0}{2}{3}{2}Electrode_{1}_master".format(filedir, electrodes[i], os.sep, type) + ".mat", "w")
        scipy.io.savemat("{0}{2}{3}{2}Electrode_{1}_master".format(filedir, electrodes[i], os.sep, type), holder)