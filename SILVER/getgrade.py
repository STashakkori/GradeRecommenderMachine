__author__ = 'sina'

import numpy
import time

def main():
    result = numpy.load("CSDataFile_ForParry_2014Nov26.csv.npz")
    data = result['data']
    orders = result['orders']
    activity_list = list(result['activity_list'])
    student_list = list(result['student_list'])

    while True:
        dummie_id = raw_input("Enter Dummie Id: ")
        activity = raw_input("Enter Activity Name: ")
        print get_grade(data, activity_list, student_list, dummie_id, activity, orders)

def get_grade(data, activity_list, student_list, dummie_id, activity, orders):
    row_index = student_list.index(dummie_id)
    col_index = activity_list.index(activity)
    return data[row_index, col_index], orders[row_index, col_index]

if __name__ == "__main__":
    main()