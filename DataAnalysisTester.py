import DataAnalysis
import h5py
import math, numpy
from matplotlib import pyplot

samp_rate = 20
sim_time = 60
nsamps = samp_rate*sim_time
cuttoff_freq = 0.1

fig = pyplot.figure()

t = numpy.linspace(0, sim_time, nsamps)
freqs = [0.1, 0.5, 1, 4]
x = 0
for i in range(len(freqs)):
  x += numpy.cos(2*math.pi*freqs[i]*t)
time_dom = fig.add_subplot(232)

fig.add_subplot(233)
pyplot.plot(t, x)
# pyplot.ylim([-5,5])
pyplot.title('Filter Input - Time Domain')
pyplot.grid(True)

f = h5py.File("test.hdf5", "w")

dset = f.create_dataset("test", data= x)
f.flush()
f.close()

da = DataAnalysis.data_analysis()
da.load_hdf5("test", "test", dataset_rename="test")
da.high_pass_filter(samp_rate, order= 7)


fig.add_subplot(236)
pyplot.plot(t, da.data)
pyplot.title('Filter Output - Time Domain')
pyplot.grid(True)

pyplot.show()
