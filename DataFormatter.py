import scipy.io
import numpy as np
import h5py
import os

def formatData(fileDir, name, *options):
    """Loads raw numpy arrays from a folder and saves them in hdf5 file format. Tagging information about the arrays may be supplied
        in a seperate file.

        Args:
            fileDir: the absolute path to a directory containing one or more numpy files.
            *options: An optional list of command-line switches or paths to additional files containing tagging information
    """
    f=h5py.File(name+".hdf5", "w")
    os.chdir(fileDir)
    for files in os.listdir("."):
        if(files.endswith(".npy")):
            tmp=np.load(files)
            dset=f.create_dataset(files[0:files.index(".npy")], len(tmp), dtype='f')
            dset.write_direct(tmp)
            f.flush()
    f.close()

    return f.filename