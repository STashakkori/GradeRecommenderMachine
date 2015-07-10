__author__ = 'sina'

import numpy
import time

def main():
    t0 = time.time()
    result = numpy.load("CSDataFile_ForParry_2014Nov26.csv.npz")
    t1 = time.time()
    print t1 - t0
    data = result['data']
    activity_list = list(result['activity_list'])
    student_list = list(result['student_list'])
    while True:
        dummie_id = raw_input("Enter Dummie Id: ")
        activity = raw_input("Enter Activity Name: ")
        print get_grade(data, activity_list, student_list, dummie_id, activity)

def get_grade(data, activity_list, student_list, dummie_id, activity):
    row_index = student_list.index(dummie_id)
    col_index = activity_list.index(activity)
    return data[row_index, col_index]

if __name__ == "__main__":
    main()