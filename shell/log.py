#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""

__revision__ = '0.1'

class LogInfo:
    def __init__(self, filename):
        fin = open(filename)
        header = fin.next()
        self.enrollment_loginfo = {}
        for line in fin:
            #enrollment_id,username,course_id,time,source,event,object
            enrollment_id,time,source,event,o = line.strip().split(",")
            if enrollment_id not in self.enrollment_loginfo:
                self.enrollment_loginfo[enrollment_id] = [[time,source,event,o]]
            else:
                self.enrollment_loginfo[enrollment_id].append([time,source,event,o])

