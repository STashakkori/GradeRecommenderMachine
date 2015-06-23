#!/usr/bin/python

"""
    csv2dict.py : script that reads a .csv file filled with grades, gpas, and exams scores and creates two dictionary
                  datastructures, one for indexing via a student's dummieid and one for indexing via a course name.
                  Once created, the dictionaries are stored in memory as json in the preprocessing directory.
"""

__author__ = 'sina'
__project__ = 'STProject'

import os
import colorama
from termcolor import colored
import re
import time
import sys

"""
    main - main method of the csv2dict program.
        :param argv: command line argument
        :type argv: string
"""
def main(argv):
    print(colored("csv2dict","blue"))
    if argv and argv.endswith(".csv"):
        studentdictionary,activitydictionary = parsecsvtodictionary(argv)
        studentdictoutputfilename = os.path.splitext(argv)[0] + "_studentdict.json"
        activitydictoutputfilename = os.path.splitext(argv)[0] + "_activitydict.json"
        storedataasjson(studentdictionary,studentdictoutputfilename)
        storedataasjson(activitydictionary,activitydictoutputfilename)

    else:
        print(colored("csv2dict ==> ERROR --> Bad filename input ~~> .csv required","red"))
        exit(1)

"""
    parsecsvtodictionary - method that reads a csv file, splits it on commas, and then populates two dictionaries with
                           relevant data. Studentdictionary is indexable by student dummieid. Activity dictionary is
                           indexable by the activity name.
"""
def parsecsvtodictionary(filename):
    with open(filename) as file:
        data = file.readlines()

    pieces = []

    for line in data:
        pieces.append(line.split(','))

    studentdictionary = {}
    activitydictionary = {}

    courseregex = 'Course'
    graderegex = 'Grade[0-9]+'
    gradegparegex = 'Grade_GPA'
    scoreregex = re.compile('_score$')
    minorregex = re.compile('_min')
    majorregex = re.compile('_major|_mjr')
    endnumberregex = re.compile('(\d)+$')
    hsgparegex = re.compile('HSGPA')

    for i in range(1,len(pieces)):
        studentdictionary[pieces[i][0]] = {}
        studentid = pieces[i][0]
        timeofactivitycounter = 0
        for j in range(1,len(pieces[i])):
            activityid = pieces[0][j].strip('\r').strip('\n')
            cell = pieces[i][j].strip('\r').strip('\n')
            if(cell and not re.match(graderegex,activityid) and not re.match(gradegparegex,activityid)):
                if activityid not in activitydictionary: activitydictionary[activityid] = {}

                # if it's a course, then we want to make that the key and grab it's grade and insert that as the value
                if(re.match(courseregex,activityid)):
                    course = cell
                    grade = pieces[i][j+131].strip('\r').strip('\n')
                    studentdictionary[studentid].setdefault(course,[]).append((grade,timeofactivitycounter))
                    activitydictionary.setdefault(course,{})
                    activitydictionary[course].setdefault(studentid,[]).append((grade,timeofactivitycounter))
                    timeofactivitycounter += 1

                # otherwise, use the column header as the key and just insert the csv entry as the value
                else:
                    score = cell
                    studentdictionary[studentid].setdefault(activityid,[]).append((score,))
                    activitydictionary[activityid].setdefault(studentid,[]).append((score,))
                file.close()
    return studentdictionary,activitydictionary

"""
    storedataasjson - method that writes an object to memory in json format.
"""
def storedataasjson(dictionary, filename):
    import json
    file = open("preprocessing/" + filename, "wb")
    json.dump(dictionary,file)
    file.close()
    print(colored("csv2dict ==> SUCCESS --> " + filename + " file written to the preprocessing directory.","cyan"))

if __name__ == "__main__":
    usage = colored("csv2dict ==> ERROR --> Improper command line arguments ~~> Usage : python csv2dict.py <gradefile.csv> ","red")
    if len(sys.argv) > 2:
        print usage
        exit(-1)

    try:
        t0 = time.time()
        input_filename = sys.argv[1]
        main(input_filename) # main("CSDataFile_ForParry_2014Nov26.csv")
        t1 = time.time()
        totaltime = t1 - t0
        print(colored("csv2dict ~=> " + str(totaltime) + " seconds.","yellow"))
    except IOError as e:
        print usage
        print e.strerror
        sys.exit(-1)