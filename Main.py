'''
    Main class for a CS course grade based recommendation system using machine learning
'''
__author__ = 'sina'
__project__ = 'STProject'

import Recommender
import numpy
import math
import sys
import pprint
import DictionaryDataOps
import MatrixDataOps
import CSDataFileParser
from scipy import stats
from sklearn.decomposition import PCA as skPCA
from sklearn.decomposition import SparsePCA as skSparsePCA
import matplotlib
import operator
import re

def main():
    ######################################################################

    '''
        * Calculations on sparse matrix *
        What we want to do here is take the matrix with means inserted in place
        of sparse values and run PCA on it. Then we want to project that back onto
        the previous full-size matrix. Then we want to plot the mean squared error
        and then do another PCA. We want to repeat this process 99 times. 100 times
        total including the previous step that included inserting the mean values.
    '''
    sparserawmatrix = Recommender.csvfiletomat("pca_input_2d_missing.csv") # Turn the original sparse csv file into a long matrix
    nanmatrix = Recommender.getnanprofile(sparserawmatrix) # generate a matrix that maps where nans are located in original dataset
    intermediateStages = []
    copyoforiginal = sparserawmatrix.copy()
    nextiterationmatrix = Recommender.fillInSparseWithAvg(copyoforiginal) # file in nan values with the mean value for that dimension
    #nextiterationmatrix = Recommender.fillInSparseWithAvg2(copyoforiginal,nanmatrix) # file in nan values with the mean value for that dimension
    numiterations = 100
    count = 0
    finalproduct = []
    for i in range(0,numiterations-1):
        covariancematrix3 = Recommender.covariancematrix(nextiterationmatrix)
        eigenvalues,eigenvectors = Recommender.eigendecompmatrix(covariancematrix3)
        eindex = Recommender.indexOfMax(eigenvalues)
        estimate = Recommender.projectpca(nextiterationmatrix,eigenvalues,eigenvectors,eindex)
        #estimate = Recommender.projectpca2(copyoforiginal,eigenvalues,eigenvectors,eindex)
        if Recommender.rootmeansquared(sparserawmatrix,estimate) != "error":
            intermediateStages.append(Recommender.rootmeansquared(sparserawmatrix,estimate))
        else:
            "error :: improper matrix dimensions"
            sys.exit(0)
        count += 1
        # last time
        if count == numiterations - 1:
            finalproduct.append(nextiterationmatrix)
        print nextiterationmatrix
        nextiterationmatrix = Recommender.fillInMatrixWithEst(nextiterationmatrix,estimate,nanmatrix)
    return

def countnumberofnansinmatrix(matrix):
    return numpy.count_nonzero(numpy.isnan(matrix))

def countnumberortotalstudents(dictionary):
    len(dictionary.keys())

def countnumberofqualifyingtudents(dictionary):
    count = 0
    flag = False
    for student in dictionary:
        if flag:
            count = count + 1
            flag = False
        for grade in dictionary[student]:
            if grade == "A" or grade == "A-" or grade == "B+" or grade == "B" or grade == "B-" or grade == "C+" or grade == "C" or grade == "C-" or grade == "D+" or grade == "D" or grade == "D-" or grade == "F" or grade == "S":
                flag = True

    if flag:
        count = count + 1

    return count

if __name__ == "__main__":
    main()