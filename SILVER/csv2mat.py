#!/usr/bin/python

"""
    csv2mat.py -
"""

__author__ = 'sina'
__project__ = 'STProject'

from termcolor import colored
import time
import sys
import csv
import numpy
import operator


def main(csv_filename):
    first_row = True
    tests = {"SATV_score", "SATM_score", "ACTEng_score", "ACTMat_score", "MathPlacement_PLM1_Score",
             "MathPlacement_PLM2_Score", "MathPlacement_PLM3_Score", "HSGPA"}
    headers = []
    student_list = []
    activity_map = {}
    data = None
    with open(csv_filename, 'r') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        num_rows = sum(1 for row in reader)

    with open(csv_filename, 'r') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        row_index = 0
        for row in reader:
            # Build a map of headers
            if first_row:
                headers = row
                num_cols = 7000 * 3
                data = numpy.zeros((num_rows, num_cols)) * numpy.nan
                first_row = False
                continue

            # Update student_map
            student_list.append(row[0])
            student_activitymap = {}

            # Populate matrix
            for i, item in enumerate(row):
                h = headers[i]
                if h in tests:
                    activity = h
                    score = item

                elif h[:6] == "Course":
                    if item == "":
                        continue

                    activity = item
                    score = row[i + 131]

                else:
                    continue

                if activity not in student_activitymap:
                    student_activitymap[activity] = 0

                trial = student_activitymap[activity] + 1
                student_activitymap[activity] += 1
                activity += "." + str(trial)

                if activity not in activity_map:
                    activity_map[activity] = len(activity_map)

                col_index = activity_map[activity]
                data[row_index, col_index] = convert_score(score)
            if row_index % 100 == 0:
                sys.stdout.write("\r" + str(row_index))
                sys.stdout.flush()
            row_index += 1
    activity_list = [item[0] for item in sorted(activity_map.items(), key=operator.itemgetter(1))]
    num_cols = len(activity_list)
    data = data[:, :num_cols]
    new_filename = csv_filename + ".npz"
    numpy.savez_compressed(new_filename, data=data, activity_list=activity_list, student_list=student_list)

def get_grade(data, activitymap, studentlist, dummieid,activity):
    row_index = studentlist.index(dummieid)
    col_index = activitymap[activity]
    return data[row_index,col_index]

def convert_score(score_string):
    grade_map = {"A": 12.0, "A-": 11.0, "B+": 10.0, "B": 9.0, "B-": 8.0, "C+": 7.0, "C": 6.0, "C-": 5.0, "D+": 4.0,
                 "D": 3.0, "D-": 2.0, "F": 0.0}
    try:
        score = float(score_string)

    except ValueError:
        if score_string not in grade_map:
            score = numpy.nan

        else:
            score = grade_map[score_string]

    return score


if __name__ == "__main__":
    if len(sys.argv) > 2:
        print "Incorrect parameters. Try again."
        exit(-1)

    try:
        t0 = time.time()
        input_filename = sys.argv[1]
        # main("CSDataFile_ForParry_2014Nov26.csv")
        main(input_filename)
        t1 = time.time()
        total_time = t1 - t0
        print(colored("csv2mat ~=> " + str(total_time) + " seconds.", "yellow"))
    except IOError as e:
        print e.strerror
        exit(-1)