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
from courseStatisticTime import *
from common import *
from highuser import *
import math
from module import *
from transfer import *
from lastday import *
from commonfeature import *

class WholeSiteFeature:
    wholesitefeaturefilename = "_feature/whole.info.model"
    def build(self):
        print "start build WholeSiteFeature..."
        enrollment = Enrollment("../data/merge/enrollment.csv")
        log = LogInfo("../data/merge/log.csv")
        commonfeature = CommonFeature()
        coursetimeinfo = CourseStatiticTimeInfo()
        coursetimeinfo.load();

        ccc = 0
        fs = {}
        for (uid, ids) in enrollment.user_enrollment_id.items():
            infos = []
            ccc += 1
            if ccc % 5000 == 0:
                print ccc
            course_id_vec = [0] * COURSE_VEC_NUM
            for id in ids:
                infos = infos + log.enrollment_loginfo.get(id, [])
                username, course_id = enrollment.enrollment_info.get(id)
                course_id_vec[coursetimeinfo.get_course_id(course_id)] = 1
            f = commonfeature.get_features_no_courseid(infos)
            fs[uid] = f + "," + ",".join(["%s" % k for k in course_id_vec])
        writepickle(WholeSiteFeature.wholesitefeaturefilename, fs)
        print "build WholeSiteFeature over!"

    def load(self):
        self.fs = loadpickle(WholeSiteFeature.wholesitefeaturefilename)

    def get_features(self, id):
        return self.fs[id]

if __name__ == "__main__":
    wholesitefeature = WholeSiteFeature()
    wholesitefeature.build()
    wholesitefeature.load()
    #print wholesitefeature.get_features("1")
