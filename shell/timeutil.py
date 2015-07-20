#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""

__revision__ = '0.1'
import time
class TimeUtil:
    @staticmethod
    def getDayWeek(day):
        t1 = TimeUtil.timestamp(day)
        return int(time.strftime("%w",time.gmtime(int(t1) + 8*60*60)))

    @staticmethod
    def diff(day1, day2):
        d1 = TimeUtil.timestamp(day1)
        d2 = TimeUtil.timestamp(day2)
        return int((d1-d2)/86400)

    @staticmethod
    def timestamp(timestr):
        if timestr.find("T")>0:
            return time.mktime(time.strptime(timestr,'%Y-%m-%dT%H:%M:%S'))
        else:
            return time.mktime(time.strptime(timestr,'%Y-%m-%d'))

    @staticmethod
    def stypetime(times):
        timeArray = time.localtime(times)
        otherStyleTime = time.strftime("%Y-%m-%dT%H:%M:%S", timeArray)
        return otherStyleTime
    
    @staticmethod
    def getnextday(day, i):
        k = TimeUtil.timestamp(day)
        k = k + 86400 * i
        timeArray = time.localtime(k)
        otherStyleTime = time.strftime("%Y-%m-%d", timeArray)
        return otherStyleTime
    @staticmethod
    def getnextdays(day, n):
        buf = []
        if n < 1:
            return buf
        for i in range(1, n+1):
            k = TimeUtil.getnextday(day, i)
            buf.append(k)
        return buf

if __name__ == "__main__":
    week = TimeUtil()
    print week.getDayWeek("2015-05-16")
    print type(week.getDayWeek("2015-05-16"))
    print week.timestamp("2015-05-16T07:08:09")
    print type(week.timestamp("2015-05-16T07:08:09"))
    print week.stypetime(week.timestamp("2015-05-16T07:08:09"))
    print week.diff("2015-05-16","2015-05-14")
    print week.diff('2014-07-11', '2014-07-05'),"X"
    print week.timestamp("2014-06-07") -  week.timestamp("2014-06-06")
    for i in range(-10, 10):
        print week.getnextday("2014-06-07", i),i
