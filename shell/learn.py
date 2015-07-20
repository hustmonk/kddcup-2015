#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""

__revision__ = '0.1'
import math
import sys
from model import *
#from randomforest import *
def read(filename):
    X = []
    Y = []
    ids = []
    for line in open(filename):
        arr = line.strip().replace("inf","1").split(",")
        y = int(arr[0])
        ids.append(arr[1])

        x = [ math.sqrt(math.fabs(float(k))) for k in arr[3:]]
        X.append(x)
        Y.append(y)
        """
        if len(X) > 10000:
            break
        """
    print len(X[0])
    return X,Y,ids

X_train, y_train, ids_train = read(sys.argv[1])
X_test, y_test, ids_test = read(sys.argv[2])
out_file = sys.argv[3]
is_valid = int(sys.argv[4])
model = Model()
print "model"
model.train(X_train, y_train, X_test, ids_test, y_test, out_file, is_valid)
