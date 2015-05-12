'''
    Class that holds most of the recommendation systems methods.
'''

__author__ = 'sina'
import numpy
import math
import scipy.stats as stats

def __init__(self):
    print("PCA class.")
    return

'''
csvfiletomat - A method that reads a .csv file into a matrix of floating points.
    :: outr :: result
    :: lib :: csv
'''
def csvfiletomat(filename):
    print("CSV file read into long matrix.")
    result = numpy.genfromtxt(filename,delimiter=',')
    return result

'''
printcsvfile - A method that pretty prints a csv file.
    :: param :: .csv
'''
def printlongmatrix(longmatrix):
    print(longmatrix)

'''
plotlongmatrix - A method that creates a scatter plot of a long matrix
    :: param :: long matrix
'''
def plotlongmatrixscatter(longmatrix):
    import matplotlib.pyplot as plt
    plt.cla()
    plt.title("CS 1440 vs CS 2440 Per Student")
    plt.scatter(longmatrix[:,0],longmatrix[:,1])
    plt.ylim(-2,14.0)
    plt.ylabel('CS 2440')
    plt.xlabel('CS 1440')
    plt.show()

'''
plotlongmatrixsubmean - A method that creates a scatter plot of a long matrix after
                        the mean has been subtracted
    :: param :: long matrix
'''
def plotlongmatrixscattersubmean(longmatrix):
    import matplotlib.pyplot as plt
    plt.cla()
    plt.title("CS 1440 vs CS 2440 Per Student With Mean Subtracted")
    plt.scatter(longmatrix[:,0],longmatrix[:,1])
    plt.ylim(-2,14.0)
    plt.ylabel('CS 2440')
    plt.xlabel('CS 1440')
    plt._show()

'''
plotlongmatrixhistogram - A method that creates 2 histograms from the raw data
'''
def plotlongmatrixhistrogram(longmatrix):
    import matplotlib.pyplot as plt
    plt.hist(longmatrix[:,0])
    #print(longmatrix[:,0].mean(axis=0))
    plt.axvline(longmatrix[:,0].mean(axis=0),color='r')
    plt.title("CS 1440 Histogram")
    plt.xlabel("1440 Grades")
    plt.ylabel("Grade Frequencies")
    plt._show()
    plt.hist(longmatrix[:,1])
    #print(longmatrix[:,1].mean(axis=0))
    plt.title("CS 2440 Histogram")
    plt.axvline(longmatrix[:,1].mean(axis=0),color='r')
    plt.xlabel("1440 Grades")
    plt.ylabel("Grade Frequencies")
    plt._show()

'''
subtractrowmeanrows - A method that subtracts the mean from the long matrix
'''
def subtractrowmeanrowslongmat(longmatrix):
    matrix = longmatrix.copy()
    mean = matrix.mean(axis=0)
    return matrix[:,0] - mean
    #return mean

'''
subtractcolmeancols - A method that subtracts the mean from the long matrix
'''
def subtractcolmeancolslongmat(longmatrix):
    matrix = longmatrix.copy()
    mean = matrix.mean(axis=0)
    #mean = numpy.repeat(longmatrix.mean(axis=0),longmatrix.shape[0],axis=0)
    return numpy.subtract(matrix[:,:],mean)

'''
covariancematrix - A method that converts a matrix to its covariance matrix
'''
def covariancematrix(longmatrix):
    matrix = longmatrix.copy()
    return numpy.cov(matrix.T)

'''
eigendecompmatrix - A method that takes in a covariance matrix and returns an array
                    of eigen values and an array of normalized eigenvectors.
'''
def eigendecompmatrix(covmatrix):
    matrix = covmatrix.copy()
    return numpy.linalg.eig(covmatrix)

