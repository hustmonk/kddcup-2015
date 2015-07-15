#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""

__revision__ = '0.1'
import math
import sys
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
kmax = [0] * 1000
def fit(X):
    for x in X:
        for i in range(len(x)):
            if x[i] > kmax[i]:
                kmax[i] = x[i]

def transfer(x):
    x1 = []
    for i in range(len(x)):
        if kmax[i] == 0:
            continue
        x1.append(x[i]/kmax[i])
    return x1
def read(filename, isFit):
    X = []
    Y = []
    ids = []
    courses = []
    for line in open(filename):
        arr = line.strip().replace("inf","1").split(",")
        y = int(arr[0])
        ids.append(arr[1])
        courses.append(arr[2])
        x = [ math.sqrt(math.fabs(float(k))) for k in arr[3:]]
        X.append(x)
        Y.append(y)
    if isFit:
        fit(X)
    fout = open(filename+".transfer", "w")
    for i in range(len(Y)):
        x = transfer(X[i])
        fout.write("%d,%s,%s,%s\n" % (Y[i],ids[i],courses[i],",".join(["%.2f" % k  for k in x]) ))
    fout.close()
read("train.txt", 1)
read("train2.txt", 0)
read("train1.txt", 0)
read("test.txt", 0)

