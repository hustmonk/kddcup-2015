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
from enrollment import *
from moreinfo import *
ids = {}
enrollment = Enrollment("../data/merge/enrollment.csv")
moreinfo = MoreDayFeature()
moreinfo.load()
def read(filename):
    for line in open(filename):
        arr = line.strip().split(",")
        id = arr[1]
        feature = ",".join(arr[3:])
        ids[id] = feature
    ids[-1] = ",".join(["0"]*450)
def write(filename):
    fout = open(filename+".merge", "w")
    for line in open(filename):
        arr = line.strip().split(",")
        id = arr[1]
        username, course_id = enrollment.enrollment_info.get(id)
        k1,k2 = moreinfo.get_features(username,id)
        fout.write("%s,%s,%s\n" % (line.strip(),ids[k1],ids[k2]))
read("train.txt")
read("test.txt")
write("train1.txt")
write("train2.txt")
