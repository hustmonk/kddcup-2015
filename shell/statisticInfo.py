#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified:

"""docstring
"""

__revision__ = '0.1'

from timeutil import *
from common import *
import cPickle as pickle
from label import *
from lastdayInfo import *
from enrollment import *
import math
class StatisticInfo:
    statisticInfoFilename = "conf/statistic.info"
    def build(self):
        enrollment = Enrollment("../data/merge/enrollment.csv")
        lastdayinfo = LastDayInfo()
        lastdayinfo.load_id_days()
        label = Label()
        count = {}
        dropcount = {}
        coursecount = {}
        dropcoursecount = {}
        dropfirstcount = {}
        count_by_course = {}
        test_count_by_course = {}
        dropcount_by_course = {}
        cc = 0
        dropcc = 0
        for (id, info) in lastdayinfo.id_days_infos.items():
            days = info[0]
            if label.contain(id) and len(days) > 0:
                lastday = days[-1]
                y = int(label.get(id))
                username, course_id = enrollment.enrollment_info.get(id)
                cc = cc + 1
                dropcc = dropcc + y
                if course_id not in count_by_course:
                    count_by_course[course_id] = {}
                    dropcount_by_course[course_id] = {}
                count_by_course[course_id][lastday] = count_by_course[course_id].get(lastday, 0) + 1
                dropcount_by_course[course_id][lastday] = dropcount_by_course[course_id].get(lastday, 0) + y
                """
                for day in days[:-1]:
                    count_by_course[course_id][day] = count_by_course[course_id].get(day, 0) + 1
                """

                count[lastday] = count.get(lastday, 0) + 1
                dropcount[lastday] = dropcount.get(lastday, 0) + y
                coursecount[course_id] = coursecount.get(course_id, 0) + 1
                dropcoursecount[course_id] = dropcoursecount.get(course_id, 0) + y
                if len(days) == 1:
                    dropfirstcount[course_id] = dropfirstcount.get(course_id, 0) + y
            else:
                ### start
                cpa = 1

            if course_id not in test_count_by_course:
                test_count_by_course[course_id] = {}
            test_count_by_course[course_id][lastday] = test_count_by_course[course_id].get(lastday, 0) + 1
            test_count_by_course[course_id]["x"] = test_count_by_course[course_id].get("x", 0) + 1
                ### end
        default = float(dropcc)/cc

        ratio_course_id = {}
        ratio_day_by_course_id = {}
        first_day_by_course_id = {}
        for course_id in coursecount:
            c = coursecount[course_id]
            d = dropcoursecount[course_id]
            ratio_course_id[course_id] = float(d)/float(c)
            #print "CC",course_id,d,c,float(d)/float(c),len(count_by_course[course_id]),len(test_count_by_course[course_id])

            default_course_id_ratio = float(d)/float(c)
            _ratio = {}
            for day in sorted(count_by_course[course_id]):
                if course_id not in first_day_by_course_id:
                    first_day_by_course_id[course_id] = day
                c1 = count_by_course[course_id][day]# + 5
                d1 = dropcount_by_course[course_id][day]# + default_course_id_ratio * 5
                _ratio[day] = float(d1)/float(c1)
                r1 = test_count_by_course[course_id][day]/float(test_count_by_course[course_id]["x"])
                #print day,c1,d1,d1/float(c1),c1/float(c),test_count_by_course[course_id][day],r1, (c1/float(c))/r1,"ERROR"
            ratio_day_by_course_id[course_id] = _ratio
            #print ""
        ratio_day = {}
        for day in count:
            c = count[day] + 10
            d = dropcount[day] + default * 10
            ratio_day[day] = float(d)/float(c)
        ratio_course_id_first = {}
        for course_id in coursecount:
            c = coursecount[course_id]
            d = dropfirstcount.get(course_id, 0)
            ratio_course_id_first[course_id] = float(d)/float(c)
        statistic = {}
        statistic["ratio_course_id_first"] = ratio_course_id_first
        statistic["ratio_day"] = ratio_day
        statistic["first_day_by_course_id"] = first_day_by_course_id
        statistic["ratio_course_id"] = ratio_course_id
        statistic["default"] = default
        statistic["ratio_day_by_course_id"] = ratio_day_by_course_id
        writepickle(StatisticInfo.statisticInfoFilename, statistic)
        print "build StatisticInfo over!"

    def load(self):
        statistic = loadpickle(StatisticInfo.statisticInfoFilename)
        self.default = statistic["default"]
        self.ratio_course_id_first = statistic["ratio_course_id_first"]
        self.ratio_day = statistic["ratio_day"]
        self.ratio_course_id = statistic["ratio_course_id"]
        self.ratio_day_by_course_id = statistic["ratio_day_by_course_id"]
        self.first_day_by_course_id = statistic["first_day_by_course_id"]

    def get_features(self, day, course_id, days, alldays, non_unique_days, nodrop_predict_days, nodrop_lasttoend_days):
        f = [0] * 467
        other_f = [0] * 30
        f[0] = self.ratio_course_id[course_id]
        f[1] = self.ratio_course_id_first[course_id]
        for i in range(21):
            if len(day) < 4:
                f[2+i] = self.default
            else:
                k = i - 10
                nd = TimeUtil.getnextday(day, k)
                f[2+i] = self.ratio_day.get(nd, self.default)
        start = 23
        #print self.first_day_by_course_id[course_id]
        if len(day) > 4:
            idx = TimeUtil.diff(day, self.first_day_by_course_id[course_id])
            f[start + idx] = 1
            if idx < 29:
                f[start + 30 + idx + 1] = 1 + f[start + 30 + idx + 1]
            f[start + 30 + idx] = 1 + f[start + 30 + idx]
            f[start + 60 + idx / 3] = 1 + f[start + 60 + idx / 3]
            f[start + 70 + idx / 6] = 1 + f[start + 70 + idx / 6]
            f[start + 75 + idx / 10] = 1 + f[start + 75 + idx / 10]
        else:
            return ",".join(["%.2f" % k for k in f]) + "," + (",".join(["%.2f" % k for k in other_f]))
        start = start + 78
        for d in days:
            idx = TimeUtil.diff(d, self.first_day_by_course_id[course_id])
            if idx >= 0 and idx < 30:
                f[start + idx] = 1
                if idx < 29:
                    f[start + 30 + idx + 1] = 1 + f[start + 30 + idx + 1]
                f[start + 30 + idx] = 1 + f[start + 30 + idx]
                f[start + 60 + idx / 3] = 1 + f[start + 60 + idx / 3]
                f[start + 70 + idx / 6] = 1 + f[start + 70 + idx / 6]
                f[start + 75 + idx / 10] = 1 + f[start + 75 + idx / 10]
            if idx < 0:
                #print d,self.first_day_by_course_id[course_id]
                f[start + 78] = f[start + 78] + 1

        start = start + 79
        XX = 0
        for d in non_unique_days:
            idx = TimeUtil.diff(d, self.first_day_by_course_id[course_id])
            if TimeUtil.diff(d, day) > 0 and idx < 30:
                XX = XX + 1
                other_f[idx] = other_f[idx] + 1
            if idx >= -18 and idx < 60:
                idx = idx + 18
                f[start + idx] = 1 + f[start + idx]
                f[start + 78 + idx/3] = f[start + 78 + idx/3] + 1
                f[start + 104 + idx/6] = f[start + 104 + idx/6] + 1
                #117
            elif idx < -18:
                f[start + 118] = f[start + 118] + 1
            elif idx >= 60:
                f[start + 119] = f[start + 119] + 1
        f[start+120] = XX
        start = start + 121

        for d in non_unique_days + nodrop_predict_days + nodrop_lasttoend_days:
            idx = TimeUtil.diff(d, self.first_day_by_course_id[course_id])
            if idx >= 18 and idx < 48:
                idx = idx - 18
                weight = 1
                f[start + idx] = weight + f[start + idx]
                f[start + 30 + idx/3] = f[start + 30 + idx/3] + weight
                f[start + 40 + idx/6] = f[start + 40 + idx/6] + weight
        start = start + 45

        #XX
        XX = 0
        for d in alldays:
            idx = TimeUtil.diff(d, self.first_day_by_course_id[course_id])
            if TimeUtil.diff(d, day) > 0 and idx < 30:
                XX = XX + 1
            if idx >= -18 and idx < 60:
                idx = idx + 18
                f[start + idx] = 1
                f[start + 78 + idx/3] = f[start + 78 + idx/3] + 1
                f[start + 104 + idx/6] = f[start + 104 + idx/6] + 1
                #117
            elif idx < -18:
                f[start + 118] = f[start + 118] + 1
            elif idx >= 60:
                f[start + 119] = f[start + 119] + 1
        f[start+120] = XX
        start = start + 121
        #print start

        return ",".join(["%.2f" % k for k in f]) + "," + (",".join(["%.2f" % k for k in other_f]))

    def get_start_idx(self, day, course_id):
        if len(day) < 4:
            return 0
        return TimeUtil.diff(day, self.first_day_by_course_id[course_id])
if __name__ == "__main__":
    statistic = StatisticInfo()
    statistic.build()
    statistic.load()
    print statistic.get_features("2014-06-17", "V4tXq15GxHo2gaMpaJLZ3IGEkP949IbE", ["2014-05-29","2014-06-17"], ["2014-05-29","2014-06-17"], ["2014-05-29","2014-06-17"], [], [])


