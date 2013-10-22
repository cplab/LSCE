from numpy import *
from scipy import signal

class DataAnalysis:
  def __init__(self):
    self.data = array([]) # Consider multiple data sets - perhaps a dictionary?
    self.sampling_rate = 0 # Hertz

  def data_initialized(self):
    """Returns true or false depending on if the data is initialized."""
    return self.data.size != 0 and self.sampling_rate > 0

  # Loaders
  def load_hdf5(self,file):
    """Loads data from an HDF5 file to be analyzed."""
    # Once the file format is standardized the method implementation will become more clear
    self.data = array(range(10)) # Temporary for now

  def load_array(self,array):
    """Loads data from a Numpy array."""
    # Sampling rate to be determined somehow
    self.data = array

  def load_npy(self,file_path):
    """Loads data from an NPY file"""
    # Sampling rate to be determined somehow
    self.data = numpy.load(file_path)

  # Analysis methods
  def high_pass_filter(self,filter_freq,channels):
    """Performs a high pass 5th order Butterworth filter on self.data"""
    if not data_initialized():
      print "Data not initialized!"
      break

    # The order of the filter should be determined in production. Maybe a parameter?
    b, a = signal.butter(5, filter_freq / (self.sampling_rate/2.), btype='high') # Normalized to Nyquist frequency

    return signal.lfilter(b, a, self.data)
