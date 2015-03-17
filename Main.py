'''
    Main class for a CS course grade based recommendation system using machine learning
'''

__author__ = 'sina'
__project__ = 'STProject'

import Recommender
import numpy
import matplotlib

def main():

    '''
        Calculations on non-sparse matrix
    '''
    rawmatrix = Recommender.csvfiletomat("pca_input_2d.csv")
    print rawmatrix
    Recommender.plotlongmatrixscatter(rawmatrix)
    Recommender.plotlongmatrixhistrogram(rawmatrix)
    print "------------"
    rawsubmeanmatrix = Recommender.subtractcolmeancolslongmat(rawmatrix)
    print rawsubmeanmatrix
    Recommender.plotlongmatrixscattersubmean(rawsubmeanmatrix)
    covariancematrix = Recommender.covariancematrix(rawsubmeanmatrix)
    print "------------"
    Recommender.printlongmatrix(covariancematrix)
    eigenvalues,eigenvectors = Recommender.eigendecompmatrix(covariancematrix)
    u,svmatrix,v = numpy.linalg.svd(covariancematrix)
    print "============"
    print svmatrix
    print "============"
    print "u"
    print u
    print "============"
    print "v"
    print v
    print "============"
    print(eigenvalues)
    print "============"
    print(eigenvectors)
    print "============"
    print(eigenvalues.max())
    #rawmatrix.plotlongmatrixscatterwithpcomp(rawmatrix,eigenvalues,eigenvectors)
    eindex = Recommender.indexOfMax(eigenvalues)
    svdlatentmatrix = Recommender.plotpcompprojection(rawmatrix,eigenvalues,eigenvectors,eindex)
    sindex = Recommender.indexOfMax(svmatrix)
    pcalatentmatrix = Recommender.plotsvd(rawmatrix,u,svmatrix,v,sindex)
    print "**:: LATENT ::**"
    print svdlatentmatrix
    print pcalatentmatrix

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
    print "NAN"
    print nanmatrix
    print sparserawmatrix
    intermediateStages = []
    filledmatrix,avg = Recommender.fillInSparseWithAvg(sparserawmatrix) # file in nan values with the mean value for that dimension
    intermediateStages.append(numpy.power(numpy.subtract(filledmatrix,filledmatrix),2)) # squared distance of original data to itself
    print "filled matrix"
    print filledmatrix
    numiterations = 100
    #convergences = numpy.empty([numiterations,sparserawmatrix.shape[0]])

    rawmatrix2submeanmatrix = filledmatrix
    #rawmatrix2submeanmatrix = Recommender.subtractcolmeancolslongmat(filledmatrix)
    print rawmatrix2submeanmatrix
    covariancematrix2 = Recommender.covariancematrix(rawmatrix2submeanmatrix)
    Recommender.printlongmatrix(covariancematrix2)
    eigenvalues,eigenvectors = Recommender.eigendecompmatrix(covariancematrix2)
    u,svmatrix,v = numpy.linalg.svd(covariancematrix2)
    print "svmatrix"
    print svmatrix
    eindex = Recommender.indexOfMax(eigenvalues)
    sindex = Recommender.indexOfMax(svmatrix)
    result1 = Recommender.plotpcompprojection(rawmatrix2submeanmatrix,eigenvalues,eigenvectors,eindex)
    intermediateStages.append(numpy.power(numpy.subtract(filledmatrix,result1),2))
    #result1 = Recommender.projectpca(rawmatrix2submeanmatrix,eigenvalues,eigenvectors,eindex)
    print "MOMENT OF TRUTH"
    print result1
    nextiterationmatrix = Recommender.fillInMatrixWithEst(filledmatrix,result1,nanmatrix)

    '''
        ***
            The next line is weird as the result has a mean squared error of 0 meaning that the estimates
            are actually the same as the average. Will investigate this for sure.
        ***
    '''
    #intermediateStages.append(numpy.power(numpy.subtract(filledmatrix,nextiterationmatrix),2))

    Recommender.plotlongmatrixscatter(nextiterationmatrix)
    #result2 = Recommender.projectsvd(rawmatrix2submeanmatrix,u,svmatrix,v,sindex)

    for i in range(0,numiterations-1):
        #nextiterationmatrix = Recommender.subtractcolmeancolslongmat(nextiterationmatrix)
        covariancematrix3 = Recommender.covariancematrix(nextiterationmatrix)
        #Recommender.printlongmatrix(covariancematrix3)
        eigenvalues,eigenvectors = Recommender.eigendecompmatrix(covariancematrix3)
        eindex = Recommender.indexOfMax(eigenvalues)
        previousiterationmatrix = Recommender.projectpca(nextiterationmatrix,eigenvalues,eigenvectors,eindex)
        #estimate = Recommender.plotpcompprojection(rawmatrix2submeanmatrix,eigenvalues,eigenvectors,eindex)
        estimate = Recommender.projectpca(rawmatrix2submeanmatrix,eigenvalues,eigenvectors,eindex)
        intermediateStages.append(numpy.power(numpy.subtract(filledmatrix,estimate),2))
        nextiterationmatrix = Recommender.fillInMatrixWithEst(filledmatrix,estimate,nanmatrix)

    Recommender.plotlongmatrixscatter(nextiterationmatrix)
    Recommender.plotConvergence(intermediateStages)

    print "^^^^ TESTING DUDE ^^^^"
    iteration = 0
    for i in intermediateStages:
        print iteration
        print "--------"
        print i
        iteration += 1

    '''
    PCA.plotpcompprojection(pcafillinavg,eigenvalues,eigenvectors,eindex)
    PCA.plotsvd(rawmatrix,u,svmatrix,v,sindex)
    '''

    return

if __name__ == "__main__":
    main()