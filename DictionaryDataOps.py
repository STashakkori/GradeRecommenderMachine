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
import base64

class loadergetter:
    studentdict = {}
    activitydict = {}

    gradelist = []
    title = ""
    numberofstudents = 0
    dummieidregex = re.compile('^[0-9]{7}')
    graderegex = re.compile('^((\*?[A-DFSIWU][+-]?) ?)?(NG|XG|NR|WB|WF|AU|XP|XC|CV|CR|WC|IE)*$')
    traditionalgraderegex = re.compile('^\*?[A-DFSIWU][+-]?$')
    takenclassregex = re.compile('^\*?[A-DFS][+-]?$')
    gradenumericsmap = {"A":4.0,"A-":3.7,"B+":3.3,"B":3.0,"B-":2.7,"C+":2.3,"C":2.0,"C-":1.7,"D+":1.3,"D":1.0,"D-":0.7,"F":0.0}
    twelvepointgrademap = {"A":12.0,"A-":11.0,"B+":10.0,"B":9.0,"B-":8.0,"C+":7.0,"C":6.0,"C-":5.0,"D+":4.0,"D":3.0,"D-":2.0,"F":0.0}
    twelvepointgrademapwithpassfail = {"A":12.0,"S":12.0,"A-":11.0,"B+":10.0,"B":9.0,"B-":8.0,"C+":7.0,"C":6.0,"C-":5.0,"D+":4.0,"D":3.0,"D-":2.0,"F":0.0,"U":0.0}

    def __init__(self):
        self.studentdict = self.load_json("preprocessing/studentdictionary.json")
        self.activitydict =self.load_json("preprocessing/activitydictionary.json")
        print "DictionaryDataOps -> datastructures loaded"

    def get_results_dictionary(self,string):
        self.gradelist = []
        self.title = string

        if self.dummieidregex.search(string):
            if string in self.studentdict:
                return self.studentdict[string]

            else:
                print "get_results :: NOT A VALID DUMMIEID ::"

        else:
            if string in self.activitydict:
                return self.activitydict[string]

            else:
                print "get_results :: NOT A VALID ACTIVITY ::"

        return None

    def load_cpickle(self,filename):
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
        j = json.loads(open(filename).read())
        f.close()
        return j

    def grademerger(self,dictionary):
        for k, v in dictionary.iteritems():
            if isinstance(v,dict):
                self.grademerger(v)
            else:
                for value in v:
                    if self.graderegex.search(value):
                        self.gradelist.append(value)

    def countsmapper(self,list):
        countmap = OrderedDict([("A",0),("A-",0),("B+",0),("B",0),("B-",0),("C+",0),("C",0),("C-",0),("D+",0),("D",0),("D-",0),("F",0),("I",0),("S",0),("U",0),("W",0),("*F",0),("Other",0)])
        for item in list:
            if self.traditionalgraderegex.search(item):
                countmap[item] = countmap.setdefault(item, 0) + 1
            else:
                countmap["Other"] = countmap.setdefault("Other", 0) + 1

        return countmap

    def allgradehistogrammer(self, dictionary):
        X = numpy.arange(len(dictionary))
        plt.bar(X, dictionary.values(), align='center', width=0.5)
        plt.xticks(X, dictionary.keys())
        ymax=max(dictionary.values()) + 1
        plt.ylim(0, ymax)
        plt.autoscale(enable=True, axis=u'x', tight=None)
        plt.title("Letter Grade Histogram of All Students That Have Taken a CS Class")
        mean = self.calculategrademean(dictionary)
        median = self.calculategrademedian(self.gradelist)
        variance = self.calculatevariance()
        starty = 120000
        plt.text(5.9, starty - 0 * 6000, "Mean Grade: " + str(mean), fontsize=8,color='red', bbox=dict(facecolor='green', alpha=0.5))
        plt.text(5.9, starty - 1 * 6000, "Median Grade: " + str(median), fontsize=8, color='red', bbox=dict(facecolor='green', alpha=0.5))
        plt.text(5.9, starty - 2 * 6000, "Mode Grade: " + self.calculatelettergrademode(dictionary), fontsize=8, color='red', bbox=dict(facecolor='green', alpha=0.5))
        plt.text(5.9, starty - 3 * 6000, "Variance: " + str(variance), fontsize=8, color='red', bbox=dict(facecolor='green', alpha=0.5))
        plt.text(5.9, starty - 4 * 6000, "Standard Deviation: " + str(statistics.stdev(self.gradelisttonumeric(self.gradelist))), fontsize=8, color='red', bbox=dict(facecolor='green', alpha=0.5))
        plt.text(5.9, starty - 5 * 6000, "Skewness: " + str(stats.skew(self.gradelisttonumeric(self.gradelist))), fontsize=8, color='red', bbox=dict(facecolor='green', alpha=0.5))
        plt.text(5.9, starty - 6 * 6000, "Kurtosis: " + str(stats.kurtosis(self.gradelisttonumeric(self.gradelist))), fontsize=8, color='red', bbox=dict(facecolor='green', alpha=0.5))
        plt.xlabel('Grades')
        plt.ylabel('Occurences')
        plt.show()

    def recordgradehistogrammer(self, dictionary):
        X = numpy.arange(len(dictionary))
        plt.bar(X, dictionary.values(), align='center', width=0.5)
        plt.xticks(X, dictionary.keys())
        ymax = max(dictionary.values()) + 1
        plt.autoscale(enable=True, axis=u'x', tight=None)
        plt.title("Letter Grade Histogram of " + self.title)
        mean = self.calculategrademean(dictionary)
        median = self.calculategrademedian(self.gradelist)
        variance = self.calculatevariance()
        numberoftakes = self.countnumberoftimesclasshasbeentaken(self.gradelist)
        passinggrades = float(self.countpassinggrades(self.gradelist)) / float(numberoftakes) * 100.0
        gradesbetterthanacminus = (float(self.countgradesbetterthanacminus(self.gradelist)) / float(numberoftakes)) * 100.0
        starty = dictionary[max(dictionary.iteritems(), key=operator.itemgetter(1))[0]] - 20
        sizeoffont = 6
        plt.text(3.4, starty - 0 * starty / 30, "Mean Grade: " + str(mean), fontsize=sizeoffont, color='black', bbox=dict(facecolor='white', alpha=0.5,edgecolor='green'))
        plt.text(3.4, starty - 1 * starty / 30, "Median Grade: " + str(median), fontsize=sizeoffont, color='black', bbox=dict(facecolor='white', alpha=0.5,edgecolor='green'))
        plt.text(3.4, starty - 2 * starty / 30, "Mode Grade: " + self.calculatelettergrademode(dictionary), fontsize=sizeoffont,color='black', bbox=dict(facecolor='white', alpha=0.5,edgecolor='green'))
        plt.text(3.4, starty - 3 * starty / 30, "Variance: " + str(variance), fontsize=sizeoffont, color='black', bbox=dict(facecolor='white', alpha=0.5,edgecolor='green'))
        plt.text(3.4, starty - 4 * starty / 30, "Standard Deviation: " + str(statistics.stdev(self.gradelisttonumeric(self.gradelist))), fontsize=sizeoffont,color='black', bbox=dict(facecolor='white', alpha=0.5,edgecolor='green'))
        plt.text(3.4, starty - 5 * starty / 30, "Skewness: " + str(stats.skew(self.gradelisttonumeric(self.gradelist))), fontsize=sizeoffont,color='black', bbox=dict(facecolor='white', alpha=0.5,edgecolor='green'))
        plt.text(3.4, starty - 6 * starty / 30, "Kurtosis: " + str(stats.kurtosis(self.gradelisttonumeric(self.gradelist))), fontsize=sizeoffont, color='black', bbox=dict(facecolor='white', alpha=0.5,edgecolor='green'))
        plt.text(3.4, starty - 7 * starty / 30, "Total Students: " + str(self.numberofstudents), fontsize=sizeoffont, color='black', bbox=dict(facecolor='white', alpha=0.5,edgecolor='green'))
        plt.text(3.4, starty - 8 * starty / 30, "Number of Times Class Has Been Taken: " + str(numberoftakes), fontsize=sizeoffont, color='black', bbox=dict(facecolor='white', alpha=0.5,edgecolor='green'))
        plt.text(3.4, starty - 9 * starty / 30, "Percent Passing Grades: " + str(passinggrades) + "%", fontsize=sizeoffont, color='black', bbox=dict(facecolor='white', alpha=0.5,edgecolor='green'))
        plt.text(3.4, starty - 10 * starty / 30, "Percent C's or Better: " + str(gradesbetterthanacminus) + "%", fontsize=sizeoffont, color='black', bbox=dict(facecolor='white', alpha=0.5,edgecolor='green'))
        plt.xlabel('Grades')
        plt.ylabel('Occurences')
        sigma = math.sqrt(variance)
        x = numpy.linspace(0,len(dictionary),1000)
        plt.plot(x,starty * mlab.normpdf(x,mean,sigma),'-r',linewidth=2)
        figure = plt.gcf()
        plt.show()
        timestring = time.strftime("%Y%m%d-%H%M%S")
        figure.savefig("figures/histogram-" + timestring)

    def calculategrademean(self, dictionary):
        sum = 0.0
        count = 0.0
        for grade in dictionary:
            if grade in self.gradenumericsmap:
                sum = sum + self.gradenumericsmap[grade] * dictionary.get(grade)
                count = count + dictionary.get(grade)

        return sum / count

    def calculategrademedian(self, list):
        numericlist = self.gradelisttonumeric(list)
        sortedlist = self.quicksort(numericlist)
        numitems = len(sortedlist)
        if len(list) % 2 == 0:
            sum = sortedlist[numitems / 2] + sortedlist[numitems / 2 + 1]
            median = sum / 2
            return median

        else:
            return sortedlist[numitems/2]

    def calculatetwelvepointgrademedian(self, list):
        numericlist = self.gradelisttotwelvepointnumeric(list)
        sortedlist = self.quicksort(numericlist)
        numitems = len(sortedlist)
        if len(list) % 2 == 0:
            sum = sortedlist[numitems / 2] + sortedlist[numitems / 2 + 1]
            median = sum / 2
            return median

        else:
            return sortedlist[len(sortedlist)/2]

    def calculatelettergrademode(self, countsmap):
        return max(countsmap.iteritems(), key=operator.itemgetter(1))[0]

    def gradenumerictoletter(self,gradenumber):
        if gradenumber <= 0.0:
            return "F"

        elif 0.0 < gradenumber <= 0.7:
            return "D-"

        elif 0.7 < gradenumber <= 1.0:
            return "D"

        elif 1.0 < gradenumber <= 1.3:
            return "D+"

        elif 1.3 < gradenumber <= 1.7:
            return "C-"

        elif 1.7 < gradenumber <= 2.0:
            return "C"

        elif 2.0 < gradenumber <= 2.3:
            return "C+"

        elif 2.3 < gradenumber <= 2.7:
            return "B-"

        elif 2.7 < gradenumber <= 3.0:
            return "B"

        elif 3.0 < gradenumber <= 3.3:
            return "B+"

        elif 3.3 < gradenumber <= 3.7:
            return "A-"

        elif 3.7 < gradenumber <= 4.0:
            return "A"

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

    def quicksort(self, list):
        less = []
        equal = []
        greater = []

        if len(list) > 1:
            pivot = list[0]
            for x in list:
                if x < pivot:
                    less.append(x)
                if x == pivot:
                    equal.append(x)
                if x > pivot:
                    greater.append(x)
            return self.quicksort(less) + equal + self.quicksort(greater)

        else:
            return list

    def gradelisttonumeric(self,list):
        newlist = []
        for grade in list:
            if grade in self.gradenumericsmap:
                newlist.append(self.gradenumericsmap[grade])

        return newlist

    def gradelisttotwelvepointnumeric(self,list):
        newlist = []
        for grade in list:
            if grade in self.twelvepointgrademap:
                newlist.append(self.twelvepointgrademap[grade])

        return newlist

    def twelvepointnumericlisttogrades(self,list):
        newlist = []
        for grade in list:
            if not numpy.isnan(grade):
                newlist.append(self.twelvepointgradenumerictoletter(grade))

        return newlist

    def calculatetwelvepointmean(self, dictionary):
        sum = 0.0
        count = 0.0

        for grade in dictionary:
            if grade in self.twelvepointgrademap:
                sum = sum + self.twelvepointgrademap[grade] * dictionary.get(grade)
                count = count + dictionary.get(grade)

        return sum / count

    def calculatevariance(self):
        numlist = self.gradelisttonumeric(self.gradelist)
        return statistics.variance(numlist)

    def calculatetwelvepointvariance(self):
        numlist = self.gradelisttotwelvepointnumeric(self.gradelist)
        return statistics.variance(numlist)

    def countgradesbetterthanacminus(self, list):
        count = 0
        for grade in list:
            if grade == "A" or grade == "A-" or grade == "B+" or grade == "B" or grade == "B-" or grade == "C+" or grade == "C":
                count = count + 1

        return count

    def countpassinggrades(self, list):
        count = 0
        for grade in list:
            if grade == "A" or grade == "A-" or grade == "B+" or grade == "B" or grade == "B-" or grade == "C+" or grade == "C" or grade == "C-" or grade == "D+" or grade == "D" or grade == "D-" or grade == "S":
                count = count + 1

        return count

    def countnumberoftimesclasshasbeentaken(self,list):
        count = 0
        for grade in list:
            if grade == "A" or grade == "A-" or grade == "B+" or grade == "B" or grade == "B-" or grade == "C+" or grade == "C" or grade == "C-" or grade == "D+" or grade == "D" or grade == "D-" or grade == "F" or grade == "S" or grade == "U":
                count = count + 1

        return count

    '''
        gradematrix :

    '''
    def convertDictionaryToMatrix(self, dictionary):
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
                temp = float('inf')
                for value in dictionary[dummieid][activity]:
                    if value in self.twelvepointgrademap and self.twelvepointgrademap[value] < temp:
                            temp = self.twelvepointgrademap[value]

                if temp == float('inf'):
                    grade = numpy.NAN
                else:
                    grade = temp

                studentlist[rowcount][columncount] = dummieid
                courselist[rowcount][columncount] = activity
                gradematrix[rowcount][columncount] = grade
                columncount += 1
            rowcount += 1

        return gradematrix, studentlist, courselist

    def storeMatrixInMemoryAscPickle(self, gradematrix, studentgrid, coursegrid, filename1, filename2, filename3):
        file = open(filename1, "wb")
        cPickle.dump(gradematrix,file,protocol=2)
        file.close()

        file = open(filename2, "wb")
        cPickle.dump(studentgrid,file,protocol=2)
        file.close()

        file = open(filename3, "wb")
        cPickle.dump(coursegrid,file,protocol=2)
        file.close()

        '''
        json.dumps([str(gradematrix.dtype),base64.b64encode(gradematrix),gradematrix.shape])
        file.close()
        file = open(filename2, "wb")
        json.dumps([str(studentgrid.dtype),base64.b64encode(studentgrid),studentgrid.shape])
        file.close()
        file = open(filename3, "wb")
        json.dumps([str(coursegrid.dtype),base64.b64encode(coursegrid),coursegrid.shape])
        file.close()
        '''



