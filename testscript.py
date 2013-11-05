import Importer
import DataFormatter
import DataAnalysis
import collections
import getopt
import sys
import os
from matplotlib import pyplot as plt


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


def is_func(instance, func):
    return isinstance(getattr(instance, func, None), collections.Callable)


def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "h", ["help"])
        except getopt.error, msg:
                raise Usage(msg)
        for option, data in opts:
            if('-h' == option or '--help' == option):
                print "LSCE test script. Usage: \"python testscript.py mat_source hdf5_dest" + \
                    "\"\n\nSupply the following arguments to run pipeline:\n\n\tmat_source: " + \
                    "The path to the raw .mat files to be imported.\n\thdf5_dest: the name to save hdf5 output file under"
            return
        if(len(args) < 2):
            raise Usage("Insufficient arguments supplied.")
        else:
            print args.__repr__()
        #Importer.loadFromMat(args[0])
        hdfile = DataFormatter.formatData(args[0], args[1])
        #print "Press any key to continue..."
        os.system("PAUSE")
        hdfile.close()
        dtool = DataAnalysis.data_analysis()
        dtool.load_hdf5(args[1], dataset_name="Electrode_12_master", group_name="raw_data")
        dtool.sampling_rate = 1000
        dtool.high_pass_filter(42)

        plt.subplot(2, 1, 1)
        plt.plot(dtool.data)
        plt.subplot(2, 1, 2)
        plt.plot(dtool.f["raw_data"]["Electrode_12_master"])
        plt.show()
        dtool.close()
    except Usage, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, "For help use --help"
        return 2

if __name__ == "__main__":
    sys.exit(main())
