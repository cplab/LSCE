import Importer
import DataFormatter
import DataAnalysis
import getopt
import sys
import h5py
import os
from matplotlib import pyplot as plt


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


def main(argv=None):
    if argv is None:
        argv = sys.argv
    run_importer = True
    run_formatter = True
    run_analysis = True
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "h", ["help", "skip-importer", "skip-formatter", "skip-analysis"])
            print "got args"
        except getopt.error, msg:
                raise Usage(msg)
        for option, data in opts:
            if('-h' == option or '--help' == option):
                print "LSCE test script. Usage: \"python testscript.py [--skip-importer] [--skip-formatter] [--skip-analysis]" +\
                    " mat_source hdf5_dest" +\
                    "\"\n\nSupply the following arguments to run pipeline:\n\n\tmat_source: " +\
                    "The path to the raw .mat files to be imported.\n\thdf5_dest: the name to save hdf5 output file under" +\
                    "\n\nAvailable modes:\n\t--skip-importer: skip importation step. Formatter wil still run using" +\
                    " mat_source as src directory." +\
                    "\n\t--skip-formatter: skip formatting step. Importer will use mat_source as usual. \n\t\t\t  Analysis will" +\
                    " use hdf5_dest if it exists." + \
                    "\n\t--skip-analysis: skip computation of analysis data. Formatter will still output to hdf5_dest. "
                return
            if('--skip-importer' == option):
                run_importer = False
            if('--skip-formatter' == option):
                run_formatter = False
            if('--skip-analysis' == option):
                run_analysis = False
        if(len(args) < 2):
            raise Usage("Insufficient arguments supplied.")
        else:
            print args.__repr__()
        print "Welcome to LSCE test script.\nThis script will perform a " + \
            "complete iteration of our pipeline, starting with the data importer."
        if(run_importer):
            print "Importing data from directory "+args[0]
            Importer.loadFromMat(args[0])
        else:
            print "Skipped importing data."
        if(run_formatter):
            print "Formatting data as hdf5 in "+args[1]+".hdf5"
            DataFormatter.formatData(args[0], args[1])
        else:
            print "Skipped formatting data."
        os.system("PAUSE")
        testing = None
        raw_data = None
        if(run_analysis):
            dtool = DataAnalysis.data_analysis()
            dtool.load_hdf5(args[1], dataset_name="Electrode_12_master", group_name="raw_data")
            dtool.sampling_rate = 1000
            testing = dtool.high_demo_filter(20)
            raw_data = dtool.f["raw_data"]["Electrode_12_master"]
        else:
            print "Skipped data analysis.\nPlaceholder groups " + \
                "\"/data_analysis/demo_filter_results\" and \"/raw_data/Electrode_12_master\" will be used."
            hdfile = h5py.File(args[1]+".hdf5", "r+")
            if("data_analysis" not in hdfile or "demo_filter_results" not in hdfile["data_analysis"]):
                print "Skipping graphs..."
                return
            testing = hdfile["data_analysis"]["demo_filter_results"]
            raw_data = hdfile["raw_data"]["Electrode_12_master"]
        os.system("PAUSE")
        plt.subplot(2, 1, 1)
        plt.plot(testing)
        plt.subplot(2, 1, 2)
        plt.plot(raw_data)
        plt.show()
        if(run_analysis):
            dtool.close()
    except Usage, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, "For help use --help"
        return 2

if __name__ == "__main__":
    sys.exit(main())
