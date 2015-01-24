__author__ = 'sina'
__project__ = 'STProject'

import PCA

def main():
    pca = PCA.csvfiletomat()
    PCA.printlongmatrix(pca)
    return

if __name__ == "__main__":
    main()