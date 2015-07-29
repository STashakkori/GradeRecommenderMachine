#!/usr/bin/python

"""
    precrossval.py -
"""
__author__ = 'sina'
__project__ = 'STProject'

from termcolor import colored
import time
import csv
import numpy
import os
import sys
import math

"""
    main
"""
def main(target_course, go_back):
    go_back = int(go_back)
    result = numpy.load("CSDataFile_ForParry_2014Nov26.csv.npz")
    data = result['data']
    orders = result['orders']
    activity_list = list(result['activity_list'])
    student_list = result['student_list']
    target_column = activity_list.index(target_course)

    tests = {"SATV_score.1", "SATM_score.1", "ACTEng_score.1", "ACTMat_score.1", "MathPlacement_PLM1_Score.1",
             "MathPlacement_PLM2_Score.1", "MathPlacement_PLM3_Score.1", "HSGPA.1"}

    # normalize test scores to be on a 12.0 scale as to not skew grade predictions
    for index, activity in enumerate(activity_list):
        if activity in tests:
            data[:, index] = (data[:, index] / numpy.nanmax(data[:, index])) * 12.0

    remove_student_index = numpy.isnan(data[:, target_column])
    student_list = student_list[~remove_student_index]
    data = data[~remove_student_index, :] # remove students that have not taken target course
    orders = orders[~remove_student_index, :]

    for i in range(0, data.shape[0]):
        target_order = int(orders[i, target_column])
        lower_bound_order = 0
        if go_back < target_order:
            lower_bound_order = target_order - go_back

        for j in range(0, data.shape[1]):
            current_grade_order = orders[i, j]
            if current_grade_order >= lower_bound_order < target_order:
                data[i, j] = numpy.nan

    validgradereference = numpy.zeros(data.shape[1])
    for i in range(0,data.shape[0]):
        for j in range(0,data.shape[1]):
            if not math.isnan(data[i][j]):
                validgradereference[j] += 1

    zerolist = numpy.where(validgradereference == 0.0)
    data = numpy.delete(data,zerolist, 1)
    orders = numpy.delete(orders,zerolist, 1)
    activity_list = list(numpy.delete(activity_list,zerolist, 0))
    target_column = activity_list.index(target_course)
    student_list = student_list[sum(~numpy.isnan(data.T)) >= 2]
    data = data[sum(~numpy.isnan(data.T)) >= 2] # remove rows that don't have at least 2 valid grades/scores in them.
    actual_vector = data[:, target_column].copy()

    """
    sindex = list(student_list).index("1400013")
    aindex = activity_list.index("C S 2440.1")
    print data[sindex][aindex]
    exit(1)
    """

    dir_name = target_course.replace(" ", "")
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    sub_dir_name = dir_name + "/" + "precrossval"

    if not os.path.exists(sub_dir_name):
        os.makedirs(sub_dir_name)

    new_filename = sub_dir_name + "/go_back" + str(go_back) + ".npz"
    numpy.savez_compressed(new_filename, data=data, activity_list=activity_list, student_list=student_list,
                           actual_vector=actual_vector)

if __name__ == "__main__":
    if len(sys.argv) > 3:
        print "Incorrect parameters. Try again."
        exit(-1)

    try:
        t0 = time.time()
        target_course = sys.argv[1]
        courses_to_go_back = sys.argv[2]
        main(target_course, courses_to_go_back)
        t1 = time.time()
        total_time = t1 - t0
        print(colored("csv2mat ~=> " + str(total_time) + " seconds.", "yellow"))
    except IOError as e:
        print e.strerror
        exit(-1)