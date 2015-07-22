#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""

__revision__ = '0.1'
from timeutil import *
from common import *
from enrollment import *

class CourseStatisticTimeInfo:
    conf_filename = "conf/course.time.info"
    def build(self):
        print "start build CourseStatisticTimeInfo..."
        enrollment = Enrollment("../data/merge/enrollment.csv")
        count = {}

        for line in open("../data/merge/log.csv"):
            #enrollment_id,username,course_id,time,source,event,object
            id,time,source,event,object = line.strip().split(",")
            if time.find("T") < 0:
                continue

            username, course_id = enrollment.enrollment_info.get(id)

            times = TimeUtil.timestamp(time)
            if course_id not in count:
                count[course_id] = []
            else:
                count[course_id].append(times)

        course_timeinfo = {}
        for (k,v) in count.items():
            v = sorted(v)
            buf = []
            for i in range(1, CIDX_VEC_NUM):
                buf.append(v[i * len(v) / CIDX_VEC_NUM])
                course_timeinfo[k] = buf

        writepickle(CourseStatisticTimeInfo.conf_filename, course_timeinfo)
        print "over build CourseStatisticTimeInfo..."

    def load(self):
        self.timeinfo = loadpickle(CourseStatisticTimeInfo.conf_filename)

        self.course_id = {}
        self.course_time = {}
        for (id, times) in self.timeinfo.items():
                self.course_id[id] = len(self.course_id)
                self.course_time[id] = sum(times)/len(times)

    def get_index(self, id, timestampe):
        infos = self.timeinfo[id]
        for i in range(len(infos)):
            if timestampe < infos[i]:
                return i
        return CIDX_VEC_NUM - 1
    
    def get_course_id(self, id):
        return self.course_id.get(id, 1)

    def get_course_time(self, id):
        return self.course_time[id]

if __name__ == "__main__":
    ct = CourseStatisticTimeInfo()
    ct.build()
    ct.load()
