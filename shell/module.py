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
from timeutil import *
from courseStatisticTimeInfo import *
from common import *
import math
import cPickle as pickle
class Module:
    conf_filename = "conf/modular.info.model"
    def build(self):
        print "start build Module..."

        label = Label()
        coursetimeinfo = CourseStatisticTimeInfo()
        coursetimeinfo.load()
        #log = Log("../data/merge/log.csv")
        #enrollment = Enrollment("../data/merge/enrollment.csv")
        log = LogInfo("../data/train/log_train.csv")
        enrollment = Enrollment("../data/train/enrollment_train.csv")
        obj = Obj()
        moduler_stat = {}
        ccc = 0
        course_stat = {}
        course_label = {}
        course_count = {}
        for id in enrollment.ids:
            ccc += 1
            if ccc % 5000 == 0:
                print ccc
            infos = log.enrollment_loginfo.get(id, [])
            y = label.get(id)
            username, course_id = enrollment.enrollment_info.get(id)
            course_stat[course_id] = course_stat.get(course_id, 0) + len(infos)
            course_count[course_id] = course_count.get(course_id, 0) + 1
            course_label[course_id] = course_label.get(course_id, 0) + int(y)
            for info in infos:
                ##time,source,event,o
                o = info[3]
                moduler_stat[o] = moduler_stat.get(o, 0) + 1

        stat = {}
        stat["moduler_stat"] = moduler_stat
        stat["course_stat"] = course_stat
        stat["course_label"] = course_label
        stat["course_count"] = course_count
        writepickle(Module.conf_filename, stat)
        print "build Module over!"

    def load(self):

        self.moduler_stat = loadpickle(Module.conf_filename)
        self.obj = Obj()
        self.course_stat = self.moduler_stat["course_stat"]
        self.course_label = self.moduler_stat["course_label"]
        self.course_count = self.moduler_stat["course_count"]
    
    def get_weight(self, o, course_id):
        default_id = "SpATywNh6bZuzm8s1ceuBUnMUAeoAHHw"
        ratio = self.course_count[course_id]/float(self.course_count[default_id])
        return 3/math.sqrt(self.moduler_stat["moduler_stat"].get(o)/ratio+1)

if __name__ == "__main__":
    userinfo = Module()
    userinfo.build()
    userinfo.load()
    #print userinfo.get_weight("bLd0qFlUenJjVXjJFYxr4hHl3GiZeCjn")
    
