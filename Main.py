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
    '''
        Calculations on non-sparse matrix
    '''

    d = DictionaryDataOps.loadergetter()
    w = MatrixDataOps.loadergetter()
    print "MATRIX HERE %%%%%%%%%***"
    print w.gradematrix
    w.pruneEmptyColumns()
    record = w.get_results("C S 1440")
    counts = w.countsmapper(record)
    d.recordgradehistogrammer(counts)
    #w.recordgradehistogrammer(record)

    exit(1)

    ######################################################################

    '''
        * Calculations on sparse matrix *
        What we want to do here is take the matrix with means inserted in place
        of sparse values and run PCA on it. Then we want to project that back onto
        the previous full-size matrix. Then we want to plot the mean squared error
        and then do another PCA. We want to repeat this process 99 times. 100 times
        total including the previous step that included inserting the mean values.
    '''
    print "**********************************"
    print "** STARTING SPARSE COMPUTATIONS **"
    print "**********************************"
    '''
    sparserawmatrix = Recommender.csvfiletomat("pca_input_2d_missing.csv") # Turn the original sparse csv file into a long matrix
    nanmatrix = Recommender.getnanprofile(sparserawmatrix) # generate a matrix that maps where nans are located in original dataset
    intermediateStages = []
    copyoforiginal = sparserawmatrix.copy()
    nextiterationmatrix = Recommender.fillInSparseWithAvg(copyoforiginal) # file in nan values with the mean value for that dimension
    print "**********************************"
    print "**     FILL IN AVERAGE STEP     **"
    print "**********************************"
    #nextiterationmatrix = Recommender.fillInSparseWithAvg2(copyoforiginal,nanmatrix) # file in nan values with the mean value for that dimension
    print "matrixwithavg"
    print nextiterationmatrix
    numiterations = 100
    count = 0
    finalproduct = []
    for i in range(0,numiterations-1):
        covariancematrix3 = Recommender.covariancematrix(nextiterationmatrix)
        eigenvalues,eigenvectors = Recommender.eigendecompmatrix(covariancematrix3)
        eindex = Recommender.indexOfMax(eigenvalues)
        estimate = Recommender.projectpca(nextiterationmatrix,eigenvalues,eigenvectors,eindex)
        #estimate = Recommender.projectpca2(copyoforiginal,eigenvalues,eigenvectors,eindex)
        print "TESTING ESTIMATE"
        print estimate
        if Recommender.rootmeansquared(sparserawmatrix,estimate) != "error":
            intermediateStages.append(Recommender.rootmeansquared(sparserawmatrix,estimate))
        else:
            "error :: improper matrix dimensions"
            sys.exit(0)
        count += 1
        # last time
        if count == numiterations - 1:
            finalproduct.append(nextiterationmatrix)
        nextiterationmatrix = Recommender.fillInMatrixWithEst(nextiterationmatrix,estimate,nanmatrix)
        print "iteration"
        print "---------"
        print i
        print "nextiterationmatrix"
        print nextiterationmatrix
'''
    # Uncomment these for graphs and pca iterations
    #Recommender.plotConvergence2(intermediateStages)
    #Recommender.plotLastStage(nextiterationmatrix)
    #CSDataFileParser.parsecsv('CSDataFile_ForParry_2014Nov26.csv')
    d = DictionaryDataOps.loadergetter()
    entry = d.get_results_dictionary("1400002")
    entry2 = d.get_results_dictionary("C S 2490")
    d.numberofstudents = countnumberofqualifyingtudents(entry2)
    print ":: STUFF ::"
    d.grademerger(entry2)
    counts = d.countsmapper(d.gradelist)
    #d.recordgradehistogrammer(counts)

    g,s,c = d.convertDictionaryToMatrix(d.studentdict)
    d.storeMatrixInMemoryAscPickle(g,s,c,"preprocessing/gradematrix.cPickle","preprocessing/studentgrid.cPickle","preprocessing/coursegrid.cPickle")

    print "TESTING THE MATRICES"

    w = MatrixDataOps.loadergetter()
    print "MATRIX HERE %%%%%%%%%***"
    print w.gradematrix
    w.pruneEmptyColumns()
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(w.gradematrix)

    print str(w.gradematrix[0][0])
    print str(w.studentgrid[0][0])
    print str(w.coursegrid[0][0])

    '''
    matrix = numpy.random.rand(d.gradematrix.shape[0],d.gradematrix.shape[1])
    print matrix.shape
    print matrix
    covariancematrix3 = Recommender.covariancematrix(matrix)
    print covariancematrix3.shape
    eigenvalues,eigenvectors = Recommender.eigendecompmatrix(covariancematrix3)
    print eigenvalues.shape
    print eigenvectors.shape
    '''

    #print d.get_results_matrix("1403262")
    testentry = w.get_results("C S 1440")
    print "TEST ENTRY"
    print testentry
    testcounts = w.countsmapper(testentry)
    print testcounts
    w.recordgradehistogrammer(testentry)

    #pp.pprint(d.coursegrid)

    #pp.pprint(studentlist)
    #pp.pprint(courselist)

    #numpy.set_printoptions(threshold=numpy.nan)
    #print matrix
    '''
    nanmatrix = Recommender.getnanprofile(gradematrix)
    intermediateStages = []
    copyoforiginal = gradematrix.copy()
    nextiterationmatrix = Recommender.fillInSparseWithAvg(copyoforiginal) # file in nan values with the mean value for that dimension
    print("NANS after :: " + str(countnumberofnansinmatrix(nextiterationmatrix)))
    print "TESTING 123 123 123 123 123"
    print nextiterationmatrix
    print "**********************************"
    print "**     FILL IN AVERAGE STEP     **"
    print "**********************************"
    #nextiterationmatrix = Recommender.fillInSparseWithAvg2(copyoforiginal,nanmatrix) # file in nan values with the mean value for that dimension
    print "matrixwithavg"
    print nextiterationmatrix
    numiterations = 100
    count = 0
    finalproduct = []
    for i in range(0,numiterations-1):
        covariancematrix3 = Recommender.covariancematrix(nextiterationmatrix)
        eigenvalues,eigenvectors = Recommender.eigendecompmatrix(covariancematrix3)
        eindex = Recommender.indexOfMax(eigenvalues)
        estimate = Recommender.projectpca(nextiterationmatrix,eigenvalues,eigenvectors,eindex)
        #estimate = Recommender.projectpca2(copyoforiginal,eigenvalues,eigenvectors,eindex)
        #print "TESTING ESTIMATE"
        #print estimate
        if Recommender.rootmeansquared(gradematrix,estimate) != "error":
            intermediateStages.append(Recommender.rootmeansquared(gradematrix,estimate))
        else:
            "error :: improper matrix dimensions"
            sys.exit(0)
        count += 1
        # last time
        if count == numiterations - 1:
            finalproduct.append(nextiterationmatrix)
        nextiterationmatrix = Recommender.fillInMatrixWithEst(nextiterationmatrix,estimate,nanmatrix)
        #print "iteration"
        #print "---------"
        #print i
        #print "nextiterationmatrix"
        #print nextiterationmatrix
    '''
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