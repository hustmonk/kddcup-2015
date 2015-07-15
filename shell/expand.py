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
from weekend import *
from coursetime import *
from common import *
from highuser import *
import math
from module import *
from transfer import *
from lastday import *
from commonfeature import *
week = Week()
class AllDayFeature:
    def build(self):
        print "start build AllDayFeature..."
        enrollment = Enrollment("../data/merge/enrollment.csv")
        label = Label()
        log = Log("../data/merge/log.csv")
        ccc = 0
        fout_log = open("log.expand.csv", "w")
        fout_enr = open("enrollment.expand.csv", "w")
        lastdayinfo = LastDayInfo()
        lastdayinfo.load_id_days()
        for id in enrollment.ids:
            ccc += 1
            if ccc % 5000 == 0:
                print ccc
            infos = log.enrollment_loginfo.get(id, [])
            username, course_id = enrollment.enrollment_info.get(id)
            days = lastdayinfo.get_days(id)
            if len(days) < 2:
                continue
            fout_enr.write("%sx,%sx,%s\n" % (id, username, course_id))
            
            firstday = infos[0][0][:10]
            for info in infos:
                day = info[0][:10]
                if day == firstday:
                    fout_log.write("%sx,%s\n" % (id, ",".join(info)))
        fout_log.close()
        fout_enr.close()

if __name__ == "__main__":
    daylevel = AllDayFeature()
    daylevel.build()
