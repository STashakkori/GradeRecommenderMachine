__author__ = 'sina'
__project__ = 'STProject'

'''
    Main class for a CS course grade based recommendation system using machine learning
'''
__author__ = 'sina'
__project__ = 'STProject'

import os
import colorama
from termcolor import colored
import re
import time

'''
    main - main method of the csv2dict program.
'''
def main(argv):
    colorama.init(autoreset=True)
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
        for j in range(1,len(pieces[i])):
            if(pieces[i][j].strip('\r').strip('\n') and not re.match(graderegex,pieces[0][j]) and not re.match(gradegparegex,pieces[0][j])):
                if pieces[0][j] not in activitydictionary: activitydictionary[pieces[0][j]] = {}

                # if it's a course, then we want to make that the key and grab it's grade and insert that as the value
                if(re.match(courseregex,pieces[0][j])):
                    studentdictionary[pieces[i][0]].setdefault(pieces[i][j].strip('\r').strip('\n'),[])
                    studentdictionary[pieces[i][0]][pieces[i][j]].append(pieces[i][j+131].strip('\r').strip('\n'))

                    activitydictionary.setdefault(pieces[i][j].strip('\r').strip('\n'),{})
                    activitydictionary[pieces[i][j].strip('\r').strip('\n')].setdefault(pieces[i][0],[])
                    activitydictionary[pieces[i][j].strip('\r').strip('\n')][pieces[i][0]].append(pieces[i][j+131].strip('\r').strip('\n'))

                # otherwise, use the column header as the key and just insert the csv entry as the value
                else:
                    studentdictionary[pieces[i][0]].setdefault(pieces[0][j].strip('\r').strip('\n'),[])
                    studentdictionary[pieces[i][0]][pieces[0][j]].append(pieces[i][j].strip('\r').strip('\n'))

                    activitydictionary[pieces[0][j].strip('\r').strip('\n')].setdefault(pieces[i][0],[])
                    activitydictionary[pieces[0][j].strip('\r').strip('\n')][pieces[i][0]].append(pieces[i][j].strip('\r').strip('\n'))

                file.close()

    return studentdictionary,activitydictionary

# Method that writes an object to memory in json format
def storedataasjson(dictionary, filename):
    import json
    file = open("preprocessing/" + filename, "wb")
    json.dump(dictionary,file)
    file.close()
    print(colored("csv2dict ==> SUCCESS --> " + filename + " file written to the preprocessing directory.","cyan"))

if __name__ == "__main__":
    t0 = time.time()
    main("CSDataFile_ForParry_2014Nov26.csv")
    t1 = time.time()
    totaltime = t1 - t0
    print(colored("csv2dict =~> " + str(totaltime) + " seconds.","yellow"))