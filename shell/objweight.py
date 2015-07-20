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
from courseStatisticTimeInfo import *
from common import *
import math
from module import *
from transfer import *
class ObjWeight:
    objweightFilename='conf/objweight.info.model'
    def build(self):
        print "start build ObjWeight..."
        enrollment = Enrollment("../data/train/enrollment_train.csv")
        label = Label()
        log = LogInfo("../data/train/log_train.csv")
        #commonfeature = CommonFeature()
        ccc = 0
        fs = {}
        fs_unique = {}

        for id in enrollment.ids:
            y = int(label.get(id))
            ccc += 1
            if ccc % 5000 == 0:
                print ccc
            infos = log.enrollment_loginfo.get(id, [])
            if len(infos) == 0:
                continue
            #weight = 1.0 / math.sqrt(len(infos))
            weight = 1.0 / len(infos)
            objs = set()
            for info in infos:
                obj = info[-1]
                self.add(fs, obj, weight, y)
                objs.add(obj)
            self.add(fs, "OBJ", weight, y)
            weight = 1.0 / len(objs)
            for obj in objs:
                obj = info[-1]
                self.add(fs_unique, obj, weight, y)

        k = {}
        k["fs"] = fs
        k["fs_unique"] = fs_unique
        writepickle(ObjWeight.objweightFilename, k)

        print "build ObjWeight over!"

    def add(self, fs, obj, weight, y):
        if obj not in fs:
            fs[obj] = [weight, y * weight]
        else:
            old = fs[obj]
            fs[obj] = [weight + old[0], y * weight + old[1]]

    def load(self):
        k = loadpickle(ObjWeight.objweightFilename)
        self.fs = k["fs"]
        self.fs_unique = k["fs_unique"]
        self.weight_default = self.fs["OBJ"]
        #print self.weight_default
        self.weight_default = self.weight_default[0]/self.weight_default[1]

    def get_weight(self, id, fs):
        if id not in fs:
            return 1.0
        weight = fs[id]
        #print weight
        weight = [weight[0] + self.weight_default * 10, weight[1]+10]
        weight = weight[0]/weight[1]
        return weight/self.weight_default

    def get_features(self, infos):
        return self._get_features(infos,self.fs_unique) + self._get_features(infos,self.fs)
        #return self._get_features(infos,self.fs)

    def _get_features(self, infos, kps):
        kv = {}
        for info in infos:
            obj = info[-1]
            kv[obj] = kv.get(obj, 0) + 1
        weight1 = 1
        weight2 = 1
        weight3 = 1
        l1 = 0
        l2 = 0
        l3 = 0
        for (k, v) in kv.items():
            _weight = self.get_weight(k, kps)
            if v > 30:
                v = 30
            l1 = l1 + v
            l2 = l2 + math.sqrt(v)
            l3 = l3 + 1
            weight1 = weight1 * math.pow(_weight, v)
            weight2 = weight2 * math.pow(_weight, math.sqrt(v))
            weight3 = weight3 * _weight
            if weight1 > 10000:
                break
        if l3 < 1:
            return [1,1,1,1,1,1]
        weights = [weight1, weight2, weight3, math.pow(weight1, 1.0/l1), math.pow(weight2, 1.0/l2), math.pow(weight3, 1.0/l3)]
        return weights

if __name__ == "__main__":
    daylevel = ObjWeight()
    daylevel.build()
    daylevel.load()
    #print daylevel.get_weight("RMtgC2bTAqEeftenUUyia504wsyzeZWf")
    print daylevel.get_features([["RMtgC2bTAqEeftenUUyia504wsyzeZWf"]])
