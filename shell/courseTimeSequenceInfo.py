#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""

__revision__ = '0.1'

import sys
import cPickle as pickle
from enrollment import *

from lastdayInfo import *

class CourseTimeSequenceInfo:
    conf_filename = "conf/course.timesequence.info.model"
    def build(self):
        print "start build CourseTimeSequenceInfo..."
        enrollment = Enrollment("../data/merge/enrollment.csv")
        last_day_info = LastDayInfo()
        last_day_info.load()
        ccc = 0
        fs = {}

        for id in enrollment.ids:
            ccc += 1
            if ccc % 5000 == 0:
                print ccc

            username, course_id = enrollment.enrollment_info.get(id)
            if username not in fs:
                fs[username] = {}
            fs[username][id] = last_day_info.get_last_day(id)

        writepickle(CourseTimeSequenceInfo.conf_filename, fs)
        print "build CourseTimeSequenceInfo over!"

    def load(self):
        self.fs = loadpickle(CourseTimeSequenceInfo.conf_filename)

    def get_course_ids_before_after(self, username, id):
        k = self.fs[username]
        if len(k) == 1:
            return [[],[]]
        k = sorted(k.items(), key=lambda x:x[1])
        for i in range(len(k)):
            if k[i][0] == id:
                break
        return [[j[0] for j in k[:i]], [j[0] for j in k[i+1:]]]
    
    def get_course_num_before_after(self, username, id):
        k = self.fs[username]
        if len(k) == 1:
            return [0,0]
        k = sorted(k.items(), key=lambda x:x[1])
        for i in range(len(k)):
            if k[i][0] == id:
                break
        return [i, len(k)-i-1]


if __name__ == "__main__":
    daylevel = CourseTimeSequenceInfo()
    daylevel.build()
    daylevel.load()
    #print daylevel.get_features("9Uee7oEuuMmgPx2IzPfFkWgkHZyPbWr0","1")
