#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified:

"""docstring
"""

__revision__ = '0.22'
from enrollment import *
from label import *
from cdate import *
from lastdayInfo import *
from timeutil import *
import sys
class UserPredictInfo:
    userPredictInfo = "conf/user.predict.info"
    def build(self):
        enrollment = Enrollment("../data/merge/enrollment.csv")
        enrollment_train = Enrollment("../data/train/enrollment_train.csv")
        label = Label()
        cdate = Cdate()

        lastdayinfo = LastDayInfo()
        lastdayinfo.load_id_days()

        infos = {}
        for id in enrollment.ids:
            username, course_id = enrollment.enrollment_info.get(id)
            enr_ids = enrollment_train.user_enrollment_id.get(username, [])
            whole_enr_ids = enrollment.user_enrollment_id.get(username, [])
            drop_predict_days = [] #days of predicttime [if a enrollment is dropout]
            nodrop_predict_days = [] #days of predicttime [if a enrollment is non_dropout]
            drop_lasttoend_days = [] #days from lastday to end day of the course [if a enrollment is dropout]
            nodrop_lasttoend_days = [] #days from lastday to end day of the course [if a enrollment is non-dropout]
            test_lasttoend_days = [] #days from lastday to end day of the course [if a enrollment is in test]
            drop_enrollment_num = 0
            nodrop_enrollment_num = 0
            test_enrollment_num = 0

            for _id in whole_enr_ids:
                # ignore itself and enrollments in train
                if _id == id or label.contain(_id):
                    continue
                test_enrollment_num = test_enrollment_num + 1
                _username, _course_id = enrollment.enrollment_info.get(_id)
                lastday = lastdayinfo.get_last_day(_id)
                end = cdate.get_course_end(_course_id)
                if len(lastday) < 1:
                    continue
                diff = TimeUtil.diff(end, lastday)
                if diff < 4:
                    continue
                test_lasttoend_days = test_lasttoend_days + TimeUtil.getnextdays(lastday, diff)

            for _id in enr_ids:
                if _id == id:
                    continue
                _y = label.get(_id)
                _username, _course_id = enrollment.enrollment_info.get(_id)
                lastday = lastdayinfo.get_last_day(_id)
                if len(lastday) < 1:
                    continue
                end = cdate.get_course_end(_course_id)
                diff = TimeUtil.diff(end, lastday)
                if _y == "1":
                    drop_enrollment_num = drop_enrollment_num + 1
                    drop_predict_days = drop_predict_days + TimeUtil.getnextdays(end, 10)
                    drop_lasttoend_days = drop_lasttoend_days + TimeUtil.getnextdays(lastday, diff)

                else:
                    nodrop_enrollment_num = nodrop_enrollment_num + 1
                    nodrop_predict_days = nodrop_predict_days + TimeUtil.getnextdays(end, 10)
                    nodrop_lasttoend_days = nodrop_lasttoend_days + TimeUtil.getnextdays(lastday, diff)
            user_enrollment_predict = {}
            user_enrollment_predict["test_enrollment_num"] = test_enrollment_num
            user_enrollment_predict["nodrop_enrollment_num"] = nodrop_enrollment_num
            user_enrollment_predict["drop_enrollment_num"] = drop_enrollment_num
            user_enrollment_predict["drop_predict_days"] = drop_predict_days
            user_enrollment_predict["nodrop_predict_days"] = nodrop_predict_days
            user_enrollment_predict["drop_lasttoend_days"] = drop_lasttoend_days
            user_enrollment_predict["nodrop_lasttoend_days"] = nodrop_lasttoend_days
            user_enrollment_predict["test_lasttoend_days"] = test_lasttoend_days
            infos[id] = user_enrollment_predict
        writepickle(UserPredictInfo.userPredictInfo, infos)

    def load(self):
        self.infos = loadpickle(UserPredictInfo.userPredictInfo)

    def get_user_enrollment_predict(self, id):
        return self.infos[id]

if __name__ == "__main__":
    user_predict_info = UserPredictInfo()
    user_predict_info.build()
    user_predict_info.load()
