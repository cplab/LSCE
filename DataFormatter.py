import scipy.io
import numpy as np
import h5py

def formatData(fileDir, *options):
	"""Loads raw numpy arrays from a folder and saves them in hdf5 file format. Tagging information about the arrays may be supplied
	   	in a seperate file.

		Args:
			fileDir: A root directory containing one or more numpy files.
			*options: An optional list of command-line switches or paths to additional files containing tagging information
	"""
	