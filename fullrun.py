import Importer
import DataFormatter
import datavisualization
import h5py
import sys

def main(argv=None):
    Importer.loadFromRaw("E:\\LSCE\\Demo", numFiles = 2)
    DataFormatter.formatData("E:\\LSCE\\Demo\\slice2_", "E:\\LSCE\\demodata")
    tmp = h5py.File("fulldata.hdf5", "r+")
    data = []
    for dataset in tmp["raw_data"].keys():
        data.append(tmp["raw_data"][dataset])
        print tmp["raw_data"][dataset][0]
    datavisualization.analyze8x8data(data=data, samprate=20000, time=2)
    tmp.close()
if __name__ == "__main__":
    sys.exit(main())
