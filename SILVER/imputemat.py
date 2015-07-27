#!/usr/bin/python

"""
    imputemat.py - script that takes a sparse numpy matrix of grade data and imputes values based on the parameters
                   passed in as command line arguments. The arguments can specify a particular algorithm that is used.
                   Algorithms include the following: MEAN, EIG, SVD, ALS.
"""

__author__ = 'sina'
__project__ = 'STProject'

import colorama
from termcolor import colored
import numpy
import time
import scipy.stats as stats
import math
import sys
import gc

"""
    main - main method of the imputemat program.
        :param argv1: command line argument -> the filename for the .npy matrix in memory.
        :type argv1: string
        :param argv2: command line argument -> the flag that specifies what imputation algorithm to use.
        :type argv2: string
"""
def main(argv1, argv2):
    colorama.init(autoreset=True)
    print(colored("imputemat","blue"))

    #testmatrix = Recommender.csvfiletomat("pca_input_2d_missing.csv")
    #testmatrix = loadmatrixfromdisk(argv1) # refactor to say loadmatrixfromdisk
    #testmatrix = numpy.load(argv1)['data']
    #testmatrix = numpy.array([[0,1,numpy.nan],[2,numpy.nan,3],[4,5,6],[numpy.nan,6,3]])
    #k = 1
    #imputed_matrix = new_pca(testmatrix,k)
    #print imputed_matrix
    #exit(1)
    #imputed_matrix = imputepcafast(testmatrix,k)

    if argv1 and argv1.endswith(".npy"):
        sparse_matrix = loadmatrixfromdisk(argv1)
        if argv2 == "ROWMEAN":
            imputed_matrix = imputerowmean(sparse_matrix)
        elif argv2 == "COLMEAN":
            imputed_matrix = imputecolmean(sparse_matrix)
        elif argv2 == "EIG":
            print ""
            imputed_matrix = imputeeigfull(sparse_matrix)
        elif argv2 == "SVD":
            print ""
            imputed_matrix = imputesvd(sparse_matrix)
        elif argv2 == "ALS":
            imputed_matrix = imputeals(sparse_matrix)
        elif argv2 == "PCA_FAST":
            imputed_matrix = imputepcafast(sparse_matrix,k)
        else:
            print(colored("mat2hist ==> ERROR --> Invalid Algorithm Option ~~> ROWMEAN, COLMEAN, EIG, SVD, or ALS required","red"))

            #storematrixinmemory(argv1,imputed_matrix)

    else:
        print(colored("dict2mat ==> ERROR --> Bad filename input ~~> .json required","red"))
        exit(1)

def imputecolmean(matrix):
    newmatrix = matrix.copy()
    mean = stats.nanmean(newmatrix,axis=0)
    inds = numpy.where(numpy.isnan(newmatrix))
    newmatrix[inds] = numpy.take(mean,inds[1])
    return newmatrix

def imputerowmean(matrix):
    mean = stats.nanmean(matrix,axis=1)
    for i in range(0,matrix.shape[0]):
        for j in range(0,matrix.shape[1]):
            if math.isnan(matrix[i,j]):
                matrix[i,j] = mean[i]
    return matrix

def imputepcafast(matrix,k):
    filledinmatrix = imputecolmean(matrix)
    rmsestack = []
    distance = float('inf')
    debug_mode = False

    for iteration in range(0,100):
        gc.collect()
        mean = filledinmatrix.mean(axis=0)
        meansubtracted = numpy.subtract(filledinmatrix[:,:],mean)
        u,v = calcals(meansubtracted,k)
        del meansubtracted
        newmatrix = numpy.dot(u,v)

        for i in range(0,newmatrix.shape[1]):
            newmatrix[:,i] += mean[i]
        del mean
        newrmse = rootmeansquared(matrix,newmatrix)
        if rmsestack:
            oldrmse = rmsestack.pop()
            distance = ((oldrmse - newrmse)/oldrmse)
            del oldrmse
        if debug_mode:
            print("iteration: " + str(iteration + 1) + "  rmse: " + str(newrmse) + "  distance: " + str(distance))
        if distance < .00001: break
        del distance
        rmsestack.append(newrmse)
        filledinmatrix[numpy.isnan(matrix)] = newmatrix[numpy.isnan(matrix)]
        del newmatrix
    return filledinmatrix

def imputepcaslow(matrix,k):
    filledinmatrix = imputecolmean(matrix)
    rmsestack = []
    distance = float('inf')

    for iteration in range(0,100):
        gc.collect()
        mean = filledinmatrix.mean(axis=0)
        meansubtracted = numpy.subtract(filledinmatrix[:,:],mean)
        u,s,v = numpy.linalg.svd(meansubtracted,full_matrices=False)
        del meansubtracted
        newmatrix = numpy.dot(u[:,:k],numpy.dot(numpy.diag(s[:k]),v[:k,:]))

        for i in range(0,newmatrix.shape[1]):
            newmatrix[:,i] += mean[i]
        del mean
        newrmse = rootmeansquared(matrix,newmatrix)
        if rmsestack:
            oldrmse = rmsestack.pop()
            distance = ((oldrmse - newrmse)/oldrmse)
            del oldrmse
        print("iteration: " + str(iteration + 1) + "  rmse: " + str(newrmse) + "  distance: " + str(distance))
        if distance < .00001: break
        del distance
        rmsestack.append(newrmse)
        filledinmatrix[numpy.isnan(matrix)] = newmatrix[numpy.isnan(matrix)]
        del newmatrix
    return filledinmatrix

