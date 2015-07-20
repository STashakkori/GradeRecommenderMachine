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
import imputemat

"""
    main - main method of the crossval program.
"""
def main(argv1, argv2, argv3, argv4):
    file_name = argv1
    base_name = os.path.splitext(file_name)[0]
    k_folds = int(argv2)
    n_iterations = int(argv3)
    target_course = argv4

    dir_name = target_course.replace(" ", "")
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    sub_dir_name = dir_name + "/crossvalin"
    if not os.path.exists(sub_dir_name):
        os.makedirs(sub_dir_name)

    goback = re.search('go_back.*', base_name).group(0)
    new_dir_name = sub_dir_name + "/" + goback
    result = numpy.load(file_name)
    data = result['data']
    activity_list = list(result['activity_list'])
    student_list = list(result['student_list'])
    actual_vector = result['actual_vector']
    target_course_column = activity_list.index(target_course)
    iterations, groupings = n_in_k_fold(data, k_folds, n_iterations, target_course_column)
    """
    #uncomment to save results. Takes a while so don't do it if not necessary
    save_data(data, k_folds, n_iterations, target_course, new_dir_name, iterations, groupings, student_list,
              activity_list)
    """
    k_components = 1
    estimates,results = run_algorithm(new_dir_name, k_components, target_course, k_folds)
    out_dir_name = dir_name + "/crossvalout"
    if not os.path.exists(out_dir_name):
        os.makedirs(out_dir_name)
    numpy.savez_compressed(out_dir_name + "/k" + str(k_components) + "_goback" + goback + "_result_matrices.npz",
                    activity_list=activity_list,student_list=student_list,
                    **{"result_matrix" + str(j) : value for j,value in enumerate(results)})

    numpy.savez_compressed(out_dir_name + "/k" + str(k_components) + "_goback" + goback + "_estimate_vectors.npz",
                   actual_vector=actual_vector,
                   **{"estimate_vector" + str(j) : value for j,value in enumerate(estimates)})

"""
    remove_target
"""
def remove_target(d, t, g, grp):
    for index, group_assignment in enumerate(grp):
        if group_assignment == g:
            row_to_remove = index
            d[row_to_remove, t] = numpy.nan
    return d

"""
    n_in_k_fold
"""
def n_in_k_fold(data, k, n, t):
    iterations = []
    groupings = []

    # generate list of numbers 1 to k in repeating sequential order for every row in data
    grouping = [(i % k) + 1 for i in range(0, len(data))]

    for iteration in range(0, n):
        random.shuffle(grouping)
        groupings.append(list(grouping))
        folded_result = []
        for group in range(1, k + 1):
            f = remove_target(data.copy(), t, group, grouping)
            folded_result.append(f)
        iterations.append(list(folded_result))
    return iterations, groupings

"""
    save_data
"""
def save_data(data, k, n, t, new_dir_name, iterations, groupings, student_list, activity_list):
    if not os.path.exists(new_dir_name):
        os.makedirs(new_dir_name)
    for i in range(0, n):
        new_filename = new_dir_name + "/iteration" + str(i) + ".npz"
        numpy.savez_compressed(new_filename, activity_list=activity_list, student_list=student_list,
                               groupings=groupings[i], **{"fold" + str(j) : value for j,value in
                                                          enumerate(iterations[i])})

"""
    run_algorithm
"""
def run_algorithm(sub_dir_name, k, t, number_folds):
    estimates = []
    results = []
    for i,iteration in enumerate(os.listdir(sub_dir_name)):
        # folds -> package that holds k number of matrices for folds.
        folds = numpy.load(sub_dir_name + "/" + "iteration" + str(i) + ".npz")
        a = list(folds['activity_list'])
        target_column = a.index(t)
        estimate = []
        for fold in range(0, number_folds):
            data_matrix = folds['fold' + str(fold)]
            groupings = folds['groupings']
            #result = imputemat.imputepcafast(data_matrix, k)
            result = imputemat.imputecolmean(data_matrix)
            results.append(result)
            for row_index, group_assignment in enumerate(groupings):
                if group_assignment == fold + 1:
                    estimate.append(result[row_index][target_column])
        estimates.append(estimate)
    return estimates, results


if __name__ == "__main__":
    usage = colored("crossval ==> ERROR --> Improper command line arguments ~~> Usage : python imputemat.py "
                    "<matrix.npy> <ROWMEAN, COLMEAN, EIG, SVD, or ALS>","red")
    if len(sys.argv) > 5:
        print usage
        exit(-1)
    try:
        t0 = time.time()
        # "precrossvalout/go_back0.npz"
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