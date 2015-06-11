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
    import Recommender
    testmatrix = Recommender.csvfiletomat("pca_input_2d_missing.csv")
    #imputedmatrix = imputesvd(testmatrix)

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
            print "test"
        elif argv2 == "ALS":
            imputedmatrix = imputeals(sparsematrix)
        else:
            print(colored("mat2hist ==> ERROR --> Invalid Algorithm Option ~~> ROWMEAN, COLMEAN, EIG, SVD, or ALS required","red"))

        print imputedmatrix
        #storematrixinmemory(argv1,imputedmatrix)

    else:
        print(colored("dict2mat ==> ERROR --> Bad filename input ~~> .json required","red"))
        exit(1)

def imputecolmean(matrix):
    mean = stats.nanmean(matrix,axis=0)
    for i in range(0,matrix.shape[0]):
        for j in range(0,matrix.shape[1]):
            if math.isnan(matrix[i,j]):
                matrix[i,j] = mean[j]
    return matrix

def imputerowmean(matrix):
    mean = stats.nanmean(matrix,axis=1)
    for i in range(0,matrix.shape[0]):
        for j in range(0,matrix.shape[1]):
            if math.isnan(matrix[i,j]):
                matrix[i,j] = mean[i]
    return matrix

def imputeeig(matrix):
    copyofmatrix = matrix.copy()
    nanprofile = getnanprofile(matrix)
    filledinmatrix = imputecolmean(copyofmatrix)

    for i in range(0,100):
        covariancematrix = numpy.cov(filledinmatrix.T)
        eigenvalues,eigenvectors = numpy.linalg.eig(covariancematrix)
        eindex = numpy.argmax(eigenvalues)
        mean = filledinmatrix.mean(axis=0)
        meancopy = filledinmatrix.mean(axis=0)
        meansubtracted = numpy.subtract(filledinmatrix[:,:],meancopy)
        print eigenvectors
        targeteigvector = eigenvectors[:,eindex]
        temp = targeteigvector.reshape(targeteigvector.size,1)
        newmatrix = numpy.dot(meansubtracted,temp)
        newmatrix = numpy.dot(newmatrix,temp.T)
        for i in range(0,newmatrix.shape[1]):
            newmatrix[:,i] += mean[i]

        #print rootmeansquared(matrix,newmatrix)

        for i in range(0,filledinmatrix.shape[0]):
            for j in range(0,filledinmatrix.shape[1]):
                if nanprofile[i,j] == 1:
                    filledinmatrix[i,j] = newmatrix[i,j]

    return filledinmatrix

def imputesvd(matrix):
    copyofmatrix = matrix.copy()
    nanprofile = getnanprofile(matrix)
    filledinmatrix = imputecolmean(copyofmatrix)

    for i in range(0,100):
        covariancematrix = numpy.cov(filledinmatrix.T)
        u,svmatrix,v = numpy.linalg.svd(covariancematrix)
        sindex = numpy.argmax(svmatrix)
        mean = filledinmatrix.mean(axis=0)
        meancopy = filledinmatrix.mean(axis=0)
        meansubtracted = numpy.subtract(filledinmatrix[:,:],meancopy)
        v = v.T
        targeteigvector = v[:,sindex]
        temp = targeteigvector.reshape(targeteigvector.size,1)
        newmatrix = numpy.dot(meansubtracted,temp)
        newmatrix = numpy.dot(newmatrix,temp.T)
        for i in range(0,newmatrix.shape[1]):
            newmatrix[:,i] += mean[i]

        print rootmeansquared(matrix,newmatrix)

        for i in range(0,filledinmatrix.shape[0]):
            for j in range(0,filledinmatrix.shape[1]):
                if nanprofile[i,j] == 1:
                    filledinmatrix[i,j] = newmatrix[i,j]

    return filledinmatrix

def imputeals(matrix):
    copyofmatrix = matrix.copy()
    nanprofile = getnanprofile(matrix)


    return None

#preprocessing/CSDataFile_ForParry_2014Nov26_grademat.npy EIG

def rootmeansquared(matrix1,matrix2):
    originalmatrix = matrix1.copy()
    modelmatrix = matrix2.copy()
    if originalmatrix.shape != modelmatrix.shape:
        return "error"

    sum = 0
    size = 0

    for i in range(0,originalmatrix.shape[0]):
        for j in range(0,originalmatrix.shape[1]):
            # if we are at a missing value we can't calculate msd so we move on
            if not math.isnan(originalmatrix[i,j]) and not math.isnan(modelmatrix[i,j]):
                difference = originalmatrix[i,j] - modelmatrix[i,j]
                square = difference**2
                sum = sum + square
                size = size + 1.0

    mean = sum/size
    return math.sqrt(mean)

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
            if math.isnan(matrix[i,j]):
                nanmatrix[i,j] = 1

    return nanmatrix

def countnumberofnansinmatrix(matrix):
    return numpy.count_nonzero(numpy.isnan(matrix))

if __name__ == "__main__":
    usage = colored("imputemat ==> ERROR --> Improper command line arguments ~~> Usage : python imputemat.py <matrix.npy> <ROWMEAN, COLMEAN, EIG, SVD, or ALS>","red")
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


