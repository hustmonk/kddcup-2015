#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified:

"""docstring
"""

__revision__ = '0.1'
from enrollment import *
from label import *
from cdate import *
from lastday import *
from timeutil import *
import sys
class Correction:
    def __init__(self, enrollmentfile,debug = False):
        self.enrollment = Enrollment("../data/merge/enrollment.csv")
        self.enrollment_train = Enrollment("../data/train/enrollment_train.csv")

        self.label = Label()
        self.cdate = Cdate()
        self.debug = debug
        self.lastdayinfo = LastDayInfo()
        self.lastdayinfo.load_id_days()

    def get_features(self, id):
        username, course_id = self.enrollment.enrollment_info.get(id)
        enr_ids = self.enrollment_train.user_enrollment_id.get(username, [])
        whole_enr_ids = self.enrollment.user_enrollment_id.get(username, [])
        dropdays = []
        nodropdays = []
        dropdays1 = []
        nodropdays1 = []
        dropnum = 0
        nodropnum = 0

        _end = self.cdate.get_course_end(course_id)
        days = self.lastdayinfo.get_days(id)
        if self.debug:
            print "id,_end,course_id,days"
            print id,_end,course_id,days
        kws = [0] * 30
        for _id in whole_enr_ids:
            _username, _course_id = self.enrollment.enrollment_info.get(_id)
            days = self.lastdayinfo.get_days(_id)
            start = self.cdate.get_course_start(_course_id)
            if self.debug:
                print start,days
            for day in days:
                diff = TimeUtil.diff(day, start)
                if self.debug:
                    print diff,day
                if diff >= 0 and diff < 30:
                    kws[diff] = kws[diff] + 1
        kws = ",".join(["%d" % k for k in kws])
        if self.debug:
            print kws
        lostdays = []
        for _id in whole_enr_ids:
            if _id == id:
                continue
            _username, _course_id = self.enrollment.enrollment_info.get(_id)
            days = self.lastdayinfo.get_days(_id)
            end = self.cdate.get_course_end(_course_id)
            if len(days) < 1:
                continue
            _y = self.label.get(_id)
            if _y == "0":
                continue
            lastday = days[-1]
            diff = TimeUtil.diff(end, lastday)
            if diff < 8:
                continue
            for i in range(1, diff+1):
                lostdays.append(TimeUtil.getnextday(lastday, i))
            if self.debug:
                print "lastday,days,end,lostdays"
                print lastday,days,end,lostdays
        for _id in enr_ids:
            if _id == id:
                continue
            _y = self.label.get(_id)
            _username, _course_id = self.enrollment.enrollment_info.get(_id)
            days = self.lastdayinfo.get_days(_id)
            end = self.cdate.get_end(_course_id)
            if self.debug:
                print "_id,_y,days,end"
                print _id,_y,days,end
            if _y == "1":
                for i in range(1, 11):
                    nday = TimeUtil.getnextday(end, i)
                    dropdays.append(nday)
                dropnum = dropnum + 1
                if len(days) < 1:
                    continue
                lastday = days[-1]
                diff = TimeUtil.diff(end, lastday)
                for i in range(1, diff+1):
                    if self.debug:
                        print TimeUtil.getnextday(lastday, i)
                    dropdays1.append(TimeUtil.getnextday(lastday, i))
            else:
                nodropnum = nodropnum + 1
                for i in range(1, 11):
                    nday = TimeUtil.getnextday(end, i)
                    nodropdays.append(nday)
                if len(days) < 1:
                    continue
                lastday = days[-1]
                diff = TimeUtil.diff(end, lastday)
                for i in range(1, diff+1):
                    if self.debug:
                        print TimeUtil.getnextday(lastday, i)
                    nodropdays1.append(TimeUtil.getnextday(lastday, i))
        if self.debug:
            print "dropdays",dropdays
            print "dropdays1",dropdays1
            print "nodropdays", nodropdays
            print "nodropdays1", nodropdays1
            print "lostdays",lostdays
        k1 = self.k_get_features(_end, dropdays)
        k2 = self.k_get_features(_end, nodropdays)
        k3 = self.k_get_features(_end, lostdays + dropdays)
        k4 = self.k_get_features(_end, dropdays1 + dropdays)
        k5 = self.k_get_features(_end, nodropdays1 + nodropdays)
        if self.debug:
            print k3,"k3"
        f = [dropnum, nodropnum, nodropnum/(dropnum+nodropnum+1.0), dropnum/(dropnum+nodropnum+1.0)]
        excited = [0] * 5
        noexcited = [0] * 5
        if dropnum > 4:
            dropnum = 4
        if nodropnum > 4:
            nodropnum = 4
        excited[dropnum] = 1
        noexcited[nodropnum] = 1

        f = ["%s" % k for k in (f + excited + noexcited)]
        f.append(k1)
        f.append(k2)
        f.append(k3)
        f.append(k4)
        f.append(k5)
        f.append(kws)
        return ",".join(f), nodropdays + nodropdays1

    def k_get_features(self,end,daylist):
        M = 12
        N = 12
        k = [0] * (M + N + (M + N)/3 + (M+N)/6)

        for day in daylist:
            idx = TimeUtil.diff(end, day)
            #print "end",end, day,idx
            if idx >= -N and idx < M:
                idx = idx + N
                k[idx] = 1 + k[idx]
                k[idx/3 + N + M] = 1 + k[idx/3 + N + M]
                k[idx/6 + (N + M) * 4 / 3 ] = 1 + k[idx/6 + (N + M) * 4 / 3]
        k = ",".join(["%d" % i for i in k])
        if self.debug:
            print k
        return k

if __name__ == "__main__":
    cor = Correction("../data/train/enrollment_train.csv",True)
    id="4936"
    print cor.get_features(sys.argv[1])
    """
    for i in range(1, 100):
        print cor.get_features(str(i))
    """
