#!/usr/bin/python

"""
    crossval.py -
"""

__author__ = 'sina'
__project__ = 'STProject'

from termcolor import colored
import numpy
import time
import sys
import random
import re
import os

"""
    main - main method of the crossval program.
"""
def main(argv1, argv2, argv3, argv4):
    file_name = argv1
    base_name = os.path.splitext(file_name)[0]
    k_folds = int(argv2)
    n_iterations = int(argv3)
    target_course = argv4
    if not os.path.exists("crossvalin/" + target_course):
        os.makedirs("crossvalin/" + target_course)
    directory_name = "crossvalin/" + target_course + "/" + re.search('_.*', base_name).group(0)
    result = numpy.load(file_name)
    data = result['data']
    activity_list = list(result['activity_list'])
    student_list = list(result['student_list'])
    target_course_column = activity_list.index(target_course)
    iterations, groupings = n_in_k_fold(data, k_folds, n_iterations, target_course_column)
    save_data(data, k_folds, n_iterations, target_course, directory_name, iterations, groupings, student_list,
              activity_list)

def remove_target(d, t, g, grp):
    for index, group_assignment in enumerate(grp):
        if group_assignment == g:
            row_to_remove = index
            d[row_to_remove, t] = numpy.nan
    return d


def n_in_k_fold(data, k, n, t):
    iterations = []
    groupings = []

    # generate list of numbers 1 to k in repeating sequential order for every row in data
    grouping = [(i % k) + 1 for i in range(0, len(data))]
    for iteration in range(0, n):
        random.shuffle(grouping)
        groupings.append(grouping.copy())
        folds = []
        for group in range(1, k + 1):
            f = remove_target(data.copy(), t, group, grouping)
            folds.append(f)
        iterations.append(list(folds))
    return iterations, groupings

def save_data(data, k, n, t, directory_name, iterations, groupings, student_list, activity_list):
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)
    for i in range(0, n):
        new_filename = directory_name + "_iter" + str(i) + ".npz"
        numpy.savez_compressed(new_filename, activity_list=activity_list, student_list=student_list,
                               groupings=groupings[i], **{"fold" + str(j) : value for j,value in
                                                          enumerate(iterations[i])})

if __name__ == "__main__":
    usage = colored("crossval ==> ERROR --> Improper command line arguments ~~> Usage : python imputemat.py "
                    "<matrix.npy> <ROWMEAN, COLMEAN, EIG, SVD, or ALS>","red")
    if len(sys.argv) > 5:
        print usage
        exit(-1)
    try:
        t0 = time.time()
        # "precrossvalout/precrossval_goback0.npz"
        input_matrix_filename = sys.argv[1]
        number_of_folds = sys.argv[2]
        number_of_iterations = sys.argv[3]
        target_course = sys.argv[4]
        main(input_matrix_filename, number_of_folds, number_of_iterations, target_course)
        t1 = time.time()
        total_time = t1 - t0
        print(colored("crossval ~=> " + str(total_time) + " seconds.","yellow"))
    except IOError as e:
        print e.strerror
        print usage
        exit(-1)