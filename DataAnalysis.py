from numpy import *
import scipy
import sys
from scipy.signal import butter, lfilter
import datetime
import atexit

import h5py

class data_analysis(object):
    """Sandbox for data analysis on a dataset."""
    
    def __init__(self, filename = None, dataset_name = None, group_name = None):
        atexit.register(self.clean_up)
        self.f = None
        self.staged_dataset = None
        self.sampling_rate = 0

        if filename is not None:
            self.load_file(filename)
            if dataset_name is not None:
                self.load_dataset(dataset_name, group_name)

    def clean_up(self):
        """Cleans up the sandbox object."""
        if self.f is None:
            print "There is no file loaded."
            return
        if 'tmp' in self.f:
            del self.f['tmp']
        self.f.flush()
        self.f.close()
        self.f = None
        self.staged_dataset = None
        self.sampling_rate = 0

    # Loaders
    def load_file(self, file_path):
        """Loads an HDF5 file. The HDF5 file must have been formatted by DataFormatter.

           Args:
               file_path: The path of the HDF5 file.
        """
        self.f = h5py.File(file_path)
        self.sampling_rate = int(self.f['raw_data'].attrs['sampling_rate'])
        print "File " + `file_path` +  " has been loaded."

    def load_dataset(self, dataset_name, group_name = None, rename = None, save = False):
        """Loads the dataset from the HDF5 file into a temporary group 'tmp' and stages it.

           Args:
               dataset_name: The name of the dataset to be loaded.
               group_name: The group of the dataset to be loaded.
               rename: The name the staged dataset is renamed as. The default rename is a time-stamped name.
               save: The option to save the loaded dataset. By default loaded datasets are copied into a 
                     temporary group 'tmp' that is wiped on system exit. Saved datasets are moved into the 
                     'data_analysis' group.
        """
        if self.f == None:
            print "There is no file currently loaded."
            return

        # Only create groups if you're going to populate them/delete them on exit - ran into some bugs with empty groups
        self.f.require_group("tmp")
        if save: self.f.require_group("data_analysis") 

        destination_group_name = "data_analysis" if save else "tmp"
        rename = str(datetime.datetime.now()) if rename is None else rename

        if group_name is not None:
            if group_name in self.f and dataset_name in self.f[group_name]:
                try:
                    # TODO Group name might be multi-level now, also group_name formatting
                    self.f.copy("/" + group_name + "/" + dataset_name, "/" + destination_group_name + "/" + rename)
                except:
                    print "Could not load dataset."
                    return
            elif not group_name in self.f:
                print "Group " + group_name + " is not found in the file."
                return
            else:
                print "Dataset " + dataset_name + " is not found in group " + group_name + "."
                return
        elif dataset_name in self.f:
            try:
                self.f.copy("/" + dataset_name, "/" + destination_group_name + "/" + rename)
            except:
                print "Could not load dataset."
                return
        else:
            print "Dataset " + dataset_name + " is not found in the root level."
            return
        self.staged_dataset = self.f[destination_group_name][rename]
        print "Dataset " + dataset_name + " loaded and staged as " + rename + "."

    def save_dataset(self, rename = None):
        """Moves the staged dataset to the 'data_analysis' group and re-stages the moved dataset. 

           Args:
               rename: The name the saved dataset is renamed as. The default rename is the current 
                       staged dataset name.
        """
        # TODO: Create a subgroup?
        if self.f == None:
            print "There is no file loaded."
            return
        elif self.staged_dataset == None:
            print "There is no dataset staged."
            return
        previous_name = ''.join(self.staged_dataset.name.split('/')[-1:])
        rename = previous_name if rename is None else rename
        self.f.require_group("data_analysis")
        try:
            self.f.move(self.staged_dataset.name, '/data_analysis/' + rename)
        except:
            print "Could not save dataset."
            return
        if rename is None:
            print "Dataset " + previous_name + " saved."
        else:
            print "Dataset " + previous_name + " saved and renamed " + rename + "."
        self.stage_dataset('data_analysis', rename)

    def rename_dataset(self, rename):
        """Renames the staged dataset."""
        if self.f == None:
            print "There is no file loaded."
            return
        elif self.staged_dataset == None:
            print "There is no dataset staged."
            return
        previous_name = ''.join(self.staged_dataset.name.split('/')[-1:])
        try:
            self.f.move(self.staged_dataset.name, '/'.join(self.staged_dataset.name.split('/')[:-1]) + '/' + rename)
        except:
            print "Could not rename dataset."
            return
        print "Dataset " + previous_name + " renamed " + rename + "."

    def stage_dataset(self, group_name, dataset_name):
        """Stages dataset. This function should NOT be used to load datasets from the HDF5 file, load_dataset() does that.
           This function is used to stage datasets in the 'tmp' or 'data_analysis' groups."""
        if self.f == None:
            print "There is no file loaded."
            return
        elif group_name != "tmp" and group_name != "data_analysis":
            print "You can only stage datasets in the 'tmp' or 'data_analysis' groups."
        self.staged_dataset = self.f[group_name][dataset_name]
        print "Dataset " + dataset_name + " staged."

    def isolate_time_range(self,time_range):
        """Isolates the staged dataset based on the range.

           Args:
               time_range: A size 2 array representing the inclusive time range in seconds to be isolated. The first element 
               is the beginning of the time range and the second element is the end of the time range.
        """
        if len(time_range) > 2 or time_range[0] < 0 or time_range[1] <= 0:
            print "Malformed time_range. time_range must be size 2."
            return
        converted_time_range = [int(time * self.sampling_rate) for time in time_range]
        if converted_time_range[0] == converted_time_range[1]:
            print "Time range is not large enough given the sampling rate. The time range must span more than one datapoint."
            return
        if 'time_range' in self.staged_dataset.attrs:
            converted_existing_time_range = [int(time * self.sampling_rate) for time in self.staged_dataset.attrs['time_range']]
            if converted_time_range[0] < converted_existing_time_range[0] or converted_time_range[1] > converted_existing_time_range[1]:
                print "Time range is outside dataset."
                return
            converted_time_range = [converted_time_range[0] - converted_existing_time_range[0], converted_time_range[1] - converted_existing_time_range[0]]
        self.staged_dataset.attrs['time_range'] = time_range
        sliced = self.staged_dataset[converted_time_range[0]:converted_time_range[1]+1]
        self.staged_dataset.resize(sliced.shape) # TODO: NEED CHUNKED DATASETS TO RESIZE
        self.staged_dataset.write_direct(sliced)
        self.f.flush()
        print "Dataset isolated based on time range."

    def run_analysis(self, fun, **kwargs):
        """Runs an analysis function on the current dataset.

           Args:
               fun: The analysis function to be run. Must take a dictionary of parameters as input.
                    The keys of the parameter dictionary are the same as the optional arguments that represent them.
               kwargs: Optional arguments specifying the requirements of the analysis function.
                       The optional arguments, values and descriptions are as follow:
                           sampling_rate(True) - The function requires the sampling rate of the dataset.
                           save(dataset_name) - A new dataset is created at that location for the analysis function to write to.
                           user_args(dictionary) - A dictionary of user supplied arguments.
        """
        if self.staged_dataset is None:
            print "There is no staged dataset. Analysis aborted."
            return
        params = {'data': self.staged_dataset}
        if 'sampling_rate'in kwargs:
            if self.sampling_rate == 0:
                print "Sampling rate not set. Analysis aborted."
                return
            params['sampling_rate'] = self.sampling_rate
        if 'save' in kwargs:
            try:
                params['save'] = self.f['data_analysis'].create_dataset(kwargs['save'], self.staged_dataset.shape, dtype=self.staged_dataset.dtype)
            except:
                print "Could not save analysis results in specified dataset name."
                return
        if 'user_args' in kwargs:
            params['user_args'] = kwargs['user_args']
        try:
            fun(params)
            self.f.flush()
        except:
            print "Exception in function."
        
# Sample analysis method
def high_demo_filter(params):
    results = params['save']
    data = params['data']
    freq = params['sampling_rate']
    print "Processing dataset. Please wait..."
    for i in range(len(data)):
        if i % (len(data)/10) == 0:
            print (i/(len(data)/10)).__repr__()+"0% complete."
        if abs(data[i]) < freq:
            results[i] = 0
        else:
            results[i] = data[i]
    return results
