#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

set -e
#build info
python objweight.py
python courseStatisticTimeInfo.py
python lastdayInfo.py
python courseTimeSequenceInfo.py
python statisticInfo.py
python transfer.py
python userStatisticInfo.py
python userPredictInfo.py

#build single feature
python baseEnrollmentFeature.py
python lastdayFeature.py
python wholeEnrollmentFeature.py
python baseTimeFeature.py
python userPredictFeature.py
python wholeWebsiteFeature.py
python dayLevelFeature.py
python statisticFeature.py
sh run.sh
