from numpy import *
from scipy import signal
import datetime

import h5py

class data_analysis(object):
  """Sandbox for data analysis on a dataset."""
  
  def __init__(self, filename = None, dataset_name = None, group_name = None):
    self.f = None
    self.data = None # Consider multiple data sets - perhaps a dictionary?
    self.sampling_rate = 2 # Hertz

    if filename is not None and dataset_name is not None:
      self.load_hdf5(filename, dataset_name, group_name)
    elif filename is not None:
      self.f = h5py.File(filename+".hdf5", "a")

  def close(self):
    self.f.close()

  def data_initialized(self):
    """Returns true or false depending on if the data initialized."""
    return self.data != None and self.sampling_rate > 0

  # Loaders
  def load_hdf5(self, filename, dataset_name, group_name=None, dataset_rename=None):
    """Loads data from an HDF5 file to be analyzed."""
    self.f = h5py.File(filename+".hdf5", "a")
    self.f.require_group("data_analysis")

    if dataset_rename is None:
      dataset_rename = str(datetime.datetime.now())

    if group_name is not None:
      if group_name in self.f and dataset_name in self.f[group_name]:
        self.f.copy("/" + group_name + "/" + dataset_name, "/data_analysis/" + dataset_rename)
      elif not group_name in self.f:
        print "Group " + group_name + " is not found in the file."
        return
      else:
        print "Dataset " + dataset_name + " is not found in group " + group_name + "."
        return
    elif dataset_name in self.f:
      self.f.copy("/" + dataset_name, "/data_analysis/" + dataset_rename)
    else:
      print "Dataset " + dataset_name + " is not found in the root level."
      return
    self.data = self.f["data_analysis"][dataset_rename]
    print "Dataset " + dataset_rename + " created and staged."

  # Analysis methods
  # TODO Really a low pass filter
  def high_pass_filter(self,filter_freq,channels= 1,order=5):
    """Performs a high pass (by default) 5th order Butterworth filter on self.data"""
    if not self.data_initialized():
      print "Data not initialized!"
      return

    # The order of the filter should be determined in production. Maybe a parameter?
    b, a = signal.butter(order, filter_freq / (self.sampling_rate/2.), btype='low') # Normalized to Nyquist frequency

    self.data = signal.lfilter(b, a, self.data)
    self.f.flush()
    
  # TODO FIX THIS SHIT  
  def low_pass_filter(self, filter_freq, channels= 1):
    """Performs a low-pass filter on self.data"""
    if not self.data_initialized():
      print "Data not initialized!"
      return
    
    # TODO: Figure out what to use as cutoff
    b, a = signal.firwin(filter_freq, cutoff = None, window = "hamming")
    
    self.data = signal.lfilter(b, a, self.data)
    self.f.flush()
