#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""

__revision__ = '0.1'

import sys
from log import *
from enrollment import *
from Object import *
from label import *
from timeutil import *
from courseStatisticTime import *
from common import *
from highuser import *
import math
from module import *
from transfer import *
from objweight import *
from cdate import *

class CommonFeature():
    def __init__(self):
        self.cdate = Cdate()
        self.coursetimeinfo = CourseStatiticTimeInfo()
        self.coursetimeinfo.load()
        self.obj = Obj()
        self.objweight = ObjWeight()
        self.objweight.load()

    def get_spend_time_idx(self, timesum):
        k = [2, 5, 10, 30, 60, 5*60, 10*60, 30 * 60, 60 * 60, 12 * 60 * 60]
        for i in range(len(k)):
            if k[i] > timesum:
                return i
        return i-1

    def get_features(self, infos, course_id, isDebug = False):

        event_count = [0] * EVENT_VEC_NUM
        category_count = [0] * CATEGORY_VEC_NUM
        u_event_count = [0] * EVENT_VEC_NUM
        uday_event_count = [0] * EVENT_VEC_NUM
        event_timesum = [0] * EVENT_VEC_NUM
        event_sqrt_timesum = [0] * EVENT_VEC_NUM
        weekday_count = [0] * WEEKDAY_VEC_NUM
        hour_count = [0] * HOUR_VEC_NUM
        cidx_count = [0] * CIDX_VEC_NUM
        cidx_by_stat_count = [0] * CIDX_VEC_NUM
        month_count = [0] * MONTH_VEC_NUM
        next_public = [0] * CIDX_VEC_NUM
        dx_by_date_count = [0] * 30
        spend_time_count = [0] * 10
        sqrt_spend_time_count = [0] * 10
        browser = 0
        server = 0
        timesum = 0
        sqrt_timesum = 0
        _p = 0
        cc = 0
        _event_idx = -1
        u_event_dict = {}
        for info in infos:
            if info[0].find("T") < 0:
                continue
            p = TimeUtil.timestamp(info[0])
            _time = 1
            _sqrt_time = 1
            if _p > p - 60 * 3:
                _time = p - _p
                _sqrt_time = math.sqrt(p - _p)
            else:
                cc += 1
            timesum = timesum + _time
            sqrt_timesum = sqrt_timesum + _sqrt_time
            if _event_idx != -1:
                event_timesum[_event_idx] = event_timesum[_event_idx] + _time/10.0
                event_sqrt_timesum[_event_idx] = event_sqrt_timesum[_event_idx] + _sqrt_time/10.0
            if isDebug:
                print timesum ,p,_p,info[0]
            _p = p
            day,timehms = info[0].split("T")
            if info[1] == "browser":
                browser += 1
            else:
                server += 1
            year,month,d = day.split("-")
            month_idx = (int(month) - 1) * 2 + int(d)/16
            month_count[month_idx] = 1

            event_idx = get_event_idx(info[2])
            _event_idx = event_idx
            category_idx = self.obj.get_category_idx(info[3])
            category_count[category_idx] = category_count[category_idx] + 1

            if info[2]+info[-1] not in u_event_dict:
                u_event_count[event_idx] = u_event_count[event_idx] + 1
            if day+info[2]+info[-1] not in u_event_dict:
                uday_event_count[event_idx] = uday_event_count[event_idx] + 1
            u_event_dict[info[2]+info[-1]] = 1
            event_count[event_idx] = event_count[event_idx] + 1

            weekday = TimeUtil.getDayWeek(day)
            weekday_count[weekday] = weekday_count[weekday] + 1
            hour = int(timehms[:2]) / 2
            hour_count[hour] = hour_count[hour] + 1
        
            cidx = self.obj.get_index(course_id, TimeUtil.timestamp(info[0]))
            cidx_count[cidx] = cidx_count[cidx] + 1

            cidx_by_stat = self.coursetimeinfo.get_index(course_id, TimeUtil.timestamp(info[0]))
            cidx_by_stat_count[cidx_by_stat] = cidx_by_stat_count[cidx_by_stat] + 1

            dx_by_date = self.cdate.get_index(course_id, day)
            dx_by_date_count[dx_by_date] = dx_by_date_count[dx_by_date] + 1
        if _p > 1:
            next_public_diff = self.obj.get_index(course_id, _p)
        else:
            next_public_diff = CIDX_VEC_NUM
        if next_public_diff > CIDX_VEC_NUM - 1:
            next_public_diff = CIDX_VEC_NUM - 1
        next_public[next_public_diff] = 1
        time_idx = self.get_spend_time_idx(timesum)
        spend_time_count[time_idx] = 1
        time_idx = self.get_spend_time_idx(sqrt_timesum)
        sqrt_spend_time_count[time_idx] = 1
        buf = []
        objw = self.objweight.get_features(infos)
        info_vec = [0] * INFO_VEC_NUM
        k = len(infos)
        if k > 3:
            k = int(math.sqrt(k - 3)) + 3
        if k > INFO_VEC_NUM-1:
            k = INFO_VEC_NUM-1
        info_vec[k] = 1
        fp = [cc, len(infos), browser, server, timesum/60.0, sqrt_timesum/60.0]
        buf.append( "%.3f" % ((browser+3.1)/(float(len(infos))+6.5)))
        if isDebug:
            print fp
        event_isclick_count = [0] * (EVENT_VEC_NUM+1)
        k = sum([1 for i in event_count if i > 0])
        #event_isclick_count[k] = 1
        #print k
        
        fv = [event_count,weekday_count,hour_count,cidx_count,cidx_by_stat_count, month_count, spend_time_count, sqrt_spend_time_count, fp, next_public, event_sqrt_timesum, event_timesum, u_event_count, objw, event_isclick_count, uday_event_count, dx_by_date_count]
        fv_debug = ["event_count","weekday_count","hour_count","cidx_count","cidx_by_stat_count", "month_count", "spend_time_count", "sqrt_spend_time_count", "fp", "next_public", "event_sqrt_timesum", "event_timesum", "u_event_count", "objw", "event_isclick_count", "uday_event_count", "dx_by_date_count"]
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
        spend_time_count = [0] * 10
        sqrt_spend_time_count = [0] * 10
        browser = 0
        server = 0
        timesum = 0
        sqrt_timesum = 0
        _p = 0
        cc = 0
        for info in infos:
            if info[0].find("T") < 0:
                continue
            p = TimeUtil.timestamp(info[0])
            if _p > p - 60 * 3 and _p <= p:
                timesum = timesum + p - _p
                sqrt_timesum = sqrt_timesum + math.sqrt(p - _p)
            else:
                cc += 1
                timesum = timesum + 1
                sqrt_timesum = sqrt_timesum + 1
            if isDebug:
                print timesum ,p,_p,info[0]
            _p = p
            day,timehms = info[0].split("T")
            if info[1] == "browser":
                browser += 1
            else:
                server += 1
            year,month,d = day.split("-")
            month_idx = (int(month) - 1) * 2 + int(d)/16
            month_count[month_idx] = 1

            event_idx = get_event_idx(info[2])
            event_count[event_idx] = event_count[event_idx] + 1

            weekday = TimeUtil.getDayWeek(day)
            weekday_count[weekday] = weekday_count[weekday] + 1
            hour = int(timehms[:2]) / 2
            hour_count[hour] = hour_count[hour] + 1
        
        time_idx = self.get_spend_time_idx(timesum)
        spend_time_count[time_idx] = 1
        time_idx = self.get_spend_time_idx(sqrt_timesum)
        sqrt_spend_time_count[time_idx] = 1
        info_vec = [0] * INFO_VEC_NUM
        k = len(infos)
        if k > 5:
            k = int(math.sqrt(k - 5 )) + 5
        if k > INFO_VEC_NUM-1:
            k = INFO_VEC_NUM-1
        info_vec[k] = 1
        buf = []
        fp = [cc, len(infos), browser, server, timesum/60.0, sqrt_timesum/60.0]
        buf.append( "%.3f" % ((browser+3.1)/(float(len(infos))+6.5)))
        if isDebug:
            print fp
        fv = [event_count,weekday_count,hour_count, month_count, spend_time_count, sqrt_spend_time_count, fp]
        fv_debug = ["event_count","weekday_count","hour_count", "month_count", "spend_time_count", "sqrt_spend_time_count", "fp"]
        for j in range(len(fv)):
            vs = fv[j]
            if isDebug:
                print fv_debug[j],vs
            for (i, v) in enumerate(vs):
                buf.append( "%.3f" % transfer(v))
        return ",".join(buf)

