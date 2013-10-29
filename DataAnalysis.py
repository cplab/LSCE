from numpy import *
from scipy import signal

import h5py

class DataAnalysis:
  
  def __init__(self, data = array([]), sampling_rate = 0):
    self.data = data # Consider multiple data sets - perhaps a dictionary?
    self.sampling_rate = sampling_rate # Hertz

  def data_initialized(self):
    """Returns true or false depending on if the data is initialized."""
    return self.data.size != 0 and self.sampling_rate > 0

  # Loaders
  def load_hdf5(self, file, dataset_name, group_name=None):
    """Loads data from an HDF5 file to be analyzed."""
    # Once the file format is standardized the method implementation will become more clear
    dataset = None
    with h5py.File(file) as f:
      if group_name is not None:
        dataset = f[group_name][dataset_name]
      else:
        dataset = f[dataset_name] # No group by default, double-check with Nick
      self.data = np.array(dataset)

  def load_array(self,array):
    """Loads data from a Numpy array."""
    # Sampling rate to be determined somehow
    self.data = array

  def load_npy(self,file_path):
    """Loads data from an NPY file"""
    # Sampling rate to be determined somehow
    self.data = numpy.load(file_path)

  # Analysis methods
  def high_pass_filter(self,filter_freq,channels,order=5):
    """Performs a high pass (by default) 5th order Butterworth filter on self.data"""
    if not data_initialized():
      print "Data not initialized!"
      break

    # The order of the filter should be determined in production. Maybe a parameter?
    b, a = signal.butter(order, filter_freq / (self.sampling_rate/2.), btype='high') # Normalized to Nyquist frequency

    return signal.lfilter(b, a, self.data)
    
  def low_pass_filter(self, filter_freq, channels):
    """Performs a low-pass filter on self.data"""
    if not data_initialized():
      print "Data not initialized!"
      break
    
    # TODO: Figure out what to use as cutoff
    b, a = signal.firwin(self.filter_freq, cutoff = None, window = "hamming")
    
    return signal.lfilter(b, a, self.data)
