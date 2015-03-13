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
    Recommender.plotpcompprojection(rawmatrix,eigenvalues,eigenvectors,eindex)
    sindex = Recommender.indexOfMax(svmatrix)
    latentmatrix = Recommender.plotsvd(rawmatrix,u,svmatrix,v,sindex)
    print "**:: LATENT ::**"
    print latentmatrix

    ######################################################################

    '''
        Calculations on sparse matrix
    '''
    sparserawmatrix = Recommender.csvfiletomat("pca_input_2d_missing.csv")
    nanmatrix = Recommender.getnanprofile(sparserawmatrix)
    print "NAN"
    print nanmatrix
    print sparserawmatrix
    filledmatrix,avg = Recommender.fillInSparseWithAvg(sparserawmatrix)
    print "filled matrix"
    print filledmatrix
    numiterations = 100
    convergences = numpy.empty([numiterations,sparserawmatrix.shape[0]])
    print "convergences"
    print convergences


    #PCA.plotpcompprojection(pcafillinavg,eigenvalues,eigenvectors,eindex)
    #resultant = PCA.plotsvd(pcafillinavg,u,svmatrix,v,sindex)
    #print "resultant"
    #print resultant

    '''
        What we want to do here is take the matrix with means inserted in place
        of sparse values and run PCA on it. Then we want to project that back onto
        the previous full-size matrix. Then we want to plot the mean squared error
        and then do another PCA. We want to repeat this process 99 times. 100 times
        total including the previous step that included inserting the mean values.
    '''

    iteration = 1
    #convergences[0,0] = iteration
    #convergences[0,1] = avg

    #for i in range(1,numiterations):
    #iteration += 1
    rawmatrix2submeanmatrix = Recommender.subtractcolmeancolslongmat(filledmatrix)
    covariancematrix2 = Recommender.covariancematrix(filledmatrix)
    Recommender.printlongmatrix(covariancematrix2)
    eigenvalues,eigenvectors = Recommender.eigendecompmatrix(covariancematrix2)
    u,svmatrix,v = numpy.linalg.svd(covariancematrix2)
    print "svmatrix"
    print svmatrix
    eindex = Recommender.indexOfMax(eigenvalues)
    sindex = Recommender.indexOfMax(svmatrix)
    S = svmatrix[sindex]
    print "S"
    print S
    print "u"
    print u
    print "v.T"
    print v.T
    print "~~~ SUCCESS TEST ~~~"
    print svmatrix * u * v.T
    #UV = numpy.dot(u.reshape(u.size,1),v.reshape(v.size,1))
    #print(":: UV ::")
    #print UV

    '''
    PCA.plotpcompprojection(pcafillinavg,eigenvalues,eigenvectors,eindex)
    PCA.plotsvd(rawmatrix,u,svmatrix,v,sindex)
    '''

    return

if __name__ == "__main__":
    main()