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
kmax = {}
filter_dict = {}
N = 1800
def fit(courses, X):
    ksum = {}
    kcount = {}
    kcount["ZZ"] = [0] * N

    ksum["ZZ"] = [0] * N
    for j in range(len(X)):
        x = X[j]
        course = courses[j]
        if course not in ksum:
            kcount[course] = [0] * N
            ksum[course] = [0] * N
        for i in range(len(x)):
            ksum[course][i] = ksum[course][i] + x[i]
            kcount[course][i] = kcount[course][i] + 1
            ksum["ZZ"][i] = ksum["ZZ"][i] + x[i]
            kcount["ZZ"][i] = kcount["ZZ"][i] + 1
    for (course, sumx) in ksum.items():
        countx = kcount[course]
        kmax[course] = [0] * N
        for i in range(N):
            if sumx[i] == 0:
                kmax[course][i] = 0
            else:
                kmax[course][i] = sumx[i] / countx[i]
    for i in range(N):
        isTrans = False
        for (course, maxx) in kmax.items():
            if maxx[i] > kmax["ZZ"][i] * 1.1 or maxx[i] < kmax["ZZ"][i] * 0.9:
                isTrans = True
                break
        if isTrans == False:
            filter_dict[i] = 1
    print len(filter_dict)

def transfer(course, x):
    x1 = []
    for i in range(len(x)):
        if kmax["ZZ"][i] < 0.001:
            continue
        if i not in filter_dict:
            if kmax[course][i] == 0 or x[i] < 0.001:
                x1.append(0.0)
            else:
                x1.append((x[i] * kmax["ZZ"][i]/kmax[course][i]))
        x1.append(x[i])
    return x1
def read(filename, isFit):
    X = []
    Y = []
    ids = []
    courses = []
    for line in open("../shell/" + filename):
        arr = line.strip().replace("inf","1").split(",")
        y = int(arr[0])
        ids.append(arr[1])
        courses.append(arr[2])
        x = [ math.sqrt(math.fabs(float(k))) for k in arr[3:]]
        X.append(x)
        Y.append(y)
    if isFit:
        fit(courses, X)
    fout = open(filename+".transfer", "w")
    for i in range(len(Y)):
        x = transfer(courses[i], X[i])
        fout.write("%d,%s,%s,%s\n" % (Y[i],ids[i],courses[i],",".join(["%.2f" % k  for k in x]) ))
    fout.close()
read("train.txt", 1)
#read("train2.txt", 0)
#read("train1.txt", 0)
read("test.txt", 0)

