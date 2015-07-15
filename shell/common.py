#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""
from timeutil import *
import cPickle as pickle

__revision__ = '0.1'

event_key = "access,discussion,nagivate,page_close,problem,video,wiki".split(",")
category_key = "video,vertical,static_tab,sequential,problem,peergrading,outlink,html,discussion,dictation,course_info,course,combinedopenended,chapter,about".split(",") #16
category_map = {}
event_map = {}
for k in event_key:
    event_map[k] = len(event_map)
    print k,event_map[k]

for k in category_key:
    category_map[k] = len(category_map)

def get_event_idx(k):
    return event_map[k]
def get_category_idx(k):
    return category_map[k]
import math
def transfer(v):
    return math.log(v+1)

def get_gap_idx(v):
    #k = [1, 2, 3, 5, 8, 13, 20, 30, 50, 80, 150, 1000]
    k = [1, 2, 3, 5, 7, 10, 13, 15, 18, 20, 25, 100000]
    for i in range(len(k)):
        if k[i] > v:
            return i
    return i
EVENT_VEC_NUM = 7
CATEGORY_VEC_NUM = 18
WEEKDAY_VEC_NUM = 7
HOUR_VEC_NUM = 12
CIDX_VEC_NUM = 15
COURSE_VEC_NUM = 39
IS_LAST_VEC_NUM = 10
ORDER_VEC_NUM=7
TRANSFER_VEC_NUM=11
MONTH_VEC_NUM=24
DAYS_VEC_NUM=20
MAX_ENROLLMENT_VEC_NUM=10
INFO_VEC_NUM=20

def get_enrollment_features(lastday, enrollment, username, lastdayinfo, _id):
    f = [0] * 4
    if len(lastday) < 4:
        return f
    ids = enrollment.user_enrollment_id.get(username, [])
    for id in ids:
        if _id == id:
            continue
        days = lastdayinfo.get_days(id)
        username, course_id = enrollment.enrollment_info.get(id)
        bf = False
        en = False
        for day in days:
            k = TimeUtil.diff(lastday, day)
            if k > 0:
                bf = True
            if k < 0:
                en = True

        if bf and en:
            f[0] = 1
        elif bf and en == False:
            f[1] = 1
        elif bf == False and en:
            f[2] = 1
        else:
            f[3] = 1
    return f

def writepickle(filename, info):
    modelFileSave = open(filename, 'wb')
    pickle.dump(info, modelFileSave)
    modelFileSave.close()

def loadpickle(filename):
    modelFileLoad = open(filename, 'rb')
    info = pickle.load(modelFileLoad)
    modelFileLoad.close()
    return info