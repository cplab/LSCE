import scipy
from scipy import signal
import h5py

def low_pass_filter(params):
    """A sample low pass filter using scipy's signal processing functions.

           Args:
               params: A dictionary of parameters passed by the method run_analysis.
                       params will always include a 'data' entry, whose value is an h5py dataset.
                       Other optional entries include 'sampling_rate', 'user_args' and 'save'. Refer
                       to the run_analysis docstring for more detail.

                       The process of writing to datasets is left to the user-defined function.
                       In this example the h5py method write_direct is used. If the 'save' option is 
                       specified in run_analysis a new dataset is created and passed in through params
                       under the entry 'save'. The user-defined function can then write to it.
    """
    data = params['data']
    print "Processing dataset. Please wait..."

    (N, Wn) = signal.buttord(wp=.2, ws=.3, gpass=2, gstop=30, analog=0)
    (b, a) = signal.butter(N, Wn, 'low')
    result = scipy.signal.lfilter(b, a, data)
    data.write_direct(result)
    return result
