#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""

__revision__ = '0.1'


from highuser import *
userinfo = Userinfo()
userinfo.build() #conf

from module import *
userinfo = Module()
userinfo.build() #conf

from lastday import *
userinfo = LastDayInfo()
userinfo.build()


from lastdayfeature import *
daylevel = LastDayFeature()
daylevel.build()

from alldayfeature import *
daylevel = AllDayFeature()
daylevel.build()

"""
from day_level_feafure import *
daylevel = DayLevelInfo()
daylevel.build()
"""

