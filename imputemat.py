#!/usr/bin/python

"""
    imputemat.py - script that takes a sparse numpy matrix of grade data and imputes values based on the parameters
                   passed in as command line arguments. The arguments can specify a particular algorithm that is used.
                   Algorithms include the following: MEAN, EIG, SVD, ALS.
"""

__author__ = 'sina'
__project__ = 'STProject'

from matplotlib import mlab
import operator
import colorama
from termcolor import colored
import cPickle
import numpy
import time
import scipy.stats as stats
import matplotlib.pyplot as plt
from collections import OrderedDict
import math
import sys

'''
    main - main method of the imputemat program.
        :param argv1: command line argument -> the filename for the .npy matrix in memory.
        :type argv1: string
        :param argv2: command line argument -> the flag that specifies what imputation algorithm to use.
        :type argv2: string
'''
def main(argv1,argv2):
    colorama.init(autoreset=True)
    print(colored("imputemat","blue"))
    if argv1 and argv1.endswith(".npy"):
        sparsematrix = loadmatrixfrommemory(argv1)
        if argv2 == "ROWMEAN":
            imputedmatrix = imputerowmean(sparsematrix)
        elif argv2 == "COLMEAN":
            imputedmatrix = imputecolmean(sparsematrix)
        elif argv2 == "EIG":
            imputedmatrix = imputeeig(sparsematrix)
        elif argv2 == "SVD":
            imputedmatrix = imputesvd(sparsematrix)
        elif argv2 == "ALS":
            imputedmatrix = imputeals(sparsematrix)
        else:
            print(colored("mat2hist ==> ERROR --> Invalid Algorithm Option ~~> ROWMEAN, COLMEAN, EIG, SVD, or ALS required","red"))

        #storematrixinmemory(argv1,imputedmatrix)

    else:
        print(colored("dict2mat ==> ERROR --> Bad filename input ~~> .json required","red"))
        exit(1)

def imputecolmean(matrix):
    mean = stats.nanmean(matrix,axis=0)
    print mean.shape
    for i in range(0,matrix.shape[0]):
        for j in range(0,matrix.shape[1]):
            if math.isnan(matrix[i,j]):
                matrix[i,j] = mean[j]
    return matrix

def imputerowmean(matrix):
    mean = stats.nanmean(matrix,axis=1)
    print mean.shape
    for i in range(0,matrix.shape[0]):
        for j in range(0,matrix.shape[1]):
            if math.isnan(matrix[i,j]):
                matrix[i,j] = mean[i]
    return matrix

def imputeeig(matrix):
    nanprofile = getnanprofile(matrix)
    copyofmatrix = matrix.copy()
    filledinmatrix = imputecolmean(copyofmatrix)
    for i in range(0,100):
        covariancematrix = numpy.cov(filledinmatrix.T)
        eigenvalues,eigenvectors = numpy.linalg.eig(covariancematrix)
        eindex = numpy.argmax(eigenvalues)
        mean = copyofmatrix.mean(axis=0)
        meancopy = copyofmatrix.mean(axis=0)
        copyofmatrix = numpy.subtract(copyofmatrix[:,:],mean)
        targeteigvector = eigenvectors[:,eindex]
        temp = targeteigvector.reshape(targeteigvector.size,1)
        newmatrix = numpy.dot(copyofmatrix,temp)
        newmatrix = numpy.dot(newmatrix,temp.T)
        for i in range(0,newmatrix.shape[1]):
            newmatrix[:i] += mean[i]

        for i in range(0,temp.shape[0]):
            for j in range(0,temp.shape[1]):
                if nanprofile[i,j] == 1:
                    temp[i,j] = newmatrix[i,j]

    return temp

def eigendecomposition(matrix):


def imputesvd(matrix):
    return None

def imputeals(matrix):
    return None

def loadmatrixfrommemory(filename):
    gradematrix = numpy.load(filename)
    return gradematrix

def storematrixinmemory(filename,matrix):
    imputedmatrixname = filename.replace("_grademat.npy","_imputedgrademat.npy")
    numpy.save(imputedmatrixname,matrix)
    print(colored("dict2mat ==> SUCCESS --> " + imputedmatrixname + " file written.","cyan"))

def getnanprofile(matrix):
    nanmatrix = numpy.zeros(shape=(matrix.shape[0],matrix.shape[1]))
    for i in range(0,matrix.shape[0]):
        for j in range(0,matrix.shape[1]):
            if j == 0 and math.isnan(matrix[i,j]):
                nanmatrix[i,j] = 1
            elif j == 1 and math.isnan(matrix[i,j]):
                nanmatrix[i,j] = 1
    return nanmatrix

if __name__ == "__main__":
    usage = colored("imputemat ==> ERROR --> Improper command line arguments ~~> Usage : python imputemat.py <matrix.npy> <dummieid or \"coursename\">","red")
    if len(sys.argv) > 3:
        print usage
        exit(-1)
    try:
        t0 = time.time()
        filename = sys.argv[1]
        algorithm = sys.argv[2]
        main(filename,algorithm) # main(["preprocessing/CSDataFile_ForParry_2014Nov26_grademat.npy","1400001"])
        t1 = time.time()
        totaltime = t1 - t0
        print(colored("imputemat =~> " + str(totaltime) + " seconds.","yellow"))
    except:
        print usage
        exit(-1)


