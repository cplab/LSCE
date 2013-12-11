import Importer
import DataFormatter
import datavisualization
import h5py
import sys

"""
Usage:

Linux/UNIX/POSIX: 
$ python fullrun.py /path/to/datadir /path/to/newhdf5file

Windows:
$ python.exe fullrun.py C:\\path\\to\\rawdata  C:\\path\\to\\newhdf5file

"""

def main(argv=None):
    #Importer.loadFromRaw(argv[1], numFiles = 2)
    DataFormatter.formatData('.', argv[2])
    tmp = h5py.File("{0}.hdf5".format(argv[2]), "r+")
    data = []
    for dataset in tmp["raw_data"].keys():
        data.append(tmp["raw_data"][dataset])
        print tmp["raw_data"][dataset][0]
    datavisualization.analyze8x8data(data=data, samprate=20000, time=2)
    tmp.close()

if __name__ == "__main__":
    sys.exit(main(argv=sys.argv))
