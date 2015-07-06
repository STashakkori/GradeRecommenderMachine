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
    activitydictfile = loadjson(argv2)
    targetcourse = argv3



def loadjson(filename):
        f = open(filename,"rb")
        j = json.loads(open(filename).read())
        f.close()
        return j

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
        for activity in studentdictionary.keys():
            if targetcourse in studentdictionary[activity]:
                columnindex = activitylabels.index(activity)
                # Grab the lowest grade out of dictionary entry.
                mingrade = float('inf')
                for value in studentdictionary[dummieid][activity]:
                    gradetuplepart = value[0]
                    if activity == "SATV_score" or activity == "SATM_score" or activity == "ACTEng_score" or activity == "ACTMat_score" or activity == "MathPlacement_PLM1_Score" or activity == "MathPlacement_PLM2_Score" or activity == "MathPlacement_PLM3_Score" or activity == "HSGPA":
                        mingrade = gradetuplepart

                    elif gradetuplepart in twelvepointgrademap and twelvepointgrademap[gradetuplepart] < mingrade:
                        mingrade = twelvepointgrademap[gradetuplepart]

                if mingrade == float('inf'):
                    grade = numpy.NAN
                else:
                    grade = mingrade
                gradematrix[rowindex][columnindex] = grade
    return gradematrix, dummieidlabels, activitylabels

"""
    createmapfromlabel - method that converts a enumerated map from a list.
"""
def createmapsfromlabels(list1,list2):
    map1 = {}
    map2 = {}
    for index,item in enumerate(list1):
        map1[item] = index

    for index,item in enumerate(list2):
        map2[item] = index

    return map1,map2

"""
    pruneemptycolumns - method that removes columns that are populated entirely with NAN's
"""
def pruneemptycolumns(gradematrix, activitylabels):
    validgradereference = numpy.zeros(gradematrix.shape[1])
    for i in range(0,gradematrix.shape[0]):
        for j in range(0,gradematrix.shape[1]):
            if not math.isnan(gradematrix[i][j]):
                validgradereference[j] += 1

    zerolist = numpy.where(validgradereference == 0.0)
    gradematrix = numpy.delete(gradematrix,zerolist,1)
    activitylabels = numpy.delete(activitylabels,zerolist,0)
    return gradematrix, activitylabels

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
        main(studentdictfile,activitydictfile,targetcourse) # main(["preprocessing/CSDataFile_ForParry_2014Nov26_studentdict.json","preprocessing/CSDataFile_ForParry_2014Nov26_activitydict.json,"C S 2440"])
        t1 = time.time()
        totaltime = t1 - t0
        print(colored("crossval ~=> " + str(totaltime) + " seconds.","yellow"))
    except IOError as e:
        print e.strerror
        print usage
        exit(-1)