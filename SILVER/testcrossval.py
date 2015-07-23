__author__ = 'sina'

import numpy
import imputemat
import statistics
from matplotlib import pyplot

def main():
    numpy.set_printoptions(threshold=numpy.nan)
    results = numpy.load("CS2440.1/crossvalout/k3_gobackgo_back0_estimate_vectors.npz")
    data0 = results['estimate_vector0']
    data1 = results['estimate_vector1']
    data2 = results['estimate_vector2']
    data3 = results['estimate_vector3']
    data4 = results['estimate_vector4']
    data5 = results['estimate_vector5']
    data6 = results['estimate_vector6']
    data7 = results['estimate_vector7']
    data8 = results['estimate_vector8']
    data9 = results['estimate_vector9']
    actual = results['actual_vector']
    mean_estimate_vector = (numpy.array(data0) + numpy.array(data1) + numpy.array(data2) + numpy.array(data3)
                            + numpy.array(data4) + numpy.array(data5) + numpy.array(data6) + numpy.array(data7)
                            + numpy.array(data8) + numpy.array(data9)) / 10

    debug_mode = False
    if debug_mode:
        print "** std deviation **"
        print numpy.std(actual)
        print "** mean **"
        print statistics.mean(actual)
        print(actual)
        pyplot.hist(mean_estimate_vector)
        pyplot.show()

    mean_estimate_vector = numpy.reshape(mean_estimate_vector, (-1, 1))
    actual = numpy.reshape(actual, (-1, 1))
    print imputemat.rootmeansquared(mean_estimate_vector, actual)

if __name__ == "__main__":
    try:
        main()

    except IOError as e:
        print e.strerror
        exit(-1)