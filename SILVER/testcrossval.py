__author__ = 'sina'

import numpy

def main():
    results = numpy.load("CS2440.1/crossvalin/_output/go_back0/iteration1.npz")
    data = results['fold1']
    groupings = results['groupings']
    a = list(results['activity_list'])
    s = list(results['student_list'])
    r = s.index("1400002")
    c = a.index("C S 2440.1")
    print data[r][c]
    print data[r][c + 1]
    print data[r][c - 1]
    print data[r][c - 2]
    print data[r][c - 3]
    print groupings
    print "**************"

    results = numpy.load("CS2440.1/crossvalin/_output/go_back0/iteration1.npz")
    data = results['fold2']
    groupings = results['groupings']
    print data[r][c]
    print data[r][c + 1]
    print data[r][c - 1]
    print data[r][c - 2]
    print data[r][c - 3]
    print groupings
    print "**************"

    results = numpy.load("CS2440.1/crossvalin/_output/go_back0/iteration1.npz")
    data = results['fold3']
    groupings = results['groupings']
    print data[r][c]
    print data[r][c + 1]
    print data[r][c - 1]
    print data[r][c - 2]
    print data[r][c - 3]
    print groupings
    print "**************"

    results = numpy.load("CS2440.1/crossvalin/_output/go_back0/iteration2.npz")
    data = results['fold1']
    groupings = results['groupings']
    print data[r][c]
    print data[r][c + 1]
    print data[r][c - 1]
    print data[r][c - 2]
    print data[r][c - 3]
    print groupings
    print "**************"

    results = numpy.load("CS2440.1/crossvalin/_output/go_back0/iteration2.npz")
    data = results['fold2']
    groupings = results['groupings']
    print data[r][c]
    print data[r][c + 1]
    print data[r][c - 1]
    print data[r][c - 2]
    print data[r][c - 3]
    print groupings
    print "**************"

    results = numpy.load("CS2440.1/crossvalin/_output/go_back0/iteration2.npz")
    data = results['fold3']
    groupings = results['groupings']
    print data[r][c]
    print data[r][c + 1]
    print data[r][c - 1]
    print data[r][c - 2]
    print data[r][c - 3]
    print groupings
    print "**************"

if __name__ == "__main__":
    main()