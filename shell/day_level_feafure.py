#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""

__revision__ = '0.1'


from highuser import *
from module import *
from transfer import *

class DayLevelInfo:
    daylevelFeatureFilename = '_feature/day.level.info.model'
    def build(self):
        print "start build DayLevelInfo..."
        coursetimeinfo = CourseStatiticTimeInfo()
        log = LogInfo("../data/merge/log.csv")
        enrollment = Enrollment("../data/merge/enrollment.csv")
        obj = Obj()
        label = Label()
        userinfo = Userinfo()
        userinfo.load()
        module = Module()
        module.load()
        transfer_day = Transfer()
        transfer_day.load()

        ccc = 0
        fs = {}
        for id in enrollment.ids:
            ccc += 1
            if ccc % 5000 == 0:
                print ccc
            infos = log.enrollment_loginfo.get(id, [])
            username, course_id = enrollment.enrollment_info.get(id)

            #time,source,event,o
            #source: browser,server
            #event:access,discussion,nagivate,page_close,problem,video,wiki
            #category:video,vertical,static_tab,sequential,problem,peergrading,outlink,html,discussion,dictation,course_info,course,combinedopenended,chapter,about
            #time:2014-06-13T09:52:49

            info_by_day = {}
            for info in infos:
                if info[0].find("T") < 0:
                    continue
                day,timehms = info[0].split("T")
                #weight = module.get_weight(info[3])
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

            f = [0] * (2 + EVENT_VEC_NUM + WEEKDAY_VEC_NUM + HOUR_VEC_NUM + CIDX_VEC_NUM)
            f[0] = transfer(_browser)
            f[1] = transfer(_server)
            fv_no_transfer = [day_event_count,day_weekday_count,day_hour_count,day_cidx_count]
            start = 2
            for vs in fv_no_transfer:
                for (i, v) in enumerate(vs):
                    f[start+i] = transfer(v)
                start = start + len(vs)
            fs[id] = ",".join(["%.2f" % k for k in f ])

        print start
        writepickle(DayLevelInfo.daylevelFeatureFilename, fs)
        print "build DayLevelInfo over!"

    def load(self):
        self.fs = loadpickle(DayLevelInfo.daylevelFeatureFilename)

    def get_features(self, id):
        return self.fs[id]

if __name__ == "__main__":
    daylevel = DayLevelInfo()
    daylevel.build()
    daylevel.load()
    #print daylevel.get_features("1")
