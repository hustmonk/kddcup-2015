#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""

__revision__ = '0.1'


from logInfoFeatureExtractor import *

class WholeEnrollmentFeature:
    featurefilename = '_feature/whole.enrollment.feature.model'
    def build(self):
        print "start build AllDayFeature..."
        enrollment = Enrollment("../data/merge/enrollment.csv")
        label = Label()
        log = LogInfo("../data/merge/log.csv")
        log_info_feature_extractor = LogInfoFeatureExtractor()
        ccc = 0
        fs = {}

        for id in enrollment.ids:
            ccc += 1
            if ccc % 5000 == 0:
                print ccc
            infos = log.enrollment_loginfo.get(id, [])
            username, course_id = enrollment.enrollment_info.get(id)
            f = log_info_feature_extractor.get_features(infos, course_id)
            fs[id] = f
        writepickle(WholeEnrollmentFeature.featurefilename, fs)
        print "build AllDayFeature over!"

    def load(self):
        self.fs = loadpickle(WholeEnrollmentFeature.featurefilename)

    def get_features(self, id):
        return self.fs[id]

if __name__ == "__main__":
    whole_enrollment_feature = WholeEnrollmentFeature()
    whole_enrollment_feature.build()
    whole_enrollment_feature.load()
    #print whole_enrollment_feature.get_features("117502")
