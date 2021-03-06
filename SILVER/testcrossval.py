__author__ = 'sina'

import numpy
import imputemat
import statistics
from matplotlib import pyplot
import pprint
import json

def main():
    results = numpy.load("CS2440.1/crossvalout/k1_goback0svd_estimate_vectors.npz")
    print results.files
    data0 = numpy.reshape(results['estimate_vector0'], (-1, 1))
    data1 = numpy.reshape(results['estimate_vector1'], (-1, 1))
    data2 = numpy.reshape(results['estimate_vector2'], (-1, 1))
    data3 = numpy.reshape(results['estimate_vector3'], (-1, 1))
    data4 = numpy.reshape(results['estimate_vector4'], (-1, 1))
    data5 = numpy.reshape(results['estimate_vector5'], (-1, 1))
    data6 = numpy.reshape(results['estimate_vector6'], (-1, 1))
    data7 = numpy.reshape(results['estimate_vector7'], (-1, 1))
    data8 = numpy.reshape(results['estimate_vector8'], (-1, 1))
    data9 = numpy.reshape(results['estimate_vector9'], (-1, 1))
    actual = numpy.reshape(results['actual_vector'], (-1, 1))
    actual = numpy.reshape(actual, (-1, 1))

    performance0 = imputemat.rootmeansquared(data0, actual)
    print performance0
    performance1 = imputemat.rootmeansquared(data1, actual)
    print performance1
    performance2 = imputemat.rootmeansquared(data2, actual)
    print performance2
    performance3 = imputemat.rootmeansquared(data3, actual)
    print performance3
    performance4 = imputemat.rootmeansquared(data4, actual)
    print performance4
    performance5 = imputemat.rootmeansquared(data5, actual)
    print performance5
    performance6 = imputemat.rootmeansquared(data6, actual)
    print performance6
    performance7 = imputemat.rootmeansquared(data7, actual)
    print performance7
    performance8 = imputemat.rootmeansquared(data8, actual)
    print performance8
    performance9 = imputemat.rootmeansquared(data9, actual)
    print performance9

    average = float(performance0 + performance1 + performance2 + performance3 + performance4 + performance5 +
                      performance6 + performance7 + performance8 + performance9) / 10

    print "*************"
    print average
    results2 = numpy.load("CS2440.1/crossvalout/k1_goback0svd_result_matrices.npz")
    print results2.files
    activities = results2['activity_list']
    print len(activities)
    target_column = list(activities).index("C S 2440.1")
    print target_column
    resultant1 = results2['result_matrix0']
    from matplotlib import pyplot as plt
    plt.plot(data0)
    plt.plot(resultant1[:,target_column])
    plt.show()

    debug_mode = True
    if debug_mode:
        print "==== mean ===="
        print numpy.mean(actual)
        numpy.set_printoptions(threshold=numpy.nan)
        print "** std deviation **"
        print numpy.std(actual)

    """
    studentmap = loadjson("../preprocessing/CSDataFile_ForParry_2014Nov26_studentdict.json")
    print studentmap["1400013"]["C S 2440"]
    """


"""
    loadjson - method that loads a json object from memory and returns it.
"""
def loadjson(filename):
        f = open(filename,"rb")
        j = json.loads(open(filename).read())
        f.close()
        return j


if __name__ == "__main__":
    try:
        main()

    except IOError as e:
        print e.strerror
        exit(-1)