__author__ = 'sina'
import cPickle
import pickle
import json

def load_cpickle(filename):
    f = open(filename,"rb")
    cp = cPickle.load(f)
    f.close()
    return cp

def load_pickle(filename):
    f = open(filename,"rb")
    p = pickle.load(f)
    f.close()
    return p

def load_json(filename):
    f = open(filename,"rb")
    j = json.loads(open(filename).read())
    f.close()
    return j