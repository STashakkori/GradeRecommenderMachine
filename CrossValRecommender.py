__author__ = 'sina'

import pprint
import cPickle
import timeit

def parsecsv(filename):
    print "TESTINGGGGG %%%%%%%"
    with open(filename) as file:
        data = file.readlines()

    pieces = []

    for line in data:
        pieces.append(line.split(','))

    studentdictionary = {}
    activitydictionary = {}

    for i in range(0,len(pieces)):
        for j in range(0,len(pieces[i])):
            if(i > 0 and pieces[i][j].strip('\r').strip('\n')):
                studentdictionary.setdefault(pieces[i][0],{})[pieces[0][j].strip('\r').strip('\n')] = pieces[i][j].strip('\r').strip('\n')

    for i in range(0,len(pieces)):
        for j in range(0,len(pieces[i])):
            if(i > 0 and pieces[i][j].strip('\r').strip('\n')):
                activitydictionary.setdefault(pieces[0][j].strip('\r').strip('\n'),{})[pieces[i][0]] = pieces[i][j].strip('\r').strip('\n')

    studentstoragefilename = "preprocessing/studentdictionary.cpickle"
    activitystoragefilename = "preprocessing/activitydictionary.cpickle"
    file1 = open(studentstoragefilename, "wb")
    file2 = open(activitystoragefilename, "wb")

    cPickle.dump(studentdictionary,file1,protocol=2)
    file1.close()
    cPickle.dump(activitydictionary,file2,protocol=2)
    file2.close()

    testarray1 = load_pickle(studentstoragefilename)
    testarray2 = load_pickle(activitystoragefilename)

    pp = pprint.PrettyPrinter(indent = 3)
    pp.pprint(testarray1)
    print("END")

    file.close()
    return


def load_pickle(filename):
    f = open(filename,"rb")
    p = cPickle.load(f)
    f.close()
    return(p)

