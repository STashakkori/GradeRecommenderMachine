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
import CSDataFileParser
from scipy import stats
from sklearn.decomposition import PCA as skPCA
from sklearn.decomposition import SparsePCA as skSparsePCA
import matplotlib
import operator
import re

twelvepointgrademap = {"A":12.0,"S":12.0,"A-":11.0,"B+":10.0,"B":9.0,"B-":8.0,"C+":7.0,"C":6.0,"C-":5.0,"D+":4.0,"D":3.0,"D-":2.0,"F":0.0,"U":0.0}

def main():
    '''
        Calculations on non-sparse matrix
    '''
    rawmatrix = Recommender.csvfiletomat("pca_input_2d.csv")
    rawsubmeanmatrix = Recommender.subtractcolmeancolslongmat(rawmatrix)
    covariancematrix = Recommender.covariancematrix(rawsubmeanmatrix)
    eigenvalues,eigenvectors = Recommender.eigendecompmatrix(covariancematrix)
    u,svmatrix,v = numpy.linalg.svd(covariancematrix)
    eindex = Recommender.indexOfMax(eigenvalues)
    svdlatentmatrix = Recommender.plotpcompprojection(rawmatrix,eigenvalues,eigenvectors,eindex)
    sindex = Recommender.indexOfMax(svmatrix)
    pcalatentmatrix = Recommender.plotsvd(rawmatrix,u,svmatrix,v,sindex)

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
    import DataOps
    d = DataOps.loadergetter()
    entry = d.get_results("1400002")
    entry2 = d.get_results("C S 2490")
    d.numberofstudents = countnumberofqualifyingtudents(entry2)
    print ":: STUFF ::"
    d.grademerger(entry2)
    counts = d.countsmapper(d.gradelist)
    #d.recordgradehistogrammer(counts)

    gradematrix, studentlist, courselist = convertDictionaryToMatrix(d.studentdict)
    print("NANS before :: " + str(countnumberofnansinmatrix(gradematrix)))
    test =  numpy.empty([3,3])
    test[:] = numpy.NAN
    test[0,0] = 5
    testmean = stats.nanmean(test)
    print "TESTING THE MEAN"
    print testmean

    print "TESTING THE MATRICES"

    print str(gradematrix[1][2])
    print str(studentlist[1][2])
    print str(courselist[1][2])

    gradematrix,studentlist,courselist = pruneEmptyColumns(gradematrix,studentlist,courselist)

    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(gradematrix)

    print d.get_results("1403262")
    print gradematrix[0]
    print courselist[0]
    print studentlist[0]
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

def convertDictionaryToMatrix(dictionary):
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
            grade = dictionary[dummieid][activity][0]
            if grade == "A" or grade == "A-" or grade == "B+" or grade == "B" or grade == "B-" or grade == "C+" or grade == "C" or grade == "C-" or grade == "D+" or grade == "D" or grade == "D-" or grade == "F" or grade == "S" or grade == "U":
                studentlist[rowcount][columncount] = dummieid
                courselist[rowcount][columncount] = activity
                gradematrix[rowcount][columncount] = twelvepointgrademap[grade]

            columncount += 1
        rowcount += 1
    print gradematrix
    return gradematrix, studentlist, courselist

def pruneEmptyColumns(gradematrix, studentlist, courselist):
    validgradereference = numpy.zeros([len(gradematrix[0]),1])

    print validgradereference
    print validgradereference.shape
    #validgradearray = [0] * len(gradematrix[0])
    for i in range(0,gradematrix.shape[0]):
        for j in range(0,gradematrix.shape[1]):
            if not math.isnan(gradematrix[i][j]):
                validgradereference[j] = validgradereference[j] + 1

    print validgradereference

    print len(studentlist[0])
    print len(courselist[0])
    print gradematrix.shape[1]

    print len(studentlist)
    print len(courselist)
    print gradematrix.shape[0]

    print "AFTER"

    studentlist = transpose(removeBlankRows(transpose(studentlist)))
    courselist = transpose(removeBlankRows(transpose(courselist)))

    zerolist,nonzerobool = numpy.where(validgradereference == 0)
    zeroarray = numpy.array(zerolist)
    print zeroarray
    for i in range(len(zeroarray)):
        gradematrix = numpy.delete(gradematrix,zeroarray[i],1)
        zeroarray = zeroarray - 1

    print len(studentlist[0])
    print len(courselist[0])
    print gradematrix.shape[1]

    print len(studentlist)
    print len(courselist)
    print gradematrix.shape[0]

    return gradematrix, studentlist, courselist

def transpose(grid):
    return zip(*grid)

def removeBlankRows(grid):
    return [list(row) for row in grid if any(row)]

if __name__ == "__main__":
    main()