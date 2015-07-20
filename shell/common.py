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

def get_vector(idx, maxv):
    k = [0] * maxv
    if idx > maxv - 1:
        idx = maxv - 1
    k[idx] = 1
    return k
def add_vector_value(arr, idx):
    if idx > len(arr) - 1:
        idx = len(arr) - 1
    arr[idx] = arr[idx] + 1

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
MAX_GAP_DAY_VEC_NUM = 10
IS_LAST_VEC_NUM = 10
ORDER_VEC_NUM=7
TRANSFER_VEC_NUM=11
MONTH_VEC_NUM=24
DAYS_VEC_NUM=15
MAX_ENROLLMENT_VEC_NUM=10
INFO_VEC_NUM=20

def writepickle(filename, info):
    modelFileSave = open(filename, 'wb')
    pickle.dump(info, modelFileSave)
    modelFileSave.close()

def loadpickle(filename):
    modelFileLoad = open(filename, 'rb')
    info = pickle.load(modelFileLoad)
    modelFileLoad.close()
    return info