'''
plotlongmatrixscatter - A method that creates a scatter plot of a long matrix
    :: param :: long matrix
'''
def plotlongmatrixscatterwithpcomp(longmatrix,evalues,evectors):
    import matplotlib.pyplot as plt
    plt.cla()
    plt.title("CS 1440 vs CS 2440 By Student")
    plt.scatter(longmatrix[:,0],longmatrix[:,1],marker="p")
    plt.ylim(-2,14.0)
    plt.ylabel('CS 2440')
    plt.xlabel('CS 1440')
    mean = longmatrix.mean(axis=0)
    xeigvsqrt = math.sqrt(evalues[0])
    yeigvsqrt = math.sqrt(evalues[1])

    x1 = (evectors[0,0] * xeigvsqrt) + mean[0]   # 0.713977
    y1 = (evectors[1,0] * xeigvsqrt) + mean[1]   # 0.700168
    x2 = (evectors[0,1] * yeigvsqrt) + mean[0]   # -0.700168
    y2 = (evectors[1,1] * yeigvsqrt) + mean[1]   # 0.7139772

    x1r = (-evectors[0,0] * xeigvsqrt) + mean[0]   # 0.713977
    y1r = (-evectors[1,0] * xeigvsqrt) + mean[1]   # 0.700168
    x2r = (-evectors[0,1] * yeigvsqrt) + mean[0]   # -0.700168
    y2r = (-evectors[1,1] * yeigvsqrt) + mean[1]   # 0.7139772

    plt.gca().set_aspect('equal', adjustable='box')
    plt.plot([mean[0],x1],[mean[1],y1],linewidth=2,color="green")
    plt.plot([mean[0],x2],[mean[1],y2],linewidth=2,color="red")

    plt.plot([mean[0],x1r],[mean[1],y1r],linewidth=2,color="green",zorder=1)
    plt.plot([mean[0],x2r],[mean[1],y2r],linewidth=2,color="red",zorder=2)

    plt.scatter(mean[0],mean[1],color="cyan",zorder=3)

    plt.draw()
    plt._show()

'''
plotpcompprojection - A method that creates a scatter plot of a long matrix
    :: param :: longmatrix : an initial data matrix.
    :: param :: evalues : eigenvalues of the covariance matrix derived from the data matrix.
    :: param :: evectors : eigenvectors of the covariance matrix derived from the data matrix.
    :: param :: index : the index of the maximum eigen value in eigenvalues.
'''
def plotpcompprojection(longmatrix,evalues,evectors,index):
    import matplotlib.pyplot as plt
    print longmatrix
    plt.cla()
    plt.title("CS 1440 vs CS 2440 By Student :: PCA")
    plt.scatter(longmatrix[:,0],longmatrix[:,1],marker="p",edgecolor="black",color="grey")
    plt.ylim(-2,14.0)
    plt.ylabel('CS 2440')
    plt.xlabel('CS 1440')
    mean = longmatrix.mean(axis=0)
    xeigvsqrt = math.sqrt(evalues[0])
    yeigvsqrt = math.sqrt(evalues[1])

    x1 = (evectors[0,0] * xeigvsqrt) + mean[0]   # 0.713977
    y1 = (evectors[1,0] * xeigvsqrt) + mean[1]   # 0.700168
    x2 = (evectors[0,1] * yeigvsqrt) + mean[0]   # -0.700168
    y2 = (evectors[1,1] * yeigvsqrt) + mean[1]   # 0.7139772

    x1r = (-evectors[0,0] * xeigvsqrt) + mean[0]   # 0.713977
    y1r = (-evectors[1,0] * xeigvsqrt) + mean[1]   # 0.700168
    x2r = (-evectors[0,1] * yeigvsqrt) + mean[0]   # -0.700168
    y2r = (-evectors[1,1] * yeigvsqrt) + mean[1]   # 0.7139772

    plt.gca().set_aspect('equal', adjustable='box')
    plt.plot([mean[0],x1],[mean[1],y1],linewidth=2,color="green")
    plt.plot([mean[0],x2],[mean[1],y2],linewidth=2,color="red")

    plt.plot([mean[0],x1r],[mean[1],y1r],linewidth=2,color="green",zorder=1)
    plt.plot([mean[0],x2r],[mean[1],y2r],linewidth=2,color="red",zorder=2)
    plt.scatter(mean[0],mean[1],color="cyan",zorder=3)

    themean = longmatrix.mean(axis=0)
    longmatrix = numpy.subtract(longmatrix[:,:],themean)
    targeteigvector = evectors[:,index]
    print "printing targets"
    print targeteigvector
    temp = targeteigvector.reshape(targeteigvector.size,1)
    print temp
    newmatrix = numpy.dot(longmatrix,temp)
    newmatrix = numpy.dot(newmatrix,temp.T)
    print newmatrix
    newmatrix[:,0] += mean[0]
    newmatrix[:,1] += mean[1]
    print "printing new matrix"
    print newmatrix
    plt.scatter(newmatrix[:,0],newmatrix[:,1],marker="p")
    plt.draw()
    #plt._show()
    return newmatrix

