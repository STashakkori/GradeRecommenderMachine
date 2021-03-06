#!/usr/bin/python

"""
    prepcrossval.py -
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
import random
import json

"""
    main - main method of the prepcrossval program.
        :param argv1: command line argument -> the course name of the target.
        :type argv1: string
        :param argv2: command line argument -> the prerequisite course to the target that we are interested in.
        :type argv2: string
"""
def main(argv1,argv2,argv3):
    colorama.init(autoreset=True)
    print(colored("crossval","blue"))
    studentdictionary = loadjson(argv1)
    activitydictionary = loadjson(argv2)
    targetcourse = argv3
    g,d,a = createcoursespecificnpy(studentdictionary,activitydictionary,targetcourse)
    #g,d,a = pruneemptycolumns(g,d,a)
    numpy.set_printoptions(threshold=numpy.nan)
    print "TESTING:"
    print len(a)
    print len(d)
    index1 = 0
    index2 = 0
    for x in range(0,len(d)):
        if d[x] == "1400002":
            index1 = x

    for x in range(0,len(a)):
        if a[x] == " C S 1100":
            index2 = x

    print g.shape
    print g[index1][index2]
    #print g[numpy.where(d == "1400002")[0]]
    #print g[numpy.where(d == "1400002")][numpy.where(a == "C S 1100")[0]]

def loadjson(filename):
        f = open(filename,"rb")
        j = json.loads(open(filename).read())
        f.close()
        return j

""" debugging
            if dummieid == "1400002":
                print targetcourse
                print targetcourseorder
                print "activity:"
                print activity
                print thiscourseorder
                print thiscoursegrade
                print "activitylabels.index(activity): " + str(activitylabels.index(activity))
                print ("thiscoursegrade in twelvepointgrademap: " + str(thiscoursegrade in twelvepointgrademap))
                print ("thiscourseorder < targetcourseorder: " + str(thiscourseorder < targetcourseorder))
                if thiscoursegrade in twelvepointgrademap: print ("twelvepointgrademap[thiscoursegrade]: " + str(twelvepointgrademap[thiscoursegrade]))
                if thiscoursegrade in twelvepointgrademap: print ("twelvepointgrademap[thiscoursegrade] < mingrade: " + str(twelvepointgrademap[thiscoursegrade] < mingrade))
                m = str(mingrade)
                print "mingrade: ",mingrade
                print "=========="
"""

def createcoursespecificnpy(studentdictionary,activitydictionary,targetcourse):
    twelvepointgrademap = {"A":12.0,"A-":11.0,"B+":10.0,"B":9.0,"B-":8.0,"C+":7.0,"C":6.0,"C-":5.0,"D+":4.0,"D":3.0,"D-":2.0,"F":0.0}
    rows = len(studentdictionary.keys())
    columns = len(activitydictionary.keys())
    dummieidlabels = studentdictionary.keys()
    dummieidlabels.sort(key=int)
    activitylabels = activitydictionary.keys()
    activitylabels.sort()
    gradematrix = numpy.empty([rows,columns],dtype='float32')
    gradematrix[:] = numpy.NAN

    for dummieid in studentdictionary:
        rowindex = dummieidlabels.index(dummieid)
        if targetcourse not in studentdictionary[dummieid]:
            #dummieidlabels.remove(dummieid)
            continue

        targetcourseorder = studentdictionary[dummieid][targetcourse][0][1]

        for activity in studentdictionary[dummieid]:
            columnindex = activitylabels.index(activity)
            #thiscoursegrade = studentdictionary[dummieid][activity][0][0]
            #thiscourseorder = studentdictionary[dummieid][activity][0][1]
            mingrade = float('inf')
            for value in studentdictionary[dummieid][activity]:
                thiscoursegrade = value[0]
                thiscourseorder = value[1]
                print "thiscoursegrade: ",thiscoursegrade
                print "thiscourseorder: ",thiscourseorder


                if activity == "SATV_score" or activity == "SATM_score" or activity == "ACTEng_score" or activity == "ACTMat_score" or activity == "MathPlacement_PLM1_Score" or activity == "MathPlacement_PLM2_Score" or activity == "MathPlacement_PLM3_Score" or activity == "HSGPA":
                    mingrade = thiscoursegrade

                elif thiscoursegrade in twelvepointgrademap and thiscourseorder < targetcourseorder and twelvepointgrademap[thiscoursegrade] < mingrade:
                    mingrade = twelvepointgrademap[thiscoursegrade]

            if mingrade == float('inf'):
                grade = numpy.NAN
            else:
                grade = mingrade
            gradematrix[rowindex][columnindex] = grade
    return gradematrix, dummieidlabels, activitylabels

"""
    pruneemptycolumns - method that removes columns that are populated entirely with NAN's
"""
def pruneemptycolumns(gradematrix, dummieidlabels, activitylabels):

    validgradereference = numpy.zeros(gradematrix.shape[1])
    for i in range(0,gradematrix.shape[0]):
        for j in range(0,gradematrix.shape[1]):
            if not math.isnan(gradematrix[i][j]):
                validgradereference[j] += 1

    zerolist = numpy.where(validgradereference == 0.0)
    activitylabels = numpy.delete(activitylabels,zerolist,0)

    #activitylabels = numpy.delete(activitylabels,gradematrix[numpy.isnan(gradematrix).all(axis=0)],0)
    #dummieidlabels = numpy.delete(dummieidlabels,gradematrix[numpy.isnan(gradematrix).all(axis=1)],0)
    gradematrix = gradematrix[~numpy.isnan(gradematrix).all(axis=0)] # prune columns
    gradematrix = gradematrix[~numpy.isnan(gradematrix).all(axis=1)] # prune rows
    return gradematrix, dummieidlabels, activitylabels

if __name__ == "__main__":
    usage = colored("crossval ==> ERROR --> Improper command line arguments ~~> Usage : python imputemat.py <matrix.npy> <ROWMEAN, COLMEAN, EIG, SVD, or ALS>","red")
    if len(sys.argv) > 4:
        print usage
        exit(-1)
    try:
        t0 = time.time()
        studentdictfile = sys.argv[1]
        activitydictfile = sys.argv[2]
        targetcourse = sys.argv[3]
        main(studentdictfile,activitydictfile,targetcourse) # main(["preprocessing/CSDataFile_ForParry_2014Nov26_studentdict.json","preprocessing/CSDataFile_ForParry_2014Nov26_activitydict.json","C S 2440"])
        t1 = time.time()
        totaltime = t1 - t0
        print(colored("crossval ~=> " + str(totaltime) + " seconds.","yellow"))
    except IOError as e:
        print e.strerror
        print usage
        exit(-1)