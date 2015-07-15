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
from weekend import *
from coursetime import *
from common import *
from highuser import *
import math
from module import *
from transfer import *
class GlobalData():
    def __init__(self, command):

    def load(self):
        log_filename = command[0]
        enrollment_filename = command[1]
        featrue_filename = command[2]
        log = Log(log_filename)
        enrollment_train = Enrollment(enrollment_filename)
        enrollment = Enrollment("../data/merge/enrollment.csv")
        self.coursetimeinfo = CourseTimeInfo()
        self.obj = Obj()
        self.label = Label()
        self.userinfo = Userinfo()
        self.userinfo.load()
        self.module = Module()
        self.module.load()
        self.transfer_day = Transfer()
        self.transfer_day.load()

