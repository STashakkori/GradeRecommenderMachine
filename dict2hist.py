#!/usr/bin/python

"""
    dict2hist.py - script that loads a dictionary from a .json file filled with grade data for students. The script then
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
    main - main method of the dict2hist program.
        :param argv: command line argument
        :type argv: string
"""
def main(argv):
    colorama.init(autoreset=True)
    print(colored("dict2hist","blue"))

if __name__ == "__main__":
    usage = colored("dict2hist ==> ERROR --> Improper command line arguments ~~> Usage : python dict2mat.py <dictionary.json> ","red")
    if len(sys.argv) > 2:
        print usage
        exit(-1)

    try:
        t0 = time.time()
        input_filename = sys.argv[1]
        #main(input_filename)
        main("preprocessing/CSDataFile_ForParry_2014Nov26_studentdict.json")
        t1 = time.time()
        totaltime = t1 - t0
        print(colored("dict2hist =~> " + str(totaltime) + " seconds.","yellow"))
    except:
        print usage
        exit(-1)