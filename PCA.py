__author__ = 'sina'
import numpy

def __init__(self):
    print("PCA class.")
    return

'''
csvfiletomat - A method that reads a .csv file into a matrix of floating points.
    :: outr :: result
    :: lib :: csv
'''
def csvfiletomat():
    print("CSV file read into matrix.")
    import csv
    result = numpy.array(list(csv.reader(open("pca_input_2d.csv","rb"),delimiter=','))).astype('float')
    return result

'''
printcsvfile - A method that pretty prints a csv file.
    :: param :: .csv
'''
def printlongmatrix(longmatrix):
    print(longmatrix)
'''
plotlongmatrix - A method that plots a long matrix
    :: param :: long matrix
'''
def plotlongmatrix(longmatrix):
    import matplotlib.pyplot as plt
    plt.plot(longmatrix)
    plt.ylabel('CS 1440 vs. CS 2440')
    plt._show

