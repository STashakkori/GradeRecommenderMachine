__author__ = 'sina'

import numpy
import nose

def matrixequality(matrix1,matrix2):
    if matrix1.shape != matrix2.shape:
        return False,None,None

    for i in range(0,matrix1.shape[0]):
        for j in range(0,matrix1.shape[1]):
            if numpy.isnan(matrix1[i][j]) and numpy.isnan(matrix2[i][j]):
               continue

            if not nose.tools.assert_almost_equal(matrix1[i][j],matrix2[i][j]):
                print matrix1[i][j]
                print matrix2[i][j]
                return False,i,j
    return True,None,None

