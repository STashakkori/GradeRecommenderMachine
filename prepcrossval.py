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
    matrix = numpy.empty(0,0)
    for key in studentdictionary.keys():
        if targetcourse in studentdictionary[key]:


    return


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