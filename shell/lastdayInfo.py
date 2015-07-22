#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""

__revision__ = '0.1'

import sys
from log import *
from enrollment import *
from common import *

class LastDayInfo:
    lastday_log_filename = 'conf/last.day.log'
    enrollment_days_filename = "conf/enrollment.days.info"
    dayindex_filename = "conf/day.index.info"

    def build(self):
        print "start LastDayInfo build..."
        log = LogInfo("../data/merge/log.csv")
        enrollment = Enrollment("../data/merge/enrollment.csv")
        ccc = 0
        last_infos = {}
        id_days_infos = {}
        dayDict = {}
        for id in enrollment.ids:
            days = set()
            ccc += 1
            if ccc % 5000 == 0:
                print ccc
            infos = log.enrollment_loginfo.get(id, [])
            buf = []
            _day = ""
            _lastTime = ""
            for info in infos:
                ##time,source,event,o
                day = info[0].split("T")[0]
                if day not in dayDict:
                    dayDict[day] = len(dayDict)
                days.add(day)
                if day != _day:
                    buf = []
                buf.append(",".join(info))
                _day = day
                _lastTime = info[0]
            last_infos[id] = buf
            days = sorted(days)

            id_days_infos[id] = [days,_lastTime]

        writepickle(LastDayInfo.lastday_log_filename, last_infos)
        writepickle(LastDayInfo.enrollment_days_filename, id_days_infos)
        writepickle(LastDayInfo.dayindex_filename, dayDict)

        print "LastDayInfo build over"

    def load(self):
        self.last_infos = loadpickle(LastDayInfo.lastday_log_filename)
        self.load_id_days()

    def load_id_days(self):
        self.id_days_infos = loadpickle(LastDayInfo.enrollment_days_filename)
        self.dayDict = loadpickle(LastDayInfo.dayindex_filename)

    def get_info(self, id):
        return [k.split(",") for k in self.last_infos[id]]

    def get_days(self, id):
        return self.id_days_infos[id][0]

    def get_last_day(self, id):
        days = self.get_days(id)
        if len(days) == 0:
            return ""
        return days[-1]

    def get_lasthour(self, id):
        hour = self.id_days_infos[id][1]
        if len(hour) < 3:
            return 0
        return int(hour[11:13])/12

    def get_day_index(self, day):
        return self.dayDict[day]

    def get_day_idx_features(self, days):
        f = [0] * len(self.dayDict)
        for day in days:
            if len(day) > 1:
                idx = self.dayDict[day]
                f[idx] = 1 + f[idx]
        return ",".join(["%d" % k for k in f])

if __name__ == "__main__":
    userinfo = LastDayInfo()
    userinfo.build()
    userinfo.load()
    print userinfo.get_info("180167")
