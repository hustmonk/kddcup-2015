#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""

__revision__ = '0.1'

import sys
from commonfeature import *
import cPickle as pickle

class MoreDayFeature:
    moreDayFeatureFilename = "_feature/moreday.info.model"
    def build(self):
        print "start build LastDayFeature..."
        enrollment = Enrollment("../data/merge/enrollment.csv")
        last_day_info = LastDayInfo()
        last_day_info.load()
        commonfeature = CommonFeature()
        ccc = 0
        fs = {}

        for id in enrollment.ids:
            ccc += 1
            if ccc % 5000 == 0:
                print ccc
            infos = last_day_info.get_info(id)
            for info in infos:
                if info[0].find("T") < 0:
                    continue
                day = info[0].split("T")[0]

            username, course_id = enrollment.enrollment_info.get(id)
            if username not in fs:
                fs[username] = {}
            fs[username][id] = day

        writepickle(MoreDayFeature.moreDayFeatureFilename, fs)
        print "build LastDayFeature over!"

    def load(self):
        self.fs = loadpickle(MoreDayFeature.moreDayFeatureFilename)

    def get_enrollment_ids(self, username, id):
        k = self.fs[username]
        if len(k) == 1:
            return [[],[]]
        k = sorted(k.items(), key=lambda x:x[1])
        for i in range(len(k)):
            if k[i][0] == id:
                break
        return [[j[0] for j in k[:i]], [j[0] for j in k[i+1:]]]
    
    def get_enrollment_features(self, username, id):
        k = self.fs[username]
        if len(k) == 1:
            return [0,0]
        k = sorted(k.items(), key=lambda x:x[1])
        for i in range(len(k)):
            if k[i][0] == id:
                break
        return [i, len(k)-i-1]

    def get_features(self, username, id):
        k = self.fs[username]
        if len(k) == 1:
            return [-1,-1]
        k = sorted(k.items(), key=lambda x:x[1])
        for i in range(len(k)):
            if k[i][0] == id:
                break
        if i == 0:
            return [-1, k[1][0]]
        elif i == len(k)-1:
            return [k[i-1][0],-1]
        else:
            return [k[i-1][0],k[i+1][0]]


if __name__ == "__main__":
    daylevel = MoreDayFeature()
    daylevel.build()
    daylevel.load()
    #print daylevel.get_features("9Uee7oEuuMmgPx2IzPfFkWgkHZyPbWr0","1")
