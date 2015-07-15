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
from cdate import *
week = Week()
class LastWeekFeature:
    def build(self):
        print "start build LastWeekFeature..."
        cdate = Cdate()
        enrollment = Enrollment("../data/merge/enrollment.csv")
        label = Label()
        log = Log("../data/merge/log.csv")
        commonfeature = CommonFeature()
        ccc = 0
        fs = {}

        for id in enrollment.ids:
            ccc += 1
            if ccc % 5000 == 0:
                print ccc
            username, course_id = enrollment.enrollment_info.get(id)
            _infos = log.enrollment_loginfo.get(id, [])
            infos = []
            for info in _infos:
                if info[0].find("T") < 0:
                    continue
                day,timehms = info[0].split("T")
                if cdate.get_index(course_id, day) > 21:
                    infos.append(info)
            f = commonfeature.get_features(infos, course_id)
            fs[id] = f
        modelFileSave = open('_feature/lastweek.info.model', 'wb')
        pickle.dump(fs, modelFileSave)
        modelFileSave.close()
        print "build LastWeekFeature over!"

    def load(self):
        modelFileLoad = open('_feature/lastweek.info.model', 'rb')
        self.fs = pickle.load(modelFileLoad)

    def get_features(self, id):
        return self.fs[id]

if __name__ == "__main__":
    daylevel = LastWeekFeature()
    daylevel.build()
    daylevel.load()
    print daylevel.get_features("117502")
