import scipy.io
import array
import numpy as np
from math import ceil
import os
import tempfile
import gc
import shutil


electrodes = [
    21, 31, 41, 51, 61, 71, 12, 22, 32, 42, 52, 62, 72, 82, 13, 23, 33,
    43, 53, 63, 73, 83, 14, 24, 34, 44, 54, 64, 74, 84, 15, 25, 35, 45,
    55, 65, 75, 85, 16, 26, 36, 46, 56, 66, 76, 86, 17, 27, 37, 47, 57,
    67, 77, 87, 28, 38, 48, 58, 68, 78
]

def __smash2(filedir, workingdir, type, fileNum):
    savedir = filedir + os.sep + type
    filename = savedir+"%04d"%(fileNum)+".raw"
    print filename
    fid = file(filename, 'rb')
    #fileSize = os.stat(filename).st_size
    #data = array.array("H")
    #data.fromfile(fid, fileSize/2)
    data = np.fromfile(fid, dtype=np.uint16)
    #print len(data)
    #temp = np.zeros((1,len(data)))
    #data = data.astype(np.float32, copy=False)
    #print len(data)
    #convertedData = [(x-32768)*0.0104 for x in data]
    #data -= 32768
    #data *= 0.0104
    numelec = 60
    #out = []
    for i in range(numelec):
        #The whole is too big to fit into memory, so we process chunk by chunk
        temp = data[i:data.size:numelec]
        temp = temp.astype(np.float32, copy=False)
        temp-=32768
        temp*=0.0104
        np.save(workingdir + os.sep + "Electrode_"+str(electrodes[i])+"_"+str(fileNum), temp)
    return

def __mergemat(filename, numFiles, Fs):    
    idealLengthPerFile = (2*60)*Fs
    index = 0
    dataheap = np.zeros((idealLengthPerFile * numFiles,1))

    for i in xrange(numFiles):
        temp = np.load(filename + str(i)+".npy")
        #if index+temp.size>=dataheap.size:
        #    dataheap.resize((index+temp.size, 1))
            #print "resizing"
        temp.resize((temp.size,1))
        dataheap[index:index+temp.size] = temp
        index = index + temp.size
    
    #get rid of extraneous because the first and last have smaller sizes
    dataheap.resize((index,1))
    
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
        print "Parsing electrode " + ii.__repr__()
        mat = scipy.io.loadmat(
            "{0}{2}Electrode_{1}_master.mat".format(filedir, ii, os.sep)
        )["dataheap"]
        print "Load success."
        data = np.array(mat[pts[0]:pts[1]], order='C', dtype=np.float32)
        data = np.subtract(data, np.mean(data))
        np.save("{0}{2}Electrode_{1}_master".format(filedir, ii, os.sep), data)
        print "saved electrode "+ ii.__repr__()
        mat = None
        gc.collect()

    return filedir

def loadFromRaw(filedir, numFiles=6, type='slice2_', Fs=20e3, saveMat=False):
    """Loads folder of raw data files and saves them in numpy or Matlab format.

    Args:
        filedir: the root folder to import
        numFiles: the number of time slices
        type: prefix of the file type, note this also determins output folder
        Fs: sampling frequency rate
        saveMat: whether to ouput Matlab files instead of Numpy files

    """
    workingdir = tempfile.mkdtemp()
    try:
        print "Smashing....\n"
        for i in xrange(numFiles):
            __smash2(filedir, workingdir, type, i)
        
        print "Merging....\n"
        for i in range(60):
            print "\r%d of %d"%(i,60)
            file = workingdir + os.sep + "Electrode_" + str(electrodes[i]) + "_"
            if (not (os.listdir(filedir).__contains__(type))):
                os.mkdir(filedir+os.sep+type)
            holder = __mergemat(file, numFiles, Fs)
            #f = open("{0}{2}{3}{2}Electrode_{1}_master".format(filedir, electrodes[i], os.sep, type) + ".mat", "w")
            if saveMat:
                scipy.io.savemat("{0}{2}{3}{2}Electrode_{1}_master".format(filedir, electrodes[i], os.sep, type), holder)
            else:
                np.save("{0}{2}{3}{2}Electrode_{1}_master".format(filedir, electrodes[i], os.sep, type), holder['dataheap'])
            holder = None
            gc.collect()
        print "\nDone!"
    finally:
        shutil.rmtree(workingdir)