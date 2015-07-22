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
class UserStatisticInfo:
    info_filename = "conf/user.statistic.info.model"
    def build(self):
        print "start build UserStatisticInfo..."
        coursetimeinfo = CourseStatisticTimeInfo()
        coursetimeinfo.load()
        log = LogInfo("../data/merge/log.csv")
        enrollment = Enrollment("../data/merge/enrollment.csv")

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
                total[username]["unique_days"] = set()
                total[username]["non_unique_days"] = []
                total[username]["lognum"] = 0
                total[username]["event"] = {}
                user_course[username] = {}
            user_course[username][course_id] = coursetimeinfo.get_course_time(course_id)
            total[username]["lognum"] = total[username]["lognum"] + len(infos)
            days = set()
            for info in infos:
                event = info[2]
                total[username]["event"][event] = total[username]["event"].get(event, 0) + 1
                if info[0].find("T") < 0:
                    continue
                day,timehms = info[0].split("T")
                days.add(day)
            for day in days:
                total[username]["unique_days"].add(day)
                total[username]["non_unique_days"].append(day)
        for (u, info) in user_course.items():
            info = sorted(info.items(), key = lambda x:x[1])
            total[u]["course_order"] = {}
            for i in range(len(info)):
                total[u]["course_order"][info[i][0]] = i

        writepickle(UserStatisticInfo.info_filename, total)
        print "build UserStatisticInfo over!"

    def load(self):
        self.total = loadpickle(UserStatisticInfo.info_filename)
        self.obj = Obj()

    def get_unique_days(self, uid):
        return self.total[uid]["unique_days"]

    def get_non_unique_days(self, uid):
        return self.total[uid]["non_unique_days"]

    def get_features(self, uid, course_id):
        info = self.total[uid]

        unique_days_vec = [0] * CIDX_VEC_NUM
        for day in info["unique_days"]:
            cidx = self.obj.get_index(course_id, TimeUtil.timestamp(day))
            unique_days_vec[cidx] = unique_days_vec[cidx] + 1

        event_vec = [0] * len(CATEGORY_VEC_NUM)
        for (i, event) in enumerate(event_key):
            event_vec[i] = info["event"].get(event, 0)

        order = info["course_order"][course_id]
        course_order_vec = get_vector(order, ORDER_VEC_NUM)

        just_num_vec = [len(info["unique_days"]), len(info["non_unique_days"]), info["lognum"]]
        fv = [unique_days_vec, event_vec, course_order_vec, just_num_vec]
        f = []
        for arr in fv:
            f = f + arr
        return f

if __name__ == "__main__":
    userinfo = UserStatisticInfo()
    userinfo.build()
    userinfo.load()
    #print userinfo.get_features("vCk71G02ss3o0puuBIhnOZwxNIZqe2KE", "3cnZpv6ReApmCaZyaQwi2izDZxVRdC01")
    #print userinfo.get_features("vCk71G02ss3o0puuBIhnOZwxNIZqe2KE", "I7Go4XwWgpjRJM8EZGEnBpkfSmBNOlsO")
    
