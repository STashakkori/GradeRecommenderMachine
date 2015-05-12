__author__ = 'sina'

def parsecsv(filename):
    print "TESTINGGGGG %%%%%%%"
    with open(filename) as file:
        data = file.readlines()

    pieces = []

    #destfile = open("preprocessing/testfile.txt","w")
    #destfile.write("TESTING 123")
    #destfile.close()

    for line in data:
        pieces.append(line.split(','))

    for i in range(0,len(pieces)):
        for j in range(0,len(pieces[i])):
            if(i == 0):
                # Headers
                print(pieces[i][j])

            if(j == 0):
                # DummyId's
                print(pieces[i][j])

    file.close()
    return

