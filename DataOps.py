__author__ = 'sina'

class DataOps:

    studentdict = {}
    activitydict = {}

    def __init__(self):
        import DataLoader
        studentdict = DataLoader.load_json("preprocessing/studentdictionary.json")
        activitydict = DataLoader.load_json("preprocessing/activitydictionary.json")
        print "DataOps :: datastructures loaded"

    def get_results(self,string):
        import re
        dummieidregex = re.compile('^[0-9]{7}')
        if dummieidregex.search(string):
            print "Dummie id detected"