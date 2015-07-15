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
from courseStatisticTime import *
from common import *
import math
import cPickle as pickle
class Module:
    def build(self):
        print "start build Module..."

        label = Label()
        coursetimeinfo = CourseStatiticTimeInfo()
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
        modelFileSave = open('conf/modular.info.model', 'wb')
        pickle.dump(stat, modelFileSave)
        modelFileSave.close()
        print "build Module over!"

    def load(self):
        modelFileLoad = open('conf/modular.info.model', 'rb')
        self.moduler_stat = pickle.load(modelFileLoad)
        self.obj = Obj()
        self.course_stat = self.moduler_stat["course_stat"]
        self.course_label = self.moduler_stat["course_label"]
        self.course_count = self.moduler_stat["course_count"]
        """
        for (k) in course_stat:
            print "%s\t%d\t%d\t%d\t%.3f\t%.3f" % (k,course_stat[k],course_label[k],course_count[k],course_label[k]/float(course_count[k]), course_stat[k]/float(course_count[k]))
        """
        """
        for (k, v) in self.moduler_stat.items():
            print k,v,self.get_weight(k)
        """
    
    def get_weight(self, o, course_id):
        default_id = "SpATywNh6bZuzm8s1ceuBUnMUAeoAHHw"
        ratio = self.course_count[course_id]/float(self.course_count[default_id])
        return 3/math.sqrt(self.moduler_stat["moduler_stat"].get(o)/ratio+1)

if __name__ == "__main__":
    userinfo = Module()
    userinfo.build()
    userinfo.load()
    #print userinfo.get_weight("bLd0qFlUenJjVXjJFYxr4hHl3GiZeCjn")
    
