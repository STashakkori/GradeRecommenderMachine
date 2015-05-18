'''
    Main class for a CS course grade based recommendation system using machine learning
'''
__author__ = 'sina'
__project__ = 'STProject'

import Recommender
import numpy
import sys
import CSDataFileParser

from sklearn.decomposition import PCA as skPCA
from sklearn.decomposition import SparsePCA as skSparsePCA
import matplotlib

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

    # Uncomment these for graphs and pca iterations
    #Recommender.plotConvergence2(intermediateStages)
    #Recommender.plotLastStage(nextiterationmatrix)

    #CSDataFileParser.parsecsv('CSDataFile_ForParry_2014Nov26.csv')
    import DataOps
    d = DataOps.loadergetter()
    entry1 = d.get_results("1400002")
    entry2 = d.get_results("C S 1440")
    print entry1["C S 1440"]
    return
if __name__ == "__main__":
    main()