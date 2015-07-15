#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""

__revision__ = '0.1'
import math
import sys
from model import *
def read(filename):
    courseInfo = {}
    for line in open(filename):
        arr = line.strip().split(",")
        y = int(arr[0])
        courseid = arr[2]
        if courseid not in courseInfo:
            courseInfo[courseid] = [[],[],[]]
        x = [float(k) for k in arr[3:]]
        courseInfo[courseid][0].append(x)
        courseInfo[courseid][1].append(y)
        courseInfo[courseid][2].append(arr[1])
    return courseInfo

courseInfo_train = read(sys.argv[1])
courseInfo_test = read(sys.argv[2])
out_file = sys.argv[3]
is_valid = int(sys.argv[4])
ys = []
ps = []
for (k,v) in courseInfo_train.items():
    print k
    X_train, y_train, ids_train = v
    X_test, y_test, ids_test = courseInfo_test[k]
    model = Model()
    p = model.train(X_train, y_train, X_test, ids_test, y_test, out_file+"/"+k, is_valid)
    for i in range(len(p)):
        ys.append(y_test[i])
        ps.append(p[i])
roc_auc = metrics.roc_auc_score(ys, ps)
print roc_auc
