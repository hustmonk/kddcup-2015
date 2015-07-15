#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""

__revision__ = '0.1'
from enrollment import *
from label import *

enrollment = Enrollment("../data/train/enrollment_train.csv")
label = Label()
stat = {}
cc = 0
yt = 0.0
for id in enrollment.ids:
    username, course_id = enrollment.enrollment_info.get(id)
    y = label.get(id)
    cc += 1
    yt += int(y)
    if username not in stat:
        stat[username] = []
    stat[username].append(y)
print yt/cc
for (k,info) in stat.items():
    if len(info) == 1:
        continue
    print info
