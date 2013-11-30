import numpy as np
import h5py
import os
import time
import ConfigParser


def timestamp():
    return time.strftime("_%H-%M-%S-0000_%m-%d-%Y_GMT", time.gmtime())


def formatData(fileDir, name, conf="config.ini", *options):
    """Loads raw numpy arrays from a folder and saves them in hdf5 file format.
        Each array will be given its own dataset under the group 'raw_data'.

        Args:
            fileDir: the absolute path to a directory containing one or more numpy files.
            name: the name of the hdf5 file to save under. ".hdf5" will be appended to the end.
            (optional arguments)
            conf: The name or location of a configuration file associated with this data.
                  If no root is given in the path, the location will be assumed to be relative
                  to fileDir.
            *options: An optional list of additional behavior to perform when formatting data.
                      Currently supported options are:
                        '-a': open the hdf5 file in append mode, do not overwrite. Files with
                              name conflicts will have a timestamp appended to their name.
    """
    #Decode launch options
    file_access_mode = 'r+' if ('-a' in options) else "w"
    f = h5py.File(name+".hdf5", file_access_mode)
    #Check if the given file already contains raw_data. If not, create it.
    if(not ('raw_data' in f)):
        data_dir = f.create_group("raw_data")
    else:
        data_dir = f['raw_data']
    tmpdir = os.path.abspath(os.curdir)
    print "Moving to "+fileDir
    os.chdir(fileDir)
    print "Beginning data format of existing npy files."
    count = 0
    for files in os.listdir("."):
        if(files.endswith(".npy")):
            count = count + 1
    i = 0
    for files in os.listdir("."):
        if(files.endswith(".npy")):
            i = i + 1
            print "Formatting file ("+i.__repr__()+"/"+count.__repr__()+"), \""+files+"\"..."
            tmp = np.load(files)
            if(files[0:files.index(".npy")] in data_dir):
                conflict_name = (files[0:files.index(".npy")] + "_conflicted_copy_" + timestamp())
                dset = data_dir.create_dataset(conflict_name, data=tmp)
            else:
                dset = data_dir.create_dataset(files[0:files.index(".npy")], data=tmp)
            dset.attrs.create("shape", np.shape(tmp))
            dset.attrs.create("dtype", tmp.dtype.__repr__())
            numsets = data_dir.attrs.get("count")
            if numsets is not None:
                data_dir.attrs.modify("count", [numsets[0] + 1])
            else:
                data_dir.attrs.modify("count", [1])
    data_dir.attrs.modify("last_modified", [timestamp()])
    #At this point, the raw datasets have each been imported from the .npy files.
    #We now read any metadata from the given configuration file.
    config = ConfigParser.SafeConfigParser(allow_no_value=True)
    if(os.listdir(".").__contains__(conf)):
        print "Attaching additional metadata found in file "+conf
        config.read(conf)
        for (key, value) in config.items("raw_data"):
            data_dir.attrs.create(key, value)
            print "raw_data: "+key.__repr__()+"="+value.__repr__()
        for section in config.sections():
            if section == "raw_data":
                continue
            if(section in data_dir.keys()):
                for (key, value) in config.items(section):
                    print section+": "+key.__repr__()+"="+value.__repr__()
                    data_dir[section].attrs.create(key, value)
            else:
                print "Error in reading config file: There is no dataset \""+section+"\". Continuing..."
        del config
    else:
        print "No config file found, cleaning up..."
    #Change directory back to the orignial working directory, in case future commands depend on it
    os.chdir(tmpdir)
    f.flush()
    f.close()


def formatwrapper(**kwargs):
    fileDir = ""
    name = ""
    options = []
    conf = "config.ini"
    for (x, y) in kwargs:
        if x == "fileDir":
            fileDir = y
        if x == "name":
            name = y
        if x == "options":
            options = y
        if x == "conf":
            conf = y
    formatData(fileDir, name, conf, options)
