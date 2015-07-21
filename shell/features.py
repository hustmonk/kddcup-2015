#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified:

"""docstring
"""

__revision__ = '0.1'


from lastdayFeature import *
from dayLevelFeature import *
from wholeWebsiteFeature import *
from wholeEnrollmentFeature import *
from statisticFeature import *
from userPredictFeature import *

from baseTimeFeature import *
from baseEnrollmentFeature import *

enrollment_filename = sys.argv[2]
featrue_filename = sys.argv[3]

feature_class_vec = [LastDayFeature(), DayLevelFeature(), WholeWebsiteFeature(), WholeEnrollmentFeature(),
                 StatisticFeature(), UserPredictFeature(), BaseTimeFeature(), BaseEnrollmentFeature()]
feature_class_vec_debug = ["LastDayFeature()", "DayLevelFeature()", "WholeWebsiteFeature()", "WholeEnrollmentFeature()", "StatisticFeature()", "UserPredictFeature()", "BaseTimeFeature()", "BaseEnrollmentFeature()"]

for feature_class in feature_class_vec:
    feature_class.load()

enrollment = Enrollment("../data/merge/enrollment.csv")
label = Label()
import math
def transfer(v):
    return math.log(v+1)
DEBUG = False
def get_features(id,IS_DEBUG=False):
    y = label.get(id)
    username, course_id = enrollment.enrollment_info.get(id)

    f = []
    start = 0
    for (i, feature_class) in enumerate(feature_class_vec):
        #print type(feature_class.get_features(id))
        x = feature_class.get_features(id)
        f.append(x)
        if DEBUG:
            print i,start,len(x.split(",")),feature_class_vec_debug
        start += len(x.split(","))
    if DEBUG:
        exit(-1)

    f = ",".join(f)
    fs = "%s,%s,%s,%s\n"  % (y, id, course_id, f)
    return fs

def process():
    fout = open(featrue_filename,"w")
    ccc = 0
    enrollment_train = Enrollment(enrollment_filename)
    for id in enrollment_train.ids:
        fs = get_features(id)
        ccc += 1
        if ccc % 5000 == 0:
            print ccc
        fout.write(fs)
    print "build over!!!"
def single(id, True):
    print get_features(id, True)

#single("200469", True)
process()

