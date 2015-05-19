__author__ = 'sina'

import cPickle
import pickle
import json
import re

class loadergetter:

    studentdict = {}
    activitydict = {}
    gradelist = []
    graderegex = re.compile('^((\*?[A-DFSIW][+-]?) ?)?(NG|XG|NR|WB|WF|AU|XP|XC|CV|CR|WC|IE)*$')
    traditionalgraderegex = re.compile('^\*?[A-DFSIW][+-]?$')

    def __init__(self):
        self.studentdict = self.load_json("preprocessing/studentdictionary.json")
        self.activitydict =self.load_json("preprocessing/activitydictionary.json")
        print "DataOps -> datastructures loaded"

    def get_results(self,string):
        dummieidregex = re.compile('^[0-9]{7}')

        if dummieidregex.search(string):
            if string in self.studentdict:
                return self.studentdict[string]

            else:
                print ":: NOT A VALID DUMMIEID ::"

        else:
            if string in self.activitydict:
                return self.activitydict[string]

            else:
                print ":: NOT A VALID ACTIVITY ::"

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

    def grademerger(self,studentmap):
        for k, v in studentmap.iteritems():
            if isinstance(v,dict):
                self.grademerger(v)
            else:
                for value in v:
                    if self.graderegex.search(value):
                        self.gradelist.append(value)

    def countsmapper(self,list):
        countmap = {}
        for item in list:
            if self.traditionalgraderegex.search(item):
                countmap[item] = countmap.setdefault(item,0) + 1
            else:
                countmap["Other"] = countmap.setdefault("Other",0) + 1

        return countmap

    def gradehistogrammer(self,list):
        import matplotlib.pyplot as plt
        import numpy
        X = numpy.arange(len(list))
        plt.bar(X,list.values(),align='center',width=0.5)
        plt.xticks(X,list.keys())
        ymax=max(list.values()) + 1
        plt.ylim(0,ymax)
        plt.autoscale(enable=True,axis=u'x',tight=None)
        plt.show()