def imputesvd(matrix,k):
    filledinmatrix = imputecolmean(matrix)
    rmsestack = []
    distance = float('inf')

    for iteration in range(0,100):
        gc.collect()
        u,s,v = numpy.linalg.svd(filledinmatrix,full_matrices=False)
        newmatrix = numpy.dot(u[:,:k],numpy.dot(numpy.diag(s[:k]),v[:k,:]))
        newrmse = rootmeansquared(matrix,newmatrix)
        if rmsestack:
            oldrmse = rmsestack.pop()
            distance = ((oldrmse - newrmse)/oldrmse)
            del oldrmse
        print("iteration: " + str(iteration + 1) + "  rmse: " + str(newrmse) + "  distance: " + str(distance))
        if distance < .00001: break
        del distance
        rmsestack.append(newrmse)
        filledinmatrix[numpy.isnan(matrix)] = newmatrix[numpy.isnan(matrix)]
        del newmatrix
    return filledinmatrix

def imputeals(matrix,k):
    filledinmatrix = imputecolmean(matrix)
    rmsestack = []
    # ^^ make single variable instead of stack.
    distance = float('inf')

    for iteration in range(0,100):
        gc.collect()
        u,v = calcals(filledinmatrix,k)
        newmatrix = numpy.dot(u,v)
        newrsse = numpy.norm(matrix - newmatrix)
        if rmsestack:
            oldrmse = rmsestack.pop()
            distance = ((oldrmse - newrsse)/oldrmse)
            del oldrmse
        print("iteration: " + str(iteration + 1) + "  rsse: " + str(newrsse) + "  distance: " + str(distance))
        if distance < .00001: break
        del distance
        rmsestack.append(newrsse)
        filledinmatrix[numpy.isnan(matrix)] = newmatrix[numpy.isnan(matrix)]
        del newmatrix
    return filledinmatrix

def calcals(matrix,k):
    oldrss = float('inf')
    rss = float('inf')
    diff = float('inf')
    x = matrix # x -> (m x n)
    m = x.shape[0]
    n = x.shape[1]
    v = numpy.random.normal(0.0,1.0,(k,n)) # v -> (k x n)
    while rss > .00001:
        utranspose = numpy.linalg.lstsq(v.T, x.T)[0]
        u = utranspose.T # u -> (m x k)
        v = numpy.linalg.lstsq(u, x)[0]
        approx = numpy.dot(u, v)
        rss = numpy.linalg.norm(x - approx)
        diff = (oldrss - rss) / oldrss
        oldrss = rss
        if diff < .00001: break
    return u, v

def imputeeigfull(matrix):
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
        targeteigvector = eigenvectors[:,eindex]
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

def imputesvdfull(matrix):
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

def fast_svd(matrix,k):
    u,v = fast_als(matrix,k)
    new_matrix = numpy.dot(u,v)
    matrix[numpy.isnan(matrix)] = new_matrix[numpy.isnan(matrix)]
    del new_matrix
    return matrix

def fast_als(matrix, k):
    oldrss = float('inf')
    rss = float('inf')
    diff = float('inf')
    x = matrix # x -> (m x n)
    m = x.shape[0]
    n = x.shape[1]
    u = numpy.random.normal(0.0, 1.0, (m, k))
    utranspose = u.T
    v = numpy.random.normal(0.0, 1.0, (k, n)) # v -> (k x n)
    count = 0

    while rss > .00001:
        for i in range(m):
            p = ~numpy.isnan(x[i, :])
            utranspose[:, i] = numpy.linalg.lstsq(v[:, p].T, x[i, p].T)[0]
        for j in range(n):
            p = ~numpy.isnan(x[:, j])
            v[:, j] = numpy.linalg.lstsq(u[p, :], x[p, j])[0]

        u = utranspose.T
        approx = numpy.dot(u, v)
        index = ~numpy.isnan(x)
        rss = numpy.linalg.norm(x[index] - approx[index]) / math.sqrt(index.size)
        diff = (oldrss - rss) / oldrss
        print(str(rss) + " " + str(diff))
        oldrss = rss
        if diff < .00001: break
    u[u > numpy.nanmax(x[:])] = numpy.nanmax(x[:])
    u[u < numpy.nanmin(x[:])] = numpy.nanmin(x[:])
    return u, v

def fast_pca(matrix,k):
    mean = numpy.nanmean(matrix, axis = 0)
    meansubtracted = numpy.subtract(matrix[:,:],mean)
    u,v = fast_als(meansubtracted,k)
    new_matrix = numpy.dot(u,v)
    matrix[numpy.isnan(matrix)] = new_matrix[numpy.isnan(matrix)]
    for i in range(0,matrix.shape[1]):
        matrix[:,i] += mean[i]
    del mean
    del new_matrix
    return matrix

def rootsumsquared(matrix1,matrix2):
    originalmatrix = matrix1.copy()
    modelmatrix = matrix2.copy()
    if originalmatrix.shape != modelmatrix.shape:
        return "error"

    sum = 0

    for i in range(0,originalmatrix.shape[0]):
        for j in range(0,originalmatrix.shape[1]):
            # if we are at a missing value we can't calculate msd so we move on
            if not math.isnan(originalmatrix[i,j]) and not math.isnan(modelmatrix[i,j]):
                difference = originalmatrix[i,j] - modelmatrix[i,j]
                square = difference ** 2
                sum = sum + square

    return math.sqrt(sum)

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
                square = difference ** 2
                sum = sum + square
                size = size + 1.0

    mean = sum/size
    return math.sqrt(mean)

def loadmatrixfromdisk(filename):
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
        main(filename,algorithm) # main(["preprocessing/CSDataFile_ForParry_2014Nov26_grademat.npy","EIG"])
        t1 = time.time()
        totaltime = t1 - t0
        print(colored("imputemat ~=> " + str(totaltime) + " seconds.","yellow"))
    except IOError as e:
        print e.strerror
        print usage
        exit(-1)


