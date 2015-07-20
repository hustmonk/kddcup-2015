#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""

__revision__ = '0.1'

from enrollment import *
from courseStatisticTimeInfo import *
from statisticInfo import *
from courseTimeSequenceInfo import *
from transfer import *

class BaseEnrollmentFeature:
    feature_filename = "_feature/base.enrollment.feature.model"

    def build(self):
        fs = {}
        enrollment = Enrollment("../data/merge/enrollment.csv")
        course_statistic_time = CourseStatisticTimeInfo()
        course_statistic_time.load()
        course_time_sequence_info = CourseTimeSequenceInfo()
        course_time_sequence_info.load()

        for id in enrollment.ids:
            username, course_id = enrollment.enrollment_info.get(id)

            course_id_vec = [0] * COURSE_VEC_NUM
            course_id_vec[course_statistic_time.get_course_id(course_id)] = 1

            whole_site_before_course_ids_vec = [0] * COURSE_VEC_NUM
            whole_site_after_course_ids_vec = [0] * COURSE_VEC_NUM

            before_course_num, after_course_num = course_time_sequence_info.get_course_num_before_after(username,id)
            before_course_ids, after_course_ids = course_time_sequence_info.get_course_ids_before_after(username,id)
            for k in before_course_ids:
                _username, k = enrollment.enrollment_info.get(k)
                whole_site_before_course_ids_vec[course_statistic_time.get_course_id(k)] = 1
            for k in after_course_ids:
                _username, k = enrollment.enrollment_info.get(k)
                whole_site_after_course_ids_vec[course_statistic_time.get_course_id(k)] = 1
            whole_site_before_course_num_vec = get_vector(before_course_num, MAX_ENROLLMENT_VEC_NUM)
            whole_site_after_course_num_vec = get_vector(after_course_num, MAX_ENROLLMENT_VEC_NUM)

            enr_ids = enrollment.user_enrollment_id.get(username, [])

            whole_site_course_ids_vec = [0] * COURSE_VEC_NUM
            for k in enr_ids:
                whole_site_course_ids_vec[course_statistic_time.get_course_id(k)] = 1
            enrollment_num = len(enr_ids)
            enrollment_num_vec = get_vector(enrollment_num, MAX_ENROLLMENT_VEC_NUM)

            user_num = len(enrollment.course_info.get(course_id, []))
            just_num_vec = [user_num, enrollment_num, before_course_num, after_course_num]

            fv = [course_id_vec, whole_site_before_course_ids_vec, whole_site_after_course_ids_vec, whole_site_before_course_num_vec, whole_site_after_course_num_vec,
                  whole_site_course_ids_vec, enrollment_num_vec, just_num_vec]

            f = []
            for arr in fv:
                f.append(",".join(["%s" % transfer(k) for k in arr]))

            fs[id] = ",".join(["%s" % k for k in f])
        writepickle(BaseEnrollmentFeature.feature_filename, fs)

    def load(self):
        self.fs = loadpickle(BaseEnrollmentFeature.feature_filename)

    def get_features(self, id):
        return self.fs[id]

if __name__ == "__main__":
    statisticFeature = BaseEnrollmentFeature()
    statisticFeature.build()
    statisticFeature.load()