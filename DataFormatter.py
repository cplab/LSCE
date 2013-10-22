import scipy.io
import numpy as np
import h5py
import os
import time

import importer

def formatData(fileDir, name, **options):
    """Loads raw numpy arrays from a folder and saves them in hdf5 file format. Tagging information about the arrays may be supplied
        in a seperate file.

        Args:
            fileDir: the absolute path to a directory containing one or more numpy files.
            *options: An optional list of command-line switches or paths to additional files containing tagging information
    """
    #Decode launch options
    file_access_mode='r+' if ('-a' in options) else "w"
    timestamp=time.strftime("_%H:%M:%S:0000_%m-%d-%Y_GMT", time.gmtime()) if ('-t' in options) else ''
    f=h5py.File(name+".hdf5", "w")
    data_dir=f.create_group("raw_data" + timestamp)
    os.chdir(fileDir)
    for files in os.listdir("."):
        if(files.endswith(".npy")):
            tmp=np.load(files)
            dset=f.create_dataset(files[0:files.index(".npy")], data=tmp)
            f.flush()
    #At this point, the raw datasets have each been imported from the .npy files.
    #We now check formatting options for important attributes, 
    f.close()
    return f