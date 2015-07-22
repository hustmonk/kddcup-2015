#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""

__revision__ = '0.1'

from enrollment import *
from lastdayInfo import *
from userStatisticInfo import *
from courseStatisticTimeInfo import *
from transfer import *

class BaseTimeFeature:
    feature_filename = "_feature/base.time.feature.model"

    def build(self):
        print "start build BaseTimeFeature..."
        fs = {}
        enrollment = Enrollment("../data/merge/enrollment.csv")
        lastdayinfo = LastDayInfo()
        lastdayinfo.load_id_days()
        user_statistic_info = UserStatisticInfo()
        user_statistic_info.load()
        coursetimeinfo = CourseStatisticTimeInfo()
        coursetimeinfo.load()
        transfer_day = Transfer()
        transfer_day.load()
        for id in enrollment.ids:
            username, course_id = enrollment.enrollment_info.get(id)

            days = lastdayinfo.get_days(id)
            # day gap info
            gap_day_vec = [0] * MAX_GAP_DAY_VEC_NUM
            gap_lastday_vec = [0] * MAX_GAP_DAY_VEC_NUM
            for i in range(len(days)-1):
                gap_day = TimeUtil.diff(days[i+1], days[i])
                add_vector_value(gap_day_vec, gap_day)

                gap_lastday = TimeUtil.diff(days[-1], days[i]) / 2 + 1
                add_vector_value(gap_lastday_vec, gap_lastday)

            alldays = user_statistic_info.get_unique_days(username)
            before_lastday_day_num = 0
            after_lastday_day_num = 0
            after_lastday_day_vec = [0] * MAX_GAP_DAY_VEC_NUM

            hold_day_in_enrollment = 0
            hold_day_in_site = 0
            hold_day_after_in_site = 0
            if len(days) > 0:
                lastday = days[-1]
                hold_day_in_enrollment = TimeUtil.diff(lastday, days[0])
                hold_day_in_site = TimeUtil.diff(lastday, sorted(alldays)[0])
                hold_day_after_in_site = TimeUtil.diff(sorted(alldays)[-1],lastday)
                for day in alldays:
                    diff = TimeUtil.diff(day, lastday) / 2
                    if diff > 0:
                        after_lastday_day_num = after_lastday_day_num + 1
                        add_vector_value(after_lastday_day_vec, diff)
                    else:
                        before_lastday_day_num = before_lastday_day_num + 1

            lastday_after_num_in_maxgap = sum(after_lastday_day_vec[:-1])

            hold_day_in_enrollment_vec = [0] * 12
            hold_day_in_site_vec = [0] * 12
            hold_day_after_in_site_vec = [0] * 12
            hold_day_in_enrollment_idx = get_gap_idx(hold_day_in_enrollment)
            hold_day_in_site_idx = get_gap_idx(hold_day_in_site)
            hold_day_after_in_site_idx = get_gap_idx(hold_day_after_in_site)
            hold_day_in_enrollment_vec[hold_day_in_enrollment_idx] = 1
            hold_day_in_site_vec[hold_day_in_site_idx] = 1
            hold_day_after_in_site_vec[hold_day_after_in_site_idx] = 1

            lastday_before_num_vec = get_vector(before_lastday_day_num, DAYS_VEC_NUM)
            lastday_after_num_vec = get_vector(after_lastday_day_num, DAYS_VEC_NUM)
            lastday_after_num_in_maxgap_vec = get_vector(lastday_after_num_in_maxgap, DAYS_VEC_NUM)

            day_len_vec = get_vector(len(days), DAYS_VEC_NUM)
            alldays_len_vec = get_vector(len(alldays), DAYS_VEC_NUM)

            day_len_half_vec = get_vector((len(days)+1)/2, DAYS_VEC_NUM/2)
            alldays_len_half_vec = get_vector((len(alldays)+1)/2, DAYS_VEC_NUM/2)

            if len(days) > 0:
                transfer_vec = transfer_day.get_features(days[-1])
            else:
                transfer_vec = transfer_day.get_features("")

            just_num_vec = [before_lastday_day_num, after_lastday_day_num, lastday_after_num_in_maxgap, len(days), len(alldays)]
            fv = [gap_day_vec, gap_lastday_vec, after_lastday_day_vec, hold_day_in_enrollment_vec, hold_day_in_site_vec, hold_day_after_in_site_vec,
                  hold_day_in_enrollment_vec, hold_day_in_site_vec, hold_day_after_in_site_vec, lastday_before_num_vec, lastday_after_num_vec,
                  lastday_after_num_in_maxgap_vec, day_len_vec, alldays_len_vec, day_len_half_vec, alldays_len_half_vec, transfer_vec, just_num_vec]
            f = []
            for arr in fv:
                f.append(",".join(["%s" % transfer(k) for k in arr]))

            fs[id] = ",".join(["%s" % k for k in f])

        writepickle(BaseTimeFeature.feature_filename, fs)
        print "build BaseTimeFeature over"

    def load(self):
        self.fs = loadpickle(BaseTimeFeature.feature_filename)

    def get_features(self, id):
        return self.fs[id]

if __name__ == "__main__":
    statisticFeature = BaseTimeFeature()
    statisticFeature.build()
    statisticFeature.load()