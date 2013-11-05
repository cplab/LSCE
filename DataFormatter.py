import numpy as np
import h5py
import os
import time


def timestamp():
    return time.strftime("_%H-%M%-S-0000_%m-%d-%Y_GMT", time.gmtime())


def formatData(fileDir, name, **options):
    """Loads raw numpy arrays from a folder and saves them in hdf5 file format.
        Each array will be given its own dataset under the group 'raw_data'.

        Args:
            fileDir: the absolute path to a directory containing one or more numpy files.
            **options: An optional list of attributes to attach to the raw_data directory
    """
    #Decode launch options
    file_access_mode = 'r+' if ('-a' in options) else "w"
    f = h5py.File(name+".hdf5", file_access_mode)
    if(not ('raw_data' in f)):
        data_dir = f.create_group("raw_data")
    else:
        data_dir = f['raw_data']
    os.chdir(fileDir)
    for files in os.listdir("."):
        if(files.endswith(".npy")):
            tmp = np.load(files)
            if(files[0:files.index(".npy")] in data_dir):
                conflict_name = (files[0:files.index(".npy")] + "_conflicted_copy_" + timestamp())
                dset = data_dir.create_dataset(conflict_name, data=tmp)
            else:
                dset = data_dir.create_dataset(files[0:files.index(".npy")], data=tmp)
            dset.attrs.create("shape", np.shape(tmp))
            dset.attrs.create("dtype", tmp.dtype)
            numsets = data_dir.attrs.get("count")
            data_dir.attrs.modify("count", [numsets[0] + 1])
            f.flush()
    data_dir.attrs.modify("last_modified", [timestamp()])
    #At this point, the raw datasets have each been imported from the .npy files.
    #We now check formatting options for important attributes
    return f