'''
plotsvd - A method that creates a scatter plot of a long matrix
    :: param :: longmatrix : an initial data matrix.
    :: param :: svalues : The singular values for longmatrix, sorted in decending order.
    :: param :: index : the index of the maximum eigen value in eigenvalues.
'''
def plotsvd(longmatrix,u,svalues,v,index):
    import matplotlib.pyplot as plt
    print longmatrix
    plt.cla()
    plt.title("CS 1440 vs CS 2440 By Student :: SVD")
    plt.scatter(longmatrix[:,0],longmatrix[:,1],marker="p",edgecolor="black",color="grey")
    plt.ylim(-2,14.0)
    plt.ylabel('CS 2440')
    plt.xlabel('CS 1440')
    mean = longmatrix.mean(axis=0)

    xeigvsqrt = math.sqrt(svalues[0])
    yeigvsqrt = math.sqrt(svalues[1])

    x1 = (v[0,0] * xeigvsqrt) + mean[0]   # 0.713977
    y1 = (v[1,0] * xeigvsqrt) + mean[1]   # 0.700168
    x2 = (v[0,1] * yeigvsqrt) + mean[0]   # -0.700168
    y2 = (v[1,1] * yeigvsqrt) + mean[1]   # 0.7139772

    x1r = (-v[0,0] * xeigvsqrt) + mean[0]   # 0.713977
    y1r = (-v[1,0] * xeigvsqrt) + mean[1]   # 0.700168
    x2r = (-v[0,1] * yeigvsqrt) + mean[0]   # -0.700168
    y2r = (-v[1,1] * yeigvsqrt) + mean[1]   # 0.7139772

    plt.gca().set_aspect('equal', adjustable='box')
    plt.plot([mean[0],x1],[mean[1],y1],linewidth=2,color="green")
    plt.plot([mean[0],x2],[mean[1],y2],linewidth=2,color="red")

    plt.plot([mean[0],x1r],[mean[1],y1r],linewidth=2,color="green",zorder=1)
    plt.plot([mean[0],x2r],[mean[1],y2r],linewidth=2,color="red",zorder=2)
    plt.scatter(mean[0],mean[1],color="cyan",zorder=3)

    themean = longmatrix.mean(axis=0)
    longmatrix = numpy.subtract(longmatrix[:,:],themean)
    targeteigvector = v[:,index]
    print "printing targets"
    print targeteigvector
    temp = targeteigvector.reshape(targeteigvector.size,1)
    print "TEMP"
    print temp
    newmatrix = numpy.dot(longmatrix,temp)
    newmatrix = numpy.dot(newmatrix,temp.T)
    print "+++ YES LOOK HERE +++"
    print newmatrix
    newmatrix[:,0] += mean[0]
    newmatrix[:,1] += mean[1]
    print "printing new matrix"
    print newmatrix
    plt.scatter(newmatrix[:,0],newmatrix[:,1],edgecolor="black",color="magenta",marker="p")
    plt.draw()
    plt._show()
    return newmatrix

