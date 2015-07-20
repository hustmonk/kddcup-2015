#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""

__revision__ = '0.1'

from courseStatisticTimeInfo import *
from objweight import *
from cdate import *

class LogInfoFeatureExtractor():
    def __init__(self):
        self.cdate = Cdate()
        self.coursetimeinfo = CourseStatisticTimeInfo()
        self.coursetimeinfo.load()
        self.obj = Obj()
        self.objweight = ObjWeight()
        self.objweight.load()

    def get_spend_time_idx(self, timesum):
        k = [2, 5, 10, 30, 60, 5*60, 10*60, 30 * 60, 60 * 60, 12 * 60 * 60]
        for i in range(len(k)):
            if k[i] > timesum:
                return i
        return i

    def get_features(self, infos, course_id, isDebug = False):
        event_count = [0] * EVENT_VEC_NUM
        u_event_count = [0] * EVENT_VEC_NUM
        uday_event_count = [0] * EVENT_VEC_NUM


        dayweek_count = [0] * WEEKDAY_VEC_NUM
        hour_count = [0] * HOUR_VEC_NUM
        month_count = [0] * MONTH_VEC_NUM

        timeidx_by_object_count = [0] * CIDX_VEC_NUM
        timeidx_by_statistic_count = [0] * CIDX_VEC_NUM
        timeidx_by_datefile_count = [0] * 30

        browser = 0
        server = 0

        spendtime_sqrt_sum = 0
        spendtime_sum = 0
        event_timesum = [0] * EVENT_VEC_NUM
        event_sqrt_timesum = [0] * EVENT_VEC_NUM

        last_timestamp = 0
        stop_num = 0
        last_event_idx = -1
        u_event_dict = {}
        for info in infos:
            if info[0].find("T") < 0:
                continue
            day,timehms = info[0].split("T")
            # source info
            if info[1] == "browser":
                browser += 1
            else:
                server += 1

            # event info
            event_idx = get_event_idx(info[2])

            event_count[event_idx] = event_count[event_idx] + 1
            if info[2]+info[-1] not in u_event_dict:
                u_event_count[event_idx] = u_event_count[event_idx] + 1
            if day+info[2]+info[-1] not in u_event_dict:
                uday_event_count[event_idx] = uday_event_count[event_idx] + 1
            u_event_dict[info[2]+info[-1]] = 1
            u_event_dict[day+info[2]+info[-1]] = 1

            # time info
            timestamp = TimeUtil.timestamp(info[0])
            spendtime = 1
            if last_timestamp > timestamp - 60 * 3:
                spendtime = timestamp - last_timestamp
            else:
                stop_num += 1
            spendtime_sum = spendtime_sum + spendtime
            spendtime_sqrt_sum = spendtime_sqrt_sum + math.sqrt(spendtime)
            if last_event_idx != -1:
                event_timesum[last_event_idx] = event_timesum[last_event_idx] + spendtime
                event_sqrt_timesum[last_event_idx] = event_sqrt_timesum[last_event_idx] + math.sqrt(spendtime)
            if isDebug:
                print spendtime_sum, timestamp,last_timestamp,info[0]
            last_timestamp = timestamp


            year,month,d = day.split("-")
            month_idx = (int(month) - 1) * 2 + int(d)/16
            month_count[month_idx] = 1

            dayweek = TimeUtil.getDayWeek(day)
            dayweek_count[dayweek] = dayweek_count[dayweek] + 1

            hour = int(timehms[:2]) / 2
            hour_count[hour] = hour_count[hour] + 1
        
            timeidx = self.obj.get_index(course_id, TimeUtil.timestamp(info[0]))
            timeidx_by_object_count[timeidx] = timeidx_by_object_count[timeidx] + 1

            timeidx = self.coursetimeinfo.get_index(course_id, TimeUtil.timestamp(info[0]))
            timeidx_by_statistic_count[timeidx] = timeidx_by_statistic_count[timeidx] + 1

            timeidx = self.cdate.get_index(course_id, day)
            timeidx_by_datefile_count[timeidx] = timeidx_by_datefile_count[timeidx] + 1
            last_event_idx = event_idx


        next_public_diff = CIDX_VEC_NUM
        if last_timestamp > 1:
            next_public_diff = self.obj.get_index(course_id, last_timestamp)
        next_public = get_vector(next_public_diff, CIDX_VEC_NUM)

        spendtime_idx = self.get_spend_time_idx(spendtime_sum)
        spend_time_count = get_vector(spendtime_idx, 10)

        spendtime_idx = self.get_spend_time_idx(spendtime_sqrt_sum)
        sqrt_spend_time_count = get_vector(spendtime_idx, 10)

        buf = []
        objw = self.objweight.get_features(infos)

        k = len(infos)
        if k > 2:
            k = int(math.sqrt(k - 2)) + 2
        info_vec = get_vector(k, INFO_VEC_NUM)

        brower_ratio = (browser+3.1)/(float(len(infos))+6.5)
        fp = [stop_num, len(infos), browser, server, spendtime_sum/60.0, spendtime_sqrt_sum/60.0, brower_ratio]
        if isDebug:
            print fp

        k = sum([1 for i in event_count if i > 0])
        event_isclick_count = get_vector(k, EVENT_VEC_NUM+1)
        
        fv = [event_count,dayweek_count,hour_count,timeidx_by_object_count,timeidx_by_statistic_count, month_count, spend_time_count, sqrt_spend_time_count, fp, next_public, event_sqrt_timesum, event_timesum, u_event_count, objw, event_isclick_count, uday_event_count, timeidx_by_datefile_count, info_vec]
        fv_debug = ["event_count","dayweek_count","hour_count","timeidx_by_object_count","timeidx_by_statistic_count", "month_count", "spend_time_count", "sqrt_spend_time_count", "fp", "next_public", "event_sqrt_timesum", "event_timesum", "u_event_count", "objw", "event_isclick_count", "uday_event_count", "timeidx_by_datefile_count", "info_vec"]
        for j in range(len(fv)):
            vs = fv[j]
            if isDebug:
                print fv_debug[j],vs
            for (i, v) in enumerate(vs):
                buf.append( "%.3f" % transfer(v))
        return ",".join(buf)

    def get_features_no_courseid(self, infos, isDebug = False):
        event_count = [0] * EVENT_VEC_NUM
        weekday_count = [0] * WEEKDAY_VEC_NUM
        hour_count = [0] * HOUR_VEC_NUM
        month_count = [0] * MONTH_VEC_NUM
        browser = 0
        server = 0
        spendtime_sum = 0
        spendtime_sqrt_sum = 0
        last_timestamp = 0
        stop_num = 0
        for info in infos:
            if info[0].find("T") < 0:
                continue
            timestamp = TimeUtil.timestamp(info[0])
            if last_timestamp > timestamp - 60 * 3 and last_timestamp <= timestamp:
                spendtime_sum = spendtime_sum + timestamp - last_timestamp
                spendtime_sqrt_sum = spendtime_sqrt_sum + math.sqrt(timestamp - last_timestamp)
            else:
                stop_num += 1
                spendtime_sum = spendtime_sum + 1
                spendtime_sqrt_sum = spendtime_sqrt_sum + 1
            if isDebug:
                print spendtime_sum ,timestamp, last_timestamp, info[0]
            last_timestamp = timestamp
            day,timehms = info[0].split("T")
            if info[1] == "browser":
                browser += 1
            else:
                server += 1
            year,month,d = day.split("-")
            month_idx = (int(month) - 1) * 2 + int(d)/16
            month_count[month_idx] = month_count[month_idx] + 1

            event_idx = get_event_idx(info[2])
            event_count[event_idx] = event_count[event_idx] + 1

            weekday = TimeUtil.getDayWeek(day)
            weekday_count[weekday] = weekday_count[weekday] + 1
            hour = int(timehms[:2]) / 2
            hour_count[hour] = hour_count[hour] + 1
        
        time_idx = self.get_spend_time_idx(spendtime_sum)
        spend_time_count_vec = get_vector(time_idx, 10)

        time_idx = self.get_spend_time_idx(spendtime_sqrt_sum)
        sqrt_spend_time_count_vec = get_vector(time_idx, 10)

        k = len(infos)
        if k > 2:
            k = int(math.sqrt(k - 2)) + 2
        info_vec = get_vector(k, INFO_VEC_NUM)

        buf = []

        brower_ratio = (browser+3.1)/(float(len(infos))+6.5)
        fp = [stop_num, len(infos), browser, server, spendtime_sum/60.0, spendtime_sqrt_sum/60.0, brower_ratio]

        if isDebug:
            print fp
        fv = [event_count,weekday_count,hour_count, month_count, spend_time_count_vec, sqrt_spend_time_count_vec, fp, info_vec]
        fv_debug = ["event_count","weekday_count","hour_count", "month_count", "spend_time_count_vec", "sqrt_spend_time_count_vec", "fp", info_vec]
        for j in range(len(fv)):
            vs = fv[j]
            if isDebug:
                print fv_debug[j],vs
            for (i, v) in enumerate(vs):
                buf.append( "%.3f" % transfer(v))
        return ",".join(buf)

