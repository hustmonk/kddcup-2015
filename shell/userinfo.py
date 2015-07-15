#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""

__revision__ = '0.1'
from common import *
from weekend import *
from Object import *

class Userinfo:
    def __init__(self):
        self.uid_num = {}
        self.uid_days = {}
        for line in open("conf/user.info"):
            uid,num,days = line.strip().split("\t")
            self.uid_num[uid] = int(num)
            self.uid_days[uid] = days.split(",")
        self.week = Week()
        self.obj = Obj()

    def get_num(self, uid):
        return self.uid_num[uid]

    def get_info(self, uid):
        return self.uid_days[uid]

    def get_features(self, uid, course_id):
        f = [0]*(CIDX_VEC_NUM+1)
        for day in self.get_info(uid):
            cidx = self.obj.get_index(course_id, self.week.times(day))
            f[cidx] = f[cidx] + 1

        f[CIDX_VEC_NUM] = self.get_num(uid)
        return f

if __name__ == "__main__":
    userinfo = Userinfo()
    print userinfo.get_features("vCk71G02ss3o0puuBIhnOZwxNIZqe2KE", "3cnZpv6ReApmCaZyaQwi2izDZxVRdC01")


