#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""

__revision__ = '0.1'

import sys
from log import *
from enrollment import *
from Object import *
from label import *
from weekend import *
from common import *
week = Week()
enrollment = Enrollment("../data/merge/enrollment.csv")
obj = Obj()
label = Label()
fout = open("conf/course.time.info","w")

count = {}
for line in open("../data/merge/log.csv"):
    #enrollment_id,username,course_id,time,source,event,object
    id,time,source,event,object = line.strip().split(",")
    username, course_id = enrollment.enrollment_info.get(id)
    if time.find("T") < 0:
        continue
    times = week.times(time)
    if course_id not in count:
        count[course_id] = []
    else:
        count[course_id].append(times)

for (k,v) in count.items():
    v = sorted(v)
    buf = []
    for i in range(CIDX_VEC_NUM):
        buf.append(v[i * len(v) / CIDX_VEC_NUM])
    fout.write("%s\t%s\n" % (k, ",".join(["%s" % k for k in buf])))

