import Importer
import DataFormatter
import datavisualization
import sys
import h5py


def main(argv=None):
    Importer.loadFromRaw("E:\\LSCE\\Demo")
    DataFormatter.formatData("E:\\LSCE\\Demo\\slice2_", "fulldata")
    tmp = h5py.File("fulldata.hdf5", "r+")
    data = []
    for dataset in tmp["raw_data"].keys():
    	data.append(tmp["raw_data"][dataset])
    	print tmp["raw_data"][dataset][0]
    datavisualization.analyze8x8data(data=data, samprate=1000, time=5)
    tmp.close()
if __name__ == "__main__":
    sys.exit(main())
