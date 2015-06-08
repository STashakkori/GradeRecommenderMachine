from matplotlib import mlab
import operator

__author__ = 'sina'
__project__ = 'STProject'

import colorama
from termcolor import colored
import cPickle
import numpy
import time
import scipy.stats as stats
import matplotlib.pyplot as plt
from collections import OrderedDict
import math

'''
    main
'''
def main(argv):
    colorama.init(autoreset=True)
    print(colored("mat2hist","blue"))
    if argv[0] and argv[0].endswith(".npy"):
        if argv[1]:
            g,d,c = loaddatastructures()
            entry = getentry(g,d,c,argv[1])
            if entry.any():
                # Begin working here. Need to now pass the slice of the matrix to the histogrammer.
                plothistogram(entry,argv[1])

            else:
                print(colored("mat2hist ==> ERROR --> Bad entry input ~~> course name or dummieid not in records","red"))
        else:
            print(colored("mat2hist ==> ERROR --> Bad entry input ~~> course name or dummieid required","red"))
            exit(1)

    else:
        print(colored("mat2hist ==> ERROR --> Bad filename input ~~> .npy required","red"))
        exit(1)

def loaddatastructures():
    grademat = numpy.load("preprocessing/CSDataFile_ForParry_2014Nov26_grademat.npy")
    dummieidgrid = loadcpickle("preprocessing/CSDataFile_ForParry_2014Nov26_dummieidgrid.cPickle")
    coursegrid = loadcpickle("preprocessing/CSDataFile_ForParry_2014Nov26_coursegrid.cPickle")
    return grademat,dummieidgrid,coursegrid

def loadcpickle(filename):
    f = open(filename,"rb")
    cp = cPickle.load(f)
    f.close()
    return cp

def getentry(grademat,dummieidgrid,coursegrid,input):
    templist = numpy.empty(0)
    for i in range(0,len(dummieidgrid)):
        for j in range(0,len(dummieidgrid[i])):
            if dummieidgrid[i][j] == input:
                for x in grademat[i]: templist = numpy.append(templist,x)
                return templist

            elif coursegrid[i][j] == input:
                templist = numpy.append(templist,grademat[i][j])

    return templist

def calculatemode(matrix):
    return stats.mode(matrix)[0][0]

def calculatemean(matrix):
    return numpy.nanmean(matrix)

def calculatemedian(matrix):
    return numpy.nanmedian(matrix)

def calculatevariance(matrix):
    return numpy.nanvar(matrix)

def countrecords(matrix):
    return matrix.shape[0]

def countstudents(matrix):
    return numpy.count_nonzero(~numpy.isnan(matrix))

def calculatepercentaboveac(matrix,numberofstudents):
    count = matrix[(~numpy.isnan(matrix))]
    count = count[(count > 5.0)]
    count = count.shape[0]
    return (float(count) / float(numberofstudents)) * 100

def calculatepercentaboveac(matrix,numberofstudents):
    count = matrix[(~numpy.isnan(matrix))]
    count = count[(count > 5.0)]
    count = count.shape[0]
    return (float(count) / float(numberofstudents)) * 100

def calculatepercentpassing(matrix,numberofstudents):
    count = matrix[(~numpy.isnan(matrix))]
    count = count[(count > 0.0)]
    count = count.shape[0]
    return (float(count) / float(numberofstudents)) * 100

def plothistogram(matrix,title):
    mean = calculatemean(matrix)
    median = calculatemedian(matrix)
    mode = calculatemode(matrix)
    variance = calculatevariance(matrix)
    records = countrecords(matrix)
    students = countstudents(matrix)
    percentabovec = calculatepercentaboveac(matrix,students)
    percentpassing = calculatepercentpassing(matrix,students)
    gradelist = twelvepointnumericlisttogrades(matrix)
    countsmap = countsmapper(gradelist)
    X = numpy.arange(len(countsmap))
    plt.bar(X, countsmap.values(), align='center', width=0.5)
    plt.xticks(X, countsmap.keys())
    plt.autoscale(enable=True, axis=u'x', tight=None)
    plt.title("Letter Grade Histogram of " + title)
    plt.xlabel('Grades')
    plt.ylabel('Occurrences')
    plt.gca().set_position((.1, .3, .8, .6))
    plt.figtext(.04,.19,"Number of records: " + str(records), fontsize=10)
    plt.figtext(.04,.16,"Number of students: " + str(students), fontsize=10)
    plt.figtext(.04,.13,"Mean: " + str(mean), fontsize=10)
    plt.figtext(.04,.10,"Median: " + str(median), fontsize=10)
    plt.figtext(.04,.07,"Mode: " + str(mode), fontsize=10)
    plt.figtext(.04,.04,"Percent above a C: " + str(percentabovec) + "%", fontsize=10)
    plt.figtext(.04,.01,"Percent passing: " + str(percentpassing) + "%", fontsize=10)
    y = countsmap[max(countsmap.iteritems(), key=operator.itemgetter(1))[0]]
    x = numpy.linspace(0,len(countsmap)-1,1000)
    sigma = math.sqrt(variance)
    plt.plot(x,y * mlab.normpdf(x,mean,sigma),'-r',linewidth=2)
    figure = plt.gcf()
    plt.show()
    timestring = time.strftime("%Y%m%d-%H%M%S")
    figure.savefig("figures/histogram-" + timestring)

def countsmapper(list):
        countmap = OrderedDict([("A",0),("A-",0),("B+",0),("B",0),("B-",0),("C+",0),("C",0),("C-",0),("D+",0),("D",0),("D-",0),("F",0)])
        for item in list:
                countmap[item] = countmap.setdefault(item, 0) + 1

        return countmap

def twelvepointnumericlisttogrades(matrix):
    newlist = []
    for grade in matrix:
        if not numpy.isnan(grade):
            newlist.append(twelvepointgradenumerictoletter(grade))

    return newlist

def twelvepointgradenumerictoletter(gradenumber):
        if gradenumber == 0.0:
            return "F"

        elif gradenumber == 2.0:
            return "D-"

        elif gradenumber == 3.0:
            return "D"

        elif gradenumber == 4.0:
            return "D+"

        elif gradenumber == 5.0:
            return "C-"

        elif gradenumber == 6.0:
            return "C"

        elif gradenumber == 7.0:
            return "C+"

        elif gradenumber == 8.0:
            return "B-"

        elif gradenumber == 9.0:
            return "B"

        elif gradenumber == 10.0:
            return "B+"

        elif gradenumber == 11.0:
            return "A-"

        elif gradenumber == 12.0:
            return "A"

if __name__ == "__main__":
    t0 = time.time()
    main(["preprocessing/CSDataFile_ForParry_2014Nov26_grademat.npy","C S 1440"])
    t1 = time.time()
    totaltime = t1 - t0
    print(colored("mat2hist =~> " + str(totaltime) + " seconds.","yellow"))