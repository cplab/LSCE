import Importer
import DataFormatter
import DataAnalysis
import collections
import getopt
import sys


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
                print "LSCE test script. Usage: \"python testscript.py mat_source hdf5_dest " + \
                    "\"\n\nSupply the following arguments to run pipeline:\n\tmat_source: " + \
                    "The path to the raw .mat files to be imported.\n\thdf5_dest: the name to save hdf5 output file under"
            return
        if(len(args) < 2):
            raise Usage("Insufficient arguments supplied.")
        else:
            print args.__repr__()
        Importer.loadFromMat(args[1])
        DataFormatter.formatData(args[1], args[2])
    except Usage, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, "For help use --help"
        return 2

if __name__ == "__main__":
    sys.exit(main())
