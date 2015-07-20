#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""

__revision__ = '0.1'


from module import *
from transfer import *

class DayLevelFeature:
    feature_filename = '_feature/day.level.feature.model'
    def build(self):
        print "start build DayLevelInfo..."
        log = LogInfo("../data/merge/log.csv")
        enrollment = Enrollment("../data/merge/enrollment.csv")
        obj = Obj()

        ccc = 0
        fs = {}
        feature_num = 0
        for id in enrollment.ids:
            ccc += 1
            if ccc % 5000 == 0:
                print ccc
            infos = log.enrollment_loginfo.get(id, [])
            username, course_id = enrollment.enrollment_info.get(id)

            info_by_day = {}
            for info in infos:
                if info[0].find("T") < 0:
                    continue
                day,timehms = info[0].split("T")
                weight = 1
                if day not in info_by_day:
                    info_by_day[day] = {}
                    info_by_day[day]["event"] = {}
                if info[1] == "browser":
                    info_by_day[day]["browser"] = info_by_day[day].get("browser", 0) + weight
                else:
                    info_by_day[day]["server"] = info_by_day[day].get("server", 0) + weight

                event_idx = get_event_idx(info[2])
                info_by_day[day]["event"][event_idx] = info_by_day[day]["event"].get(event_idx, 0) + weight

                info_by_day[day]["dayofweek"] = TimeUtil.getDayWeek(day)

                hour = int(timehms[:2]) / 2
                info_by_day[day]["hour"] = hour
        
                cidx = obj.get_index(course_id, TimeUtil.timestamp(info[0]))
                info_by_day[day]["cidx"] = cidx

            day_event_count = [0] * EVENT_VEC_NUM
            day_weekday_count = [0] * WEEKDAY_VEC_NUM
            day_hour_count = [0] * HOUR_VEC_NUM
            day_cidx_count = [0] * CIDX_VEC_NUM
            _browser = 0
            _server = 0
            for (day, info) in info_by_day.items():
                for (k,v) in info["event"].items():
                    day_event_count[k] = day_event_count[k] + math.sqrt(v)
                _browser = _browser + math.sqrt(info.get("browser", 0))
                _server = _server + math.sqrt(info.get("server", 0))
                day_weekday_count[info["dayofweek"]] = day_weekday_count[info["dayofweek"]] + 1
                day_hour_count[info["hour"]] = day_hour_count[info["hour"]] + 1
                day_cidx_count[info["cidx"]] = day_cidx_count[info["cidx"]] + 1

            just_num_vec = [_browser, _server]
            fv = [day_event_count, day_weekday_count, day_hour_count, day_cidx_count, just_num_vec]

            f = []
            feature_num = 0
            for arr in fv:
                feature_num += len(arr)
                arr = ["%s" % transfer(k) for k in arr]
                f.append(",".join(arr))
            fs[id] = ",".join(f)
        writepickle(DayLevelFeature.feature_filename, fs)
        print "build DayLevelInfo over!", feature_num

    def load(self):
        self.fs = loadpickle(DayLevelFeature.feature_filename)

    def get_features(self, id):
        return self.fs[id]

if __name__ == "__main__":
    daylevel = DayLevelFeature()
    daylevel.build()
    daylevel.load()
    #print daylevel.get_features("1")
