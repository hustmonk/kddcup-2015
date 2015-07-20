#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""

__revision__ = '0.1'
from enrollment import *
from lastdayInfo import *
from statisticInfo import *
from userStatisticInfo import *
class StatisticFeature:
    statisticFeatureFilename = "_feature/statistic.info.model"

    def build(self):
        fs = {}
        enrollment = Enrollment("../data/merge/enrollment.csv")
        lastdayinfo = LastDayInfo()
        lastdayinfo.load_id_days()
        statistic = StatisticInfo()
        statistic.load()
        user_statistic_info = UserStatisticInfo()
        user_statistic_info.load()
        for id in enrollment.ids:
            days = lastdayinfo.get_days(id)
            if len(days) == 0:
                lastday = ""
            else:
                lastday = days[-1]
            username, course_id = enrollment.enrollment_info.get(id)
            non_unique_days = user_statistic_info.get_non_unique_days(username)
            unique_days = user_statistic_info.get_unique_days(username)

            f = statistic.get_features(lastday, course_id, days, unique_days, non_unique_days)
            fs[id] = f
        writepickle(StatisticFeature.statisticFeatureFilename, fs)

    def load(self):
        self.fs = loadpickle(StatisticFeature.statisticFeatureFilename)

    def get_features(self, id):
        return self.fs[id]

if __name__ == "__main__":
    statisticFeature = StatisticFeature()
    statisticFeature.build()
    statisticFeature.load()
