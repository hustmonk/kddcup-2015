#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""

__revision__ = '0.1'


from logInfoFeatureExtractor import *

class WholeWebsiteFeature:
    whole_website_feature_filename = "_feature/whole.info.model"
    def build(self):
        print "start build WholeWebsiteFeature ..."
        enrollment = Enrollment("../data/merge/enrollment.csv")
        log = LogInfo("../data/merge/log.csv")
        log_info_feature_extractor = LogInfoFeatureExtractor()
        coursetimeinfo = CourseStatisticTimeInfo()
        coursetimeinfo.load();

        ccc = 0
        fs = {}
        for (uid, ids) in enrollment.user_enrollment_id.items():
            infos = []
            ccc += 1
            if ccc % 5000 == 0:
                print ccc
            course_id_vec = [0] * COURSE_VEC_NUM
            for id in ids:
                infos = infos + log.enrollment_loginfo.get(id, [])
                username, course_id = enrollment.enrollment_info.get(id)
                course_id_vec[coursetimeinfo.get_course_id(course_id)] = 1
            f = log_info_feature_extractor.get_features_no_courseid(infos)
            fs[uid] = f + "," + ",".join(["%s" % k for k in course_id_vec])
        writepickle(WholeWebsiteFeature.whole_website_feature_filename, fs)
        print "build WholeWebsiteFeature over!"

    def load(self):
        self.fs = loadpickle(WholeWebsiteFeature.whole_website_feature_filename)
        self.enrollment = Enrollment("../data/merge/enrollment.csv")

    def get_features(self, id):
        username, course_id = self.enrollment.enrollment_info.get(id)
        return self.fs[username]

if __name__ == "__main__":
    whole_website_feature = WholeWebsiteFeature()
    whole_website_feature.build()
    whole_website_feature.load()
    #print wholesitefeature.get_features("1")