'''
 projectpca - A method that
    :: param :: longmatrix : an initial data matrix.
'''
def projectpca(longmatrix,evalues,evectors,index):
    matrixcopy = longmatrix.copy()
    mean = matrixcopy.mean(axis=0)
    themean = matrixcopy.mean(axis=0)
    matrixcopy = numpy.subtract(matrixcopy[:,:],themean)
    targeteigvector = evectors[:,index]
    print "printing previous before projection"
    print longmatrix
    temp = targeteigvector.reshape(targeteigvector.size,1)
    newmatrix = numpy.dot(matrixcopy,temp)
    newmatrix = numpy.dot(newmatrix,temp.T)
    newmatrix[:,0] += mean[0]
    newmatrix[:,1] += mean[1]
    print "printing new matrix projectpca"
    print newmatrix
    return newmatrix

def projectpca2(longmatrix,evalues,evectors,index):
    import matplotlib.pyplot as plt
    print longmatrix
    plt.cla()
    plt.title("CS 1440 vs CS 2440 By Student :: PCA")
    plt.scatter(longmatrix[:,0],longmatrix[:,1],marker="p",edgecolor="black",color="grey")
    plt.ylim(-2,14.0)
    plt.ylabel('CS 2440')
    plt.xlabel('CS 1440')
    mean = longmatrix.mean(axis=0)
    xeigvsqrt = math.sqrt(evalues[0])
    yeigvsqrt = math.sqrt(evalues[1])

    x1 = (evectors[0,0] * xeigvsqrt) + mean[0]   # 0.713977
    y1 = (evectors[1,0] * xeigvsqrt) + mean[1]   # 0.700168
    x2 = (evectors[0,1] * yeigvsqrt) + mean[0]   # -0.700168
    y2 = (evectors[1,1] * yeigvsqrt) + mean[1]   # 0.7139772

    x1r = (-evectors[0,0] * xeigvsqrt) + mean[0]   # 0.713977
    y1r = (-evectors[1,0] * xeigvsqrt) + mean[1]   # 0.700168
    x2r = (-evectors[0,1] * yeigvsqrt) + mean[0]   # -0.700168
    y2r = (-evectors[1,1] * yeigvsqrt) + mean[1]   # 0.7139772

    plt.gca().set_aspect('equal', adjustable='box')
    plt.plot([mean[0],x1],[mean[1],y1],linewidth=2,color="green")
    plt.plot([mean[0],x2],[mean[1],y2],linewidth=2,color="red")

    plt.plot([mean[0],x1r],[mean[1],y1r],linewidth=2,color="green",zorder=1)
    plt.plot([mean[0],x2r],[mean[1],y2r],linewidth=2,color="red",zorder=2)
    plt.scatter(mean[0],mean[1],color="cyan",zorder=3)

    themean = longmatrix.mean(axis=0)
    longmatrix = numpy.subtract(longmatrix[:,:],themean)
    targeteigvector = evectors[:,index]
    print "printing targets"
    print targeteigvector
    temp = targeteigvector.reshape(targeteigvector.size,1)
    print temp
    newmatrix = numpy.dot(longmatrix,temp)
    newmatrix = numpy.dot(newmatrix,temp.T)
    print newmatrix
    newmatrix[:,0] += mean[0]
    newmatrix[:,1] += mean[1]
    print "printing new matrix"
    print newmatrix
    plt.scatter(newmatrix[:,0],newmatrix[:,1],marker="p")
    #plt.draw()
    #plt._show()
    return newmatrix

def indexOfMax(matrix):
    return numpy.argmax(matrix)

def fillInSparseWithAvg(matrix):
    mean = stats.nanmean(matrix,axis=0)
    print mean

    for i in range(0,matrix.shape[0]):
        for j in range(0,matrix.shape[1]):
            if j == 0 and math.isnan(matrix[i,j]):
                matrix[i,j] = mean[j]
            elif j == 1 and math.isnan(matrix[i,j]):
                matrix[i,j] = mean[j]
    return matrix

