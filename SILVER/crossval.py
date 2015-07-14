#!/usr/bin/python

"""
    crossval.py -
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

"""
    main - main method of the crossval program.
        :param argv1: command line argument -> the course name of the target.
        :type argv1: string
        :param argv2: command line argument -> the prerequisite course to the target that we are interested in.
        :type argv2: string
"""
def main(argv1,argv2):
    filename = argv1
    k = int(argv2)
    colorama.init(autoreset=True)
    print(colored("crossval","blue"))
    result = numpy.load(argv1)
    data = result['data']
    activity_list = result['activity_list']
    student_list = result['student_list']
    kfold(data, k, activity_list, student_list)


def kfold(data, k, activity_list, student_list):
    data_copy = data.copy()
    # generate list of numbers 1 to k in repeating sequential order for every row in data
    groupings = [(i % 10)+1 for i in range(0,len(data))]
    random.shuffle(groupings)

    for group_number in range(1, k + 1):
        temp_matrixlist = []
        for index, group_assignment in enumerate(groupings):
            if group_assignment == group_number:
                row_toremove = index
                data_copy[row_toremove, :] = numpy.nan

        # for i in range(0, k):
        #     temp_matrixlist.append(data_copy.copy())

        new_filename = "crossvalin/crossvalinfold" + str(group_number) + ".npz"
        numpy.savez_compressed(new_filename, *[temp_matrixlist[i] for i in range(0, k)], activity_list=activity_list, student_list=student_list, groupings=groupings)

if __name__ == "__main__":
    usage = colored("crossval ==> ERROR --> Improper command line arguments ~~> Usage : python imputemat.py <matrix.npy> <ROWMEAN, COLMEAN, EIG, SVD, or ALS>","red")
    if len(sys.argv) > 3:
        print usage
        exit(-1)
    try:
        t0 = time.time()
        # "precrossvalout/precrossval_goback0.npz"
        inputmatrix_filename = sys.argv[1]
        numberof_folds = sys.argv[2]
        numberof_iterations = sys.argv[3]
        target_course = sys.argv[3]
        main(inputmatrix_filename, numberof_folds)
        t1 = time.time()
        totaltime = t1 - t0
        print(colored("crossval ~=> " + str(totaltime) + " seconds.","yellow"))
    except IOError as e:
        print e.strerror
        print usage
        exit(-1)