#!/usr/bin/python

"""
    mat2hist.py - script that reads a .csv file filled with grades, gpas, and exams scores and creates two dictionary
                  datastructures, one for indexing via a student's dummieid and one for indexing via a course name.
                  Once created, the dictionaries are stored in memory.
"""

__author__ = 'sina'
__project__ = 'STProject'

from matplotlib import mlab
import operator
import colorama
from termcolor import colored
import cPickle
import numpy
import time
import scipy.stats as stats
import matplotlib.pyplot as plt
from collections import OrderedDict
import math
import sys

'''
    main - main method of the mat2hist program.
        :param argv1: command line argument -> the filename for the .npy matrix in memory.
        :type argv1: string
        :param argv2: command line argument -> the dummieid or the coursename to be histogrammed.
        :type argv2: string
'''
def main(argv1,argv2):
    colorama.init(autoreset=True)
    print(colored("mat2hist","blue"))
    if argv1 and argv1.endswith(".npy"):
        if argv2:
            g,d,c = loaddatastructures(argv1)
            entry,flag = getentry(g,d,c,argv2)
            if entry.any():
                plothistogram(entry,flag,argv2)

            else:
                print(colored("mat2hist ==> ERROR --> Bad entry input ~~> course name or dummieid not in records","red"))
        else:
            print(colored("mat2hist ==> ERROR --> Bad entry input ~~> course name or dummieid required","red"))
            exit(1)

    else:
        print(colored("mat2hist ==> ERROR --> Bad filename input ~~> .npy required","red"))
        exit(1)

"""
    loaddatastructures - method that loads the numpy matrix gradematrix along with the 2d lists dummieid and courseid
                         out of memory into datastructures and returns them.
"""
def loaddatastructures(matrixfilename):
    gradematrix = numpy.load(matrixfilename)
    dummieidgrid = loadcpickle(matrixfilename.replace("_grademat.npy","_dummieidgrid.cPickle"))
    coursegrid = loadcpickle(matrixfilename.replace("_grademat.npy","_coursegrid.cPickle"))
    return gradematrix,dummieidgrid,coursegrid

"""
    loadcpickle - method that loads a .cPickle file from memory into a datastructure and returns it.
"""
def loadcpickle(filename):
    f = open(filename,"rb")
    cp = cPickle.load(f)
    f.close()
    return cp

"""
    getentry - method that uses the dummieid or coursename commandline argument to retrieve a single row from the grade
               matrix. That row is then returned.
"""
def getentry(grademat,dummieidgrid,coursegrid,input):
    templist = numpy.empty(0)
    for i in range(0,len(dummieidgrid)):
        for j in range(0,len(dummieidgrid[i])):
            if dummieidgrid[i][j] == input:
                for x in grademat[i]: templist = numpy.append(templist,x)
                return templist,"student"

            elif coursegrid[i][j] == input:
                templist = numpy.append(templist,grademat[i][j])
    return templist,"course"

def calculatemode(matrix):
    if matrix.shape[0] == 1: return matrix[0]
    return stats.mode(matrix)[0][0]

def calculatemean(matrix):
    if matrix.shape[0] == 1: return matrix[0]
    return numpy.nanmean(matrix)

def calculatemedian(matrix):
    if matrix.shape[0] == 1: return matrix[0]
    return numpy.nanmedian(matrix)

def calculatevariance(matrix):
    if matrix.shape[0] == 1: return 0
    return numpy.nanvar(matrix)

def countrecords(matrix):
    return matrix.shape[0]

def countstudents(matrix):
    if matrix.shape[0] == 1: return 1
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

def plothistogram(matrix,flag,title):
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
    if flag == "course":
        plt.figtext(.04,.16,"Number of students: " + str(students), fontsize=10)
    else:
        plt.figtext(.04,.16,"Number of courses taken: " + str(students), fontsize=10)
    plt.figtext(.04,.13,"Mean: " + str(mean), fontsize=10)
    plt.figtext(.04,.10,"Median: " + str(median), fontsize=10)
    plt.figtext(.04,.07,"Mode: " + str(mode), fontsize=10)
    plt.figtext(.04,.04,"Percent above a C: " + str(percentabovec) + "%", fontsize=10)
    plt.figtext(.04,.01,"Percent passing: " + str(percentpassing) + "%", fontsize=10)
    y = countsmap[max(countsmap.iteritems(), key=operator.itemgetter(1))[0]]
    x = numpy.linspace(0,len(countsmap)-1,1000)
    if matrix.shape[0] > 1:
        sigma = math.sqrt(variance)
        plt.plot(x,y * mlab.normpdf(x,mean,sigma),'-r',linewidth=2)
    figure = plt.gcf()
    #plt.show()
    timestring = time.strftime("%Y%m%d-%H%M%S")
    figurename = "figures/histogram-" + timestring
    figure.savefig(figurename)
    print(colored("mat2hist ==> SUCCESS --> " + figurename + " file written.","cyan"))

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
    usage = colored("mat2hist ==> ERROR --> Improper command line arguments ~~> Usage : python mat2hist.py <matrix.npy> <dummieid or \"coursename\">","red")
    if len(sys.argv) > 3:
        print usage
        exit(-1)
    try:
        t0 = time.time()
        matrixfile = sys.argv[1]
        entrykey = sys.argv[2]
        main(matrixfile,entrykey) # main(["preprocessing/CSDataFile_ForParry_2014Nov26_grademat.npy","1400001"])
        t1 = time.time()
        totaltime = t1 - t0
        print(colored("mat2hist =~> " + str(totaltime) + " seconds.","yellow"))
    except:
        print usage
        exit(-1)