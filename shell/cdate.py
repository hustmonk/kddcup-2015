#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""

from timeutil import *
from common import *
__revision__ = '0.1'
class Cdate:
    def __init__(self):
        self.info = {}

        for line in open("../data/date.csv"):
            #course_id,from,to
            course_id,_from,to = line.strip().split(',')
            self.info[course_id] = [_from, to]

    def get_index(self, course_id, day):
        diff = TimeUtil.diff(day, self.info[course_id][0])
        if diff < 0 or diff >= 30:
            return 0
        return diff

    def get_course_start(self, course_id):
        return self.info[course_id][0]

    def get_course_end(self, course_id):
        return self.info[course_id][1]

if __name__ == "__main__":
    cdate = Cdate()
    print cdate.get_index("bWdj2GDclj5ofokWjzoa5jAwMkxCykd6", "2014-06-13")
