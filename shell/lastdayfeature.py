#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""

__revision__ = '0.1'

import sys

from lastdayInfo import *
from logInfoFeatureExtractor import *
from objweight import *
import cPickle as pickle
class LastDayFeature:
    feature_filename = '_feature/lastday.info.model'
    def build(self):
        print "start build LastDayFeature..."
        enrollment = Enrollment("../data/merge/enrollment.csv")
        last_day_info = LastDayInfo()
        last_day_info.load()
        loginfo_feature_extractor = LogInfoFeatureExtractor()
        ccc = 0
        fs = {}

        for id in enrollment.ids:
            ccc += 1
            if ccc % 5000 == 0:
                print ccc
            infos = last_day_info.get_info(id)
            username, course_id = enrollment.enrollment_info.get(id)
            f = loginfo_feature_extractor.get_features(infos, course_id)
            fs[id] = f
        writepickle(LastDayFeature.feature_filename, fs)
        print "build LastDayFeature over!"

    def load(self):
        self.fs = loadpickle(LastDayFeature.feature_filename)

    def get_features(self, id):
        return self.fs[id]

if __name__ == "__main__":
    daylevel = LastDayFeature()
    daylevel.build()
    daylevel.load()
    #print daylevel.get_features("1")
