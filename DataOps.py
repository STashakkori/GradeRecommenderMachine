__author__ = 'sina'

import cPickle
import pickle
import json

class loadergetter:

    studentdict = {}
    activitydict = {}

    def __init__(self):
        self.studentdict = self.load_json("preprocessing/studentdictionary.json")
        self.activitydict =self.load_json("preprocessing/activitydictionary.json")
        print "DataOps :: datastructures loaded"

    def get_results(self,string):
        import re
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