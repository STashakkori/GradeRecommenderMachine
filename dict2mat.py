__author__ = 'sina'
__project__ = 'STProject'

import os
import colorama
from termcolor import colored
import cPickle
import numpy
import json
import math
import time

def main(argv):
    colorama.init(autoreset=True)
    print(colored("dict2mat","blue"))
    if argv and argv.endswith(".json"):
        studentmap = loadjson(argv)
        g,d,c = convertdictionarytomatrix(studentmap)
        g,d,c = pruneemptycolumns(g,d,c)
        storematrixandlistsinmemory(g,d,c,argv)

    else:
        print(colored("dict2mat ==> ERROR --> Bad filename input ~~> .json required","red"))
        exit(1)

def loadjson(filename):
        f = open(filename,"rb")
        j = json.loads(open(filename).read())
        f.close()
        return j

def convertdictionarytomatrix(dictionary):
    twelvepointgrademap = {"A":12.0,"A-":11.0,"B+":10.0,"B":9.0,"B-":8.0,"C+":7.0,"C":6.0,"C-":5.0,"D+":4.0,"D":3.0,"D-":2.0,"F":0.0}
    rows = len(dictionary.keys())
    columns = max(len(dictionary[x]) for x in dictionary.keys())
    studentlist = [[None for x in range(columns + 1)] for x in range(rows + 1)]
    courselist = [[None for x in range(columns + 1)] for x in range(rows + 1)]
    gradematrix = numpy.empty([rows + 1, columns + 1])
    gradematrix[:] = numpy.NAN
    rowcount = 0

    for dummieid in dictionary:
        columncount = 0
        for activity in dictionary[dummieid]:
            # Grab the lowest grade out of dictionary entry.
            temp = float('inf')
            for value in dictionary[dummieid][activity]:
                if value in twelvepointgrademap and twelvepointgrademap[value] < temp:
                    temp = twelvepointgrademap[value]

            if temp == float('inf'):
                grade = numpy.NAN
            else:
                grade = temp

            studentlist[rowcount][columncount] = dummieid
            courselist[rowcount][columncount] = activity
            gradematrix[rowcount][columncount] = grade
            columncount += 1
        rowcount += 1

    return gradematrix, studentlist, courselist

def pruneemptycolumns(gradematrix, dummieidgrid, coursegrid):
    validgradereference = numpy.zeros([len(gradematrix[0]),1])
    for i in range(0,gradematrix.shape[0]):
        for j in range(0,gradematrix.shape[1]):
            if not math.isnan(gradematrix[i][j]):
                validgradereference[j] = validgradereference[j] + 1

    dummieidgrid = transpose(removeblankrows(transpose(dummieidgrid)))
    coursegrid = transpose(removeblankrows(transpose(coursegrid)))

    zerolist,nonzerobool = numpy.where(validgradereference == 0)
    zeroarray = numpy.array(zerolist)
    for i in range(len(zeroarray)):
        gradematrix = numpy.delete(gradematrix,zeroarray[i],1)
        zeroarray = zeroarray - 1

    return gradematrix, dummieidgrid, coursegrid

def transpose(grid):
    return zip(*grid)

def removeblankrows(grid):
    return [list(row) for row in grid if any(row)]

def storematrixandlistsinmemory(gradematrix, dummieidgrid, coursegrid, filename):
        gradematrixname = os.path.splitext(filename)[0].replace("_studentdict","") + "_grademat.npy"
        dummieidgridname = os.path.splitext(filename)[0].replace("_studentdict","") + "_dummieidgrid.cPickle"
        coursegridname = os.path.splitext(filename)[0].replace("_studentdict","") + "_coursegrid.cPickle"
        numpy.save(gradematrixname,gradematrix)
        print(colored("dict2mat ==> SUCCESS --> " + gradematrixname + " file written.","cyan"))

        file = open(dummieidgridname, "wb")
        cPickle.dump(dummieidgrid,file,protocol=2)
        file.close()
        print(colored("dict2mat ==> SUCCESS --> " + dummieidgridname + " file written.","cyan"))

        file = open(coursegridname, "wb")
        cPickle.dump(coursegrid,file,protocol=2)
        file.close()
        print(colored("dict2mat ==> SUCCESS --> " + coursegridname + " file written.","cyan"))

if __name__ == "__main__":
    t0 = time.time()
    main("preprocessing/CSDataFile_ForParry_2014Nov26_studentdict.json")
    t1 = time.time()
    totaltime = t1 - t0
    print(colored("dict2mat =~> " + str(totaltime) + " seconds.","yellow"))