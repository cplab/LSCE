import Importer
import DataFormatter
import datavisualization
import getopt
import sys
import h5py
import os
from matplotlib import pyplot as plt


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


def main(argv=None):
    Importer.loadFromRaw("E:\\LSCE\\110112")
    DataFormatter.formatData("E:\\LSCE\\110112\\slice2_", "fulldata")
    tmp = h5py.File("fulldata.hdf5", "r+")
    data = []
    for dataset in tmp["raw_data"].keys():
    	data.append(tmp["raw_data"][dataset])
    	print tmp["raw_data"][dataset][0]
    print data
    print data[0][1][0]
    print (data[0][1][0]+5).__repr__()
    datavisualization.analyze8x8data(data=data, samprate=1000, time=5)
    tmp.close()
if __name__ == "__main__":
    sys.exit(main())