def fillInSparseWithAvg2(matrix, nanprofile):
    mean = stats.nanmean(matrix,axis=0)
    print mean

    for i in range(0,matrix.shape[0]):
        for j in range(0,matrix.shape[1]):
            if nanprofile[i,j] == 1:
                matrix[i,j] = mean[j]
    return matrix

def fillInMatrixWithEst(matrix,estimates,nanprofile):
    temp = matrix.copy()
    print ",,,,,,, testing matrix ,,,,,,,"
    print temp
    print ",,,,,,, testing estimates ,,,,,,,"
    print estimates
    print ",,,,,,, testing nanprofile ,,,,,,,"
    print nanprofile
    for i in range(0,temp.shape[0]):
        for j in range(0,temp.shape[1]):
            if nanprofile[i,j] == 1:
                temp[i,j] = estimates[i,j]
    print ",,,,,,, testing result ,,,,,,,"
    print temp
    return temp

def getnanprofile(matrix):
    nanmatrix = numpy.zeros(shape=(matrix.shape[0],matrix.shape[1]))
    for i in range(0,matrix.shape[0]):
        for j in range(0,matrix.shape[1]):
            if j == 0 and math.isnan(matrix[i,j]):
                nanmatrix[i,j] = 1
            elif j == 1 and math.isnan(matrix[i,j]):
                nanmatrix[i,j] = 1
    return nanmatrix

def plotConvergence(matrix):
    import matplotlib.pyplot as plt
    import matplotlib.axes as ax

    plt.cla()
    plt.title("Missing Value Imputation :: Convergence of Estimates")
    plt.ylabel('Mean Squared Error')
    plt.xlabel('Iteration')
    plt.xlim(0,10.0)
    plt.ylim(0.1540,0.1545)
    #plt.ylim(.95,1.05)
    #plt.ylim(0,1.05)
    #plt.ylim(0,.1)
    iteration = 0

    for i in matrix:
        print i
        tempsum = numpy.mean(i,axis = 1)
        print "%%%%% tempsum %%%%%"
        print tempsum
        tempsum2 = numpy.mean(tempsum,axis = 0)
        error = numpy.sqrt(tempsum2)
        print iteration
        print "#### SUM ####"
        print error
        temp = numpy.empty([i.shape[0],1])
        temp.fill(iteration)
        print "TEMP"
        print temp
        plt.scatter(iteration,error,edgecolor="black",color="magenta",marker="p")
        iteration += 1

    plt.xticks(numpy.arange(0,10,1.0))
    plt.grid()
    plt.show()
    return

def plotConvergence2(matrix):
    import matplotlib.pyplot as plt
    import matplotlib.axes as ax

    plt.cla()
    plt.title("Missing Value Imputation :: Convergence of Estimates")
    plt.ylabel('Mean Squared Error')
    plt.xlabel('Iteration')
    plt.xlim(0,100.0)
    #plt.ylim(0.1540,0.1545)
    #plt.ylim(.95,1.05)
    #plt.ylim(0,1.05)
    plt.ylim(.9,1.2)
    iteration = 0
    count = 0

    for i in matrix:
        print i
        plt.scatter(count,i,edgecolor="black",color="magenta",marker="p")
        count = count + 1

    plt.xticks(numpy.arange(0,10,1.0))
    plt.grid()
    plt.show()
    return

def plotLastStage(finalmatrix):
    plotlongmatrixscatter(finalmatrix)

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
                size = size + 1

    mean = sum/size
    return math.sqrt(mean)

'''
def fillInMatrixWithEst(matrix,estimates,nanprofile):
    temp = matrix.copy()
    print nanprofile
    for i in range(0,temp.shape[0]):
        for j in range(0,temp.shape[1]):
            if nanprofile[i,j] == 1:
                temp[i,j] = estimates[i,j]
    print ",,,,,,, testing result ,,,,,,,"
    print temp
    return temp
'''