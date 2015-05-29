__author__ = 'sina'

import pprint
import cPickle
import pickle
import time
import matplotlib.pyplot as plt
import pandas
import re

studentstoragefilename = "preprocessing/studentdictionary.json"
activitystoragefilename = "preprocessing/activitydictionary.json"

def parsecsv(filename):
    print "TESTINGGGGG %%%%%%%"
    with open(filename) as file:
        data = file.readlines()

    pieces = []

    for line in data:
        pieces.append(line.split(','))

    studentdictionary = {}
    activitydictionary = {}

    scoreregex = re.compile('_score$')
    courseregex = 'Course'
    graderegex = 'Grade[0-9]+'
    gradegparegex = 'Grade_GPA'
    minorregex = re.compile('_min')
    majorregex = re.compile('_major|_mjr')
    endnumberregex = re.compile('(\d)+$')
    hsgparegex = re.compile('HSGPA')

    '''
        print scoreregex.search(teststring1,re.IGNORECASE)
        print re.match('course',teststring2)
        print re.match('grade',teststring3)
        print re.match('grade_gpa',teststring4)
        print minorregex.search(teststring5,re.IGNORECASE)
        print majorregex.search(teststring6,re.IGNORECASE)
        print majorregex.search(teststring7,re.IGNORECASE)
        print endnumberregex.search(teststring8,re.IGNORECASE)
    '''

    t0 = time.time()

    for i in range(1,len(pieces)):
        studentdictionary[pieces[i][0]] = {}

        for j in range(1,len(pieces[i])):

            if(pieces[i][j].strip('\r').strip('\n') and not re.match(graderegex,pieces[0][j]) and not re.match(gradegparegex,pieces[0][j])):
                if pieces[0][j] not in activitydictionary: activitydictionary[pieces[0][j]] = {}

                # if it's a course, then we want to make that the key and grab it's grade and insert that as the value
                if(re.match(courseregex,pieces[0][j])):
                    studentdictionary[pieces[i][0]].setdefault(pieces[i][j].strip('\r').strip('\n'),[])
                    studentdictionary[pieces[i][0]][pieces[i][j]].append(pieces[i][j+131].strip('\r').strip('\n'))

                    activitydictionary.setdefault(pieces[i][j].strip('\r').strip('\n'),{})
                    activitydictionary[pieces[i][j].strip('\r').strip('\n')].setdefault(pieces[i][0],[])
                    activitydictionary[pieces[i][j].strip('\r').strip('\n')][pieces[i][0]].append(pieces[i][j+131].strip('\r').strip('\n'))

                # otherwise, use the column header as the key and just insert the csv entry as the value
                else:
                    studentdictionary[pieces[i][0]].setdefault(pieces[0][j].strip('\r').strip('\n'),[])
                    studentdictionary[pieces[i][0]][pieces[0][j]].append(pieces[i][j].strip('\r').strip('\n'))

                    activitydictionary[pieces[0][j].strip('\r').strip('\n')].setdefault(pieces[i][0],[])
                    activitydictionary[pieces[0][j].strip('\r').strip('\n')][pieces[i][0]].append(pieces[i][j].strip('\r').strip('\n'))

                file.close()

    #pp = pprint.PrettyPrinter(indent=3)
    #pp.pprint(activitydictionary)

    storedataasjson(studentdictionary,studentstoragefilename)
    storedataasjson(activitydictionary,activitystoragefilename)

    print "** PARSING COMPLETE **"

