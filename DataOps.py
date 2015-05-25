__author__ = 'sina'

import cPickle
import pickle
import json
import re
import statistics
import scipy.stats as stats
import matplotlib.pyplot as plt
import numpy
import operator
import time

class loadergetter:
    studentdict = {}
    activitydict = {}
    gradelist = []
    title = ""
    graderegex = re.compile('^((\*?[A-DFSIWU][+-]?) ?)?(NG|XG|NR|WB|WF|AU|XP|XC|CV|CR|WC|IE)*$')
    traditionalgraderegex = re.compile('^\*?[A-DFSIWU][+-]?$')
    gradenumericsmap = {"A":4.0,"A-":3.7,"B+":3.3,"B":3.0,"B-":2.7,"C+":2.3,"C":2.0,"C-":1.7,"D+":1.3,"D":1.0,"D-":0.7,"F":0.0}
    customparametricmap = {"A":11.0,"A-":10.0,"B+":9.0,"B":8.0,"B-":7.0,"C+":6.0,"C":5.0,"C-":4.0,"D+":3.0,"D":2.0,"D-":1.0,"F":0.0}

    def __init__(self):
        self.studentdict = self.load_json("preprocessing/studentdictionary.json")
        self.activitydict =self.load_json("preprocessing/activitydictionary.json")
        print "DataOps -> datastructures loaded"

    def get_results(self,string):
        dummieidregex = re.compile('^[0-9]{7}')
        self.title = string

        if dummieidregex.search(string):
            if string in self.studentdict:
                return self.studentdict[string]

            else:
                print "get_results :: NOT A VALID DUMMIEID ::"

        else:
            if string in self.activitydict:
                return self.activitydict[string]

            else:
                print "get_results :: NOT A VALID ACTIVITY ::"

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
        from collections import OrderedDict
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
        mean = self.calculatelettergrademean(dictionary)
        median = self.calculatelettergrademedian(self.gradelist)
        paradistpga = self.calculateparametricdistribution(dictionary, 4)
        paradist = self.calculateparametricdistribution(dictionary, 12)
        variance = self.calculatevariance(dictionary)
        starty = 120000
        plt.text(5.9, starty - 0 * 6000, "Mean Grade: " + str(mean), fontsize=12,color='red', bbox=dict(facecolor='green', alpha=0.5))
        plt.text(5.9, starty - 1 * 6000, "Median Grade: " + str(median), fontsize=12, color='red', bbox=dict(facecolor='green', alpha=0.5))
        plt.text(5.9, starty - 2 * 6000, "Mode Grade: " + self.calculatelettergrademode(dictionary), fontsize=12, color='red', bbox=dict(facecolor='green', alpha=0.5))
        plt.text(5.9, starty - 3 * 6000, "Parametric Distribution(GPA scale): " + str(paradistpga), fontsize=12, color='red', bbox=dict(facecolor='green', alpha=0.5))
        plt.text(5.9, starty - 4 * 6000, "Parametric Distribution: " + str(paradist), fontsize=12, color='red', bbox=dict(facecolor='green', alpha=0.5))
        plt.text(5.9, starty - 5 * 6000, "Variance: " + str(variance), fontsize=12, color='red', bbox=dict(facecolor='green', alpha=0.5))
        plt.text(5.9, starty - 6 * 6000, "Standard Deviation: " + str(statistics.stdev(self.gradelisttonumeric(self.gradelist))), fontsize=12, color='red', bbox=dict(facecolor='green', alpha=0.5))
        plt.text(5.9, starty - 7 * 6000, "Skewness: " + str(stats.skew(self.gradelisttonumeric(self.gradelist))), fontsize=12, color='red', bbox=dict(facecolor='green', alpha=0.5))
        plt.text(5.9, starty - 8 * 6000, "Kurtosis: " + str(stats.kurtosis(self.gradelisttonumeric(self.gradelist))), fontsize=12, color='red', bbox=dict(facecolor='green', alpha=0.5))
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
        mean = self.calculatelettergrademean(dictionary)
        median = self.calculatelettergrademedian(self.gradelist)
        paradistpga = self.calculateparametricdistribution(dictionary, 4)
        paradist = self.calculateparametricdistribution(dictionary, 12)
        variance = self.calculatevariance()
        starty = dictionary[max(dictionary.iteritems(), key=operator.itemgetter(1))[0]] - 20
        plt.text(3.4, starty - 0 * starty / 20, "Mean Grade: " + str(mean), fontsize=12, color='red', bbox=dict(facecolor='green', alpha=0.5))
        plt.text(3.4, starty - 1 * starty / 20, "Median Grade: " + str(median), fontsize=12, color='red', bbox=dict(facecolor='green', alpha=0.5))
        plt.text(3.4, starty - 2 * starty / 20, "Mode Grade: " + self.calculatelettergrademode(dictionary), fontsize=12,color='red', bbox=dict(facecolor='green', alpha=0.5))
        plt.text(3.4, starty - 3 * starty / 20, "Parametric Distribution(GPA scale): " + str(paradistpga), fontsize=12,color='red', bbox=dict(facecolor='green', alpha=0.5))
        plt.text(3.4, starty - 4 * starty / 20, "Parametric Distribution: " + str(paradist), fontsize=12, color='red', bbox=dict(facecolor='green', alpha=0.5))
        plt.text(3.4, starty - 5 * starty / 20, "Variance: " + str(variance), fontsize=12, color='red', bbox=dict(facecolor='green', alpha=0.5))
        plt.text(3.4, starty - 6 * starty / 20, "Standard Deviation: " + str(statistics.stdev(self.gradelisttonumeric(self.gradelist))), fontsize=12,color='red', bbox=dict(facecolor='green', alpha=0.5))
        plt.text(3.4, starty - 7 * starty / 20, "Skewness: " + str(stats.skew(self.gradelisttonumeric(self.gradelist))), fontsize=12,color='red', bbox=dict(facecolor='green', alpha=0.5))
        plt.text(3.4, starty - 8 * starty / 20, "Kurtosis: " + str(stats.kurtosis(self.gradelisttonumeric(self.gradelist))), fontsize=12, color='red', bbox=dict(facecolor='green', alpha=0.5))
        plt.xlabel('Grades')
        plt.ylabel('Occurences')
        plt.show()
        timestring = time.strftime("%Y%m%d-%H%M%S")
        plt.savefig("figures/histogram-" + timestring)

    def calculatelettergrademean(self, dictionary):
        sum = 0.0
        count = 0.0
        for grade in dictionary:
            if grade in self.gradenumericsmap:
                sum = sum + self.gradenumericsmap[grade]
                count = count + 1.0
        return sum / count

    def calculatelettergrademedian(self, list):
        numericlist = self.gradelisttonumeric(list)
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

    def calculateparametricdistribution(self,dictionary,flag):
        sum = 0.0
        count = 0.0

        if flag != 4 and flag != 12:
            print "calculateparametricdistribution :: NOT A VALID FLAG ::"
            return

        if not flag or flag == 4:
            for grade in dictionary:
                if grade in self.gradenumericsmap:
                    sum = sum + self.gradenumericsmap[grade]
                    count = count + 1.0

        if flag == 12:
            for grade in dictionary:
                if grade in self.customparametricmap:
                    sum = sum + self.customparametricmap[grade]
                    count = count + 1.0

        return sum/count

    def calculatevariance(self):
        numlist = self.gradelisttonumeric(self.gradelist)
        return statistics.variance(numlist)