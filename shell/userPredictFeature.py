#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified:

"""docstring
"""

__revision__ = '0.1'
from enrollment import *
from label import *
from cdate import *
from lastdayInfo import *
from timeutil import *
from userPredictInfo import *
import sys
class UserPredictFeature:
    feature_filename = "_feature/user.predict.feature"

    def build(self):
        print "start build UserPredictFeature..."
        enrollment = Enrollment("../data/merge/enrollment.csv")
        user_predict_info = UserPredictInfo()
        user_predict_info.load()
        cdate = Cdate()

        fs = {}
        for id in enrollment.ids:
            user_enrollment_predict = user_predict_info.get_user_enrollment_predict(id)
            test_enrollment_num = user_enrollment_predict["test_enrollment_num"]
            nodrop_enrollment_num = user_enrollment_predict["nodrop_enrollment_num"]
            drop_enrollment_num = user_enrollment_predict["drop_enrollment_num"]

            drop_predict_days = user_enrollment_predict["drop_predict_days"]
            nodrop_predict_days = user_enrollment_predict["nodrop_predict_days"]
            drop_lasttoend_days = user_enrollment_predict["drop_lasttoend_days"]
            nodrop_lasttoend_days = user_enrollment_predict["nodrop_lasttoend_days"]
            test_lasttoend_days = user_enrollment_predict["test_lasttoend_days"]

            username, course_id = enrollment.enrollment_info.get(id)
            end = cdate.get_course_end(course_id)
            k1 = self.k_get_features(end, drop_predict_days)
            k2 = self.k_get_features(end, nodrop_predict_days)
            k3 = self.k_get_features(end, test_lasttoend_days) #TODO
            k4 = self.k_get_features(end, drop_predict_days + drop_lasttoend_days)
            k5 = self.k_get_features(end, nodrop_predict_days + nodrop_lasttoend_days)

            drop_ratio = drop_enrollment_num / (drop_enrollment_num + nodrop_enrollment_num + 1.0)
            nondrop_ratio = nodrop_enrollment_num/(drop_enrollment_num + nodrop_enrollment_num + 1.0)
            f = [test_enrollment_num, nodrop_enrollment_num, drop_enrollment_num, drop_ratio, nondrop_ratio]
            nodrop_enrollment_num_vec = get_vector(nodrop_enrollment_num, 5)
            drop_enrollment_num_vec = get_vector(drop_enrollment_num, 5)
            test_enrollment_num_vec = get_vector(test_enrollment_num, 5)

            f = ["%s" % k for k in (f + nodrop_enrollment_num_vec + drop_enrollment_num_vec + test_enrollment_num_vec)]
            f.append(k1)
            f.append(k2)
            f.append(k3)
            f.append(k4)
            f.append(k5)
            fs[id] = ",".join(f)
        writepickle(UserPredictFeature.feature_filename, fs)
        print "build UserPredictFeature over!"

    def load(self):
        self.fs = loadpickle(UserPredictFeature.feature_filename)

    def get_features(self, id):
        return self.fs[id]

    def k_get_features(self,end,daylist):
        M = 15
        N = 15
        k = [0] * (M + N + (M + N)/3)

        for day in daylist:
            idx = TimeUtil.diff(end, day)
            if idx >= -N and idx < M:
                idx = idx + N
                k[idx] = 1 + k[idx]
                k[idx/3 + N + M] = 1 + k[idx/3 + N + M]
        k = ",".join(["%d" % i for i in k])

        return k

if __name__ == "__main__":
    user_predict_feature = UserPredictFeature()
    user_predict_feature.build()
    user_predict_feature.load()
