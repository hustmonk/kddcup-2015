#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""

__revision__ = '0.1'


from commonfeature import *

class AllDayFeature:
    def build(self):
        print "start build AllDayFeature..."
        enrollment = Enrollment("../data/merge/enrollment.csv")
        label = Label()
        log = LogInfo("../data/merge/log.csv")
        commonfeature = CommonFeature()
        ccc = 0
        fs = {}

        for id in enrollment.ids:
            ccc += 1
            if ccc % 5000 == 0:
                print ccc
            infos = log.enrollment_loginfo.get(id, [])
            username, course_id = enrollment.enrollment_info.get(id)
            f = commonfeature.get_features(infos, course_id)
            fs[id] = f
        modelFileSave = open('_feature/allday.info.model', 'wb')
        pickle.dump(fs, modelFileSave)
        modelFileSave.close()
        print "build AllDayFeature over!"

    def load(self):
        modelFileLoad = open('_feature/allday.info.model', 'rb')
        self.fs = pickle.load(modelFileLoad)

    def get_features(self, id):
        return self.fs[id]

if __name__ == "__main__":
    daylevel = AllDayFeature()
    daylevel.build()
    daylevel.load()
    #print daylevel.get_features("117502")
