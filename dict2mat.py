#!/usr/bin/python

"""
    dict2mat.py - script that loads a dictionary from a .json file filled with grade data for students. The script then
                  converts that data to a numpy matrix of grades and two lists filled with course data and student
                  dummie id data for reference. The matrix and two lists are saved in memory in the preprocessing
                  directory.
"""

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
import sys

"""
    main - main method of the dict2mat program.
        :param argv: command line argument
        :type argv: string
"""
def main(argv):
    colorama.init(autoreset=True)
    print(colored("dict2mat","blue"))
    if argv and argv.endswith(".json"):
        studentmap = loadjson(argv)
        g,d,c,sv,sm,ae,am,m1,m2,m3,h = convertdictionarytomatrix(studentmap)
        g,d,c,sv,sm,ae,am,m1,m2,m3,h = pruneemptycolumns(g,d,c,sv,sm,ae,am,m1,m2,m3,h)
        storematrixandlistsinmemory(g,d,c,sv,sm,ae,am,m1,m2,m3,h,argv)

    else:
        print(colored("dict2mat ==> ERROR --> Bad filename input ~~> .json required","red"))
        exit(1)

"""
    loadjson - method that loads a json object from memory and returns it.
"""
def loadjson(filename):
        f = open(filename,"rb")
        j = json.loads(open(filename).read())
        f.close()
        return j

"""
    convertdictionarytomatrix - method that loops through a dictionary that is indexable by student and generates an
                                equivalent 3 datastructures. Gradematrix is a numpy matrix of all the grades. Dummieidgrid
                                is a 2d list that holds dummie ids. Coursegrid is a 2d list that holds course names. Both
                                Dummieidgrid and coursegrid have the same dimensions as gradematrix and have an element
                                to element correspondence.
"""
def convertdictionarytomatrix(dictionary):
    twelvepointgrademap = {"A":12.0,"A-":11.0,"B+":10.0,"B":9.0,"B-":8.0,"C+":7.0,"C":6.0,"C-":5.0,"D+":4.0,"D":3.0,"D-":2.0,"F":0.0}
    rows = len(dictionary.keys())
    columns = max(len(dictionary[x]) for x in dictionary.keys())
    dummieidgrid = [[None for x in range(columns + 1)] for x in range(rows + 1)]
    coursegrid = [[None for x in range(columns + 1)] for x in range(rows + 1)]
    satvgrid = [[None for x in range(columns + 1)] for x in range(rows + 1)]
    satmgrid = [[None for x in range(columns + 1)] for x in range(rows + 1)]
    actenggrid = [[None for x in range(columns + 1)] for x in range(rows + 1)]
    actmatgrid = [[None for x in range(columns + 1)] for x in range(rows + 1)]
    mathplm1grid = [[None for x in range(columns + 1)] for x in range(rows + 1)]
    mathplm2grid = [[None for x in range(columns + 1)] for x in range(rows + 1)]
    mathplm3grid = [[None for x in range(columns + 1)] for x in range(rows + 1)]
    hsgpagrid = [[None for x in range(columns + 1)] for x in range(rows + 1)]

    gradematrix = numpy.empty([rows + 1, columns + 1])
    gradematrix[:] = numpy.NAN
    rowcount = 0
    testcount = 0

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

            dummieidgrid[rowcount][columncount] = dummieid
            coursegrid[rowcount][columncount] = activity
            gradematrix[rowcount][columncount] = grade

            if activity == "SATV_score":
                satvgrid[rowcount][0:columns+1] = [dictionary[dummieid][activity]] * (columns + 1)

            if activity == "SATM_score":
                satmgrid[rowcount][0:columns+1] = [dictionary[dummieid][activity]] * (columns + 1)

            if activity == "ACTEng_score":
                actenggrid[rowcount][0:columns+1] = [dictionary[dummieid][activity]] * (columns + 1)

            if activity == "ACTMat_score":
                actmatgrid[rowcount][0:columns+1] = [dictionary[dummieid][activity]] * (columns + 1)

            if activity == "MathPlacement_PLM1_Score":
                mathplm1grid[rowcount][0:columns+1] = [dictionary[dummieid][activity]] * (columns + 1)

            if activity == "MathPlacement_PLM2_Score":
                mathplm2grid[rowcount][0:columns+1] = [dictionary[dummieid][activity]] * (columns + 1)

            if activity == "MathPlacement_PLM3_Score":
                mathplm3grid[rowcount][0:columns+1] = [dictionary[dummieid][activity]] * (columns + 1)

            if activity == "HSGPA":
                hsgpagrid[rowcount][0:columns+1] = [dictionary[dummieid][activity]] * (columns + 1)

            columncount += 1
        rowcount += 1
    return gradematrix, dummieidgrid, coursegrid, satvgrid, satmgrid, actenggrid, actmatgrid, mathplm1grid, mathplm2grid, mathplm3grid, hsgpagrid

