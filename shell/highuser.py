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
class Userinfo:
    def build(self):
        print "start build Userinfo..."
        coursetimeinfo = CourseStatiticTimeInfo()
        coursetimeinfo.load()
        log = LogInfo("../data/merge/log.csv")
        enrollment = Enrollment("../data/merge/enrollment.csv")
        obj = Obj()
        total = {}
        ccc = 0
        user_course = {}
        for id in enrollment.ids:
            ccc += 1
            if ccc % 5000 == 0:
                print ccc
            infos = log.enrollment_loginfo.get(id, [])
            username, course_id = enrollment.enrollment_info.get(id)
            if course_id == "course_id":
                continue
            if username not in total:
                total[username] = {}
                total[username]["day"] = set()
                total[username]["lognum"] = 0
                total[username]["category"] = {}
                user_course[username] = {}
            user_course[username][course_id] = coursetimeinfo.get_course_time(course_id)
            total[username]["lognum"] = total[username]["lognum"] + len(infos)
            for info in infos:
                category = info[2]
                total[username]["category"][category] = total[username]["category"].get(category, 0) + 1
                if info[0].find("T") < 0:
                    continue
                day,timehms = info[0].split("T")
                total[username]["day"].add(day)
        for (u, info) in user_course.items():
            info = sorted(info.items(), key = lambda x:x[1])
            total[u]["course_order"] = {}
            for i in range(len(info)):
                total[u]["course_order"][info[i][0]] = i

        modelFileSave = open('conf/user.info.model', 'wb')
        pickle.dump(total, modelFileSave)
        modelFileSave.close()
        print "build Userinfo over!"

    def load(self):
        modelFileLoad = open('conf/user.info.model', 'rb')
        self.total = pickle.load(modelFileLoad)

        self.obj = Obj()
        """
        for (k, v) in self.total.items():
            days = v["day"]
            print "%s\t%d\t%s" % (k, len(days), days)
        """

    def get_days(self,uid):
        return self.total[uid]["day"]
    
    def get_features(self, uid, course_id):
        info = self.total[uid]
        f = [0]*(CIDX_VEC_NUM+2+EVENT_VEC_NUM+ORDER_VEC_NUM)
        f[0] = len(info["day"])
        f[1] = info["lognum"]
        start = 2
        for day in info["day"]:
            cidx = self.obj.get_index(course_id, TimeUtil.timestamp(day))
            f[start + cidx] = f[start + cidx] + 1
        start = 2 + CIDX_VEC_NUM
        for (i,event) in enumerate(event_key):
            f[i + start] = info["category"].get(event, 0)

        start = 2 + CIDX_VEC_NUM + EVENT_VEC_NUM
        order = info["course_order"][course_id]
        if order >= ORDER_VEC_NUM-1:
            order = ORDER_VEC_NUM-1
        f[order+start] = 1
        return f

if __name__ == "__main__":
    userinfo = Userinfo()
    userinfo.build()
    userinfo.load()
    #print userinfo.get_features("vCk71G02ss3o0puuBIhnOZwxNIZqe2KE", "3cnZpv6ReApmCaZyaQwi2izDZxVRdC01")
    #print userinfo.get_features("vCk71G02ss3o0puuBIhnOZwxNIZqe2KE", "I7Go4XwWgpjRJM8EZGEnBpkfSmBNOlsO")
    
