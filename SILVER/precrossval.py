#!/usr/bin/python

"""
    precrossval.py -
"""
__author__ = 'sina'
__project__ = 'STProject'

from termcolor import colored
import time
import sys
import csv
import numpy
import operator

"""
    main
"""
def main(target, goback):
    goback = int(goback)
    result = numpy.load("CSDataFile_ForParry_2014Nov26.csv.npz")
    data = result['data']
    orders = result['orders']
    activity_list = list(result['activity_list'])
    student_list = result['student_list']
    target_column = activity_list.index(target)
    removestudent_index = numpy.isnan(data[:, target_column])
    student_list = list(student_list[~removestudent_index])
    data = data[~removestudent_index, :]
    orders = orders[~removestudent_index, :]

    for i in range(0, data.shape[0]):
        target_order = int(orders[i, target_column])
        newtarget_order = 0
        if goback < target_order:
            newtarget_order = target_order - goback

        for j in range(0, data.shape[1]):
            if orders[i, j] >= newtarget_order:
                data[i, j] = numpy.nan

    new_filename = "precrossvalout/precrossval_goback" + str(goback) + ".npz"
    numpy.savez_compressed(new_filename, data=data, activity_list=activity_list, student_list=student_list)

if __name__ == "__main__":
    if len(sys.argv) > 3:
        print "Incorrect parameters. Try again."
        exit(-1)

    try:
        t0 = time.time()
        target_course = sys.argv[1]
        courses_togoback = sys.argv[2]
        main(target_course, courses_togoback)
        t1 = time.time()
        total_time = t1 - t0
        print(colored("csv2mat ~=> " + str(total_time) + " seconds.", "yellow"))
    except IOError as e:
        print e.strerror
        exit(-1)