"""
    pruneemptycolumns - method that removes columns that are populated entirely with NAN's
"""
def pruneemptycolumns(gradematrix, dummieidgrid, coursegrid, satvgrid, satmgrid, actenggrid, actmatgrid, mathplm1grid, mathplm2grid, mathplm3grid, hsgpagrid):
    validgradereference = numpy.zeros([len(gradematrix[0]),1])
    for i in range(0,gradematrix.shape[0]):
        for j in range(0,gradematrix.shape[1]):
            if not math.isnan(gradematrix[i][j]):
                validgradereference[j] = validgradereference[j] + 1

    dummieidgrid = transpose(removeblankrows(transpose(dummieidgrid)))
    coursegrid = transpose(removeblankrows(transpose(coursegrid)))
    satvgrid = transpose(removeblankrows(transpose(satvgrid)))
    satmgrid = transpose(removeblankrows(transpose(satmgrid)))
    actenggrid = transpose(removeblankrows(transpose(actenggrid)))
    actmatgrid = transpose(removeblankrows(transpose(actmatgrid)))
    mathplm1grid = transpose(removeblankrows(transpose(mathplm1grid)))
    mathplm2grid = transpose(removeblankrows(transpose(mathplm2grid)))
    mathplm3grid = transpose(removeblankrows(transpose(mathplm3grid)))
    hsgpagrid = transpose(removeblankrows(transpose(hsgpagrid)))

    zerolist,nonzerobool = numpy.where(validgradereference == 0)
    zeroarray = numpy.array(zerolist)
    for i in range(len(zeroarray)):
        gradematrix = numpy.delete(gradematrix,zeroarray[i],1)
        zeroarray = zeroarray - 1

    return gradematrix, dummieidgrid, coursegrid, satvgrid, satmgrid, actenggrid, actmatgrid, mathplm1grid, mathplm2grid, mathplm3grid, hsgpagrid

"""
    transpose - method that transposes a 2d list datastructure.
"""
def transpose(grid):
    return zip(*grid)

"""
    removeblankrows - method that removes empty rows from a 2d list datastructure.
"""
def removeblankrows(grid):
    return [list(row) for row in grid if any(row)]

"""
    storematrixandlistsinmemory - method that stores gradematrix, dummieidgrid, and coursegrid into memory.
"""
def storematrixandlistsinmemory(gradematrix, dummieidgrid, coursegrid, satvgrid, satmgrid, actenggrid, actmatgrid, mathplm1grid, mathplm2grid, mathplm3grid, hsgpagrid, filename):
        gradematrixname = os.path.splitext(filename)[0].replace("_studentdict","") + "_grademat.npy"
        dummieidgridname = os.path.splitext(filename)[0].replace("_studentdict","") + "_dummieidgrid.cPickle"
        coursegridname = os.path.splitext(filename)[0].replace("_studentdict","") + "_coursegrid.cPickle"
        satvgridname = os.path.splitext(filename)[0].replace("_studentdict","") + "_satvgrid.cPickle"
        satmgridname = os.path.splitext(filename)[0].replace("_studentdict","") + "_satmgrid.cPickle"
        actenggridname = os.path.splitext(filename)[0].replace("_studentdict","") + "_actenggrid.cPickle"
        actmatgridname = os.path.splitext(filename)[0].replace("_studentdict","") + "_actmatgrid.cPickle"
        mathplm1gridname = os.path.splitext(filename)[0].replace("_studentdict","") + "_mathplm1grid.cPickle"
        mathplm2gridname = os.path.splitext(filename)[0].replace("_studentdict","") + "_mathplm2grid.cPickle"
        mathplm3gridname = os.path.splitext(filename)[0].replace("_studentdict","") + "_mathplm3grid.cPickle"
        hsgpagridname = os.path.splitext(filename)[0].replace("_studentdict","") + "_hsgpagrid.cPickle"
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

        file = open(satvgridname, "wb")
        cPickle.dump(satvgrid,file,protocol=2)
        file.close()
        print(colored("dict2mat ==> SUCCESS --> " + satvgridname + " file written.","cyan"))

        file = open(satmgridname, "wb")
        cPickle.dump(satmgrid,file,protocol=2)
        file.close()
        print(colored("dict2mat ==> SUCCESS --> " + satmgridname + " file written.","cyan"))

        file = open(actenggridname, "wb")
        cPickle.dump(actenggrid,file,protocol=2)
        file.close()
        print(colored("dict2mat ==> SUCCESS --> " + actenggridname + " file written.","cyan"))

        file = open(actmatgridname, "wb")
        cPickle.dump(actmatgrid,file,protocol=2)
        file.close()
        print(colored("dict2mat ==> SUCCESS --> " + actmatgridname + " file written.","cyan"))

        file = open(mathplm1gridname, "wb")
        cPickle.dump(mathplm1grid,file,protocol=2)
        file.close()
        print(colored("dict2mat ==> SUCCESS --> " + mathplm1gridname + " file written.","cyan"))

        file = open(mathplm2gridname, "wb")
        cPickle.dump(mathplm2grid,file,protocol=2)
        file.close()
        print(colored("dict2mat ==> SUCCESS --> " + mathplm2gridname + " file written.","cyan"))

        file = open(mathplm3gridname, "wb")
        cPickle.dump(mathplm3grid,file,protocol=2)
        file.close()
        print(colored("dict2mat ==> SUCCESS --> " + mathplm3gridname + " file written.","cyan"))

        file = open(hsgpagridname, "wb")
        cPickle.dump(hsgpagrid,file,protocol=2)
        file.close()
        print(colored("dict2mat ==> SUCCESS --> " + hsgpagridname + " file written.","cyan"))

if __name__ == "__main__":
    usage = colored("dict2mat ==> ERROR --> Improper command line arguments ~~> Usage : python dict2mat.py <dictionary.json> ","red")
    if len(sys.argv) > 2:
        print usage
        exit(-1)

    try:
        t0 = time.time()
        input_filename = sys.argv[1]
        main(input_filename) # main("preprocessing/CSDataFile_ForParry_2014Nov26_studentdict.json")
        t1 = time.time()
        totaltime = t1 - t0
        print(colored("dict2mat ~=> " + str(totaltime) + " seconds.","yellow"))
    except IOError as e:
        print usage
        exit(-1)