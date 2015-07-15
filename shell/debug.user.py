#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""
import sys
from enrollment import *
from commonfeature import *
__revision__ = '0.1'
enrollment = Enrollment("../data/merge/enrollment.csv")
commonfeature = CommonFeature()
infos = []
for line in open("../data/merge/log.csv"):
    id = line.split(",")[0]
    if id == sys.argv[1]:
        enrollment_id,time,source,event,o = line.strip().split(",")
        infos.append([time,source,event,o])
    elif len(infos) > 1:
        username, course_id = enrollment.enrollment_info.get(sys.argv[1])
        print "\n".join([k[0] for k in infos])
        f = commonfeature.get_features(infos, course_id, True)
        #f = commonfeature.get_features_no_courseid(infos,  True)
        print f
        break
