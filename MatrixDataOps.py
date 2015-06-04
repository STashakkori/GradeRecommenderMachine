__author__ = 'sina'

import cPickle
import pickle
import json
import re
import statistics
import scipy.stats as stats
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import numpy
import operator
import time
from collections import OrderedDict
import math

class loadergetter:

    gradematrix = None
    studentgrid = None
    coursegrid = None

    dummieidregex = re.compile('^[0-9]{7}')

    def __init__(self):
        self.gradematrix = self.load_cpickle("preprocessing/gradematrix.cPickle")
        self.studentgrid = self.load_cpickle("preprocessing/studentgrid.cPickle")
        self.coursegrid = self.load_cpickle("preprocessing/coursegrid.cPickle")
        print "MatrixDataOps -> datastructures loaded"

    def load_cpickle(self, filename):
        f = open(filename,"rb")
        cp = cPickle.load(f)
        f.close()
        return cp

    def load_pickle(self,filename):
        f = open(filename,"rb")
        p = pickle.load(f)
        f.close()
        return p

    def load_json(self,filename):
        f = open(filename,"rb")
        p = pickle.load(f)
        f.close()
        return p

    def countsmapper(self,list):
        countmap = OrderedDict([("A",0),("A-",0),("B+",0),("B",0),("B-",0),("C+",0),("C",0),("C-",0),("D+",0),("D",0),("D-",0),("F",0),("I",0),("S",0),("U",0),("W",0),("*F",0),("Other",0)])
        for item in list:
            if not numpy.isnan(item) and self.twelvepointgradenumerictoletter(item) in countmap:
                countmap[self.twelvepointgradenumerictoletter(item)] = countmap.setdefault(self.twelvepointgradenumerictoletter(item), 0) + 1

        return countmap

    def pruneEmptyColumns(self):
        validgradereference = numpy.zeros([len(self.gradematrix[0]),1])
        for i in range(0,self.gradematrix.shape[0]):
            for j in range(0,self.gradematrix.shape[1]):
                if not math.isnan(self.gradematrix[i][j]):
                    validgradereference[j] = validgradereference[j] + 1

        print "VALID GRADE REFERENCE"
        print validgradereference

        self.studentgrid = self.transpose(self.removeBlankRows(self.transpose(self.studentgrid)))
        self.coursegrid = self.transpose(self.removeBlankRows(self.transpose(self.coursegrid)))

        zerolist,nonzerobool = numpy.where(validgradereference == 0)
        zeroarray = numpy.array(zerolist)
        print zeroarray
        for i in range(len(zeroarray)):
            self.gradematrix = numpy.delete(self.gradematrix,zeroarray[i],1)
            zeroarray = zeroarray - 1

    def transpose(self, grid):
        return zip(*grid)

    def removeBlankRows(self, grid):
        return [list(row) for row in grid if any(row)]

    def get_results(self,input):
        if self.dummieidregex.search(input):
            print "TEST1"
            for i in range(0,len(self.studentgrid)):
                for j in range(0,len(self.studentgrid[i])):
                    if self.studentgrid[i][j] == input:
                        return self.gradematrix[i]

        else:
            print "TEST2"
            templist = []
            for i in range(0,len(self.coursegrid)):
                for j in range(0,len(self.coursegrid[i])):
                    if self.coursegrid[i][j] == input:
                        templist.append(self.gradematrix[i][j])

            return templist
        return None

    def recordgradehistogrammer(self, list):
        #X = numpy.arange(len(dictionary))
        #plt.bar(X, dictionary.values(), align='center', width=0.5)
        #plt.xticks(X, dictionary.keys())
        #ymax = max(dictionary.values()) + 1
        #grades = self.twelvepointnumericlisttogrades(list)
        numberoftakes = self.countnumberoftimesclasshasbeentaken(list)
        passinggrades = float(self.countpassinggrades(list)) / float(numberoftakes) * 100
        gradesbetterthanacminus = (float(self.countgradesbetterthanacminus(list)) / float(numberoftakes)) * 100.0
        mean = self.calculatemean(list)
        median = self.calculatemedian(list)
        mode = self.calculatemode(list)
        variance = self.calculatevariance(list,mean)
        print numberoftakes
        print self.countpassinggrades(list)
        print passinggrades
        print gradesbetterthanacminus
        print mean
        print median
        print mode
        print variance
        '''
        passinggrades = float(self.countpassinggrades(grades)) / float(numberoftakes) * 100.0
        gradesbetterthanacminus = (float(self.countgradesbetterthanacminus(grades)) / float(numberoftakes)) * 100.0
        starty = dictionary[max(dictionary.iteritems(), key=operator.itemgetter(1))[0]] - 20
        sizeoffont = 6
        plt.text(3.4, starty - 7 * starty / 30, "Total Students: " + str(self.numberofstudents), fontsize=sizeoffont, color='black', bbox=dict(facecolor='white', alpha=0.5,edgecolor='green'))
        plt.text(3.4, starty - 8 * starty / 30, "Number of Times Class Has Been Taken: " + str(numberoftakes), fontsize=sizeoffont, color='black', bbox=dict(facecolor='white', alpha=0.5,edgecolor='green'))
        plt.text(3.4, starty - 9 * starty / 30, "Percent Passing Grades: " + str(passinggrades) + "%", fontsize=sizeoffont, color='black', bbox=dict(facecolor='white', alpha=0.5,edgecolor='green'))
        plt.text(3.4, starty - 10 * starty / 30, "Percent C's or Better: " + str(gradesbetterthanacminus) + "%", fontsize=sizeoffont, color='black', bbox=dict(facecolor='white', alpha=0.5,edgecolor='green'))
        plt.autoscale(enable=True, axis=u'x', tight=None)
        plt.title("Letter Grade Histogram of " + title)
        plt.xlabel('Grades')
        plt.ylabel('Occurences')
        plt.show()
        '''

    def twelvepointgradenumerictoletter(self,gradenumber):
        if gradenumber == 0.0:
            return "F"

        elif gradenumber == 2.0:
            return "D-"

        elif gradenumber == 3.0:
            return "D"

        elif gradenumber == 4.0:
            return "D+"

        elif gradenumber == 5.0:
            return "C-"

        elif gradenumber == 6.0:
            return "C"

        elif gradenumber == 7.0:
            return "C+"

        elif gradenumber == 8.0:
            return "B-"

        elif gradenumber == 9.0:
            return "B"

        elif gradenumber == 10.0:
            return "B+"

        elif gradenumber == 11.0:
            return "A-"

        elif gradenumber == 12.0:
            return "A"

    def countnumberoftimesclasshasbeentaken(self,list):
        count = 0
        for grade in list:
            if not numpy.isnan(grade):
                count += 1

        return count

    def countpassinggrades(self,list):
        count = 0
        for grade in list:
            if not numpy.isnan(grade) and grade >= 2.0:
                count += 1

        return count

    def countgradesbetterthanacminus(self,list):
        count = 0
        for grade in list:
            if not numpy.isnan(grade) and grade >= 6.0:
                count += 1

        return count

    def calculatemean(self,list):
        sum = 0
        count = 0
        for grade in list:
            if not numpy.isnan(grade):
                sum += grade
                count += 1

        return sum/count

    def calculatemedian(self,list):
        return stats.nanmedian(list)

    def calculatemode(self,list):
        return stats.mode(list,axis=None)

    def calculatevariance(self,list,mean):
        sumsquareddiff = 0
        count = 0
        for grade in list:
            if not numpy.isnan(grade):
                count += 1
                sumsquareddiff += abs(grade - mean)**2

        return sumsquareddiff / count