# Method that writes an object to memory in json format
def storedataasjson(dictionary, filename):
    import json
    file = open(filename, "wb")
    json.dump(dictionary,file)
    file.close()

    '''
    # Scores
    if(scoreregex.search(pieces[0][j].strip('\r').strip('\n')),re.IGNORECASE):
        studentdictionary[pieces[i][0]] = {}
        studentdictionary[pieces[i][0]]["scores"] = {}
        studentdictionary[pieces[i][0]]["scores"][pieces[0][j].strip('\r').strip('\n')] = pieces[i][j].strip('\r').strip('\n')

    # Courses
    elif(re.match(courseregex,pieces[0][j].strip('\r').strip('\n'))):
        studentdictionary[pieces[i][0]] = {}
        studentdictionary[pieces[i][0]]["courses"] = {}
        studentdictionary[pieces[i][0]]["courses"][pieces[0][j].strip('\r').strip('\n')] = {}
        studentdictionary[pieces[i][0]]["courses"][pieces[0][j].strip('\r').strip('\n')][pieces[i][j].strip('\r').strip('\n')] =
        print "test"

    # Grades
    elif(re.match(graderegex,pieces[0][j].strip('\r').strip('\n'))):
        print "test"

    # Grade gpa
    elif(re.match(gradegparegex,pieces[0][j].strip('\r').strip('\n'))):
        print "test"

    # Minor degree
    elif(minorregex.search(pieces[0][j].strip('\r').strip('\n')),re.IGNORECASE):
        print "test"

    # Major degree
    elif(majorregex.search(pieces[0][j].strip('\r').strip('\n')),re.IGNORECASE):
        print "test"

    # Highschool gpa
    elif(hsgparegex.search(pieces[0][j].strip('\r').strip('\n')),re.IGNORECASE):
        print "test"

    # Degree
    else:
        print "test"

    if(j >= 158 and j <= 419):
        merged.append(pieces[i][j])

    # datastructure.setdefault(firstkey,{})[second key] = value
    studentdictionary.setdefault(pieces[i][0],{})[pieces[0][j].strip('\r').strip('\n')] = pieces[i][j].strip('\r').strip('\n')
    activitydictionary.setdefault(pieces[0][j].strip('\r').strip('\n'),{})[pieces[i][0]] = pieces[i][j].strip('\r').strip('\n')
    '''

    '''
    s = pandas.Series(merged)

    counts = pandas.DataFrame(s.value_counts())

    print ("COUNTS****")
    plt.hist(counts.values,len(counts),normed=1,facecolor='green',alpha=0.75)
    plt.plot(50,len(counts),'r--',linewidth=1)
    plt.xlabel(titles)
    plt.show()

    t1 = time.time()
    ttotal1 = t1 - t0
    print("Time of datastructure load: " + str(ttotal1))

    print("MERGED")
    #print merged
    '''

'''
SERIALIZATION PERFORMANCE TESTING
*********************************

    # cPickle
    t0 = time.time()
    studentstoragefilename = "preprocessing/studentdictionary.cpickle"
    activitystoragefilename = "preprocessing/activitydictionary.cpickle"
    file1 = open(studentstoragefilename, "wb")
    file2 = open(activitystoragefilename, "wb")

    cPickle.dump(studentdictionary,file1,protocol=2)
    file1.close()
    cPickle.dump(activitydictionary,file2,protocol=2)
    file2.close()
    t1 = time.time()
    ttotal2 = t1 - t0
    print("Time of cPickle write: " + str(ttotal2))

    t0 = time.time()
    testarray1 = load_cpickle(studentstoragefilename)
    testarray2 = load_cpickle(activitystoragefilename)
    t1 = time.time()
    ttotal3 = t1 - t0
    print("Time of cPickle read: " + str(ttotal3))
    cpickletotal = ttotal2 + ttotal3
    print("*** cpickle total: " + str(cpickletotal))

    ##########

    # pickle
    t0 = time.time()
    studentstoragefilename = "preprocessing/studentdictionary.pickle"
    activitystoragefilename = "preprocessing/activitydictionary.pickle"
    file1 = open(studentstoragefilename, "wb")
    file2 = open(activitystoragefilename, "wb")
    pickle.dump(studentdictionary,file1,protocol=2)
    file1.close()
    pickle.dump(activitydictionary,file2,protocol=2)
    file2.close()
    t1 = time.time()
    ttotal4 = t1 - t0
    print("Time of pickle write: " + str(ttotal4))

    t0 = time.time()
    testarray1 = load_pickle(studentstoragefilename)
    testarray2 = load_pickle(activitystoragefilename)
    t1 = time.time()
    ttotal5 = t1 - t0

    print("Time of pickle read: " + str(ttotal5))
    pickletotal = ttotal4 + ttotal5
    print("*** pickle total: " + str(pickletotal))

    ##########

    # json
    t0 = time.time()
    studentstoragefilename = "preprocessing/studentdictionary.json"
    activitystoragefilename = "preprocessing/activitydictionary.json"
    file1 = open(studentstoragefilename, "wb")
    file2 = open(activitystoragefilename, "wb")
    json.dump(studentdictionary,file1)
    file1.close()
    json.dump(activitydictionary,file2)
    file2.close()
    t1 = time.time()
    ttotal6 = t1 - t0
    print("Time of json write: " + str(ttotal6))

    t0 = time.time()
    testarray1 = json.loads(open(studentstoragefilename).read())
    testarray2 = json.loads(open(activitystoragefilename).read())
    t1 = time.time()
    ttotal7 = t1 - t0
    print("Time of json read: " + str(ttotal7))
    jsontotal = ttotal6 + ttotal7
    print("*** json total: " + str(jsontotal))

    #pp = pprint.PrettyPrinter(indent = 3)
    #pp.pprint(testarray1)
    print("END")
'''
