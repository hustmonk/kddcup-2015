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
def read(filename,day):
    X = []
    Y = []
    ids = []
    for line in open(filename):
        arr = line.strip().replace("inf","1").split(",")
        y = int(arr[0])
        if day == 1:
            #if arr[3] != "1":
            if int(arr[4]) >= 15:
                continue
        else:
            #if arr[3] == "1":
            if int(arr[4]) < 15:
                continue
        ids.append(arr[1])

        x = [ math.sqrt(math.fabs(float(k))) for k in arr[3:]]
        X.append(x)
        Y.append(y)
    return X,Y,ids
def deal(day):
    X_train, y_train, ids_train = read(sys.argv[1], day)
    X_test, y_test, ids_test = read(sys.argv[2], day)
    out_file = sys.argv[3] + "." + str(day)
    is_valid = int(sys.argv[4])
    model = Model()
    print "model"
    model.train(X_train, y_train, X_test, ids_test, y_test, out_file, is_valid)
deal(1)
deal(2)
