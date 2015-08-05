__author__ = 'sina'

import numpy
import imputemat

def main():
    file = numpy.load("CS2440.1/precrossval/go_back0.npz")
    print file.files
    data = file['data']
    student_list = file['student_list']
    activity_list = file['activity_list']
    actual_vector = file['actual_vector']
    algorithm = "svd"
    k_components = 4
    result_svd, u_svd, v_svd = imputemat.fast_svd_predict(data.copy(), k_components)
    algorithm = "pca"
    k_components = 2
    result_pca, u_pca, v_pca = imputemat.fast_pca_predict(data.copy(), k_components)
    numpy.savez_compressed("CS2440.1/prediction/stuff.npz", result_svd=result_svd, u_svd=u_svd, v_svd=v_svd,
                           result_pca=result_pca, u_pca=u_pca, v_pca=v_pca, student_list=student_list,
                           actual_vector=actual_vector)

if __name__ == "__main__":
    try:
        main()

    except IOError as e:
        print e.strerror
        exit(-1)